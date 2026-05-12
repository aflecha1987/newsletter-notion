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
        "emoji": "🤝",
        "titulo": "EE.UU. y China firman tregua arancelaria histórica: del 145% al 30% en un día",
        "cuerpo": (
            "El 12 de mayo de 2026, tras tres días de intensas negociaciones en Ginebra, Estados Unidos "
            "y China alcanzaron un acuerdo de reducción arancelaria de 90 días que ha sacudido los mercados "
            "globales. Washington redujo sus aranceles sobre productos chinos del 145% al 30%, mientras "
            "que Pekín bajó los suyos del 125% al 10%. Adicionalmente, China acordó suspender las "
            "restricciones a la exportación de tierras raras, elementos críticos para la fabricación de "
            "semiconductores, vehículos eléctricos y tecnología de defensa. Ambos lados establecieron un "
            "mecanismo permanente de consulta encabezado por el viceprimer ministro He Lifeng y el "
            "secretario del Tesoro estadounidense Scott Bessent. Las bolsas mundiales celebraron el "
            "acuerdo con fuertes alzas. El 'Consenso de Ginebra' marca un punto de inflexión en la "
            "guerra comercial más larga de la historia reciente."
        ),
        "fuente_label": "Xataka — EE.UU. y China firman tregua de 90 días",
        "fuente_url": "https://www.xataka.com/empresas-y-economia/estados-unidos-china-firman-tregua-90-dias-reducen-aranceles-115-alivio-para-economia-mundial",
    },
    {
        "emoji": "🤖",
        "titulo": "DeepSeek V4 funciona con chips chinos: el fin de la dependencia de Nvidia",
        "cuerpo": (
            "El 24 de abril, la startup china DeepSeek presentó su modelo V4, el primero en ser construido "
            "nativamente para los chips Ascend de Huawei en lugar de hardware de Nvidia. El rendimiento de "
            "V4 Pro supera al de GPT-5.5 en múltiples benchmarks a una décima parte del coste. La noticia "
            "provocó que Alibaba, ByteDance y Tencent cursaran pedidos de cientos de miles de procesadores "
            "Ascend 950PR a Huawei, un hito para la industria semiconductor china. La valoración de "
            "DeepSeek escaló de 10.000 millones a 50.000 millones de dólares en cuestión de semanas. "
            "Los analistas señalan que el lanzamiento de V4 ha acelerado el ecosistema de chips chinos "
            "más que cualquier política gubernamental."
        ),
        "fuente_label": "Fortune — DeepSeek V4 AI model price performance China",
        "fuente_url": "https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/",
    },
    {
        "emoji": "🚀",
        "titulo": "2026: el 'momento SpaceX' del espacio comercial chino",
        "cuerpo": (
            "Analistas y medios especializados han bautizado 2026 como el 'Momento SpaceX' de China. "
            "Casi diez empresas privadas de cohetes —LandSpace, CAS Space, Tianbing Technology— aceleran "
            "su camino a la bolsa, con la normativa ya habilitando OPVs para empresas que demuestren "
            "avances en recuperación de motores de cohetes líquidos. En paralelo, la Agencia Espacial "
            "Nacional China (CNSA) confirmó una agenda intensiva: la misión Shenzhou-23 (tripulada), "
            "el primer acercamiento de Tianwen-2 a su asteroide objetivo, y los ensayos de vuelo del "
            "cohete reutilizable Larga Marcha 10, pieza clave para el aterrizaje lunar tripulado "
            "previsto antes de 2030. El 15.º Plan Quinquenal designa el espacio como 'industria pilar "
            "emergente', integrando la órbita como infraestructura habilitadora de toda la economía."
        ),
        "fuente_label": "Baiguan News — China SpaceX Moment 2026 commercial space",
        "fuente_url": "https://www.baiguan.news/p/china-spacex-moment-2026-commercial-space-ipo-satellite-constellation-starlink-competition-reusable-rockets-galaxyspace-landspace",
    },
    {
        "emoji": "🚂",
        "titulo": "BYD lleva sus trenes autónomos a Sudamérica: la otra gran apuesta de China",
        "cuerpo": (
            "Más allá de los coches eléctricos, BYD inaugura en 2026 su primera línea de trenes autónomos "
            "en São Paulo (Brasil), consolidando su presencia en infraestructuras de transporte inteligente. "
            "La compañía está presente en más de 120 países y sigue apostando por las exportaciones como "
            "motor de crecimiento, con fábricas activas en Hungría, Brasil y Tailandia. BYD mantiene su "
            "hoja de ruta: liderar el transporte electrificado a escala mundial, desde turismos hasta "
            "autobuses, camiones y trenes, convirtiendo a China en el gran exportador de movilidad limpia "
            "del siglo XXI."
        ),
        "fuente_label": "La Jornada — Trenes autónomos, la otra apuesta de BYD",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/05/07/economia/trenes-autonomos-la-otra-apuesta-de-la-firma-china-byd",
    },
    {
        "emoji": "☀️",
        "titulo": "China instala más solar que carbón: un hito histórico en la transición energética",
        "cuerpo": (
            "Por primera vez en la historia, la capacidad instalada de energía solar en China supera a "
            "la del carbón en 2026. El Consejo de Electricidad de China prevé añadir más de 400 GW de "
            "nueva capacidad a lo largo del año, de los cuales más de 300 GW corresponden a fuentes "
            "renovables (solar y eólica). China ya suma más de 1,5 teravatios de proyectos solares y "
            "eólicos en distintas etapas —casi el doble que el resto del mundo junto—. El plan de doblar "
            "la energía limpia para 2035 sigue adelante con las dos grandes eléctricas estatales "
            "invirtiendo 1 billón de yuanes anuales en la red eléctrica."
        ),
        "fuente_label": "Global Energy Monitor — China leads world in wind and solar",
        "fuente_url": "https://globalenergymonitor.org/es/report/china-continues-to-lead-the-world-in-wind-and-solar-with-twice-as-much-capacity-under-construction-as-the-rest-of-the-world-combined/",
    },
    {
        "emoji": "🏗️",
        "titulo": "El túnel más largo del mundo: China une Dalian y Yantai bajo el mar de Bohai",
        "cuerpo": (
            "China avanza con el proyecto del túnel submarino Bohai, la megaestructura ferroviaria más "
            "ambiciosa de la historia: 123 kilómetros bajo el estrecho de Bohai que unirán las ciudades "
            "de Dalian y Yantai en tan solo 40 minutos en tren de alta velocidad, frente a las más de "
            "8 horas actuales por carretera. La inversión supera los 220.000 millones de yuanes "
            "(aproximadamente 36.000 millones de dólares). Se estima que 7 millones de personas "
            "utilizarán el túnel anualmente. El periodo 2026-2030 es la ventana objetivo para el inicio "
            "de las obras, consolidando la apuesta de China por la infraestructura de alta velocidad "
            "como columna vertebral del desarrollo económico regional."
        ),
        "fuente_label": "Xataka — La nueva megaestructura china: túnel submarino más largo del mundo",
        "fuente_url": "https://www.xataka.com/ingenieria-y-megaconstrucciones/nueva-megaestructura-china-coloso-submarino-tunel-ferroviario-largo-mundo",
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
    title = "China Al Dia — Semana 6-12 Mayo 2026"
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
