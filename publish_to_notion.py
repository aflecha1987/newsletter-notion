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
        "emoji": "🦾",
        "titulo": "Unitree Robotics aprobada para su OPV de $6.200 millones en el STAR Market de Shanghái",
        "cuerpo": (
            "El 1 de junio de 2026, la comisión de listado de la Bolsa de Shanghái aprobó oficialmente "
            "la salida a bolsa de Unitree Robotics, el mayor fabricante de robots humanoides de China "
            "—y del mundo—. La empresa busca recaudar 4.200 millones de yuanes (~608 millones de dólares) "
            "con una valoración total de 42.000 millones de yuanes (~6.200 millones de dólares). Fundada "
            "en Hangzhou en 2016 por Wang Xingxing, Unitree acumula 1.700 millones de yuanes en ingresos "
            "y controla el 69,75% del mercado mundial de robots cuadrúpedos. El IPO fue revisado en solo "
            "73 días —velocidad récord—, señal de la prioridad estratégica que Pekín concede al sector."
        ),
        "fuente_label": "Caixin Global — Unitree Fast-Tracks Shanghai IPO at $6.2B Valuation",
        "fuente_url": "https://www.caixinglobal.com/2026-05-26/unitree-fast-tracks-shanghai-ipo-with-target-valuation-of-62-billion-102447449.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Kimi K2.6: el mejor modelo de IA open-source del mundo en programación autónoma",
        "cuerpo": (
            "Moonshot AI lanzó Kimi K2.6 en abril de 2026, obteniendo entre 56 y 59 puntos en "
            "SWE-Bench Pro —la referencia más exigente para evaluar la programación autónoma de IAs—, "
            "lo que lo sitúa a la cabeza de todos los modelos de código abierto disponibles. Es el "
            "tercer salto de la familia K2 en menos de un año: K2 (julio 2025), K2.5 (enero 2026) y "
            "K2.6 (abril 2026). Los tres modelos son open-weights y se ofrecen a precios inferiores "
            "a sus equivalentes occidentales. Alibaba, por su parte, ha superado los 1.000 millones "
            "de descargas de sus modelos Qwen abiertos, consolidando la estrategia de IA abierta de China."
        ),
        "fuente_label": "SCMP — China's Moonshot AI launches Kimi K2.6, No.1 among open-source systems",
        "fuente_url": "https://www.scmp.com/tech/tech-trends/article/3331971/chinas-moonshot-ai-launches-new-model-lauded-no-1-among-open-source-systems",
    },
    {
        "emoji": "🏭",
        "titulo": "CATL despliega robots humanoides en su fábrica: 99% de éxito y triple productividad humana",
        "cuerpo": (
            "CATL, el mayor fabricante mundial de baterías para vehículos eléctricos, ha desplegado "
            "a gran escala robots humanoides Xiaomo —desarrollados por la startup Spirit AI, respaldada "
            "por el propio CATL— en su planta de Luoyang (Henan). Los robots conectan enchufes de alta "
            "tensión en las líneas de producción con un 99% de tasa de éxito y una productividad tres "
            "veces superior a la humana, gracias a que trabajan sin pausas. Su modelo de IA "
            "Vision-Language-Action les permite adaptarse en tiempo real a variaciones del entorno. "
            "CATL califica este despliegue como el primero a gran escala de robots humanoides en "
            "producción industrial de alto volumen en el mundo."
        ),
        "fuente_label": "SCMP — CATL marks trailblazing deployment of humanoid robots at scale",
        "fuente_url": "https://www.scmp.com/tech/big-tech/article/3336939/chinas-catl-marks-trailblazing-deployment-humanoid-robots-scale-factory-floor",
    },
    {
        "emoji": "🔩",
        "titulo": "ENGINEAI abre la fábrica de robots humanoides más rápida del mundo: 1 unidad cada 15 minutos",
        "cuerpo": (
            "La empresa ENGINEAI inauguró una planta inteligente de más de 12.000 m² en el distrito "
            "Honghualing de Shenzhen, donde ya salen de la línea los primeros robots T800. La instalación "
            "está diseñada para producir un robot humanoide cada 15 minutos —la tasa más alta del mundo—. "
            "Otra empresa, Leju Robotics (Guangdong), cuenta con capacidad para 10.000 unidades al año. "
            "China se ha fijado el objetivo de desplegar entre 28.000 y 100.000 robots humanoides a lo "
            "largo de 2026. Datos de 2025 confirman que el 87-90% de los robots humanoides enviados "
            "globalmente ya son de fabricación china."
        ),
        "fuente_label": "Interesting Engineering — ENGINEAI's factory builds one humanoid robot every 15 mins",
        "fuente_url": "https://interestingengineering.com/ai-robotics/china-engineai-humanoid-robot-factory",
    },
    {
        "emoji": "🚀",
        "titulo": "Tianwen-2 llega al asteroide Kamo'oalewa: muestras previstas para julio de 2026",
        "cuerpo": (
            "En junio de 2026, la sonda Tianwen-2 —lanzada en mayo de 2025— completa 13 meses de "
            "travesía e inicia su inserción orbital alrededor del asteroide Kamooalewa (469219), "
            "un cuasi-satélite de la Tierra de entre 40 y 100 metros de diámetro. Su espectro de "
            "reflectancia recuerda a la roca lunar, lo que sugiere que podría ser un fragmento expulsado "
            "por un antiguo impacto en la Luna. La sonda está caracterizando la forma, rotación y "
            "composición del asteroide antes de descender a recoger muestras, previstas para julio de 2026. "
            "Las muestras regresarán a la Tierra a finales de 2026 o principios de 2027, convirtiendo "
            "a China en el segundo país —tras Japón— en traer material de un asteroide."
        ),
        "fuente_label": "Space.com — China's Tianwen-2 heads for mysterious quasi-moon asteroid",
        "fuente_url": "https://www.space.com/space-exploration/missions/chinas-tianwen-2-spacecraft-sends-home-1st-photo-as-it-heads-for-mysterious-quasi-moon-asteroid",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate récord de exportaciones en mayo: 160.644 unidades al exterior (+80,4%)",
        "cuerpo": (
            "BYD cerró mayo de 2026 con 383.453 vehículos eléctricos e híbridos vendidos en total, "
            "de los cuales 160.644 fueron exportaciones —nuevo máximo histórico con un crecimiento del "
            "80,4% interanual—. La compañía ha elevado su objetivo de exportaciones 2026 a 1,5 millones "
            "de unidades, frente a 1,3 millones anteriormente, mientras los mercados de Asia-Pacífico, "
            "Europa y Latinoamérica siguen absorbiendo demanda. En abril los NEV superaron por primera "
            "vez el 50% de todas las exportaciones de coches chinos, y la penetración de NEV en el "
            "mercado doméstico alcanzó el 60%."
        ),
        "fuente_label": "Electric Cars Report — BYD May 2026: record overseas demand",
        "fuente_url": "https://electriccarsreport.com/2026/06/byd-may-2026-sales-rise-as-overseas-demand-reaches-new-record/",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones chinas: +14% en Q1 2026, con África (+32%) y UE (+21%) liderando el avance",
        "cuerpo": (
            "Las exportaciones chinas en el primer trimestre de 2026 alcanzaron los 977.600 millones "
            "de dólares (+14% interanual), impulsadas por la manufactura avanzada y los sectores ligados "
            "a la IA. Los principales motores de crecimiento por destino fueron Africa (+32%), "
            "la Union Europea (+21%) y el Sudeste Asiatico (+20%). Las exportaciones a Estados Unidos "
            "cayeron un 16% por las tensiones arancelarias, pero China ha diversificado activamente "
            "sus mercados y el impacto global es limitado. El superavit comercial se mantiene "
            "en niveles record, consolidando a China como el primer exportador mundial."
        ),
        "fuente_label": "U.S.-China Economic Review Commission — China Bulletin May 5, 2026",
        "fuente_url": "https://www.uscc.gov/trade-bulletins/china-bulletin-may-5-2026",
    },
    {
        "emoji": "🤖",
        "titulo": "Forbes China AI TOP 50 2026: las empresas que lideran la revolución de la productividad",
        "cuerpo": (
            "Forbes China publico su Ranking AI TOP 50 de 2026, destacando a las empresas chinas que "
            "estan redefiniendo la productividad a traves de la inteligencia artificial. El listado abarca "
            "desde gigantes como Alibaba, Baidu y Huawei hasta startups de IA agentica, vision por "
            "computadora y modelos de lenguaje especializados. China ya cuenta con 602 millones de "
            "usuarios de IA generativa —mas de la mitad del total mundial— y las industrias de IA "
            "centrales superaron el billon de yuanes en valor en 2025. El 15 Plan Quinquenal se propone "
            "que el 90% de la economia productiva integre IA en sus procesos para 2030."
        ),
        "fuente_label": "Forbes China — 2026 AI TOP 50: Companies Powering a Productivity Revolution",
        "fuente_url": "https://www.barchart.com/story/news/2076578/forbes-china-unveils-the-2026-ai-top-50-these-companies-powering-a-productivity-revolution",
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
    title = "China Al Dia — Semana 26 Mayo - 2 Junio 2026"
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
