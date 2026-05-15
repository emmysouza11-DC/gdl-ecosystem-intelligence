# GDL Ecosystem Intelligence

> Análisis de datos del ecosistema tecnológico, mercado laboral y vivienda en la Zona Metropolitana de Guadalajara (ZMG)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Data](https://img.shields.io/badge/Fuentes-INEGI%20·%20ENOE%20·%20DENUE-green)
![Status](https://img.shields.io/badge/Status-En%20desarrollo-orange)

---

## Pregunta de investigación

**¿Ha generado el boom del nearshoring en Jalisco una brecha salarial entre trabajadores del sector tech y el resto de la economía — y está esa brecha correlacionada con el aumento en los precios de vivienda en la ZMG?**

Guadalajara es hoy el hub tecnológico más importante de México fuera de la CDMX: más de 1,000 empresas tech, $890 millones en IED en 2025 (Oracle, Microsoft, Intel) y una tasa de crecimiento del ecosistema del 16.8% anual. Sin embargo, no existe ninguna fuente pública que consolide y responda visualmente esta pregunta con datos abiertos.

Este proyecto lo hace.

---

## Estructura del repositorio

```
gdl-ecosystem-intelligence/
│
├── data/
│   ├── raw/              # Datos originales sin modificar (ENOE, DENUE, SE)
│   ├── processed/        # Datos limpios listos para análisis
│   └── external/         # Referencias externas (shapefiles ZMG, catálogos)
│
├── notebooks/
│   ├── 01_eda_enoe.ipynb          # Exploración: salarios y empleo ZMG
│   ├── 02_eda_denue.ipynb         # Exploración: densidad empresas tech
│   ├── 03_eda_ied.ipynb           # Exploración: inversión extranjera Jalisco
│   ├── 04_correlacion_vivienda.ipynb  # Análisis: salarios vs precios renta
│   └── 05_hallazgos_finales.ipynb # Síntesis y visualizaciones exportables
│
├── src/
│   ├── ingestion/        # Scripts de descarga y carga de datos
│   ├── analysis/         # Funciones de análisis y estadística
│   └── visualization/    # Helpers para gráficas reproducibles
│
├── reports/
│   ├── figures/          # Gráficas exportadas (PNG/SVG)
│   └── executive_summary.pdf  # Resumen ejecutivo de hallazgos
│
├── docs/
│   └── fuentes.md        # Documentación de fuentes de datos
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Módulos de análisis

| Módulo | Fuente | Pregunta que responde |
|---|---|---|
| Empleo y salarios tech | ENOE INEGI (2018–2024) | ¿Cuánto gana un trabajador tech vs no-tech en ZMG? |
| Densidad empresas | DENUE INEGI | ¿Dónde se concentran las empresas tech en la ZMG? |
| Inversión extranjera | Secretaría de Economía | ¿Cuánta IED ha llegado a Jalisco y de qué sectores? |
| Precio de vivienda | INFONAVIT / portales | ¿Cómo han evolucionado las rentas por municipio? |
| Egresados tech | SEP / ANUIES | ¿Cuántos profesionales tech se gradúan en GDL por año? |

---

## Hallazgos principales

> *En construcción — se actualizará al concluir cada semana de análisis.*

---

## Cómo reproducir el análisis

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/gdl-ecosystem-intelligence.git
cd gdl-ecosystem-intelligence

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar notebooks en orden
jupyter notebook notebooks/
```

---

## Fuentes de datos

Todos los datos utilizados son **públicos y de acceso libre**:

- [ENOE - INEGI](https://www.inegi.org.mx/programas/enoe/15ymas/) — Encuesta Nacional de Ocupación y Empleo
- [DENUE - INEGI](https://www.inegi.org.mx/app/mapa/denue/) — Directorio Estadístico Nacional de Unidades Económicas
- [Secretaría de Economía](https://www.gob.mx/se) — Inversión Extranjera Directa por estado
- [INFONAVIT](https://portalmx.infonavit.org.mx/) — Indicadores del mercado de vivienda
- [ANUIES](https://www.anuies.mx/) — Estadísticas de educación superior

---

## Stack tecnológico

- **Python 3.11** — pipeline ETL y análisis estadístico
- **pandas / numpy** — transformación y limpieza de datos
- **matplotlib / seaborn / plotly** — visualización exploratoria
- **Power BI** — dashboard interactivo publicado
- **Jupyter Notebooks** — análisis documentado y reproducible
- **GitHub Actions** *(futuro)* — actualización automática de datos

---

## Autor

Proyecto de análisis de datos desarrollado como parte del portafolio profesional.
Guadalajara, Jalisco — 2025

---

*Los datos utilizados son públicos. El análisis y las conclusiones son del autor.*
