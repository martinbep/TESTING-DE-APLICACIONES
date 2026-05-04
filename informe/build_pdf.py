# -*- coding: utf-8 -*-
"""
Genera el PDF del informe TPO2.
Uso: pip install reportlab  &&  python build_pdf.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import black, grey, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether
)


HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(HERE, "BenitezPotochek_1195640_03052026_TPO2.pdf")
RESOURCES = os.path.join(HERE, "resources")
REPO_URL = "https://github.com/martinbep/TESTING-DE-APLICACIONES"


ss = getSampleStyleSheet()

style_titulo = ParagraphStyle(
    "tit", parent=ss["Title"], fontName="Helvetica-Bold",
    fontSize=22, textColor=black, alignment=TA_CENTER, spaceAfter=24,
)
style_meta = ParagraphStyle(
    "meta", parent=ss["Normal"], fontName="Helvetica",
    fontSize=12, leading=18, alignment=TA_LEFT, spaceAfter=6,
)
style_h1 = ParagraphStyle(
    "h1", parent=ss["Heading1"], fontName="Helvetica-Bold",
    fontSize=14, textColor=black, spaceBefore=14, spaceAfter=10,
)
style_body = ParagraphStyle(
    "body", parent=ss["Normal"], fontName="Helvetica",
    fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=6,
)
style_bullet = ParagraphStyle(
    "bul", parent=style_body, leftIndent=18, spaceAfter=2,
)
style_code = ParagraphStyle(
    "code", parent=ss["Code"], fontName="Courier",
    fontSize=9, leading=12, leftIndent=10, rightIndent=10,
    backColor=HexColor("#F4F4F4"), borderColor=HexColor("#CCCCCC"),
    borderWidth=0.5, borderPadding=6, spaceBefore=4, spaceAfter=8,
)
style_indice = ParagraphStyle(
    "idx", parent=style_body, fontSize=11, leading=20, spaceAfter=2,
)


def numerar(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 9)
    canv.setFillColor(grey)
    canv.drawCentredString(A4[0] / 2, 1.2 * cm, str(doc.page))
    canv.restoreState()


def p(t, s=style_body):
    return Paragraph(t, s)


def code(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = t.replace("\n", "<br/>").replace("  ", "&nbsp;&nbsp;")
    return Paragraph(t, style_code)


def bul(items):
    return [Paragraph("&#8226;&nbsp;&nbsp;" + i, style_bullet) for i in items]


def captura(nombre, descripcion):
    path = os.path.join(RESOURCES, nombre)
    if os.path.exists(path):
        try:
            img = Image(path)
            iw, ih = img.imageWidth, img.imageHeight
            ratio = min(15 * cm / iw, 9 * cm / ih, 1.0)
            img._restrictSize(iw * ratio, ih * ratio)
            return KeepTogether([img, p(f"<i>{descripcion}</i>", style_body)])
        except Exception:
            pass
    return p(f"[ Captura: {nombre} – {descripcion} ]", style_body)


def linea_indice(titulo, pagina):
    puntos = "." * max(2, 70 - len(titulo) - len(str(pagina)))
    return Paragraph(f"{titulo}{puntos}{pagina}", style_indice)


def build():
    s = []

    # ================ PORTADA ================
    s.append(Spacer(1, 4 * cm))
    s.append(p("TESTING DE APLICACIONES", style_titulo))
    s.append(Spacer(1, 3 * cm))
    s.append(p("Martín Benítez Potochek", style_meta))
    s.append(Spacer(1, 0.4 * cm))
    s.append(p("Materia: Testing de Aplicaciones", style_meta))
    s.append(Spacer(1, 0.4 * cm))
    s.append(p("Docente: Laime Huanca Abel Israel", style_meta))
    s.append(Spacer(1, 0.4 * cm))
    s.append(p("Fecha: 03/05/2026", style_meta))
    s.append(Spacer(1, 0.4 * cm))
    s.append(p("Título: TPO2 – Automatización de pruebas y pipeline CI/CD", style_meta))
    s.append(PageBreak())

    # ================ ÍNDICE ================
    s.append(p("Índice", style_h1))
    s.append(Spacer(1, 0.2 * cm))
    s.append(linea_indice("Parte 1 – Diseño del escenario de prueba", 3))
    s.append(linea_indice("Parte 2 – Automatización de pruebas", 3))
    s.append(linea_indice("Parte 3 – Implementación del pipeline (CI/CD)", 4))
    s.append(linea_indice("Parte 4 – Evidencia y análisis", 5))
    s.append(linea_indice("Parte 5 – Reflexión", 6))
    s.append(linea_indice("Conclusiones personales", 6))
    s.append(linea_indice("Propuestas de futuras mejoras", 6))
    s.append(linea_indice("Bibliografía", 7))
    s.append(PageBreak())

    # ================ PARTE 1 ================
    s.append(p("Parte 1 – Diseño del escenario de prueba", style_h1))
    s.append(p(
        "Para el TP elegí hacer una calculadora simple en Python con cuatro operaciones: "
        "sumar, restar, multiplicar y dividir. Es una funcionalidad fácil de probar y "
        "permite cubrir los tres tipos de casos que pide la consigna."
    ))
    s.append(p("<b>Escenario:</b> el usuario realiza operaciones aritméticas básicas."))
    s.append(p("<b>Casos de prueba:</b>"))
    s.extend(bul([
        "<b>Caso exitoso:</b> sumar(2, 3). Resultado esperado: 5.",
        "<b>Caso de error:</b> dividir(10, 0). Resultado esperado: lanza un error porque no se puede dividir por cero.",
        "<b>Caso borde:</b> sumar(-5, 3). Resultado esperado: -2 (suma con un número negativo).",
    ]))

    # ================ PARTE 2 ================
    s.append(p("Parte 2 – Automatización de pruebas", style_h1))
    s.append(p(
        "Los tres casos se automatizaron con pytest. Cada test es una función "
        "que llama a la calculadora y verifica el resultado con un assert."
    ))
    s.append(code(
        "import pytest\n"
        "from app.calculadora import sumar, dividir\n"
        "\n"
        "def test_sumar_dos_numeros():\n"
        "    assert sumar(2, 3) == 5\n"
        "\n"
        "def test_dividir_por_cero():\n"
        "    with pytest.raises(ValueError):\n"
        "        dividir(10, 0)\n"
        "\n"
        "def test_sumar_con_negativos():\n"
        "    assert sumar(-5, 3) == -2"
    ))
    s.append(PageBreak())

    # ================ PARTE 3 ================
    s.append(p("Parte 3 – Implementación del pipeline (CI/CD)", style_h1))
    s.append(p(
        "El pipeline está configurado con GitHub Actions, en el archivo "
        "<b>.github/workflows/tests.yml</b>. Cada vez que se hace un push al repositorio, "
        "GitHub corre los tests automáticamente y muestra si pasaron o no."
    ))
    s.append(p("<b>Pasos que ejecuta el pipeline:</b>"))
    s.extend(bul([
        "Bajar el código del repositorio.",
        "Instalar Python.",
        "Instalar las dependencias (pytest).",
        "Ejecutar los tests con pytest.",
        "Subir el reporte HTML como artefacto descargable.",
    ]))
    s.append(PageBreak())

    # ================ PARTE 4 ================
    s.append(p("Parte 4 – Evidencia y análisis", style_h1))
    s.append(p("<b>Capturas del pipeline ejecutándose:</b>"))
    s.append(captura("captura1_actions.png", "Pestaña Actions con el run en verde."))
    s.append(captura("captura2_steps.png", "Detalle del run con los pasos en verde."))
    s.append(captura("captura3_logs.png", "Logs del paso de pytest mostrando los tests OK."))
    s.append(captura("captura4_artefacto.png", "Artefacto del reporte disponible para descargar."))

    s.append(p("<b>Resultado:</b> los 3 tests terminaron OK."))
    s.append(p("<b>Repositorio:</b> " + REPO_URL))

    s.append(p("<b>¿Qué ventaja aporta automatizar pruebas dentro del pipeline?</b>"))
    s.append(p(
        "Que los tests corren solos cada vez que se sube código. Así nadie se olvida "
        "de probar antes de subir y los errores aparecen al toque."
    ))
    s.append(p("<b>¿Qué impacto tiene esto en la calidad del software?</b>"))
    s.append(p(
        "Mejora porque evita que código roto llegue a la rama principal. Cada cambio "
        "queda validado antes de quedar fijo en el proyecto."
    ))
    s.append(PageBreak())

    # ================ PARTE 5 ================
    s.append(p("Parte 5 – Reflexión", style_h1))
    s.append(p("<b>1. ¿Qué beneficios tiene automatizar pruebas frente a hacerlas manualmente?</b>"))
    s.append(p(
        "Son más rápidas y se ejecutan siempre igual. A mano uno puede saltearse un caso, "
        "automatizado no."
    ))
    s.append(p("<b>2. ¿Qué dificultades encontraste al implementar el pipeline?</b>"))
    s.append(p(
        "Lo más complicado fue armar el archivo del pipeline, sobre todo respetar la "
        "indentación porque cualquier espacio mal puesto rompe el workflow."
    ))
    s.append(p("<b>3. ¿Dónde aplicarías este enfoque en un entorno real?</b>"))
    s.append(p(
        "En cualquier proyecto donde más de una persona toque el mismo código. Así cada "
        "cambio queda validado antes de mergearlo y se evitan bugs en producción."
    ))

    s.append(p("Conclusiones personales", style_h1))
    s.append(p(
        "El TP me sirvió para entender en la práctica cómo funciona la automatización "
        "de pruebas. Una cosa es leerlo en la teoría y otra es ver el tilde verde "
        "aparecer solo en GitHub después de hacer un push."
    ))

    s.append(p("Propuestas de futuras mejoras", style_h1))
    s.append(p(
        "Sumaría más tests para cubrir más casos, agregaría medición de cobertura del "
        "código y probaría la calculadora en distintas versiones de Python."
    ))

    s.append(p("Bibliografía", style_h1))
    s.append(p(
        "TOLEDO, Federico. Capítulo: automatización de pruebas funcionales. Introducción "
        "a las pruebas en los sistemas de información. Montevideo, Uruguay: Abstracta, 2014."
    ))
    s.append(p("Documentación oficial de pytest: https://docs.pytest.org"))
    s.append(p("Documentación oficial de GitHub Actions: https://docs.github.com/actions"))

    return s


def main():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2.5 * cm, rightMargin=2.5 * cm,
        topMargin=2.5 * cm, bottomMargin=2 * cm,
        title="TPO2 - Testing de Aplicaciones",
        author="Martin Benitez Potochek",
    )
    doc.build(build(), onLaterPages=numerar, onFirstPage=lambda c, d: None)
    print(f"OK -> {OUTPUT}")


if __name__ == "__main__":
    main()
