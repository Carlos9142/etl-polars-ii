# etl/read_explore.py
import argparse
from pathlib import Path
import subprocess
import polars as pl
from rich.console import Console
from rich.table import Table

console = Console()

def quick_summary(df: pl.DataFrame):
    """Genera dos resúmenes: general y por columna"""
    col_summary = pl.DataFrame({
        "columna": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "nulos": list(df.null_count().row(0))
    })
    general = pl.DataFrame([{
        "filas": df.height,
        "columnas": df.width,
        "min_fecha": df["fecha"].min() if "fecha" in df.columns else None,
        "max_fecha": df["fecha"].max() if "fecha" in df.columns else None,
        "sucursales": df["sucursal"].n_unique() if "sucursal" in df.columns else None
    }])
    return general, col_summary

def show_table(df: pl.DataFrame, title: str):
    """Muestra un DataFrame como tabla bonita en consola"""
    table = Table(title=title)
    for col in df.columns:
        table.add_column(col, style="cyan")
    for row in df.rows():
        table.add_row(*[str(x) if x is not None else "-" for x in row])
    console.print(table)

def ensure_input_files(input_glob: str):
    """Verifica si hay archivos CSV; si no, genera datos de prueba"""
    path = Path(input_glob.replace("*.csv", ""))
    files = list(path.glob("*.csv"))
    if not files:
        console.print("⚠️ No se encontraron archivos en data/input/", style="bold yellow")
        console.print("🤖 Generando dataset de prueba con make_sample_data.py...", style="cyan")
        subprocess.run(["python", "etl/make_sample_data.py"], check=True)
    else:
        console.print(f"✅ Se encontraron {len(files)} archivo(s) en {path}", style="green")

def main():
    parser = argparse.ArgumentParser(description="Exploración de CSV con Polars + Rich + Hardening")
    parser.add_argument("--input_glob", default="data/input/*.csv")
    parser.add_argument("--out_dir", default="data/output")
    args = parser.parse_args()

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    console.rule("[bold green] ETL Lectura y Exploración [/bold green]")

    try:
        # Verificar o generar archivos
        ensure_input_files(args.input_glob)

        # Leer datos
        df = pl.read_csv(args.input_glob, try_parse_dates=True)
        console.print("✅ Archivos leídos correctamente.", style="bold green")

        # Generar resúmenes
        general, col_summary = quick_summary(df)

        # Guardar en CSV
        general.write_csv(f"{args.out_dir}/resumen_general.csv")
        col_summary.write_csv(f"{args.out_dir}/resumen_columnas.csv")

        # Mostrar en consola
        show_table(general, "Resumen General")
        show_table(col_summary, "Resumen por Columna")

        console.print(f"📂 Resultados guardados en: {args.out_dir}", style="bold blue")

    except Exception as e:
        console.print(f"❌ Error crítico: {e}", style="bold red")

    console.rule("[bold green] Fin del proceso [/bold green]")

if __name__ == "__main__":
    main()


