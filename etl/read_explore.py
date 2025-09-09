# etl/read_explore.py
import argparse
from pathlib import Path
import polars as pl
from rich.console import Console
from rich.table import Table

console = Console()

def quick_summary(df: pl.DataFrame):
    # Resumen por columna
    col_summary = pl.DataFrame({
        "columna": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "nulos": list(df.null_count().row(0))
    })
    # Resumen general
    general = pl.DataFrame([{
        "filas": df.height,
        "columnas": df.width,
        "min_fecha": df["fecha"].min() if "fecha" in df.columns else None,
        "max_fecha": df["fecha"].max() if "fecha" in df.columns else None,
        "sucursales": df["sucursal"].n_unique() if "sucursal" in df.columns else None
    }])
    return general, col_summary

def show_table(df: pl.DataFrame, title: str):
    """Muestra un DataFrame como tabla bonita en consola con Rich"""
    table = Table(title=title)
    for col in df.columns:
        table.add_column(col, style="cyan")
    for row in df.rows():
        table.add_row(*[str(x) if x is not None else "-" for x in row])
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Exploración de CSV con Polars + Rich")
    parser.add_argument("--input_glob", default="data/input/*.csv")
    parser.add_argument("--out_dir", default="data/output")
    args = parser.parse_args()

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    console.rule("[bold green] ETL Lectura y Exploración [/bold green]")

    try:
        df = pl.read_csv(args.input_glob, try_parse_dates=True)
        console.print(f"✅ Archivos leídos desde: {args.input_glob}", style="bold green")
    except Exception as e:
        console.print(f"❌ Error al leer archivos: {e}", style="bold red")
        return

    general, col_summary = quick_summary(df)

    # Guardar
    general.write_csv(f"{args.out_dir}/resumen_general.csv")
    col_summary.write_csv(f"{args.out_dir}/resumen_columnas.csv")

    # Mostrar tablas bonitas
    show_table(general, "Resumen General")
    show_table(col_summary, "Resumen por Columna")

    console.print(f"📂 Resultados guardados en: {args.out_dir}", style="bold blue")
    console.rule("[bold green] Fin del proceso [/bold green]")

if __name__ == "__main__":
    main()

