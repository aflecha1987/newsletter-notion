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

def p_links(links):
    """Multiple source links block."""
    rich = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(links):
        rich.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
        if i < len(links) - 1:
            rich.append({"type": "text", "text": {"content": " · "}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}}

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
    # --- PORTADA ---
    {
        "emoji": "🎓",
        "titulo": "China reforma su universidad: elimina 12.200 carreras obsoletas y las sustituye por IA, robótica y chips",
        "cuerpo": (
            "Entre 2021 y 2025, China revocó o suspendió 12.200 programas de grado universitario —más del 30% del mapa "
            "académico nacional— y añadió 10.200 nuevos centrados en inteligencia artificial, robótica, fabricación "
            "inteligente, biometría, neutralidad de carbono y gobernanza digital. Los programas eliminados se concentran "
            "en humanidades, lenguas extranjeras y administración de empresas, disciplinas que el gobierno considera "
            "saturadas o desconectadas del mercado laboral. Con 12,7 millones de graduados esperados en 2026, China "
            "apuesta por una mano de obra especializada en tecnología de frontera como palanca de competitividad global. "
            "Es la mayor reestructuración educativa a nivel mundial en décadas."
        ),
        "fuentes": [
            ("Gizmodo ES", "https://es.gizmodo.com/china-aplica-una-reestructuracion-educativa-al-eliminar-12-200-carreras-universitarias-en-cinco-anos-y-reemplazarlas-con-ia-robotica-e-inteligencia-encarnada-2000242247"),
            ("BioBioChile", "https://www.biobiochile.cl/noticias/sociedad/debate/2026/06/24/china-elimina-mas-de-12-mil-carreras-universitarias-por-la-ia-las-considera-obsoletas-y-las-reemplaza.shtml"),
            ("Diario Financiero", "https://www.df.cl/internacional/economia/china-elimina-mas-de-12-000-carreras-universitarias-y-acelera-formacion-en"),
        ],
    },
    # --- TECNOLOGÍA E IA ---
    {
        "emoji": "🤖",
        "titulo": "DeepSeek lanza V4: 1,6 billones de parámetros en chips Huawei y precios mínimos",
        "cuerpo": (
            "DeepSeek presentó su modelo V4 con 1,6 billones de parámetros, la primera gran IA de frontera entrenada "
            "íntegramente sobre procesadores Huawei Ascend (fabricados por SMIC), prescindiendo de hardware Nvidia. "
            "Los precios rompen el mercado: $3,48 por millón de tokens en la versión Pro y tan solo $0,28 en la versión "
            "Flash, muy por debajo de OpenAI y Anthropic. En benchmarks internos, V4 rinde de forma favorable frente a "
            "GPT-5 y Gemini 3.1 Pro. El lanzamiento consolida el ecosistema chino de IA soberana: chips domésticos + "
            "modelo de frontera de código abierto, un hito que los analistas equiparan a un nuevo «momento DeepSeek»."
        ),
        "fuentes": [
            ("Fortune", "https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/"),
            ("Tom's Hardware", "https://www.tomshardware.com/tech-industry/artificial-intelligence/deepseek-launches-1-6-trillion-parameter-v4-on-huawei-chips-as-us-escalates-ai-theft-accusations"),
            ("SCMP", "https://www.scmp.com/tech/big-tech/article/3354938/another-deepseek-moment-huawei-milestone-alters-china-trajectory-chip-race-analysts"),
        ],
    },
    {
        "emoji": "💾",
        "titulo": "Huawei introduce la «Ley de Escalado Tau»: chips equivalentes a 1,4 nm para 2031",
        "cuerpo": (
            "Huawei anunció la nueva Ley de Escalado Tau (τ), un marco teórico propio que establece cómo optimizar "
            "el rendimiento de chips sin depender de la reducción física del nodo. Según la empresa, esta metodología "
            "sentaría las bases para alcanzar una densidad de transistores equivalente a un proceso de 1,4 nanómetros "
            "en sus chips de IA de alta gama para 2031, usando las capacidades de SMIC. El avance apunta a que China "
            "puede seguir escalando potencia computacional por rutas alternativas a la litografía EUV de última "
            "generación, esquivando las restricciones de exportación estadounidenses."
        ),
        "fuentes": [
            ("SCMP", "https://www.scmp.com/tech/big-tech/article/3354938/another-deepseek-moment-huawei-milestone-alters-china-trajectory-chip-race-analysts"),
            ("CSIS", "https://www.csis.org/analysis/deepseek-huawei-export-controls-and-future-us-china-ai-race"),
        ],
    },
    {
        "emoji": "🗣️",
        "titulo": "Premier Li Qiang: «Los avances tecnológicos de China son una oportunidad para el mundo»",
        "cuerpo": (
            "El primer ministro Li Qiang defendió esta semana los avances tecnológicos de China ante la comunidad "
            "internacional, señalando que el crecimiento de empresas como Huawei y Unitree ofrece opciones más "
            "asequibles a mercados de todo el mundo. Li también reconoció la necesidad de una gobernanza rigurosa "
            "de la IA: «No podemos ignorar los riesgos de perder el control de la tecnología. Si la gobernanza no "
            "sigue el ritmo, podría haber graves consecuencias». El mensaje subraya el enfoque chino de liderazgo "
            "tecnológico responsable en el marco del 15.º Plan Quinquenal."
        ),
        "fuentes": [
            ("La Jornada", "https://www.jornada.com.mx/noticia/2026/06/24/economia/avances-tecnologicos-de-china-son-una-oportunidad-no-una-amenaza-dice-el-premier-li-quiang"),
        ],
    },
    {
        "emoji": "🦾",
        "titulo": "Unitree escala a 75.000 robots humanoides y 115.000 cuadrúpedos al año",
        "cuerpo": (
            "La startup de robótica Unitree Robotics —líder global en robots cuadrúpedos— anunció que ampliará su "
            "capacidad de producción a 75.000 robots humanoides y 115.000 robots cuadrúpedos anuales. En 2026, se "
            "espera que Unitree alcance una cuota del 49,3% del mercado chino de humanoides. El sector global prevé "
            "despachar 35.000 unidades humanoides este año —un aumento del 94% anual—, con China dominando la "
            "comercialización real mientras los rivales occidentales siguen mayoritariamente en fase de prototipo."
        ),
        "fuentes": [
            ("La Jornada", "https://www.jornada.com.mx/noticia/2026/05/10/economia/china-apuesta-a-robots-con-inteligencia-artificial-para-todo-tipo-de-labores"),
        ],
    },
    # --- ECONOMÍA ---
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de EVs chinos baten récord histórico en mayo: $9.200 millones (+50%)",
        "cuerpo": (
            "Las exportaciones chinas de vehículos eléctricos e híbridos alcanzaron en mayo de 2026 un nuevo récord "
            "mensual de $9.200 millones, casi un 50% más que el mismo período del año anterior. BYD lideró con "
            "160.644 unidades exportadas en mayo, un 80% más en términos anuales; las exportaciones suponen ya el "
            "42% de sus ventas totales. El sudeste asiático se consolidó como motor de crecimiento, absorbiendo "
            "$1.200 millones en vehículos chinos el pasado mes. BYD mantiene su objetivo de 1,5 millones de ventas "
            "en el exterior en 2026, siendo ya el mayor fabricante de EVs del mundo por delante de Tesla."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-06-24/china-s-electric-vehicle-exports-reach-record-high-in-may"),
            ("GreentechLead", "https://greentechlead.com/electric-vehicle/chinas-ev-exports-hit-record-9-2-bn-as-southeast-asia-drives-demand-surge-53904"),
            ("IEA Global EV Outlook 2026", "https://www.iea.org/reports/global-ev-outlook-2026/manufacturing-and-trade"),
        ],
    },
    # --- ENERGÍA ---
    {
        "emoji": "⚡",
        "titulo": "China impone consumo mínimo obligatorio de renovables en todos los sectores (Orden N.º 42)",
        "cuerpo": (
            "El 22 de junio, cuatro ministerios chinos publicaron conjuntamente la Orden N.º 42, que establece por "
            "primera vez cuotas mínimas obligatorias de consumo de energía renovable en todos los sectores de la "
            "economía, con plena entrada en vigor el 1 de agosto de 2026. La medida supone un cambio histórico: de "
            "incentivos voluntarios a evaluación obligatoria con metas regionales diferenciadas. Analistas del sector "
            "prevén una ola de inversión en solar fotovoltaico, almacenamiento de energía e hidrógeno verde. La "
            "medida se enmarca en el objetivo nacional de duplicar el suministro de energía no fósil para 2035."
        ),
        "fuentes": [
            ("PV Tech", "https://www.pv-tech.org/china-issues-renewables-consumption-rules-set-to-fuel-new-growth-cycle-for-solar-pv-and-energy-storage/"),
            ("Carbon Brief", "https://www.carbonbrief.org/china-briefing-11-june-2026-tech-clampdown-extreme-weather-provinces-energy-plans/"),
        ],
    },
    # --- ESPACIO ---
    {
        "emoji": "🚀",
        "titulo": "Tianwen-2 en camino: la misión más ambiciosa de China visita un asteroide y un cometa",
        "cuerpo": (
            "Desde junio de 2026, la sonda Tianwen-2 ha iniciado su travesía hacia el asteroide Kamoʻoalewa "
            "(2016 HO3) y posteriormente a un cometa, en la misión planetaria más compleja que China ha emprendido. "
            "El viaje combina sobrevuelo, órbita y aterrizaje en dos cuerpos celestes distintos, con el objetivo de "
            "recuperar muestras y estudiar el origen del sistema solar. En paralelo, la Estación Espacial Tiangong "
            "suma ya 21 acoplamientos acumulados (12 Shenzhou + 9 Tianzhou) y opera con tripulaciones permanentes "
            "de tres personas, con el siguiente hito en octubre: Shenzhou-24 con el primer cosmonauta pakistaní."
        ),
        "fuentes": [
            ("NASASpaceFlight", "https://www.nasaspaceflight.com/2026/02/china-roundup-020526/"),
            ("Space Odyssey Hub", "https://spaceodysseyhub.com/articles/china-tiangong-space-station-2026"),
        ],
    },
    {
        "emoji": "👩‍🚀",
        "titulo": "Shenzhou-23: Lai Ka-ying, primera astronauta de Hong Kong en el espacio",
        "cuerpo": (
            "El 25 de mayo de 2026, Lai Ka-ying —ex oficial de la Policía de Hong Kong— se convirtió en la primera "
            "persona de Hong Kong en viajar al espacio, a bordo de la Shenzhou-23. Su presencia refuerza la "
            "integración de Hong Kong en los grandes proyectos científicos nacionales y simboliza la apertura del "
            "programa espacial chino. La Shenzhou-23 forma parte de la rotación regular de la Estación Tiangong; "
            "el siguiente lanzamiento será la Shenzhou-24 en octubre de 2026, que incluirá al primer cosmonauta "
            "pakistaní, consolidando la dimensión internacional de la exploración espacial china."
        ),
        "fuentes": [
            ("Universe Discovery", "https://www.universediscovery.com/tiangong-space-station-2026/"),
            ("New Space Economy", "https://newspaceeconomy.ca/2026/03/17/chinas-space-program-past-present-and-future/"),
        ],
    },
]


def build_blocks():
    today = "25 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio y educacion.", bold=False),
        divider(),
    ]

    sections = {
        "🎓 EDUCACIÓN": [NOTICIAS[0]],
        "🤖 TECNOLOGÍA E INTELIGENCIA ARTIFICIAL": NOTICIAS[1:5],
        "📈 ECONOMÍA": [NOTICIAS[5]],
        "⚡ ENERGÍA Y MEDIO AMBIENTE": [NOTICIAS[6]],
        "🚀 ESPACIO": NOTICIAS[7:],
    }

    for section_title, items in sections.items():
        blocks.append(h1(section_title))
        for n in items:
            blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
            blocks.append(p(n["cuerpo"]))
            blocks.append(p_links(n["fuentes"]))
            blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 18-25 Junio 2026"
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
