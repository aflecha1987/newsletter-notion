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
        "emoji": "🏗️",
        "titulo": "China prepara la mayor inversión en infraestructura de IA de la historia: $295.000 millones",
        "cuerpo": (
            "El 9 de junio, Bloomberg reveló que China está preparando un plan de 2 billones de yuanes "
            "(~295.000 millones de dólares) a cinco años para construir una red nacional de centros de "
            "datos de IA interconectados. El plan, liderado por la Comisión Nacional de Desarrollo y "
            "Reforma, confía la operación a China Mobile y China Telecom, y establece que al menos el "
            "80% de la tecnología —incluidos los chips de IA— provenga de proveedores locales como "
            "Huawei, reduciendo la dependencia de Nvidia. Para 2028, el objetivo es tener todos los "
            "centros de datos integrados en un único sistema coherente a nivel nacional."
        ),
        "fuente_label": "Bloomberg — China Plans $295 Billion Investment in Nationwide AI Data Centers",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout",
    },
    {
        "emoji": "🤖",
        "titulo": "China: líder mundial indiscutible en robots humanoides, Wall Street quiere invertir",
        "cuerpo": (
            "Según CNBC, los robots humanoides se han convertido en la próxima gran oportunidad de "
            "inversión en IA, con China como 'el líder más claro en este momento', mientras EE.UU. "
            "'juega a ponerse al día'. China instala cerca de la mitad de todos los robots industriales "
            "del mundo —unas 300.000 unidades frente a 34.000 en EE.UU.—. Startups chinas como Galaxy "
            "Bot, UnitTree y otras ya han firmado contratos reales con fábricas, hospitales y centros "
            "comerciales. El mercado de robots humanoides podría superar el billón de dólares en los "
            "próximos años, con China posicionada para capturar la mayor parte de ese valor."
        ),
        "fuente_label": "CNBC — Humanoid robots touted as next AI investment opportunity",
        "fuente_url": "https://www.cnbc.com/2026/06/03/humanoid-robots-trillion-dollar-ai-market.html",
    },
    {
        "emoji": "🏆",
        "titulo": "El Foro Económico Mundial premia a empresas chinas de IA en su lista de Pioneros Tecnológicos 2026",
        "cuerpo": (
            "El WEF publicó su edición 2026 de los 100 Pioneros Tecnológicos globales, con IA y "
            "robótica dominando la selección de 23 países. La empresa china Xense Robotics fue "
            "destacada por sus innovadores sensores de tacto multimodal que permiten a los robots "
            "manipular objetos con la misma destreza que una mano humana, abriendo el paso a la "
            "'IA encarnada'. Aproximadamente la mitad de las 100 empresas elegidas se enfocan en "
            "IA, robótica e infraestructura para la siguiente generación de sistemas inteligentes."
        ),
        "fuente_label": "The AI Insider — AI and Robotics Dominate WEF's 2026 Technology Pioneers List",
        "fuente_url": "https://theaiinsider.tech/2026/06/10/ai-robotics-dominate-world-economic-forums-2026-technology-pioneers-list/",
    },
    {
        "emoji": "💰",
        "titulo": "Startups chinas de IA recaudaron $16.500 millones en el primer trimestre de 2026",
        "cuerpo": (
            "Las startups chinas captaron aproximadamente 16.500 millones de dólares en el primer "
            "trimestre de 2026, con empresas de IA como StepFun, Moonshot AI y Galaxy Bot liderando "
            "las rondas de inversión. Los sectores más dinámicos fueron aplicaciones de IA, robótica, "
            "semiconductores, tecnología industrial, hardware inteligente y software comercial. La "
            "cifra refleja la creciente confianza del capital internacional en el ecosistema "
            "tecnológico chino, pese a las tensiones geopolíticas con EE.UU."
        ),
        "fuente_label": "Mean.ceo — Startups in China News, June 2026",
        "fuente_url": "https://blog.mean.ceo/startups-china-news-june-2026/",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de autos chinos +73% en mayo: BYD supera los 160.000 vehículos en un mes",
        "cuerpo": (
            "Las exportaciones de automóviles de China se dispararon un 73% interanual en mayo de "
            "2026, alcanzando aproximadamente 809.000 vehículos en un solo mes. Los vehículos "
            "eléctricos e híbridos enchufables casi se duplicaron hasta 435.000 unidades. BYD, "
            "el mayor exportador, superó las 160.000 unidades —un 80% más que mayo de 2025— y "
            "elevó su objetivo anual para 2026 a 1,3 millones de unidades exportadas. China está "
            "en camino de exportar más de 10 millones de vehículos en 2026, consolidándose como "
            "primer exportador de automóviles del mundo."
        ),
        "fuente_label": "Cadena 3 — Exportaciones de autos chinos aumentan 73% en mayo",
        "fuente_url": "https://www.cadena3.com/noticia/mundo/las-exportaciones-de-autos-chinos-aumentan-73-en-mayo-impulsadas-por-electricos_561085",
    },
    {
        "emoji": "🌐",
        "titulo": "China preside APEC 2026 en Shenzhen: IA, drones y libre comercio en la agenda global",
        "cuerpo": (
            "China asumió la presidencia de APEC 2026, con la cumbre principal prevista para "
            "noviembre en Shenzhen. La ciudad presentará drones de pasajeros en fase final de "
            "prueba, robots humanoides integrados en servicios públicos y transporte automatizado. "
            "La agenda prioriza la gobernanza de la IA centrada en el bien común, la resiliencia "
            "de cadenas de suministro globales y la infraestructura digital. El comercio entre "
            "China y las economías APEC supone el 57% del comercio exterior chino, lo que "
            "convierte esta cumbre en un escaparate estratégico de primer orden."
        ),
        "fuente_label": "Diario Financiero — China despliega su potencial en preparativos de APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "☀️",
        "titulo": "China fabrica más energía solar de la que el planeta entero necesita instalar",
        "cuerpo": (
            "Un análisis reciente revela que la capacidad de fabricación de paneles solares de "
            "China supera ya la demanda global de instalación solar en su conjunto. Lejos de ser "
            "un problema, esto abre la puerta a abaratar los costes de instalación en todo el mundo "
            "y acelerar la transición energética global. La capacidad instalada de energía eólica "
            "y solar de China creció un 22% en 2025, y solar y eólica lideraron la generación "
            "limpia en el país por primera vez en la historia. La IA se integra progresivamente "
            "para optimizar la distribución de energía renovable."
        ),
        "fuente_label": "Algoritmomag — China ya puede fabricar más energía solar de la que el planeta necesita",
        "fuente_url": "https://algoritmomag.com/china-energia-solar/",
    },
    {
        "emoji": "⚛️",
        "titulo": "El Plan Quinquenal apuesta por la computación cuántica e IA como motores del futuro",
        "cuerpo": (
            "El 15.º Plan Quinquenal chino (2026-2030) sitúa la computación cuántica e inteligencia "
            "artificial como tecnologías centrales para el crecimiento económico. Las metas incluyen "
            "la expansión de computadoras cuánticas escalables, el desarrollo de una red de "
            "comunicación cuántica espacio-tierra integrada y grandes infraestructuras de cómputo "
            "para sistemas de IA avanzados. El presupuesto en Ciencia y Tecnología creció un 7,1% "
            "hasta 1,3 billones de yuanes, con las industrias emergentes apuntando a superar los "
            "10 billones de yuanes para 2030."
        ),
        "fuente_label": "The Quantum Insider — China's Five-Year Plan Targets Quantum Leadership and AI",
        "fuente_url": "https://thequantuminsider.com/2026/03/05/chinas-new-five-year-plan-specifically-targets-quantum-leadership-and-ai-expansion/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, energia y estrategia global.", bold=False),
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
    title = "China Al Dia — Semana 4-11 Junio 2026"
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
