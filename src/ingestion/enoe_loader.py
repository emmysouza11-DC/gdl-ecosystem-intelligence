"""
ingestion/enoe_loader.py
Descarga y preprocesamiento de microdatos ENOE (INEGI) para la ZMG.

Uso:
    python src/ingestion/enoe_loader.py --year 2024 --quarter 4

Salida:
    data/processed/enoe_zmg_{year}_T{quarter}.parquet
"""

import pandas as pd
import numpy as np
import argparse
from pathlib import Path

# Municipios de la ZMG (clave INEGI, entidad 14 = Jalisco)
ZMG_MUNICIPIOS = {
    "039": "Guadalajara",
    "120": "Zapopan",
    "098": "Tlaquepaque",
    "101": "Tonalá",
    "097": "Tlajomulco de Zúñiga",
    "070": "El Salto",
}

# Ramas económicas tech (SCIAN 2 dígitos)
RAMAS_TECH = [11]

# Variables a conservar del microdato ENOE (SDEMT)
VARIABLES_ENOE = [
    "ent",          # Entidad federativa
    "mun",          # Municipio
    "rama_est2",    # Rama de actividad (2 dígitos)
    "ing_x_hrs",    # Ingreso por hora
    "anios_esc",    # Años de escolaridad
    "pos_ocu",      # Posición en la ocupación
    "tue_b",        # Tamaño unidad económica
    "sex",          # Sexo
    "eda",          # Edad
    "fac_tri",      # Factor de expansión trimestral
]

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def find_enoe_file(year: int, quarter: int) -> Path | None:
    """
    Busca el archivo ENOE en múltiples ubicaciones y formatos de nombre.
    Soporta:
        data/raw/enoe/{year}/SDEMT{yy}{qq}c.csv
        data/raw/enoe/{year}/ENOE_SDEMT{qq}{yy}.csv
        data/raw/enoe/{year}/SDEMT_trim{q}_{year}.csv
        data/raw/enoe/SDEMT{yy}{qq}c.csv  (sin subcarpeta)
    """
    yy = str(year)[2:]
    qq = f"{quarter:02d}"
    base = RAW_DIR / "enoe"
    year_dir = base / str(year)

    candidates = [
        # Con subcarpeta por año
        year_dir / f"SDEMT{yy}{qq}c.csv",
        year_dir / f"ENOE_SDEMT{qq}{yy}.csv",
        year_dir / f"SDEMT_trim{quarter}_{year}.csv",
        # Sin subcarpeta (fallback)
        base / f"SDEMT{yy}{qq}c.csv",
        base / f"ENOE_SDEMT{qq}{yy}.csv",
        base / f"SDEMT_trim{quarter}_{year}.csv",
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def load_enoe_quarter(year: int, quarter: int) -> pd.DataFrame:
    """
    Carga el microdato ENOE de un trimestre específico.

    Args:
        year: Año (ej. 2024)
        quarter: Trimestre 1-4

    Returns:
        DataFrame filtrado para ZMG con variables relevantes
    """
    filepath = find_enoe_file(year, quarter)

    if filepath is None:
        print(f"[!] Archivo no encontrado: {year} T{quarter}")
        print(f"    Descargarlo de: https://www.inegi.org.mx/programas/enoe/15ymas/")
        print(f"    Colocar en: data/raw/enoe/{year}/")
        return pd.DataFrame()

    print(f"[+] Cargando {filepath.name} ({year} T{quarter})...")
    df = pd.read_csv(filepath, dtype=str, low_memory=False, encoding="latin-1")

    # Normalizar nombres de columna a minúsculas
    df.columns = df.columns.str.lower()

    # Filtrar Jalisco (entidad 14)
    if "ent" in df.columns:
        df = df[df["ent"] == "14"].copy()

    # Filtrar municipios ZMG
    if "mun" in df.columns:
        df = df[df["mun"].isin(ZMG_MUNICIPIOS.keys())].copy()

    # Conservar solo variables relevantes disponibles
    cols_available = [c for c in VARIABLES_ENOE if c in df.columns]
    df = df[cols_available].copy()

    # Convertir variables numéricas
    for col in ["ing_x_hrs", "anios_esc", "eda", "fac_tri"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Etiquetar sector tech
    if "rama_est2" in df.columns:
        df["rama_est2_num"] = pd.to_numeric(df["rama_est2"], errors="coerce")
        df["es_tech"] = df["rama_est2_num"].isin(RAMAS_TECH)

    # Etiquetar municipio
    if "mun" in df.columns:
        df["municipio_nombre"] = df["mun"].map(ZMG_MUNICIPIOS)

    # Metadatos del periodo
    df["year"] = year
    df["quarter"] = quarter
    df["periodo"] = f"{year}-T{quarter}"

    print(f"    Registros ZMG: {len(df):,}")
    if "es_tech" in df.columns:
        print(f"    Trabajadores tech: {df['es_tech'].sum():,} ({df['es_tech'].mean()*100:.1f}%)")

    return df


def save_processed(df: pd.DataFrame, year: int, quarter: int) -> None:
    """Guarda el DataFrame procesado en formato parquet."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"enoe_zmg_{year}_T{quarter}.parquet"
    df.to_parquet(out_path, index=False)
    print(f"[+] Guardado en: {out_path}")


def load_multiple_quarters(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Carga y concatena múltiples trimestres ENOE.

    Args:
        start_year: Año inicial (ej. 2023)
        end_year: Año final (ej. 2025)

    Returns:
        DataFrame con todos los trimestres concatenados
    """
    dfs = []
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            df = load_enoe_quarter(year, quarter)
            if not df.empty:
                dfs.append(df)

    if not dfs:
        print("[!] No se encontraron archivos. Ver docs/fuentes.md para instrucciones de descarga.")
        return pd.DataFrame()

    full_df = pd.concat(dfs, ignore_index=True)
    print(f"\n[+] Total registros cargados: {len(full_df):,}")
    return full_df


def summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera estadísticas descriptivas de salarios tech vs no-tech por periodo.

    Returns:
        DataFrame con medias, medianas y conteos por grupo y periodo
    """
    if df.empty:
        return pd.DataFrame()

    stats = (
        df.groupby(["periodo", "es_tech"])["ing_x_hrs"]
        .agg(
            media="mean",
            mediana="median",
            p25=lambda x: x.quantile(0.25),
            p75=lambda x: x.quantile(0.75),
            n="count",
        )
        .reset_index()
    )
    stats["sector"] = stats["es_tech"].map({True: "Tech", False: "No-Tech"})
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carga microdatos ENOE para ZMG")
    parser.add_argument("--year", type=int, required=True, help="Año (ej. 2024)")
    parser.add_argument("--quarter", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()

    df = load_enoe_quarter(args.year, args.quarter)
    if not df.empty:
        save_processed(df, args.year, args.quarter)
