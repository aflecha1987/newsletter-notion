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
        "titulo": "China lanza Shenzhou-23: un astronauta pasará un año en órbita y la primera astronauta de Hong Kong viaja al espacio",
        "cuerpo": (
            "El 24 de mayo, China lanzó con éxito la misión Shenzhou-23 desde Jiuquan, enviando tres "
            "astronautas a la estación Tiangong. Por primera vez, uno de ellos permanecerá un año completo "
            "en órbita —ensayo clave para futuras misiones lunares tripuladas antes de 2030—. Otro hito: "
            "Lai Ka-ying, doctora en informática forense criada en Hong Kong, se convierte en la primera "
            "astronauta de la ciudad en el programa espacial chino. La tripulación relevará a la del "
            "Shenzhou-21, que lleva más de 200 días en órbita."
        ),
        "fuente_label": "NPR — China launches Shenzhou-23 spacecraft",
        "fuente_url": "https://www.npr.org/2026/05/25/g-s1-124179/china-launches-shenzhou-23-spacecraft",
    },
    {
        "emoji": "💾",
        "titulo": "Huawei presenta LogicFolding: un avance revolucionario en chips que esquiva las sanciones de EE.UU.",
        "cuerpo": (
            "El 25 de mayo, en un simposio de semiconductores en Shanghái, Huawei presentó su nueva "
            "arquitectura LogicFolding y la Ley Tau de Escalado: una innovación que reduce el tiempo "
            "que tardan las señales en recorrer los chips, mejorando densidad y rendimiento sin necesitar "
            "los equipos de litografía más avanzados que China tiene vedados. Sus chips Kirin, que "
            "incorporarán LogicFolding en el segundo semestre de 2026, alcanzarán densidad equivalente "
            "a procesos de 1,4 nm para 2031. Las acciones de SMIC subieron un 7,6% tras el anuncio."
        ),
        "fuente_label": "Fortune — Huawei touts chip breakthrough to shorten gap with TSMC",
        "fuente_url": "https://fortune.com/2026/05/25/huawei-touts-chip-breakthrough-to-shorten-gap-with-tsmc/",
    },
    {
        "emoji": "🤖",
        "titulo": "DeepSeek baja un 75% el precio de su IA más potente: 17 veces más barata que GPT-5.5",
        "cuerpo": (
            "El 25 de mayo, DeepSeek anunció un descuento permanente del 75% sobre el modelo V4-Pro, "
            "su IA insignia lanzada en abril. El coste de uso queda en $1,74 por millón de tokens de "
            "entrada, frente a los $30 de GPT-5.5, con rendimiento igual o superior en benchmarks "
            "independientes de razonamiento y codificación. El modelo es de código abierto, soporta "
            "más de un millón de tokens de contexto y redefine la competencia global en IA: no solo "
            "el mejor rendimiento, sino accesible a escala mundial."
        ),
        "fuente_label": "La Nación — DeepSeek aplica descuento permanente del 75% al V4-Pro",
        "fuente_url": "https://www.lanacion.com.ar/tecnologia/la-china-deepseek-aplicara-un-descuento-permanente-del-75-al-precio-del-modelo-de-ia-v4-pro-nid25052026/",
    },
    {
        "emoji": "🦾",
        "titulo": "Robots humanoides chinos cosechan té y se entrenan para el mercado laboral",
        "cuerpo": (
            "A mediados de mayo, 24 equipos de robots humanoides fueron desplegados en las laderas de "
            "Fuding (Fujian) para la primera etapa del relevo de los Juegos Mundiales de Robots "
            "Humanoides 2026, cosechando té en terreno de montaña irregular. En paralelo, la primera "
            "fábrica china de producción masiva de humanoides —alianza entre Leju Robotics y Dongfang "
            "Precision en Guangdong— lleva dos meses fabricando 10.000 robots al año con 77 "
            "controles de calidad por unidad. Un exjefe de robótica de la NASA declaró en Fortune: "
            "'América construye el tipo equivocado de robots, y China lo sabe.'"
        ),
        "fuente_label": "Interesting Engineering — China tests humanoid robots in tea farms",
        "fuente_url": "https://interestingengineering.com/ai-robotics/china-tests-humanoid-robots-in-tea-farms-before-the-2026-world-robot-games",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones de China en abril: +14,1% interanual, superávit récord de $84.800 millones",
        "cuerpo": (
            "Los datos de comercio exterior de abril de 2026 batieron expectativas: las exportaciones "
            "chinas crecieron un 14,1% interanual, recuperándose con fuerza respecto al +2,5% de "
            "marzo. El superávit comercial se amplió hasta $84.800 millones, su nivel más alto del año. "
            "Las exportaciones hacia EE.UU. repuntaron un 11,3%, revirtiendo la caída del 26,5% de "
            "marzo. Los fabricantes chinos aceleraron envíos ante la demanda global de componentes "
            "impulsada por el encarecimiento del petróleo. Las exportaciones de automóviles de "
            "pasajeros crecieron un 60,6% interanual en el primer trimestre."
        ),
        "fuente_label": "CNBC — China April exports rebound strongly after sluggish March",
        "fuente_url": "https://www.cnbc.com/amp/2026/05/09/china-april-exports-rebound-strongly-after-sluggish-march.html",
    },
    {
        "emoji": "⚡",
        "titulo": "China activa la turbina eólica marina más grande del mundo: 20 MW para 96.000 hogares",
        "cuerpo": (
            "En mayo, Mingyang Smart Energy activó en las aguas cercanas a Hainan la turbina eólica "
            "marina más grande del mundo: 20 megavatios de potencia, capaz de abastecer a 96.000 "
            "hogares al año. China ya tiene más de 448 gigavatios de capacidad eólica y solar en "
            "construcción —la mitad del total mundial— y su potencia renovable operativa supera "
            "1,6 teravatios. En paralelo, el país construye embalses de bombeo hidroeléctrico a "
            "velocidad sin precedentes para almacenar el excedente renovable."
        ),
        "fuente_label": "Canal26 — China activa la turbina eólica marina más grande del mundo",
        "fuente_url": "https://www.canal26.com/internacionales/2026/05/16/energia-renovable-a-gran-escala-china-activa-la-turbina-eolica-marina-mas-grande-del-mundo-capaz-de-abastecer-a-96000-hogares/",
    },
    {
        "emoji": "🚄",
        "titulo": "China supera los 50.000 km de alta velocidad e invierte $20.900 millones en ferrocarriles en Q1",
        "cuerpo": (
            "China ha cruzado el umbral de los 50.000 kilómetros de red ferroviaria de alta velocidad, "
            "consolidando la mayor red del mundo por un margen enorme. Solo en el primer trimestre de "
            "2026, los ferrocarriles chinos completaron una inversión en activos fijos de $20.900 "
            "millones. Entre los proyectos más ambiciosos destaca el futuro tren submarino del "
            "Estrecho de Bohai, que unirá Dalian y Yantai a 250 km/h, con inversión estimada de "
            "220.000-300.000 millones de yuanes. También avanza la línea Shenzhen-Jiangmen (116 km, "
            "50.000 millones de yuanes), que reducirá el trayecto a menos de 60 minutos."
        ),
        "fuente_label": "Excélsior — China supera los 50 mil km de trenes de alta velocidad",
        "fuente_url": "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD desbanca a Tesla y se convierte en el mayor vendedor de coches eléctricos del mundo",
        "cuerpo": (
            "En 2025, BYD vendió 2,26 millones de vehículos 100% eléctricos, superando a Tesla por "
            "primera vez en la historia. Con sus híbridos enchufables, las entregas totales de BYD "
            "alcanzaron 4,54 millones de unidades. China representó el 75% de la producción global "
            "de EVs en 2025 y exportó un récord de más de 2,5 millones de coches eléctricos al "
            "extranjero. Los precios competitivos de BYD, Geely y Chery están reconfigurando el "
            "mercado global de la automoción."
        ),
        "fuente_label": "CNBC — China's BYD overtakes Tesla as world's top EV seller for the first time",
        "fuente_url": "https://www.cnbc.com/2026/01/02/chinas-byd-to-overtake-tesla-as-worlds-top-ev-seller-for-first-time.html",
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
    title = "China Al Dia — Semana 19-26 Mayo 2026"
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
