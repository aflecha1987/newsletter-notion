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
        "titulo": "La energía solar supera al carbón por primera vez en la historia de China",
        "cuerpo": (
            "Al cierre de julio de 2026, la capacidad fotovoltaica instalada alcanzó 1.286 millones de kW, "
            "superando por primera vez a la del carbón con 1.285 millones de kW. Un hito histórico que "
            "marca el fin de la era del carbón como tecnología dominante en China. En paralelo, en el "
            "primer semestre de 2026 las renovables generaron el 41,2 % de toda la electricidad del país, "
            "el porcentaje más alto jamás registrado, y China añadió 117 GW de nueva capacidad renovable "
            "—equivalente al 73,9 % de toda la nueva capacidad eléctrica instalada en esos seis meses."
        ),
        "fuente_label": "Infobae — La energía solar supera por primera vez al carbón en China (1 sep 2026)",
        "fuente_url": "https://www.infobae.com/america/agencias/2026/09/01/la-energia-solar-supera-por-primera-vez-al-carbon-en-capacidad-instalada-en-china/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek desarrolla su propio chip de IA para romper la dependencia de Nvidia",
        "cuerpo": (
            "La startup china DeepSeek, valorada en más de 50.000 millones de dólares tras su última ronda "
            "de financiación, ha comenzado a desarrollar su propio chip de IA para tareas de inferencia. "
            "Con este movimiento busca reducir su dependencia de Nvidia y Huawei. La empresa lanzó su "
            "modelo V4 en abril de 2026, entrenado parcialmente en chips Ascend de Huawei. Mientras tanto, "
            "Baidu y Alibaba también aceleran el desarrollo de sus propios procesadores, consolidando un "
            "ecosistema de IA chino cada vez más autónomo frente a las restricciones tecnológicas de EE.UU."
        ),
        "fuente_label": "Ambito — DeepSeek busca desarrollar su chip IA",
        "fuente_url": "https://www.ambito.com/tecnologia/deepseek-busca-desarrollar-su-chip-ia-reducir-su-dependencia-nvidia-y-huawei-n6296989",
    },
    {
        "emoji": "🤖",
        "titulo": "Robot 'Centauro' con el 95% de componentes nacionales redefine la robótica mundial",
        "cuerpo": (
            "Shanghai-based Run Robotics presentó el primer robot híbrido rueda-pierna del mundo en la "
            "Conferencia Mundial de IA 2026, construido con más del 95 % de componentes de fabricación "
            "china. La empresa ya tiene pedidos comerciales y planea iniciar producción en línea de "
            "ensamblaje en el cuarto trimestre de 2026. China cuenta con ~2 millones de robots industriales "
            "operativos —4,5 veces más que Japón— y el 54 % de los robots industriales instalados en el "
            "mundo en 2025 fueron desplegados en China. El XV Plan Quinquenal coloca la robótica con IA "
            "en el corazón de la estrategia industrial nacional."
        ),
        "fuente_label": "The Silicon Review — China Robot 'Centaur' Innovation Reshapes AI Future",
        "fuente_url": "https://thesiliconreview.com/2026/07/china-ai-robot-future-revolution",
    },
    {
        "emoji": "📦",
        "titulo": "Récord histórico: 3,75 billones de dólares en comercio exterior en el primer semestre",
        "cuerpo": (
            "China registró 25,47 billones de yuanes (~3,75 billones de USD) en comercio exterior en el "
            "primer semestre de 2026, un nuevo máximo histórico. Los sectores estrella: automóviles "
            "(+65,3 %, con 5,096 millones de unidades exportadas), hardware computacional (+56,6 %), "
            "baterías de litio (+37,6 %) y aerogeneradores (+35,6 %). Los astilleros chinos captaron "
            "1.131 de los 1.481 buques encargados globalmente, aproximadamente el 72 % del mercado "
            "mundial de construcción naval."
        ),
        "fuente_label": "TLC Magazine México — China rompe récord de comercio exterior en el primer semestre",
        "fuente_url": "https://tlcmagazinemexico.com.mx/index.php/2026/07/16/china-rompe-record-de-comercio-exterior-en-el-primer-semestre-de-2026/",
    },
    {
        "emoji": "🚄",
        "titulo": "China supera los 50.000 km de alta velocidad ferroviaria — la mayor red del mundo",
        "cuerpo": (
            "Con la inauguración de nuevas líneas —Xi'an-Shiyan (257 km a 350 km/h) en junio y "
            "Shenzhen-Jiangmen (116+ km, menos de 1 hora entre ciudades)—, China consolida la red de "
            "alta velocidad ferroviaria más grande del planeta. En paralelo, se desarrolla un nuevo tren "
            "con velocidad operativa de 400 km/h (pruebas a 450 km/h), que se convertiría en el tren "
            "comercial más rápido del mundo. La inversión en activos fijos ferroviarios en el primer "
            "trimestre de 2026 alcanzó 20.090 millones de dólares."
        ),
        "fuente_label": "Excélsior — China supera los 50 mil kilómetros de trenes de alta velocidad",
        "fuente_url": "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico",
    },
    {
        "emoji": "🚀",
        "titulo": "Un astronauta chino completa un año en el espacio; China apunta a la Luna en 2030",
        "cuerpo": (
            "Un astronauta de la misión Shenzhou completa un año completo en órbita a bordo de la "
            "estación espacial Tiangong, marcando un nuevo hito en resistencia espacial china. China "
            "planea enviar astronautas a la Luna antes de 2030 y construir la Estación Internacional "
            "de Investigación Lunar para 2035. Además, el C919 —avión de pasajeros de fabricación "
            "nacional con más de 42.000 vuelos comerciales— opera ya vuelos internacionales diarios "
            "entre Pekín y Ulán Bator desde el 12 de agosto de 2026."
        ),
        "fuente_label": "La Jornada — China envía un astronauta al espacio por un año (25 may 2026)",
        "fuente_url": "https://www.jornada.com.mx/2026/05/25/ciencias/a06n1cie",
    },
    {
        "emoji": "⚡",
        "titulo": "China desperdicia 360 TWh renovables — y ya construye embalses gigantes para almacenarlos",
        "cuerpo": (
            "El mayor desafío de China en energía ya no es generar electricidad renovable: es almacenarla. "
            "Durante el primer semestre de 2026, China habría desaprovechado ~360 TWh de generación eólica "
            "y solar porque la red no puede absorber toda la energía producida. La respuesta: construir "
            "embalses hidráulicos de bombeo a escala masiva para almacenar el excedente. China instala "
            "más eólica en un año que Estados Unidos en toda su historia, acelerando la búsqueda de "
            "soberanía energética."
        ),
        "fuente_label": "Somos Eléctricos — China tiene tanta energía solar y eólica que empieza a desperdiciarla",
        "fuente_url": "https://www.somoselectricos.com/curiosidades/china-tiene-tanta-energia-solar-eolica-que-empieza-desperdiciarla-360-twh-solo-seis-meses/20260820093543062406.html",
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
    title = "China Al Dia — Semana 26 Ago - 2 Sep 2026"
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
    print(f"Semana: 26 Ago - 2 Sep 2026")
    print(f"Noticias incluidas: {len(NOTICIAS)}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "").replace("-", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id}")
    print(f"\nListo!")
    print(f"URL: {page_url}")
    return page_url


if __name__ == "__main__":
    create_notion_page()
