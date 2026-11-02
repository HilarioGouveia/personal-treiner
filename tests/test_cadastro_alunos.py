"""Regressões do cadastro, sem acessar a API ou o banco de dados."""

import sys
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from requests import Response

from pydantic import ValidationError
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "frontend"))

from backend.app.schemas.schemas import AlunoCreate
from services import api_client


class CadastroAlunoTests(unittest.TestCase):
    def setUp(self):
        listar = patch.object(api_client, "get_alunos", return_value=[])
        criar = patch.object(api_client, "criar_aluno")
        self.addCleanup(listar.stop)
        self.addCleanup(criar.stop)
        listar.start()
        self.criar = criar.start()
        self.app = AppTest.from_file(str(ROOT / "frontend/app.py"), default_timeout=10)
        self.app.run()
        self.app.switch_page("pages/01_Alunos.py").run()
        self.assertFalse(self.app.exception)

    def preencher(self):
        self.app.text_input[0].set_value("Ana Silva")
        self.app.text_input[1].set_value("ana@example.com")
        self.app.text_input[2].set_value("senha-teste")
        self.app.date_input[0].set_value(date(2020, 2, 29))

    def enviar(self):
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)

    def test_data_exibida_no_formato_brasileiro(self):
        self.assertEqual(self.app.date_input[0].proto.format, "DD/MM/YYYY")

    def test_obrigatorios_impedem_envio(self):
        self.enviar()
        self.criar.assert_not_called()
        self.assertIn("campos obrigatórios", self.app.error[0].value)

    def test_cadastro_envia_data_iso_compativel_com_backend(self):
        self.criar.return_value = SimpleNamespace(status_code=201)
        self.preencher()
        self.enviar()
        self.criar.assert_called_once()
        payload = self.criar.call_args.args[0]
        self.assertEqual(payload["data_nascimento"], "2020-02-29")
        self.assertEqual(AlunoCreate(**payload).data_nascimento, date(2020, 2, 29))
        self.assertTrue(self.app.success)
        self.assertFalse(self.app.error)

    def test_falha_api_nao_exibe_sucesso(self):
        for response in (None, SimpleNamespace(status_code=400), SimpleNamespace(status_code=500)):
            with self.subTest(response=response):
                self.criar.return_value = response
                self.preencher()
                self.enviar()
                self.assertTrue(self.app.error)
                self.assertFalse(self.app.success)

    def test_exibe_erro_de_email_duplicado_da_api(self):
        response = Response()
        response.status_code = 400
        response._content = '{"detail":"E-mail já cadastrado no sistema."}'.encode("utf-8")
        self.criar.return_value = response
        self.preencher()
        self.enviar()
        self.assertIn("E-mail já cadastrado", self.app.error[0].value)
        self.assertFalse(self.app.success)


class DataNascimentoSchemaTests(unittest.TestCase):
    def aluno(self, **kwargs):
        return AlunoCreate(nome="Ana", email="ana@example.com", senha="teste", **kwargs)

    def test_data_opcional(self):
        self.assertIsNone(self.aluno().data_nascimento)
        self.assertIsNone(self.aluno(data_nascimento=None).data_nascimento)

    def test_rejeita_data_impossivel_e_formato_local_na_api(self):
        for value in ("2023-02-29", "1990-13-01", "31/12/1990", "None"):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                self.aluno(data_nascimento=value)


if __name__ == "__main__":
    unittest.main()
