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
        "emoji": "🚀",
        "titulo": "Tianwen-2 llega al asteroide cuasi-luna de la Tierra: hito histórico de la exploración espacial",
        "cuerpo": (
            "La sonda Tianwen-2 ha alcanzado el asteroide Kamoʻoalewa (469219), uno de los siete "
            "'cuasi-satélites' conocidos de la Tierra, un cuerpo de entre 40 y 100 metros que orbita "
            "el Sol sincronizado con nuestro planeta. Observadores de radio amateur en Alemania y los "
            "Países Bajos confirmaron el encuentro detectando las señales de telemetría. Durante las "
            "próximas cuatro semanas, la sonda cartografiará y estudiará la superficie antes de las "
            "maniobras de muestreo. Las muestras están previstas para regresar a la Tierra en 2027. "
            "En paralelo, la Shenzhou-23 fue lanzada el 24 de mayo con tres taikonautas —uno de ellos "
            "permanecerá un año completo en la estación espacial—, consolidando 2026 como el año más "
            "ambicioso de la historia espacial china."
        ),
        "fuente_label": "Scientific American — Tianwen-2 llega a la cuasi-luna de la Tierra",
        "fuente_url": "https://www.scientificamerican.com/article/chinas-tianwen-2-spacecraft-arrives-at-one-of-earths-mysterious-quasi-moons/",
    },
    {
        "emoji": "💾",
        "titulo": "Huawei anuncia LogicFolding: una arquitectura de chip que acortará distancias con TSMC",
        "cuerpo": (
            "El 25 de mayo, Huawei presentó su arquitectura LogicFolding, un diseño que acortará el "
            "cableado interno de los chips, reduciendo las distancias de comunicación entre transistores. "
            "Los chips Kirin de finales de 2026 serán los primeros en utilizarla, y su densidad de "
            "transistores equivaldrá a procesos de 1,4 nanómetros en un plazo de cinco años. SMIC, "
            "socio exclusivo de Huawei para los Ascend de IA, avanza en producción en nodo de 5 nm "
            "con un objetivo de 1,6 millones de chips de alta gama para aceleradores de IA en 2026. "
            "China está forjando una cadena de suministro de hardware de IA completamente doméstica."
        ),
        "fuente_label": "Fortune — Huawei touts chip breakthrough to shorten gap with TSMC",
        "fuente_url": "https://fortune.com/2026/05/25/huawei-touts-chip-breakthrough-to-shorten-gap-with-tsmc/",
    },
    {
        "emoji": "📡",
        "titulo": "China lanza la segunda fase de pruebas del 6G con el 40% de las patentes globales",
        "cuerpo": (
            "El 5 de junio, China confirmó el arranque de la segunda fase de pruebas técnicas del 6G "
            "con un programa piloto de colaboración ministerial-provincial. China ya controla el 40% "
            "de las patentes globales en 6G, y la nueva generación promete velocidades de 10 a 100 "
            "veces superiores al 5G, con cobertura terrestre, aérea, marítima y espacial integradas. "
            "En paralelo, la red 5G sigue su expansión imparable: más de 4,8 millones de estaciones "
            "base activas y más de 1.200 millones de usuarios conectados, con dos de cada tres "
            "usuarios móviles chinos ya en 5G."
        ),
        "fuente_label": "People's Daily — China lanza programa piloto 6G ministerial-provincial",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0605/c92121-20464118.shtml",
    },
    {
        "emoji": "🤖",
        "titulo": "Robots humanoides: China produce 62.500 unidades en 2026 y controla el 90% del mercado global",
        "cuerpo": (
            "El sector de robots humanoides en China alcanza su velocidad de crucero: se estima la "
            "producción de 62.500 unidades en 2026, más del triple de las 18.000 de 2025. En marzo "
            "abrió en Guangdong la primera fábrica capaz de producir 10.000 robots humanoides al año "
            "en una sola línea. Las empresas chinas controlan el 90% del mercado mundial de humanoides. "
            "El sector recaudó 68.100 millones de yuanes solo en el primer trimestre de 2026, más que "
            "en todo 2025. Los humanoides ya trabajan en cadenas de montaje de NIO, Zeekr y otros "
            "fabricantes de vehículos eléctricos."
        ),
        "fuente_label": "Global Times — China's humanoid robot industry accelerates commercialization",
        "fuente_url": "https://www.globaltimes.cn/page/202606/1362565.shtml",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de coches eléctricos chinos explotan: +73% en mayo, BYD bate su propio récord",
        "cuerpo": (
            "China exportó en mayo 809.000 vehículos de pasajeros (+73% interanual), de los que "
            "435.000 eran vehículos de nueva energía, más del doble que hace un año. BYD lideró "
            "con 160.644 unidades exportadas (+80,4% interanual), su nuevo récord histórico, "
            "aspirando a 1,5 millones de ventas internacionales en 2026, un 43% más que en 2025. "
            "El motor principal sigue siendo el shock del precio del petróleo derivado del conflicto "
            "en el Estrecho de Ormuz. Según la AIE, China ya domina la fabricación global de baterías "
            "y componentes eléctricos clave para toda la industria del automóvil."
        ),
        "fuente_label": "Global China EV — BYD leads China's record May NEV month",
        "fuente_url": "https://www.globalchinaev.com/post/byd-leads-chinas-record-may-nev-month-with-377000-units-and-surging-exports",
    },
    {
        "emoji": "⚡",
        "titulo": "Hito histórico: la energía solar supera al carbón en capacidad instalada en China",
        "cuerpo": (
            "En 2026, China alcanza un punto de inflexión histórico: por primera vez, la capacidad "
            "instalada de energía solar supera a la del carbón. La solar y la eólica alcanzarán el "
            "50% de la potencia instalada antes de que acabe el año. China añadirá más de 300 "
            "gigavatios de capacidad renovable en 2026, dentro de un total de 400 GW de nueva "
            "generación. A finales de año, las energías no fósiles representarán el 63% de la "
            "capacidad instalada total, mientras el peso del carbón caerá al 31%. En paralelo, el "
            "país construye una red de embalses de bombeo para almacenar el excedente renovable."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🌐",
        "titulo": "China lleva la fibra y el 5G a zonas rurales y remotas: conectividad como bien público",
        "cuerpo": (
            "Como parte del 15.º Plan Quinquenal, China ha lanzado un programa para llevar "
            "infraestructura 5G y banda ancha a zonas rurales, montañosas, fronterizas y forestales. "
            "La conectividad en estas regiones es clave para la igualdad educativa, el acceso "
            "universal a servicios médicos, la modernización agrícola y la revitalización rural. "
            "El programa forma parte de la estrategia de 'prosperidad común' que busca que ninguna "
            "comunidad quede excluida de la revolución digital, convirtiendo la infraestructura "
            "digital en un bien público tan fundamental como la electricidad o el agua potable."
        ),
        "fuente_label": "Prensa Latina — China por más infraestructura y conectividad digital en áreas rurales",
        "fuente_url": "https://www.prensa-latina.cu/2026/05/29/china-por-mas-infraestructura-y-conectividad-digital-en-areas-rurales/",
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
    title = "China Al Dia — Semana 5-12 Junio 2026"
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
