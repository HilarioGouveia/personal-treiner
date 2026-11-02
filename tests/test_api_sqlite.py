"""Integração HTTP + SQLite em arquivo temporário, sem alterar o banco local."""

import sqlite3
import sys
import unittest
from datetime import date
import bcrypt
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.core.database import get_db
from app.main import app
from app.models.models import Base


class AlunosSQLiteTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / "test.db"
        self.engine = create_engine(f"sqlite:///{self.path.as_posix()}", connect_args={"check_same_thread": False})
        self.addCleanup(self.engine.dispose)

        @event.listens_for(self.engine, "connect")
        def foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

        Base.metadata.create_all(self.engine)
        sessions = sessionmaker(bind=self.engine)

        def db_override():
            with sessions() as session:
                yield session

        previous = app.dependency_overrides.copy()
        self.addCleanup(lambda: setattr(app, "dependency_overrides", previous))
        app.dependency_overrides[get_db] = db_override
        self.client = self.enterContext(TestClient(app))
        self.payload = dict(nome="Ana Silva", email="ana@example.com", senha="senha-teste", data_nascimento="1990-12-31")

    def counts(self):
        with sqlite3.connect(self.path) as connection:
            result = tuple(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in ("usuarios", "alunos"))
        connection.close()
        return result

    def test_persistencia_data_vinculo_e_hash_apos_nova_conexao(self):
        response = self.client.post("/api/v1/alunos/", json=self.payload)
        self.assertEqual(response.status_code, 201, response.text)
        created = response.json()
        self.assertEqual(created["data_nascimento"], "1990-12-31")
        self.assertNotIn("senha", created)
        self.assertNotIn("senha_hash", created)
        self.engine.dispose()
        with sqlite3.connect(self.path) as connection:
            row = connection.execute("SELECT a.data_nascimento, u.senha_hash, u.email FROM alunos a JOIN usuarios u ON u.id=a.usuario_id WHERE a.id=?", (created["id"],)).fetchone()
        connection.close()
        self.assertEqual(row[0], "1990-12-31")
        self.assertEqual(row[2], self.payload["email"])
        self.assertNotEqual(row[1], self.payload["senha"])
        self.assertTrue(bcrypt.checkpw(self.payload["senha"].encode(), row[1].encode()))
        listed = self.client.get("/api/v1/alunos/")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json(), [created])

    def test_email_duplicado_nao_cria_registros(self):
        self.assertEqual(self.client.post("/api/v1/alunos/", json=self.payload).status_code, 201)
        response = self.client.post("/api/v1/alunos/", json=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.counts(), (1, 1))

    def test_data_invalida_rejeitada_sem_persistir(self):
        self.payload["data_nascimento"] = "1990-02-30"
        response = self.client.post("/api/v1/alunos/", json=self.payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.counts(), (0, 0))

    def test_nascimento_opcional_persistido_como_null(self):
        self.payload.pop("data_nascimento")
        response = self.client.post("/api/v1/alunos/", json=self.payload)
        self.assertEqual(response.status_code, 201, response.text)
        with sqlite3.connect(self.path) as connection:
            self.assertIsNone(connection.execute("SELECT data_nascimento FROM alunos").fetchone()[0])
        connection.close()

    def test_falha_perfil_reverte_usuario(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("CREATE TRIGGER falha_aluno BEFORE INSERT ON alunos BEGIN SELECT RAISE(ABORT, 'falha simulada'); END")
        connection.close()
        with self.assertRaises(IntegrityError):
            self.client.post("/api/v1/alunos/", json=self.payload)
        self.assertEqual(self.counts(), (0, 0))

    def test_senha_longa_rejeitada_sem_gravar(self):
        self.payload["senha"] = "á" * 37
        self.assertEqual(self.client.post("/api/v1/alunos/", json=self.payload).status_code, 422)
        self.assertEqual(self.counts(), (0, 0))

    def test_avaliacao_persiste_e_aparece_no_historico(self):
        aluno = self.client.post("/api/v1/alunos/", json=self.payload).json()
        payload = dict(aluno_id=aluno["id"], data_avaliacao="2026-11-02", peso_kg=70.5,
                       altura_cm=175, percentual_gordura=15, medidas_json={"braco_cm": 32})
        response = self.client.post("/api/v1/avaliacoes/", json=payload)
        self.assertEqual(response.status_code, 201, response.text)
        self.engine.dispose()
        with sqlite3.connect(self.path) as connection:
            row = connection.execute("SELECT data_avaliacao, peso_kg FROM avaliacoes_fisicas").fetchone()
        connection.close()
        self.assertEqual(row, ("2026-11-02", 70.5))
        listed = self.client.get(f"/api/v1/avaliacoes/aluno/{aluno['id']}")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json(), [response.json()])

    def test_avaliacao_sem_data_usa_hoje(self):
        aluno = self.client.post("/api/v1/alunos/", json=self.payload).json()
        response = self.client.post("/api/v1/avaliacoes/", json={"aluno_id": aluno["id"], "peso_kg": 70})
        self.assertEqual(response.status_code, 201, response.text)
        self.assertEqual(response.json()["data_avaliacao"], date.today().isoformat())

    def test_avaliacao_aluno_inexistente(self):
        response = self.client.post("/api/v1/avaliacoes/", json={"aluno_id": 999, "peso_kg": 70})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Aluno não encontrado.")

    def test_mensalidade_criacao_consulta_e_baixa(self):
        aluno = self.client.post("/api/v1/alunos/", json=self.payload).json()
        response = self.client.post("/api/v1/mensalidades/", json={"aluno_id": aluno["id"], "data_vencimento": "2026-11-10", "valor": 150})
        self.assertEqual(response.status_code, 201, response.text)
        mensalidade = response.json()
        listed = self.client.get(f"/api/v1/mensalidades/aluno/{aluno['id']}")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json(), [mensalidade])
        paid = self.client.patch(f"/api/v1/mensalidades/{mensalidade['id']}", json={"status": "PAGO"})
        self.assertEqual(paid.status_code, 200, paid.text)
        self.assertEqual(paid.json()["status"], "PAGO")
        self.assertEqual(paid.json()["data_pagamento"], date.today().isoformat())


if __name__ == "__main__":
    unittest.main()
