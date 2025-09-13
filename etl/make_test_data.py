# etl/make_test_data.py
from pathlib import Path
import csv

Path("tests").mkdir(parents=True, exist_ok=True)

rows = [
    {"fecha": "2025-09-01", "sucursal": "CDMX", "sku": "A1", "cantidad": 2, "precio": 100.0},
    {"fecha": "2025-09-02", "sucursal": "GDL", "sku": "B2", "cantidad": 1, "precio": 200.0},
]

file_path = "tests/data_test.csv"
with open(file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Archivo de prueba creado en: {file_path}")
