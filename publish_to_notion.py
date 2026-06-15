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
        "titulo": "Hito histórico: la capacidad solar china supera por primera vez al carbón",
        "cuerpo": (
            "En 2026, China alcanza un punto de inflexión energético sin precedentes: su capacidad instalada "
            "de energía solar supera a la del carbón por primera vez en la historia. Al cierre del año, "
            "las fuentes no fósiles —lideradas por solar y eólica— representarán el 63% de la capacidad "
            "total, mientras el carbón cae al 31%. China añadirá más de 300 GW de nueva energía renovable "
            "solo en 2026, suficiente para abastecer varios países europeos. La energía solar y eólica ya "
            "generan más del 25% de la electricidad del país, también por primera vez en un mes calendario. "
            "En 2025, las renovables ya cubrieron el 100% del crecimiento de la demanda eléctrica nacional."
        ),
        "fuente_label": "Bloomberg — China's Solar Capacity on Course to Surpass Coal",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-02-03/china-s-solar-power-capacity-on-course-to-surpass-coal-this-year",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate su propio récord: 160.000 unidades exportadas en mayo, +80% interanual",
        "cuerpo": (
            "BYD registró en mayo de 2026 un nuevo máximo histórico de exportaciones: 160.644 vehículos "
            "eléctricos enviados al exterior, un 80% más que en mayo de 2025. Las exportaciones ya "
            "representan el 42% de sus ventas totales. El mercado chino de vehículos eléctricos alcanzó "
            "1,36 millones de unidades en mayo, con los coches eléctricos ocupando el 62,9% de la cuota "
            "de mercado total. Las exportaciones totales de automóviles de China saltaron un 73% en mayo "
            "impulsadas por el precio del combustible. BYD mantiene su objetivo de 1,5 millones de "
            "exportaciones para 2026, un 40% más que en 2025."
        ),
        "fuente_label": "Global China EV — BYD leads China's record May NEV month",
        "fuente_url": "https://www.globalchinaev.com/post/byd-leads-chinas-record-may-nev-month-with-377000-units-and-surging-exports",
    },
    {
        "emoji": "🚀",
        "titulo": "China acelera en el espacio: Long March 12B vuela y Qianfan supera 200 satélites",
        "cuerpo": (
            "Junio arranca con una racha de lanzamientos históricos. El 1 de junio, el nuevo cohete "
            "reutilizable Long March 12B realizó su vuelo inaugural desde Jiuquan cargando satélites "
            "operativos de la constelación Qianfan —sin aviso previo—. Los días 4 y 5, los cohetes "
            "Long March 6A y 8 añadieron 36 nuevos satélites a Qianfan, superando los 200 satélites "
            "en esta constelación de internet de banda ancha. El 11 de junio, un Long March 5 puso en "
            "órbita un satélite de comunicaciones desde Wenchang. China acumula más de 25 lanzamientos "
            "espaciales en lo que va de 2026, un ritmo sin precedentes."
        ),
        "fuente_label": "Space News — Qianfan hits 200 satellites with Long March 8 and 6A launches",
        "fuente_url": "https://spacenews.com/qianfan-constellation-deployment-hits-200-satellites-with-long-march-8-and-6a-launches/",
    },
    {
        "emoji": "🤖",
        "titulo": "Robots humanoides: de los laboratorios a las calles — 35.000 unidades globales en 2026",
        "cuerpo": (
            "Según la Academia Damo de Alibaba, 2026 es el año de inflexión de los robots humanoides: "
            "pasan de la fase de verificación tecnológica a la comercialización a gran escala. Los envíos "
            "globales alcanzarán las 35.000 unidades este año, un salto del 94% interanual. En Shenzhen, "
            "Guangzhou y otras ciudades chinas es ya cotidiano ver robots en ascensores de hoteles, "
            "restaurantes y centros comerciales. La industria robótica china se afianza como la primera "
            "del mundo en presencia real de mercado, mientras sus competidoras estadounidenses siguen "
            "mayoritariamente en fase de desarrollo y captación de inversión."
        ),
        "fuente_label": "La Jornada — China apuesta a robots con IA para todo tipo de labores",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/05/10/economia/china-apuesta-a-robots-con-inteligencia-artificial-para-todo-tipo-de-labores",
    },
    {
        "emoji": "💻",
        "titulo": "China, segunda potencia mundial en computación IA: 1,59 millones de PFLOPS",
        "cuerpo": (
            "China se ha posicionado como la segunda nación del mundo en capacidad de computación "
            "inteligente, con 1,59 millones de PFLOPS y más de 10,85 millones de racks de IA operativos. "
            "El crecimiento está impulsado por gigantes tecnológicos como Alibaba, Tencent, Huawei y "
            "Baidu, que aceleran su inversión en centros de datos de IA de próxima generación. Este "
            "músculo computacional es el sustrato sobre el que se apoya la ambición de que la IA integre "
            "el 90% de la economía china para 2030, según el Plan Quinquenal vigente."
        ),
        "fuente_label": "El Ecosistema Startup — China 2026: 1,59M PFLOPS en computación IA",
        "fuente_url": "https://ecosistemastartup.com/china-2026-159m-pflops-y-1085m-racks-en-computacion-ia/",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones chinas en abril: $359.000 millones, récord impulsado por la IA",
        "cuerpo": (
            "China cerró abril de 2026 con exportaciones de 359.000 millones de dólares, un incremento "
            "del 14% interanual. El principal motor fue el auge de los productos vinculados a la "
            "inteligencia artificial: servidores, chips de memoria, equipos de telecomunicaciones y "
            "componentes para centros de datos. Las exportaciones de bienes de alta tecnología siguen "
            "siendo el motor principal del comercio exterior chino, consolidando al país como el mayor "
            "exportador del mundo por valor total y reforzando su papel central en las cadenas de "
            "suministro globales de tecnología."
        ),
        "fuente_label": "Ámbito — China: exportaciones abril $359.000M impulsadas por IA",
        "fuente_url": "https://www.ambito.com/tecnologia/china-cierra-abril-exportaciones-us359000-millones-impulsadas-el-auge-la-inteligencia-artificial-n6277559",
    },
    {
        "emoji": "🌐",
        "titulo": "APEC 2026 en Shenzhen: China propone un organismo mundial de gobernanza de IA",
        "cuerpo": (
            "A cinco meses de la cumbre APEC del 18-19 de noviembre en Shenzhen, China ya lidera la "
            "agenda global. Bajo el lema 'Construyendo una comunidad de Asia y el Pacífico para prosperar "
            "juntos', los tres ejes son: gobernanza de IA para el bien común, resiliencia de las cadenas "
            "de suministro y formalización de la economía digital. Xi Jinping ha propuesto crear una "
            "Organización Mundial de Cooperación en Inteligencia Artificial con sede en Shanghái, la "
            "primera vez que hace pública esta iniciativa de alcance global. Shenzhen, capital tecnológica "
            "de China, será la vitrina de su liderazgo industrial y digital ante los líderes del Pacífico."
        ),
        "fuente_label": "APEC — China Unveils APEC 2026 Theme and Priorities in Shenzhen",
        "fuente_url": "https://www.apec.org/press/news-releases/2025/china-unveils-apec-2026-theme-and-priorities-in-shenzhen",
    },
]


def build_blocks():
    today = date.today().strftime("%d de junio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: energia, vehiculos electricos, espacio, inteligencia artificial y diplomacia global.", bold=False),
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
    title = "China Al Dia — Semana 9-15 Junio 2026"
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
