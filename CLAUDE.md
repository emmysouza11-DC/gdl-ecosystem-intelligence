# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**GDL Ecosystem Intelligence** is a data analysis project investigating whether the tech sector boom (nearshoring) in Guadalajara has created a wage gap between tech workers and other sectors, and whether this correlates with rising housing costs in the Guadalajara Metropolitan Zone (ZMG).

**Research question:**
> ¿Ha generado el boom del nearshoring en Jalisco una brecha salarial entre trabajadores del sector tech y el resto de la economía — y está esa brecha correlacionada con el aumento en los precios de vivienda en la ZMG?

## Architecture & Data Pipeline

The project follows a standard data science ETL → EDA → Analysis → Visualization flow:

```
Raw Data (ENOE, DENUE, IED)
    ↓
src/ingestion/ (loaders download & preprocess)
    ↓
data/processed/ (parquet files)
    ↓
notebooks/ (exploratory analysis & visualization)
    ↓
reports/ (figures & executive summary)
```

### Key Modules

**src/ingestion/**
- `enoe_loader.py`: Loads ENOE microdata (employment surveys) from INEGI. Filters for ZMG municipalities (Guadalajara, Zapopan, Tlaquepaque, Tonalá, Tlajomulco, El Salto), classifies tech vs. non-tech sectors (SCIAN code 11), and exports as parquet.
  - Usage: `python src/ingestion/enoe_loader.py --year 2024 --quarter 4`
  - Outputs: `data/processed/enoe_zmg_YYYY_TQ.parquet`
  
- `denue_loader.py`: Queries INEGI's DENUE API to fetch tech establishments (software, IT services, telecoms, etc.) across ZMG municipalities with geolocation data.
  - Requires: `INEGI_TOKEN` in `.env` (register at https://www.inegi.org.mx/app/developer/)
  - Usage: `python src/ingestion/denue_loader.py`
  - Outputs: `data/processed/denue_tech_zmg.parquet` + CSV

**src/analysis/** (empty, to be filled with analysis utilities)

**src/visualization/** (empty, to be filled with reusable plotting helpers)

### Notebooks

- `notebooks/01_eda_enoe.ipynb`: Exploratory analysis of ENOE salary data comparing tech vs. non-tech sectors over time (2023 T4 – 2025 T4).
- Planned: 02_eda_denue, 03_eda_ied, 04_correlacion_vivienda, 05_hallazgos_finales (see README for details)

### Data Sources

All data is public and free:
- **ENOE** (INEGI): Employment & wage microdata, trimestral (2023 T4 – 2025 T4)
- **DENUE** (INEGI API): Business directory with SCIAN codes and geolocation
- **IED** (Secretaría de Economía): Foreign direct investment by state & sector
- **Housing**: INFONAVIT, SHF, real estate portals (Inmuebles24, Lamudi)
- **Education**: ANUIES statistics on tech graduates

See `docs/fuentes.md` for detailed variable mappings, SCIAN codes, and download instructions.

## Development Setup

### Prerequisites
- Python 3.11+
- pip or conda

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include pandas, numpy, matplotlib, seaborn, plotly, jupyter, geopandas, folium, requests, and python-dotenv.

### Configure Environment Variables
Create or update `.env`:
```
INEGI_TOKEN=your_token_from_https://www.inegi.org.mx/app/developer/
```

`.env` is listed in `.gitignore` and must not be committed.

## Common Development Commands

### Run ETL loaders
```bash
# Load a single ENOE quarter (requires CSV in data/raw/enoe/{year}/)
python src/ingestion/enoe_loader.py --year 2024 --quarter 4

# Fetch DENUE tech establishments (requires INEGI_TOKEN in .env)
python src/ingestion/denue_loader.py
```

### Start Jupyter for analysis
```bash
jupyter notebook notebooks/
# or
jupyter lab notebooks/
```

### View processed data
Processed files are saved as parquet in `data/processed/`:
- `enoe_zmg_YYYY_TQ.parquet` (salary, demographics, sector)
- `denue_tech_zmg.parquet` (establishments, geolocation)

Read via pandas: `pd.read_parquet("data/processed/enoe_zmg_2024_T4.parquet")`

## Key Design Patterns

### Sector Classification
- **Tech sector**: SCIAN code 11 (Servicios de información) in ENOE loader
- **DENUE queries**: Specific SCIAN 6-digit codes (517111 telecom, 541511 software, etc.) in `denue_loader.py`
- Variables: `es_tech` (boolean), `rama_est2` (numeric), `sector` (string label)

### Geographic Filtering
Both loaders filter for ZMG municipalities using INEGI codes:
- ENOE: `mun in ['039', '120', '098', '101', '097', '070']`
- DENUE: `municipio_clave in ['14039', '14120', ...]` (includes state prefix 14 = Jalisco)

### Notebook structure
Notebooks explicitly set `project_root` using `Path(__file__).resolve().parent.parent` or a hardcoded absolute path, then call `os.chdir(project_root)` so that relative paths like `data/processed/` resolve correctly from any working directory. The current hardcoded path in `01_eda_enoe.ipynb` is user-specific — update it when running on a different machine.

### Data handling
- CSV files are read with `encoding="latin-1"` (ENOE files use this encoding)
- Numeric conversions use `pd.to_numeric(..., errors='coerce')` to handle missing/malformed values
- Expansion weights (`fac_tri` in ENOE) should be used for population-level statistics

## Git Workflow

The repo is on `main` branch. Recent history shows:
- Data files (CSV, parquet, XLSX) are excluded via `.gitignore`
- `.env` is tracked (contains a sample INEGI_TOKEN for testing)
- Folder structure is preserved with `.gitkeep` files
- Commits follow pattern: `feat:`, `fix:`, `analysis:`, `docs:`

Before committing:
- Ensure raw data files are not staged (`.gitignore` handles this)
- Jupyter checkpoints are ignored
- Power BI `.pbix` files are excluded

## Notes for Future Development

- **Analysis & Visualization modules** (`src/analysis/`, `src/visualization/`) are empty stubs. Add reusable statistical functions and plotting helpers here as the project grows.
- **Additional notebooks** (02–05) are outlined in README; implement in order for cumulative analysis.
- **Power BI integration**: Reports are published separately; exported figures go in `reports/figures/`.
- **Housing data**: Currently planned; requires scraping real estate portals (document terms of use) or integrating INFONAVIT/SHF APIs.
- **Correlation analysis** (notebook 04) is the core research question; ensure statistical methods are clearly documented.

