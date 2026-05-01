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
        "emoji": "🚗",
        "titulo": "Auto China 2026: Pekín acoge el mayor escaparate automotriz del mundo con 222 debuts globales",
        "cuerpo": (
            "Del 24 de abril al 3 de mayo, Pekín acoge la edición 2026 del Salón Internacional del "
            "Automóvil, el mayor escaparate del sector en el mundo. Con más de 1.000 expositores de 21 "
            "países, 380.000 m² y 222 debuts mundiales, el evento confirma a China como capital global "
            "de la innovación automotriz. La IA fue la protagonista: Roland Berger lo resumió en una "
            "frase: 'La IA es la llave de la victoria en la carrera automovilística de 2026.' Entre los "
            "grandes lanzamientos: el XPeng GX (750 km de autonomía, hardware L4 listo, 58.000 dólares), "
            "el BYD Denza Z (hypercar descapotable +1.000 CV, destino a Europa) y el BYD Formula X, un "
            "concept deportivo que anticipa la próxima generación de coches eléctricos de altas prestaciones."
        ),
        "fuente_label": "Electrek — Beijing Auto Show 2026: a glimpse at the future",
        "fuente_url": "https://electrek.co/2026/04/26/beijing-auto-show-2026-insane-glimpse-future-auto-industry/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4: 1,6 billones de parámetros, 1 millón de tokens de contexto y precios que agitan al sector",
        "cuerpo": (
            "El 24 de abril, DeepSeek lanzó su modelo V4 en dos variantes bajo licencia MIT: V4 Flash "
            "(284.000 millones de parámetros) y V4 Pro (1,6 billones de parámetros, el mayor modelo "
            "open-weight del mundo). Con una ventana de contexto de 1 millón de tokens —8 veces mayor "
            "que su versión anterior— y un precio de 0,30 dólares por millón de tokens (7 veces más "
            "barato que GPT-5.5), DeepSeek vuelve a agitar el mercado global de la IA. Preentrenado en "
            "más de 32 billones de tokens, alcanza ~81% en SWE-bench para programación. La arquitectura "
            "Mixture of Experts (MoE) y el optimizador Muon marcan su eficiencia computacional. Una "
            "nueva demostración de que la innovación china en IA no necesita el hardware más avanzado."
        ),
        "fuente_label": "WwwhatsnNew — DeepSeek V4 Pro: el open-weight más grande del mundo",
        "fuente_url": "https://wwwhatsnew.com/2026/04/26/deepseek-v4-pro-flash-modelo-open-weight-precio-abril-2026/",
    },
    {
        "emoji": "🛡️",
        "titulo": "China bloquea la compra de Manus por Meta por 2.000 millones: la IA es seguridad nacional",
        "cuerpo": (
            "El 27 de abril, la Comisión Nacional de Desarrollo y Reforma de China ordenó a Meta y la "
            "startup de IA Manus deshacer su acuerdo de adquisición de 2.000 millones de dólares, citando "
            "seguridad nacional y riesgo de transferencia tecnológica. Manus, fundada en China y reubicada "
            "en Singapur, desarrolla agentes de IA de propósito general capaces de ejecutar tareas "
            "complejas de forma autónoma. La investigación se inició en enero; en marzo, sus fundadores "
            "fueron convocados a revisiones regulatorias. El episodio confirma que para Pekín la IA no "
            "es solo una industria: es un activo estratégico que no se negocia con potencias extranjeras."
        ),
        "fuente_label": "CNBC — China blocks Meta's $2 billion takeover of AI startup Manus",
        "fuente_url": "https://www.cnbc.com/2026/04/27/meta-manus-china-blocks-acquisition-ai-startup.html",
    },
    {
        "emoji": "🤖",
        "titulo": "El primer astronauta robot del mundo será chino: Engine AI prepara el PM01 para el espacio",
        "cuerpo": (
            "Engine AI anunció el despliegue de su robot humanoide PM01 en un programa de exploración "
            "espacial junto a Beijing Interstellar Human Spaceflight Technology. El PM01 mide 1,38 m, "
            "pesa 40 kg y está equipado con sensores de alta precisión, respuesta de movimiento "
            "ultrarrápida y toma de decisiones autónoma. La misión tiene como objetivo enviar un "
            "humanoide al espacio para realizar reparaciones, exploración y monitoreo en entornos de "
            "alto riesgo, reduciendo la exposición de los astronautas humanos. China aspira a convertirse "
            "en el primer país en desplegar un robot humanoide autónomo en órbita."
        ),
        "fuente_label": "Interesting Engineering — World's first robot astronaut: China",
        "fuente_url": "https://interestingengineering.com/ai-robotics/worlds-first-humanoid-robot-astronaut-china",
    },
    {
        "emoji": "📈",
        "titulo": "PMI manufacturero chino sube a 52,2 en abril: el mayor crecimiento desde diciembre de 2020",
        "cuerpo": (
            "El Índice de Gerentes de Compras (PMI) manufacturero de China escaló hasta 52,2 en abril "
            "de 2026, desde 50,8 en marzo, su nivel más alto desde diciembre de 2020 y muy por encima "
            "del umbral de expansión (50). La aceleración fue impulsada por nuevos pedidos —segunda tasa "
            "más alta en casi cinco años— y la fuerte demanda relacionada con la inteligencia artificial. "
            "Las perspectivas del sector manufacturero se mantienen brillantes según UOB, aunque el PMI "
            "no manufacturero retrocedió a 49,4, afectado por las disrupciones en cadenas de suministro "
            "y las tensiones en Oriente Medio."
        ),
        "fuente_label": "FXStreet ES — China: perspectivas de manufactura brillantes",
        "fuente_url": "https://www.fxstreet.es/news/china-perspectivas-de-manufactura-brillantes-demanda-se-suaviza-uob-202604302011",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar china supera al carbón por primera vez en capacidad instalada",
        "cuerpo": (
            "En 2026, la capacidad instalada de energía solar en China superará a la del carbón por "
            "primera vez en la historia, consolidando al país como líder indiscutible de la transición "
            "energética global. Solo este año, China añadirá más de 300 gigavatios de nueva capacidad "
            "eólica y solar. Para finales de 2026, las fuentes no fósiles representarán el 63% del mix "
            "energético nacional. El proyecto de corriente continua Tíbet-Gran Área de la Bahía, cuando "
            "esté operativo, transportará más de 43.000 millones de kWh de electricidad limpia al sur "
            "del país. China fabrica el 80% de los paneles solares del mundo y el 60% de las turbinas eólicas."
        ),
        "fuente_label": "Redimin — Energía solar en China superará al carbón en 2026",
        "fuente_url": "https://www.redimin.cl/energia-solar-en-china-superara-al-carbon-en-2026-el-dato-de-300-gw-que-reordena-su-sistema-electrico/",
    },
    {
        "emoji": "🚀",
        "titulo": "Récord histórico: China lanza 3 cohetes Larga Marcha en solo 19 horas y alcanza el lanzamiento 640",
        "cuerpo": (
            "Durante la última semana de abril, China completó varios lanzamientos orbitales de notable "
            "relevancia. El 25 de abril, el cohete Larga Marcha 6 colocó en órbita el satélite de "
            "observación terrestre PRSC-EO3 de Pakistán, misión número 640 de la serie Larga Marcha, "
            "reforzando la cooperación espacial con países del Sur Global. En un fin de semana de "
            "actividad sin precedentes, China ejecutó 3 lanzamientos en tan solo 19 horas, estableciendo "
            "un nuevo hito operacional. El acumulado de lanzamientos posiciona a China como la potencia "
            "con mayor cadencia de lanzamiento orbital del mundo en 2026."
        ),
        "fuente_label": "Space.com — China breaks record with 3 Long March launches in 19 hours",
        "fuente_url": "https://www.space.com/space-exploration/launches-spacecraft/china-breaks-record-with-3-long-march-rocket-launches-in-19-hour-stretch-video",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
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
    title = "China Al Dia — Semana 25 Abril - 1 Mayo 2026"
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
