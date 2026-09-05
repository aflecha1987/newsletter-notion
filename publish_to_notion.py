#!/usr/bin/env python3
"""
Publica la newsletter semanal de China Al Dia en Notion.
Uso: NOTION_TOKEN=<token> python publish_to_notion.py
"""

import json
import os
import subprocess
import sys
from datetime import date

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
PARENT_PAGE_ID = os.environ.get("PARENT_PAGE_ID", "34ae9ac6c5268056bd3cfeddc772dddc")

if not NOTION_TOKEN:
    print("ERROR: define la variable de entorno NOTION_TOKEN antes de ejecutar.")
    sys.exit(1)

API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def notion_request(method, endpoint, data=None):
    url = f"{API_BASE}{endpoint}"
    cmd = [
        "curl", "-s", "-X", method, url,
        "-H", f"Authorization: Bearer {NOTION_TOKEN}",
        "-H", "Content-Type: application/json",
        "-H", f"Notion-Version: {NOTION_VERSION}",
    ]
    if data:
        cmd += ["-d", json.dumps(data, ensure_ascii=False)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error curl: {result.stderr}")
        sys.exit(1)
    if not result.stdout.strip():
        print("Error: respuesta vacia del servidor")
        sys.exit(1)
    resp = json.loads(result.stdout)
    if resp.get("object") == "error":
        print(f"Error Notion API: {resp.get('message')}")
        sys.exit(1)
    return resp


# --- Bloques Notion ---

def h1(text):
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def p(text, bold=False):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text},
                                         "annotations": {"bold": bold}}]}}

def p_link(label, url):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Fuente: "}},
                {"type": "text", "text": {"content": label, "link": {"url": url}},
                 "annotations": {"italic": True, "color": "blue"}}
            ]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def callout(text, emoji="📌"):
    return {"object": "block", "type": "callout",
            "callout": {"icon": {"type": "emoji", "emoji": emoji},
                        "rich_text": [{"type": "text", "text": {"content": text}}]}}

def quote(text):
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


