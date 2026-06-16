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
        "emoji": "📦",
        "titulo": "Exportaciones de China +19,4% en mayo: el auge de la IA bate todas las previsiones",
        "cuerpo": (
            "El 9 de junio, la Administración General de Aduanas de China publicó los datos de mayo: "
            "las exportaciones crecieron un 19,4% interanual hasta 376.780 millones de dólares, "
            "superando ampliamente la previsión del 15% de los analistas. Las importaciones subieron "
            "un 27,4% y el superávit comercial se disparó a 105.400 millones de dólares, el mayor en "
            "meses. En el acumulado enero-mayo, el comercio total alcanzó los 20,68 billones de yuanes "
            "(~2,86 billones de dólares), un +15,3% interanual. Las exportaciones a EE. UU. crecieron "
            "un 35,4% anual, con los productos de tecnología e inteligencia artificial como principales "
            "motores del crecimiento."
        ),
        "fuente_label": "La Jornada — China anuncia exportaciones +19,4% en mayo",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/06/09/economia/-china-anuncia-que-sus-exportaciones-escalaron-194-en-mayo-por-encima-de-lo-esperado",
    },
    {
        "emoji": "🪪",
        "titulo": "China crea el primer 'DNI' del mundo para robots humanoides: 28.000 ya registrados",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de la Información implementó un sistema de "
            "identificación digital obligatorio para todos los robots humanoides fabricados en China. "
            "Cada unidad recibe un código único de 29 caracteres —más largo que el documento de identidad "
            "humano— que lo acompañará de la fabricación al reciclaje. La medida ya abarca a más de "
            "100 fabricantes y más de 28.000 robots de unos 200 modelos han sido registrados. Es el "
            "primer sistema de este tipo a escala nacional en el mundo, diseñado para garantizar la "
            "trazabilidad y la supervisión de una industria que crece a ritmo vertiginoso."
        ),
        "fuente_label": "Infobae — Más de 28.000 robots humanoides ya tienen DNI en China",
        "fuente_url": "https://www.infobae.com/tecno/2026/06/04/mas-de-28000-robots-humanoides-ya-tienen-dni-asi-funciona-este-inedito-sistema-de-identificacion/",
    },
    {
        "emoji": "🏫",
        "titulo": "Shanghái inaugura la primera 'escuela para robots humanoides' del mundo",
        "cuerpo": (
            "El National and Local Co-Built Humanoid Robotics Innovation Center de Shanghái abrirá "
            "en julio el primer centro de entrenamiento heterogéneo de robots humanoides del mundo: "
            "más de 5.000 m² en el distrito de Zhangjiang donde más de 100 tipos de robots de más de "
            "una docena de empresas entrenarán simultáneamente, generando hasta 50.000 datos de "
            "entrenamiento diarios. En la provincia de Fujian ya opera una escuela experimental donde "
            "decenas de humanoides practican tareas físicas bajo supervisión humana, preparando el "
            "terreno para el despliegue industrial masivo."
        ),
        "fuente_label": "Wwwhatsnew — Centro entrenamiento robots humanoides Shanghái 2026",
        "fuente_url": "https://wwwhatsnew.com/2026/05/27/centro-entrenamiento-robots-humanoides-shanghai-china-2026/",
    },
    {
        "emoji": "🚦",
        "titulo": "Robots humanoides dirigen el tráfico en Hangzhou junto a agentes humanos",
        "cuerpo": (
            "La ciudad de Hangzhou desplegó una brigada de 15 robots con inteligencia artificial que "
            "trabajan junto a agentes de tránsito en zonas turísticas de alto flujo e intersecciones "
            "estratégicas, incluyendo las inmediaciones del famoso Lago del Oeste. Los robots detectan "
            "infracciones, guían a peatones y coordinan el tráfico vehicular en tiempo real, convirtiendo "
            "Hangzhou en una de las primeras ciudades del mundo con robótica humanoide integrada en la "
            "gestión del espacio urbano cotidiano."
        ),
        "fuente_label": "Noticias de la Calle — China pone robots humanoides a controlar el tránsito",
        "fuente_url": "https://www.noticiasdelacalle.com.ar/noticias/2026/05/19/170337-china-puso-en-funcionamiento-robots-humanoides-para-controlar-el-transito-urbano",
    },
    {
        "emoji": "🌐",
        "titulo": "China lidera la APEC 2026: Shenzhen, vitrina tecnológica global en noviembre",
        "cuerpo": (
            "China preside la cumbre APEC el 18 y 19 de noviembre en Shenzhen, el Silicon Valley chino. "
            "Para garantizar los consensos previos, las autoridades programaron casi 300 reuniones "
            "ministeriales y técnicas a lo largo del año. El lema elegido es 'Construyendo una Comunidad "
            "Asia-Pacífico para Prosperar Juntos', con tres ejes: apertura, innovación y cooperación. "
            "La inteligencia artificial, la economía digital y la resiliencia de las cadenas de suministro "
            "centrarán la agenda. China busca convertir la cumbre en una plataforma de su liderazgo "
            "industrial y tecnológico ante las principales economías del mundo."
        ),
        "fuente_label": "Diario Financiero — China despliega potencial tecnológico en preparativos APEC",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "⚡",
        "titulo": "China se convierte en el primer 'electroestado' del mundo: solar supera al carbón",
        "cuerpo": (
            "Junio de 2026 marca un hito histórico: por primera vez, la capacidad solar instalada en "
            "China supera a la generada con carbón. En febrero de 2026, la energía limpia ya representaba "
            "el 52% de la capacidad eléctrica total. China instaló 446 GW de nueva capacidad renovable "
            "solo en 2025 —más que el resto del mundo en conjunto—, elevando su parque total a más de "
            "2,34 TW. Controla el 80% de los paneles solares del planeta, el 60% de las turbinas "
            "eólicas y el 70% de las baterías para vehículos eléctricos. Analistas acuñan el término "
            "'electroestado' para describir este modelo que está redefiniendo la geopolítica global."
        ),
        "fuente_label": "La Casa de Mitia — China, la era del electroestado",
        "fuente_url": "https://www.lacasademitia.es/articulo/economia/china-era-electroestado-estrategia-china-transicion-energetica-global-alessandro-scassellati/20260612093846191721.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "El XV Plan Quinquenal: tecnología y autosuficiencia como ejes del poder global",
        "cuerpo": (
            "A mitad de 2026, el XV Plan Quinquenal (2026-2030) gana velocidad de crucero. Su objetivo "
            "central: dejar de competir por costes y hacerlo por control tecnológico. La IA como "
            "infraestructura transversal, el 6G, la robótica, la biotecnología y los drones son los "
            "pilares del modelo. El gobierno fijó que el 70% de la economía incorpore IA para 2027 y "
            "el 90% para 2030. El presupuesto en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones "
            "de yuanes. Las industrias emergentes apuntan a superar los 10 billones de yuanes en valor "
            "para 2030, convirtiendo la tecnología en el motor del desarrollo de las próximas dos décadas."
        ),
        "fuente_label": "The Conversation — 2026-2030: cinco años para consolidar el poder global de China",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
    },
]


def build_blocks():
    today = date.today().strftime("%d de junio de %Y")
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
    title = "China Al Dia — Semana 9-16 Junio 2026"
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
