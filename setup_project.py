# setup_project.py
from pathlib import Path

# Carpetas que vamos a crear
folders = [
    "data/input",
    "data/output",
    "etl"
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Archivos básicos
(Path("requirements.txt")).write_text("polars\n", encoding="utf-8")

(Path("etl/read_explore.py")).write_text("""\
import polars as pl

def main():
    print("Hola! Este es tu script base read_explore.py")
    # Aquí luego pegaremos la lógica completa del ETL

if __name__ == "__main__":
    main()
""", encoding="utf-8")

print("✅ Estructura creada con éxito en ETL_Polars II.")