NOTICIAS = [
    {
        "emoji": "☀️",
        "titulo": "La energía solar supera al carbón por primera vez en capacidad instalada — hito histórico mundial",
        "cuerpo": (
            "Al cierre de julio de 2026, la capacidad fotovoltaica instalada en China alcanzó 1.286 GW, "
            "superando por primera vez en la historia los 1.285 GW de la energía a carbón. La energía "
            "solar se convierte así en la mayor fuente de electricidad del país por potencia instalada, "
            "representando el 31,5 % del parque eléctrico nacional. Solo en los primeros siete meses del "
            "año, la generación solar creció un 15,5 % interanual, alcanzando 802.400 millones de kWh. "
            "China confirmó el hito el 1 de septiembre de 2026."
        ),
        "fuente_label": "Infobae — La energía solar supera por primera vez al carbón en China",
        "fuente_url": "https://www.infobae.com/america/agencias/2026/09/01/la-energia-solar-supera-por-primera-vez-al-carbon-en-capacidad-instalada-en-china/",
    },
    {
        "emoji": "🌐",
        "titulo": "Xi Jinping en la Cumbre de la OCS en Bishkek y visita de Estado a Egipto",
        "cuerpo": (
            "Del 30 de agosto al 3 de septiembre, el presidente Xi Jinping participó en la Cumbre de la "
            "Organización de Cooperación de Shanghái (OCS) en Bishkek, Kirguistán, junto con líderes de "
            "Rusia, India e Irán. La cumbre concluyó con la adopción de la 'Declaración de Biskek' y la "
            "firma de casi 30 acuerdos de cooperación regional. En su visita de Estado a Egipto, Xi y el "
            "presidente Al-Sisi anunciaron proyectos conjuntos que incluyen un centro de negocios al este "
            "de El Cairo y una línea ferroviaria eléctrica en el delta del Nilo."
        ),
        "fuente_label": "Xinhua en español — Xi asiste a cumbre de OCS y realiza visita de Estado",
        "fuente_url": "https://spanish.news.cn/temas/202608/hd02.html",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate todos los récords en agosto: 440.293 unidades y exportaciones +134 %",
        "cuerpo": (
            "BYD entregó 440.293 vehículos de nueva energía en agosto de 2026, su mejor mes del año, "
            "incluyendo un récord de 256.230 coches 100 % eléctricos (+18 % interanual). La cifra más "
            "llamativa fue la de exportaciones: 189.466 unidades enviadas al exterior, un incremento del "
            "134,45 % respecto a agosto de 2025. En el acumulado de enero a agosto, las exportaciones "
            "ya representan el 43,56 % de las ventas totales. BYD también reportó un aumento del 30 % "
            "en sus beneficios gracias al tirón de los mercados europeos, latinoamericanos y del sudeste asiático."
        ),
        "fuente_label": "Somos Eléctricos — El récord de BYD que preocupa a sus rivales",
        "fuente_url": "https://www.somoselectricos.com/coches-electricos/record-byd-que-preocupa-rivales-256230-coches-electricos-mes/20260903124946062821.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Kimi K3 entra en el top 3 mundial de modelos de IA y China lanza el plan AI+",
        "cuerpo": (
            "El modelo Kimi K3 de la empresa china Moonshot AI debutó en el tercer puesto del ranking "
            "global de Artificial Analysis, solo por detrás de los últimos modelos de Anthropic y OpenAI. "
            "En el segmento de generación de vídeo, Kling compite directamente con Sora y Veo. En agosto, "
            "el gobierno chino lanzó oficialmente el plan AI+, que plantea usar la inteligencia artificial "
            "como infraestructura transversal para todos los sectores productivos del país."
        ),
        "fuente_label": "Guillermo del Pino — Mejores IA chinas en 2026",
        "fuente_url": "https://guillermodelpino.com/hub/mejores-ia-chinas-2026",
    },
    {
        "emoji": "🦾",
        "titulo": "Producción de robots humanoides supera las 100.000 unidades — China controla el 97 % del mercado",
        "cuerpo": (
            "China superará las 100.000 unidades de robots humanoides producidas en 2026, según el "
            "Ministerio de Industria y Tecnología de la Información. Los envíos mundiales crecieron un "
            "272 % en el primer semestre, y las empresas chinas concentraron el 97 % del total global. "
            "Marcas como Unitree, UBTECH y Agibot ya despliegan robots en fábricas de BYD y Geely Zeekr, "
            "donde realizan tareas logísticas y de ensamblaje. Un robot puede sustituir a 2-3 operarios, "
            "ahorrando más de 150.000 yuanes anuales en costes laborales."
        ),
        "fuente_label": "Confirmado.net — Producción de robots humanoides de China superará las 100.000 unidades",
        "fuente_url": "https://confirmado.net/la-produccion-de-robots-humanoides-de-china-superara-las-100-000-unidades-este-ano/",
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e 7: China prepara su misión más ambiciosa a la Luna en busca de agua en el polo sur",
        "cuerpo": (
            "China se encuentra a pocas semanas del lanzamiento de Chang'e 7, la misión robótica más "
            "compleja de su programa lunar. La sonda incluirá cuatro vehículos —orbitador, módulo de "
            "alunizaje, rover y un dispositivo de saltos— que trabajarán en el polo sur lunar, donde se "
            "sospecha la existencia de hielo de agua. La misión portará instrumentos para perforar y "
            "analizar directamente el hielo, algo que ningún país ha intentado aún con misiones robóticas. "
            "China compite con EE.UU. por establecer el primer campamento permanente en la Luna."
        ),
        "fuente_label": "El Español — China, a pocas horas de su misión más compleja a la Luna",
        "fuente_url": "https://www.elespanol.com/omicrono/defensa-y-espacio/20260823/china-pocas-horas-mision-compleja-luna-busca-agua-arrebatar-liderazgo-espacial-nasa/1003744359223_0.html",
    },
    {
        "emoji": "📈",
        "titulo": "XV Plan Quinquenal 2026-2030: autosuficiencia tecnológica y PIB que supera los 20 billones",
        "cuerpo": (
            "El XV Plan Quinquenal (2026-2030) reorienta la economía china hacia la innovación original "
            "y la autosuficiencia científica, priorizando semiconductores, IA, robótica, 6G y biotecnología. "
            "Para 2026, China mantiene un crecimiento cercano al 4,5-5 % del PIB, y las proyecciones del "
            "FMI sitúan la economía china por encima de los 20 billones de dólares. El plan incluye también "
            "la ampliación del mercado interno para reducir la dependencia de las exportaciones, en lo que "
            "los analistas llaman el 'gran reequilibrio' de la economía china."
        ),
        "fuente_label": "China Briefing — China en 2026: sectores clave a observar",
        "fuente_url": "https://www.china-briefing.com/news/china-en-2026-sectores-clave-a-observar/",
    },
    {
        "emoji": "🤝",
        "titulo": "Feria Internacional de Xiamen: 123 países confirman presencia — nueva ampliación del TLC con Suiza",
        "cuerpo": (
            "La 26.ª Feria Internacional de Inversión y Comercio de China se celebrará del 8 al 11 de "
            "septiembre en Xiamen, con delegaciones de 123 países y regiones y 60 pabellones nacionales. "
            "El evento consolida a China como eje del comercio y la inversión multilateral. En paralelo, "
            "China y Suiza avanzan en la ampliación del Acuerdo de Libre Comercio bilateral, con el "
            "objetivo de duplicar la cobertura de productos con preferencias arancelarias."
        ),
        "fuente_label": "Xinhua — Feria Internacional de Inversión y Comercio de China",
        "fuente_url": "https://spanish.news.cn/temas/202608/hd02.html",
    },
    {
        "emoji": "✈️",
        "titulo": "Air China estrena el avión COMAC C919 en ruta internacional: Beijing-Ulán Bator",
        "cuerpo": (
            "A partir del 12 de agosto de 2026, Air China comenzó a operar un vuelo diario entre Beijing "
            "y Ulán Bator (Mongolia) con el COMAC C919, el avión de fuselaje estrecho de fabricación "
            "100 % nacional. Es uno de los primeros despliegues comerciales internacionales del avión, "
            "fabricado íntegramente en China como alternativa al Boeing 737 y al Airbus A320. El modelo "
            "ya opera en docenas de rutas domésticas y su exportación a varias aerolíneas asiáticas "
            "está en negociación activa."
        ),
        "fuente_label": "Xinhua en español — Air China opera vuelo con avión de fabricación nacional a Ulán Bator",
        "fuente_url": "https://spanish.news.cn/temas/202608/hd02.html",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio y sociedad.", bold=False),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        blocks.append(p_link(n["fuente_label"], n["fuente_url"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 29 Ago - 5 Sep 2026"
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🇨🇳"},
        "cover": {"type": "external", "external": {
            "url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
        }},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": build_blocks(),
    }

    print(f"Creando pagina en Notion: '{title}'")
    print(f"Noticias incluidas: {len(NOTICIAS)}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "").replace("-", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id}")
    print(f"\nListo!")
    print(f"URL: {page_url}")
    return page_url


if __name__ == "__main__":
    create_notion_page()
