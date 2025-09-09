# etl/make_sample_data.py
from pathlib import Path
import csv
import random
from datetime import date, timedelta

# Crear carpeta si no existe
Path("data/input").mkdir(parents=True, exist_ok=True)

# Fechas de ejemplo (últimos 7 días)
hoy = date.today()
fechas = [hoy - timedelta(days=i) for i in range(7)]

# Sucursales y productos ficticios
sucursales = ["CDMX", "GDL", "MTY"]
productos = [
    ("A1", 150.0),
    ("B2", 299.9),
    ("C3", 99.5),
    ("D4", 450.0),
]

# Generar filas aleatorias
rows = []
for f in fechas:
    for suc in sucursales:
        sku, precio = random.choice(productos)
        cantidad = random.randint(1, 5)
        rows.append({
            "fecha": f.strftime("%Y-%m-%d"),
            "sucursal": suc,
            "sku": sku,
            "cantidad": cantidad,
            "precio": precio,
        })

# Guardar archivo
file_path = "data/input/ventas_demo.csv"
with open(file_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print(f"✅ Archivo de prueba creado en: {file_path}")
print(f"Total de filas: {len(rows)}")
