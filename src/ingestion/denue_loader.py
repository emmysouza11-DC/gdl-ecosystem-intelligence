"""
ingestion/denue_loader.py
Descarga establecimientos del sector tech en ZMG via API DENUE (INEGI).

Uso:
    python src/ingestion/denue_loader.py

Requisito:
    Token de API gratuito en https://www.inegi.org.mx/app/developer/
    Agregar al archivo .env: INEGI_TOKEN=tu_token_aqui

Salida:
    data/processed/denue_tech_zmg.parquet
"""

import requests
import pandas as pd
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

INEGI_TOKEN = os.getenv("INEGI_TOKEN", "")
BASE_URL = "https://www.inegi.org.mx/app/api/denue/v1/consulta"

PROCESSED_DIR = Path("data/processed")

# Municipios ZMG — clave completa (estado + municipio)
ZMG_MUNICIPIOS = {
    "14039": "Guadalajara",
    "14120": "Zapopan",
    "14098": "Tlaquepaque",
    "14101": "Tonalá",
    "14097": "Tlajomulco de Zúñiga",
    "14070": "El Salto",
}

# Actividades SCIAN tech (6 dígitos — grupos relevantes)
ACTIVIDADES_TECH = [
    "517111",  # Telefonía
    "517210",  # Telecomunicaciones inalámbricas
    "518111",  # Centros de procesamiento de datos
    "518112",  # Hospedaje de páginas web
    "519130",  # Portales de búsqueda en internet
    "541511",  # Desarrollo y diseño de software
    "541512",  # Consultoría en computación
    "541513",  # Diseño de sistemas de cómputo
    "541519",  # Otros servicios de consultoría TI
    "611310",  # Universidades (para contexto del ecosistema)
]


def get_establecimientos(municipio_clave: str, actividad: str, token: str) -> list:
    """
    Consulta establecimientos de una actividad en un municipio via API DENUE.

    Args:
        municipio_clave: Clave INEGI del municipio (ej. "14039")
        actividad: Código SCIAN de actividad
        token: Token de API INEGI

    Returns:
        Lista de establecimientos (dicts)
    """
    url = f"{BASE_URL}/Buscar/{actividad}/{municipio_clave}/0/0/1000/{token}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        return []

    except requests.exceptions.RequestException as e:
        print(f"    [!] Error en API: {e}")
        return []


def fetch_all_tech_establishments() -> pd.DataFrame:
    """
    Descarga todos los establecimientos tech en todos los municipios ZMG.

    Returns:
        DataFrame con establecimientos tech ZMG
    """
    if not INEGI_TOKEN:
        print("[!] Token INEGI no encontrado.")
        print("    1. Regístrate en https://www.inegi.org.mx/app/developer/")
        print("    2. Crea un archivo .env con: INEGI_TOKEN=tu_token")
        return pd.DataFrame()

    all_records = []

    for mun_clave, mun_nombre in ZMG_MUNICIPIOS.items():
        print(f"\n[+] Descargando: {mun_nombre} ({mun_clave})")

        for actividad in ACTIVIDADES_TECH:
            establecimientos = get_establecimientos(mun_clave, actividad, INEGI_TOKEN)

            for est in establecimientos:
                record = {
                    "municipio_clave": mun_clave,
                    "municipio_nombre": mun_nombre,
                    "actividad_scian": actividad,
                    "id": est.get("ID", ""),
                    "nombre": est.get("Nombre", ""),
                    "razon_social": est.get("RazonSocial", ""),
                    "personal_ocupado": est.get("PersonalOcupado", ""),
                    "telefono": est.get("Telefono", ""),
                    "correo": est.get("Correo", ""),
                    "latitud": est.get("Latitud", None),
                    "longitud": est.get("Longitud", None),
                    "calle": est.get("Calle", ""),
                    "colonia": est.get("Colonia", ""),
                    "cp": est.get("CP", ""),
                }
                all_records.append(record)

            time.sleep(0.2)  # Respetar rate limit de la API

    if not all_records:
        print("[!] No se obtuvieron registros.")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)
    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")

    print(f"\n[+] Total establecimientos tech ZMG: {len(df):,}")
    print(df.groupby("municipio_nombre").size().sort_values(ascending=False).to_string())

    return df


def save_processed(df: pd.DataFrame) -> None:
    """Guarda el DataFrame procesado."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / "denue_tech_zmg.parquet"
    df.to_parquet(out_path, index=False)
    print(f"\n[+] Guardado en: {out_path}")

    # También exportar CSV para revisión rápida
    csv_path = PROCESSED_DIR / "denue_tech_zmg.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"[+] CSV exportado en: {csv_path}")


if __name__ == "__main__":
    df = fetch_all_tech_establishments()
    if not df.empty:
        save_processed(df)
