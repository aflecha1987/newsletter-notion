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
        "emoji": "🤖",
        "titulo": "Barclays: China necesitará 24 millones de robots humanoides para 2035",
        "cuerpo": (
            "Un informe de Barclays Research publicado el 19 de mayo sitúa a China como el epicentro de la "
            "revolución de la robótica humanoide. El banco proyecta que China podría desplegar hasta 24 millones "
            "de robots humanoides para 2035, compensando hasta el 60% de la brecha laboral causada por el "
            "envejecimiento de su población. En 2025, China ya acaparó el 85% de los despliegues mundiales de "
            "robots humanoides, liderado por empresas como AgiBot, Unitree y UBTech. La clave: el dominio chino "
            "de minerales críticos y su infraestructura energética hacen prácticamente insustituible su posición "
            "en la cadena de suministro global de robótica."
        ),
        "fuente_label": "Bloomberg — Barclays Says Robots May Offset 60% of China's Population Slump",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-05-19/barclays-says-robots-may-offset-60-of-china-s-population-slump",
    },
    {
        "emoji": "📱",
        "titulo": "Huawei HDC 2026: HarmonyOS 7 y el nuevo ecosistema de IA (12-14 junio)",
        "cuerpo": (
            "Huawei ha anunciado su Conferencia de Desarrolladores 2026 (HDC) para los días 12 al 14 de junio. "
            "El evento es el mayor escaparate del ecosistema tecnológico independiente de China y este año tendrá "
            "como estrella el lanzamiento oficial de HarmonyOS 7, con nuevas capacidades de IA integradas en el "
            "núcleo del sistema operativo. El HDC también presentará avances en las herramientas para "
            "desarrolladores, la estrategia de ecosistema y las alianzas internacionales del sistema operativo "
            "que compite directamente con Android e iOS. Se esperan más de 6.000 desarrolladores presenciales "
            "y decenas de miles de participantes virtuales."
        ),
        "fuente_label": "Pandaily — Huawei HDC 2026 Set for June 12–14: HarmonyOS 7 Officially Confirmed",
        "fuente_url": "https://pandaily.com/huawei-hdc-2026-harmonyos-7",
    },
    {
        "emoji": "🦾",
        "titulo": "La brecha se amplía: China lidera la robótica humanoide a nivel global",
        "cuerpo": (
            "Un análisis publicado en mayo documenta 'La brecha creciente': la distancia que separa a China del "
            "resto del mundo en robótica humanoide no para de aumentar. Mientras las startups chinas ya tienen "
            "contratos reales en fábricas, hospitales y centros comerciales, sus competidoras estadounidenses "
            "siguen en fases de prueba. China cuenta con más de 150 empresas activas en robótica y produce "
            "alrededor de 280.000 nuevas unidades al año, con planes de aumentar la producción un 94% a lo "
            "largo de 2026. Los inversores globales están apostando por que los robots humanoides "
            "transformarán la industria y el hogar en la próxima década."
        ),
        "fuente_label": "CNBC — Humanoid robots trillion dollar AI market",
        "fuente_url": "https://www.cnbc.com/amp/2026/06/03/humanoid-robots-trillion-dollar-ai-market.html",
    },
    {
        "emoji": "🧠",
        "titulo": "IA abierta como ventaja estratégica: el modelo chino que desafía a Silicon Valley",
        "cuerpo": (
            "Un análisis de la Comisión de Revisión Económica y Seguridad EE.UU.-China (USCC) describe cómo "
            "la estrategia de IA abierta de China —fomentar la publicación de modelos de código abierto como "
            "DeepSeek y Qwen— está reforzando su dominio industrial, no debilitándolo. China cuenta ya con más "
            "de 600 millones de usuarios de IA generativa, más de la mitad del total global. La estrategia "
            "permite que la IA china se integre en cadenas de suministro globales, acelera la retroalimentación "
            "de datos y consolida estándares tecnológicos propios, creando una ventaja competitiva estructural."
        ),
        "fuente_label": "South China Morning Post — China takes confident strides to develop more AI innovation in 2026",
        "fuente_url": "https://www.scmp.com/tech/tech-war/article/3338528/tech-war-china-takes-confident-strides-develop-more-ai-innovation-2026",
    },
    {
        "emoji": "💼",
        "titulo": "Summer Davos en Dalian: 'Innovando a escala' — 23-25 junio 2026",
        "cuerpo": (
            "El Foro Económico Mundial celebrará su 17.ª Reunión Anual de los Nuevos Campeones —el llamado "
            "'Davos de Verano'— en la ciudad de Dalian, China, del 23 al 25 de junio de 2026, bajo el lema "
            "'Innovando a escala'. Asistirán más de 1.500 líderes de negocios, gobiernos y ciencia de todo el "
            "mundo. Los ejes del debate serán: los nuevos flujos del comercio global, la próxima etapa de la "
            "economía china, la tecnología en la economía real, el empleo para la próxima generación y la "
            "transición energética como fuente de competitividad internacional."
        ),
        "fuente_label": "World Economic Forum — Summer Davos 2026: What to Expect in Dalian",
        "fuente_url": "https://www.weforum.org/stories/2026/05/summer-davos-2026-what-to-expect-in-dalian-china/",
    },
    {
        "emoji": "🌏",
        "titulo": "APEC 2026 en Shenzhen: China escenifica su liderazgo tecnológico global",
        "cuerpo": (
            "China se prepara para albergar la cumbre del Foro de Cooperación Económica Asia-Pacífico (APEC) "
            "el 18 y 19 de noviembre en Shenzhen. La ciudad, considerada el 'Silicon Valley chino' con 17 "
            "millones de habitantes, está desplegando soluciones urbanas de última generación: transporte "
            "autónomo, drones de pasajeros en fase final de prueba, robots humanoides en servicios públicos y "
            "redes 5G-Advanced de última generación. La agenda girará en torno a la gobernanza global de la "
            "IA, la resiliencia de las cadenas de suministro y la infraestructura digital para el mundo."
        ),
        "fuente_label": "Diario Financiero — China despliega su potencial tecnológico y comercial en APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "🛸",
        "titulo": "China invierte $8.400 millones en centros de datos en órbita espacial",
        "cuerpo": (
            "Una startup de Pekín, Orbital Chenguang, ha recibido el respaldo del gobierno chino con líneas de "
            "crédito de 57.700 millones de yuanes (≈ $8.400 millones) procedentes de los principales bancos "
            "estatales del país. El objetivo: construir una infraestructura de computación de más de 1 GW en "
            "órbita baja antes de 2035, aprovechando la energía solar continua y el enfriamiento natural del "
            "vacío. Es la mayor inversión conocida en computación orbital en el mundo, y coincide con la "
            "creación por parte del Ministerio de Industria y TI del Comité Profesional de Computación Espacial "
            "para coordinar estándares e incentivos del sector."
        ),
        "fuente_label": "SpaceNews — China backs orbital data center startup with $8.4 billion in credit lines",
        "fuente_url": "https://spacenews.com/china-backs-orbital-data-center-startup-with-8-4-billion-in-credit-lines/",
    },
    {
        "emoji": "🚀",
        "titulo": "El espacio como industria pilar: China lanza la estrategia Space+",
        "cuerpo": (
            "En su 15.º Plan Quinquenal (2026-2030), China designa oficialmente el sector espacial como "
            "'industria pilar emergente' y lanza la estrategia Space+, que unifica exploración, satélites, IA "
            "espacial, recolección de datos, monitoreo de debris, bases lunares y marcianas, minería espacial y "
            "producción de energía en el espacio en un solo marco coordinado. El plan también contempla un "
            "programa de defensa contra asteroides y proyectos de exploración en los bordes del Sistema Solar, "
            "consolidando a China como segunda potencia espacial mundial y principal rival de NASA."
        ),
        "fuente_label": "SpaceNews — China designates space sector an 'emerging pillar industry'",
        "fuente_url": "https://spacenews.com/china-designates-space-sector-an-emerging-pillar-industry-sets-deep-space-ambitions-in-new-economic-blueprint/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today} · Semana 28 mayo - 4 junio 2026", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, robotica e inteligencia artificial.", bold=False),
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
    title = "China Al Dia — Semana 28 Mayo - 4 Junio 2026"
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
