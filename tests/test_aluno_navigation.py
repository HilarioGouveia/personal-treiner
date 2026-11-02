"""Tabela de alunos e contexto compartilhado entre módulos."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class NavegacaoAlunoTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(ROOT / "frontend"))
        env = patch.dict(os.environ, {"DEMO_MODE": "true"})
        env.start()
        self.addCleanup(env.stop)

    def abrir(self):
        app = AppTest.from_file(str(ROOT / "frontend/app.py"), default_timeout=15).run()
        app.switch_page("pages/01_Alunos.py").run()
        self.assertFalse(app.exception)
        return app

    def test_acoes_aparecem_so_apos_selecionar_linha(self):
        app = self.abrir()
        self.assertEqual(len(app.dataframe[0].value), 2)
        self.assertFalse(any(b.label == "Treinos" for b in app.button))
        app.session_state["tabela_alunos_1_2"] = {"selection": {"rows": [1], "columns": [], "cells": []}}
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any(b.label == "Treinos" for b in app.button))

    def test_atalhos_abrem_modulos_com_segundo_aluno(self):
        for label, key in [("Treinos", "treino_aluno"), ("Avaliações", "avaliacao_aluno"), ("Financeiro", "financeiro_aluno")]:
            with self.subTest(label=label):
                app = self.abrir()
                app.session_state["tabela_alunos_1_2"] = {"selection": {"rows": [1], "columns": [], "cells": []}}
                app.run()
                next(b for b in app.button if b.label == label).click().run()
                self.assertFalse(app.exception)
                self.assertEqual(app.session_state.aluno_selecionado_id, 2)
                self.assertEqual(app.selectbox(key=key).value, 2)
                if key == "treino_aluno":
                    self.assertEqual(app.selectbox(key="viz_aluno").value, 2)

    def test_troca_de_aluno_preserva_id_entre_modulos(self):
        app = self.abrir()
        # Mesmo nome não deve colidir: os seletores usam IDs.
        app.session_state.demo_dados["alunos"][1]["nome"] = "Ana Exemplo"
        app.switch_page("pages/03_Avaliacoes.py").run()
        app.selectbox(key="avaliacao_aluno").set_value(2).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.aluno_selecionado_id, 2)
        app.switch_page("pages/04_Financeiro.py").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="financeiro_aluno").value, 2)


if __name__ == "__main__":
    unittest.main()
