import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "frontend"))
from utils.charts import grafico_evolucao


class EvolucaoTests(unittest.TestCase):
    def test_primeira_medicao_tem_marcador_visivel(self):
        df = pd.DataFrame({"data_avaliacao": pd.to_datetime(["2026-11-02"]), "peso_kg": [70]})
        chart = grafico_evolucao(df, "peso_kg", "Peso (kg)")
        spec = chart.to_dict()
        self.assertTrue(spec["mark"]["point"]["filled"])
        self.assertGreater(spec["mark"]["point"]["size"], 0)
        self.assertEqual(len(chart.data), 1)
        self.assertEqual(chart.data.iloc[0]["peso_kg"], 70)

    def test_medicoes_ordenadas_sem_inventar_gordura_ausente(self):
        df = pd.DataFrame({"data_avaliacao": pd.to_datetime(["2026-11-02", "2026-09-02", "2026-10-02"]), "percentual_gordura": [None, 20, 19]})
        chart = grafico_evolucao(df, "percentual_gordura", "Gordura (%)")
        chart.to_dict()
        self.assertEqual(chart.data["percentual_gordura"].tolist(), [20, 19])
        self.assertEqual(len(df), 3)

    def test_datas_em_formato_brasileiro(self):
        df = pd.DataFrame({"data_avaliacao": pd.to_datetime(["2026-11-02"]), "peso_kg": [70]})
        spec = grafico_evolucao(df, "peso_kg", "Peso (kg)").to_dict()
        self.assertEqual(spec["encoding"]["x"]["axis"]["format"], "%d/%m/%Y")
        self.assertEqual(spec["encoding"]["tooltip"][0]["format"], "%d/%m/%Y")


if __name__ == "__main__":
    unittest.main()
