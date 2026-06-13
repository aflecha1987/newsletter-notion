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
        "titulo": "China lanza el mayor plan de IA de la historia: 295.000 millones de dólares en centros de datos",
        "cuerpo": (
            "El 9 de junio, Bloomberg reveló que China está preparando un plan de 2 billones de yuanes "
            "(295.000 millones de dólares) para construir una red nacional de centros de datos de IA. "
            "El plan, liderado por la Comisión Nacional de Desarrollo y Reforma, exige que el 80% de "
            "la tecnología —incluyendo chips— provenga de fabricantes chinos como Huawei, desplazando "
            "a NVIDIA. China Mobile y China Telecom operarán los hubs. El objetivo: completar la red "
            "de cómputo nacional hacia 2028 y liderar la IA mundial en la próxima década."
        ),
        "fuente_label": "Bloomberg — China Plans $295 Billion Investment in Nationwide AI Data Centers",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior chino crece 15,3% en los primeros cinco meses de 2026",
        "cuerpo": (
            "Datos oficiales publicados el 9 de junio confirman que el comercio exterior de China "
            "alcanzó los 20,68 billones de yuanes (~2,86 billones de dólares) entre enero y mayo de "
            "2026, un 15,3% más que el mismo período del año anterior. Las importaciones subieron un "
            "20,5%, señal de una reactivación de la demanda interna. El motor principal fueron las "
            "exportaciones de tecnología de IA. China se consolida como la primera economía exportadora "
            "del mundo, batiendo expectativas trimestre a trimestre."
        ),
        "fuente_label": "Últimas Noticias — Comercio exterior chino crece más de lo esperado",
        "fuente_url": "https://ultimasnoticias.com.ve/opinion/comercio-exterior-chino-crece-mas-de-lo-esperado-en-los-primeros-cinco-meses-de-2026/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD dispara exportaciones un 80,7% en mayo: apunta a superar objetivos en APEC 2026",
        "cuerpo": (
            "En mayo de 2026, BYD incrementó sus exportaciones de vehículos de nueva energía un 80,7% "
            "interanual. La empresa confía en superar su objetivo anual en un 15% adicional. En paralelo, "
            "China acelera los preparativos para la cumbre del APEC 2026, prevista para el 18-19 de "
            "noviembre en Shenzhen, donde los vehículos eléctricos, la IA y las cadenas de suministro "
            "serán los ejes del debate económico regional. BYD ya es el mayor fabricante mundial de "
            "coches eléctricos."
        ),
        "fuente_label": "Bloomberg Línea — BYD confía en superar exportaciones 2026",
        "fuente_url": "https://www.bloomberglinea.com/negocios/byd-confia-en-que-las-exportaciones-de-2026-superaran-en-un-15-su-anterior-objetivo/",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23: el primer taikonauta de Hong Kong y una misión de un año en el espacio",
        "cuerpo": (
            "El 24 de mayo, China lanzó la misión Shenzhou-23 con tres astronautas: el comandante Zhu "
            "Yangzhu, Zhang Zhiyuan y Lai Ka-ying, la primera astronauta de Hong Kong en viajar al "
            "espacio. La misión histórica tiene como objetivo que uno de los taikonautas permanezca "
            "en órbita durante un año completo, estudiando los límites de adaptación humana en el "
            "espacio para preparar las futuras expediciones lunares antes de 2030. La tripulación "
            "ya está operativa en la estación Tiangong."
        ),
        "fuente_label": "NPR — China launches Shenzhou 23 spacecraft",
        "fuente_url": "https://www.npr.org/2026/05/25/g-s1-124179/china-launches-shenzhou-23-spacecraft",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito mundial: China transmite energía solar inalámbrica a múltiples objetivos en movimiento",
        "cuerpo": (
            "Investigadores de la Universidad de Xidian lograron un avance sin precedentes en el "
            "proyecto 'Zhuri' (Perseguidor del Sol): por primera vez en el mundo se transmitió energía "
            "inalámbrica simultáneamente a múltiples objetivos en movimiento. El sistema alcanzó una "
            "eficiencia del 20,8% a 100 metros y suministró 143 vatios a un dron en vuelo a 30 km/h "
            "desde 30 metros. El plan: lanzar paneles de 10 kW al espacio en 2026, un prototipo de "
            "500 kW en 2030, y una estación de 2 GW en 2050."
        ),
        "fuente_label": "Xinhua — China hits new milestone in space solar power project",
        "fuente_url": "https://english.news.cn/20260518/1a8b6d6c735b487aafc14c17bf686175/c.html",
    },
    {
        "emoji": "⚡",
        "titulo": "State Grid encarga 8.500 robots IA para operar la red eléctrica más grande del mundo",
        "cuerpo": (
            "State Grid Corporation of China ha encargado 8.500 robots con IA por 6.800 millones de "
            "yuanes (~1.000 millones de dólares) para 2026. El despliegue incluye 5.000 robots "
            "cuadrúpedos para inspeccionar líneas de alta tensión, 3.000 robots de doble brazo para "
            "operar en subestaciones y robots humanoides para trabajos de ultra-alta tensión donde "
            "el riesgo humano es máximo. Si el resto de eléctricas chinas replican el modelo, el gasto "
            "sectorial podría superar los 10.000 millones de yuanes solo en 2026."
        ),
        "fuente_label": "Interesting Engineering — China plans 8,500 AI robots for power grid",
        "fuente_url": "https://interestingengineering.com/ai-robotics/china-8500-robots-power-grid",
    },
    {
        "emoji": "💻",
        "titulo": "China, segunda potencia mundial en cómputo IA: 1,59 millones de PFLOPS operativos",
        "cuerpo": (
            "China opera ya 1,59 millones de PFLOPS de potencia de cómputo inteligente (FP16) en "
            "10,85 millones de racks de centros de datos, posicionándose como la segunda potencia "
            "mundial en infraestructura de IA. La Administración Nacional de Datos publicó en abril "
            "un plan para construir antes de 2028 un ecosistema de datos validados que garantice el "
            "suministro de datos de entrenamiento. Con más de 600 millones de usuarios de IA generativa, "
            "China ya es el mayor mercado de IA del planeta."
        ),
        "fuente_label": "Ecosistema Startup — China 2026: 1,59M PFLOPS y 10,85M racks en computación IA",
        "fuente_url": "https://ecosistemastartup.com/china-2026-159m-pflops-y-1085m-racks-en-computacion-ia/",
    },
]


def build_blocks():
    today = "13 de junio de 2026"
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
    title = "China Al Dia — Semana 7-13 Junio 2026"
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
