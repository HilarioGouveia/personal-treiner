"""Demonstração completa sem rede e com dados isolados por sessão."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "frontend"))


class DemoTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {"DEMO_MODE": "true"})
        env.start()
        self.addCleanup(env.stop)
        network = patch("requests.sessions.Session.request", side_effect=AssertionError("Demo não deve usar rede"))
        self.network = network.start()
        self.addCleanup(network.stop)

    def nova_sessao(self):
        app = AppTest.from_file(str(ROOT / "frontend/app.py"), default_timeout=15).run()
        self.assertFalse(app.exception)
        self.assertFalse(app.text_input)
        return app

    def clicar(self, app, label):
        next(b for b in app.button if b.label == label).click().run()
        self.assertFalse(app.exception)

    def test_paginas_funcionam_sem_api(self):
        app = self.nova_sessao()
        for page in ("01_Alunos.py", "02_Treinos.py", "03_Avaliacoes.py", "04_Financeiro.py"):
            with self.subTest(page=page):
                app.switch_page("pages/" + page).run()
                self.assertFalse(app.exception)
                self.assertTrue(any("Modo demonstração" in info.value for info in app.info))
        self.network.assert_not_called()

    def test_cadastro_isolamento_e_restauracao(self):
        app = self.nova_sessao()
        app.switch_page("pages/01_Alunos.py").run()
        app.text_input[0].set_value("Carla Demo")
        app.text_input[1].set_value("carla@example.com")
        app.text_input[2].set_value("senha-descartada")
        self.clicar(app, "Salvar Aluno")
        self.assertTrue(app.success)
        self.assertEqual(len(app.session_state.demo_dados["alunos"]), 3)
        self.assertNotIn("senha", app.session_state.demo_dados["alunos"][-1])
        other = self.nova_sessao()
        other.switch_page("pages/01_Alunos.py").run()
        self.assertEqual(len(other.session_state.demo_dados["alunos"]), 2)
        self.clicar(app, "Restaurar demonstração")
        self.assertEqual(len(app.session_state.demo_dados["alunos"]), 2)
        self.network.assert_not_called()

    def test_avaliacao_e_baixa_persistem_entre_paginas(self):
        app = self.nova_sessao()
        app.switch_page("pages/03_Avaliacoes.py").run()
        antes = len(app.session_state.demo_dados["avaliacoes"])
        self.clicar(app, "💾 Salvar Avaliação Física")
        self.assertEqual(len(app.session_state.demo_dados["avaliacoes"]), antes + 1)
        app.switch_page("pages/04_Financeiro.py").run()
        self.clicar(app, "✅ Dar Baixa (Pago)")
        mensalidade = next(m for m in app.session_state.demo_dados["mensalidades"] if m["id"] == 2)
        self.assertEqual(mensalidade["status"], "PAGO")
        self.assertTrue(mensalidade["data_pagamento"])
        app.switch_page("pages/03_Avaliacoes.py").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.session_state.demo_dados["avaliacoes"]), antes + 1)
        self.network.assert_not_called()


if __name__ == "__main__":
    unittest.main()
