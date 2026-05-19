from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "reports", "GDL_Ecosystem_Intelligence_Ejecutivo.pdf")
DASHBOARD_IMG = os.path.join(BASE_DIR, "reports", "figures", "11_dashboard_powerbi.png")

# Colores
AZUL_MARINO = colors.HexColor("#1E3A5F")
AZUL_CLARO = colors.HexColor("#2E86AB")
GRIS = colors.HexColor("#666666")
GRIS_CLARO = colors.HexColor("#F5F5F5")

def build_styles():
    styles = getSampleStyleSheet()
    custom = {
        "titulo": ParagraphStyle("titulo", fontSize=15, textColor=AZUL_MARINO,
                                  alignment=TA_CENTER, spaceAfter=6, leading = 20, fontName="Helvetica-Bold"),
        "subtitulo": ParagraphStyle("subtitulo", fontSize=10, textColor=AZUL_CLARO,
                                     alignment=TA_CENTER, spaceAfter=6,leading = 14, fontName="Helvetica"),
        "seccion": ParagraphStyle("seccion", fontSize=11, textColor=AZUL_MARINO,
                                   spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=9, textColor=colors.black,
                                spaceAfter=4, fontName="Helvetica", leading=14,
                                alignment=TA_JUSTIFY),
        "pregunta": ParagraphStyle("pregunta", fontSize=10, textColor=AZUL_MARINO,
                                    fontName="Helvetica-BoldOblique", alignment=TA_CENTER,
                                    spaceAfter=8, leading=16),
        "footer": ParagraphStyle("footer", fontSize=7, textColor=GRIS,
                                  alignment=TA_CENTER, fontName="Helvetica"),
        "conclusion": ParagraphStyle("conclusion", fontSize=9, textColor=colors.black,
                                      fontName="Helvetica", leading=14, spaceAfter=4,
                                      alignment=TA_JUSTIFY),
    }
    return custom

def build_hallazgos_table():
    data = [
        ["Hallazgo", "Valor", "Fuente"],
        ["Brecha salarial tech vs no-tech (2024-T4)", "+34%\n($69.77 vs $52.08 MXN/hora)", "ENOE · INEGI"],
        ["Crecimiento de la brecha (2023-T4 → 2024-T4)", "+12.4 pp", "ENOE · INEGI"],
        ["Establecimientos tech en ZMG", "552\n(49% en Guadalajara)", "DENUE · INEGI"],
        ["Correlación brecha salarial ↔ vivienda SHF", "r = 0.001\n(no significativa)", "ENOE + SHF"],
    ]
    table = Table(data, colWidths=[7.5*cm, 4.5*cm, 4*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL_MARINO),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("BACKGROUND", (0,1), (-1,-1), GRIS_CLARO),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRIS_CLARO]),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 8),
        ("ALIGN", (1,0), (1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
    ]))
    return table

def build_stack_table():
    data = [
        ["Herramienta", "Uso"],
        ["Python 3.11 · pandas · matplotlib · seaborn", "ETL y análisis exploratorio"],
        ["geopandas", "Visualización geoespacial"],
        ["Jupyter Notebooks", "Análisis reproducible"],
        ["Power BI Desktop", "Dashboard ejecutivo"],
        ["GitHub · Claude Code", "Control de versiones y desarrollo"],
    ]
    table = Table(data, colWidths=[9*cm, 7*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL_CLARO),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRIS_CLARO]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ]))
    return table

def generate():
    styles = build_styles()
    doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=1.2*cm, bottomMargin=1.2*cm)
    story = []

    # PÁGINA 1
    story.append(Paragraph("GDL Ecosystem Intelligence", styles["titulo"]))
    story.append(Paragraph("Nearshoring, Brecha Salarial y Vivienda en la ZMG · 2023–2025", styles["subtitulo"]))
    story.append(HRFlowable(width="100%", thickness=2, color=AZUL_MARINO, spaceAfter=6))

    story.append(Paragraph("Pregunta de Investigación", styles["seccion"]))
    story.append(Paragraph(
        "¿Ha generado el boom del nearshoring en Jalisco una brecha salarial entre trabajadores "
        "del sector tech y el resto de la economía, y está esa brecha correlacionada con el "
        "aumento en los precios de vivienda en la ZMG?", styles["pregunta"]))

    story.append(Paragraph("Hallazgos Principales", styles["seccion"]))
    story.append(build_hallazgos_table())
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Dashboard Ejecutivo", styles["seccion"]))
    if os.path.exists(DASHBOARD_IMG):
        story.append(Image(DASHBOARD_IMG, width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Emmanuel Souza · Data Science Portfolio · GitHub: emmysouza11-DC · Guadalajara, Jalisco · 2025",
        styles["footer"]))

    # PÁGINA 2
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    story.append(Paragraph("GDL Ecosystem Intelligence", styles["titulo"]))
    story.append(Paragraph("Metodología y Conclusiones", styles["subtitulo"]))
    story.append(HRFlowable(width="100%", thickness=2, color=AZUL_MARINO, spaceAfter=6))

    story.append(Paragraph("Stack Tecnológico", styles["seccion"]))
    story.append(build_stack_table())
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Fuentes de Datos", styles["seccion"]))
    story.append(Paragraph(
        "ENOE (INEGI) — salarios y empleo ZMG · DENUE (INEGI) — establecimientos tech "
        "por municipio · SHF — Índice de Precios de Vivienda ZMG · "
        "870,194 registros procesados · 9 trimestres analizados (2023-T4 a 2025-T4)",
        styles["body"]))

    story.append(Paragraph("Limitaciones Metodológicas", styles["seccion"]))
    story.append(Paragraph(
        "• Muestra ENOE sector tech menor a 50 registros en 2025-T1 y 2025-T2 — "
        "KPIs acotados al rango 2023-T4/2024-T4 donde la muestra es estadísticamente confiable.",
        styles["body"]))
    story.append(Paragraph(
        "• Se recomienda complementar con microdatos IMSS para mayor robustez en trimestres recientes.",
        styles["body"]))
    story.append(Paragraph(
        "• La correlación con vivienda requiere series más largas (5+ años) para conclusiones definitivas.",
        styles["body"]))

    story.append(Paragraph("Conclusión", styles["seccion"]))
    story.append(Paragraph(
        "El análisis confirma la existencia de una brecha salarial tech/no-tech documentada y "
        "creciente en la ZMG durante el período 2023-2024 (+34% en 2024-T4, creciendo +12.4 pp "
        "desde 2023-T4), consistente con el proceso de nearshoring en Jalisco.",
        styles["conclusion"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Sin embargo, no se encontró correlación estadística entre esa brecha y el índice de "
        "precios de vivienda SHF (r = 0.001). Los precios de vivienda en la ZMG muestran una "
        "trayectoria independiente de la evolución salarial del sector tech en el período analizado, "
        "lo que sugiere que otros factores estructurales explican el encarecimiento inmobiliario "
        "de la zona metropolitana.",
        styles["conclusion"]))

    story.append(Spacer(1, 2*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GRIS, spaceAfter=8))
    story.append(Paragraph(
        "Proyecto de portafolio profesional en Data Science · Datos públicos · Uso educativo y de investigación",
        styles["footer"]))
    story.append(Paragraph(
        "Emmanuel Souza · GitHub: emmysouza11-DC · Guadalajara, Jalisco · 2025",
        styles["footer"]))

    doc.build(story)
    print(f"PDF generado exitosamente: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate()
