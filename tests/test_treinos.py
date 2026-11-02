"""Regressão das ações do formulário de treino."""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "frontend"))
from services import api_client


class FormularioTreinoTests(unittest.TestCase):
    def setUp(self):
        for name, value in {
            "get_alunos": [{"id": 7, "nome": "Ana"}],
            "get_exercicios": [{"id": 3, "nome": "Supino", "grupo_muscular": "Peitoral", "url_video": None}],
            "get_fichas_aluno": [],
        }.items():
            mock = patch.object(api_client, name, return_value=value)
            self.addCleanup(mock.stop)
            mock.start()
        criar = patch.object(api_client, "criar_ficha_treino", return_value=SimpleNamespace(status_code=201))
        self.addCleanup(criar.stop)
        self.criar = criar.start()
        self.app = AppTest.from_file(str(ROOT / "frontend/app.py"), default_timeout=10).run()
        self.app.switch_page("pages/02_Treinos.py").run()
        self.assertFalse(self.app.exception)

    def clicar(self, label):
        next(button for button in self.app.button if button.label == label).click().run()
        self.assertFalse(self.app.exception)

    def adicionar(self):
        self.app.text_input[0].set_value("Ficha ABC")
        self.clicar("➕ Adicionar Exercício à Ficha")

    def test_adicionar_e_publicar_preserva_titulo_e_envia_item(self):
        self.adicionar()
        self.assertEqual(len(self.app.session_state.itens_treino_temp), 1)
        self.criar.assert_not_called()
        self.clicar("💾 Salvar e Publicar Ficha de Treino")
        self.criar.assert_called_once()
        payload = self.criar.call_args.args[0]
        self.assertEqual(payload["titulo"], "Ficha ABC")
        self.assertEqual(payload["aluno_id"], 7)
        self.assertEqual(payload["itens"][0]["exercicio_id"], 3)
        self.assertNotIn("exercicio_nome", payload["itens"][0])
        self.assertEqual(self.app.session_state.itens_treino_temp, [])

    def test_limpar_nao_publica_ficha(self):
        self.adicionar()
        self.clicar("🗑️ Limpar Lista de Exercícios")
        self.assertEqual(self.app.session_state.itens_treino_temp, [])
        self.criar.assert_not_called()

    def test_publicar_sem_titulo_exibe_validacao(self):
        self.clicar("💾 Salvar e Publicar Ficha de Treino")
        self.assertIn("Informe o título", self.app.error[0].value)
        self.criar.assert_not_called()
