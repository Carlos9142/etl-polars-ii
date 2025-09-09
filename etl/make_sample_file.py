# etl/make_sample_file.py
from pathlib import Path
import csv

# Crear carpeta "samples" si no existe
Path("samples").mkdir(parents=True, exist_ok=True)

rows = [
    {"fecha": "2025-09-01", "sucursal": "CDMX", "sku": "A1", "cantidad": 2, "precio": 150.0},
    {"fecha": "2025-09-01", "sucursal": "CDMX", "sku": "B2", "cantidad": 1, "precio": 299.9},
    {"fecha": "2025-09-02", "sucursal": "GDL", "sku": "A1", "cantidad": 3, "precio": 150.0},
    {"fecha": "2025-09-03", "sucursal": "MTY", "sku": "C3", "cantidad": 5, "precio": 99.5},
]

file_path = "samples/ventas_demo.csv"
with open(file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Archivo de ejemplo creado en: {file_path}")
