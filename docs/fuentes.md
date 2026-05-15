# Fuentes de datos — GDL Ecosystem Intelligence

Documentación de cada fuente utilizada: URL de acceso, variables clave, período disponible y notas de descarga.

---

## 1. ENOE — Encuesta Nacional de Ocupación y Empleo

**Organismo:** INEGI  
**URL:** https://www.inegi.org.mx/programas/enoe/15ymas/  
**Acceso:** Descarga directa, gratuito  
**Periodicidad:** Trimestral (desde 2005)  
**Períodos utilizados:** 2018 T1 — 2024 T4  

### Variables clave para este proyecto

| Variable | Descripción |
|---|---|
| `ent` | Clave de entidad (14 = Jalisco) |
| `mun` | Clave de municipio |
| `rama_est2` | Rama de actividad económica |
| `ing_x_hrs` | Ingreso por hora trabajada |
| `cs_p13_1` | Nivel de escolaridad |
| `anios_esc` | Años de escolaridad |
| `pos_ocu` | Posición en la ocupación |
| `tue_b` | Tamaño de unidad económica |

### Notas de descarga

- Descargar archivos SDEMT (microdatos de trabajadores) por trimestre
- Filtrar por `ent == 14` (Jalisco) y municipios ZMG: 039, 097, 098, 101, 120
- Los municipios ZMG: Guadalajara (039), Zapopan (120), Tlaquepaque (098), Tonalá (101), Tlajomulco (097), El Salto (070)
- Rama tech relevante: código `43` (Información en medios masivos) + `51` (Servicios profesionales)

---

## 2. DENUE — Directorio Estadístico Nacional de Unidades Económicas

**Organismo:** INEGI  
**URL:** https://www.inegi.org.mx/app/mapa/denue/  
**API:** https://www.inegi.org.mx/app/api/denue/v1/consulta/  
**Acceso:** API con token gratuito (registro en INEGI)  
**Actualización:** Semestral  

### Variables clave

| Variable | Descripción |
|---|---|
| `id` | Clave única del establecimiento |
| `nom_estab` | Nombre del establecimiento |
| `codigo_act` | Código SCIAN de actividad |
| `per_ocu` | Personal ocupado (rango) |
| `municipio` | Municipio |
| `latitud / longitud` | Coordenadas |

### Códigos SCIAN relevantes (sector tech)

```
517 — Telecomunicaciones
518 — Procesamiento electrónico de información
519 — Otros servicios de información
541 — Servicios profesionales, científicos y técnicos
  5415 — Diseño de sistemas de cómputo
  5416 — Consultoría en administración
```

### Notas de descarga

- Registrarse en https://www.inegi.org.mx/app/developer/ para obtener token
- Consultar por municipio + código SCIAN
- Filtrar establecimientos con `per_ocu >= 3` (5-10 personas o más) para excluir micro-negocios informales

---

## 3. Inversión Extranjera Directa — Secretaría de Economía

**Organismo:** Secretaría de Economía  
**URL:** https://www.gob.mx/se/acciones-y-programas/competitividad-e-innovacion-inversion-extranjera-directa  
**Acceso:** Descarga de Excel trimestral, gratuito  
**Periodicidad:** Trimestral  
**Períodos:** 2010 — 2024  

### Variables clave

| Variable | Descripción |
|---|---|
| Entidad | Estado receptor |
| Sector | SCIAN 2 dígitos |
| Monto (MDD) | Millones de dólares |
| País de origen | País del inversionista |
| Trimestre | Período de reporte |

### Notas de descarga

- Archivo: `IED_por_entidad_federativa.xlsx`
- Filtrar por entidad = Jalisco
- Sectores de interés: 31-33 (Manufactura electrónica), 51-54 (Tech/Info/Prof)

---

## 4. Precios de vivienda — INFONAVIT / SHF

**Organismo:** INFONAVIT + Sociedad Hipotecaria Federal  
**URL INFONAVIT:** https://portalmx.infonavit.org.mx/wps/portal/infonavitmx/inicio  
**URL SHF:** https://www.shf.gob.mx/estadisticas/  
**Acceso:** Reportes públicos descargables  

### Variables clave

| Variable | Descripción |
|---|---|
| Municipio | ZMG |
| Precio mediano renta | MXN por mes |
| Precio mediano venta | MXN |
| Precio/m² | Indicador de mercado |
| Trimestre | Período |

### Notas de descarga

- SHF publica el Índice SHF de Precios de la Vivienda por estado
- Complementar con datos scrapeados de portales (Inmuebles24, Lamudi) si se requiere nivel colonia

---

## 5. Egresados de educación superior — ANUIES

**Organismo:** ANUIES (Asociación Nacional de Universidades)  
**URL:** https://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior/anuario-estadistico-de-educacion-superior  
**Acceso:** Descarga de anuarios estadísticos, gratuito  
**Periodicidad:** Anual  

### Variables clave

| Variable | Descripción |
|---|---|
| Institución | UdeG, Tec, UNIVA, etc. |
| Programa educativo | Carrera |
| Campo de formación | Tecnología, Ingeniería, etc. |
| Egresados | Número por año |
| Municipio | Sede del campus |

### Carreras tech de interés

- Ingeniería en Sistemas Computacionales
- Ingeniería en Tecnologías de la Información
- Ciencias de Datos / Inteligencia Artificial
- Ingeniería en Software
- Licenciatura en Informática

---

## Notas generales

- Todos los datos son **públicos y de acceso libre**
- Los microdatos de ENOE pueden ser pesados (>500MB por año). Usar `pd.read_csv(chunksize=...)` para leerlos eficientemente
- Para los shapefiles de municipios ZMG: descargar Marco Geoestadístico INEGI en https://www.inegi.org.mx/temas/mg/
- Los datos de renta de portales inmobiliarios requieren scraping — documentar términos de uso antes de proceder
