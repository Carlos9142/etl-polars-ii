# tests/test_read_explore.py
import unittest
import polars as pl
from etl.read_explore import quick_summary

class TestReadExplore(unittest.TestCase):

    def setUp(self):
        # Este método se ejecuta antes de cada test
        self.df = pl.read_csv("tests/data_test.csv")

    def test_resumen_general(self):
        general, col_summary = quick_summary(self.df)

        # Verificar que hay 2 filas y 5 columnas
        self.assertEqual(int(general["filas"][0]), 2)
        self.assertEqual(int(general["columnas"][0]), 5)

        # Verificar que la sucursal aparece 2 veces (únicas = 2)
        self.assertEqual(int(general["sucursales"][0]), 2)

    def test_columnas(self):
        _, col_summary = quick_summary(self.df)

        # Verificar que las columnas esperadas existen
        expected_cols = {"fecha", "sucursal", "sku", "cantidad", "precio"}
        self.assertTrue(expected_cols.issubset(set(col_summary["columna"].to_list())))

if __name__ == "__main__":
    unittest.main()
