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
        "titulo": "WAIC 2026: Shanghai acoge la mayor Conferencia Mundial de IA de la historia",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghai fue el epicentro global de la inteligencia artificial con la "
            "Conferencia Mundial de IA 2026 (WAIC). Por primera vez, la superficie expositiva superó los "
            "100.000 metros cuadrados, reuniendo a más de 1.100 empresas y exhibiendo 3.000 productos, "
            "de los cuales más de 300 se presentaron por primera vez en el mundo. El presidente Xi Jinping "
            "anunció la creación de un centro internacional de cooperación en IA junto a la CELAC, "
            "reforzando el papel de China como puente tecnológico hacia el Sur Global."
        ),
        "fuente_label": "CGTN Español — Últimas innovaciones en la WAIC 2026",
        "fuente_url": "https://espanol.cgtn.com/2026/07/19/ARTI1784426596140231",
    },
    {
        "emoji": "🚀",
        "titulo": "Long March 10B: China recupera su primer cohete orbital del mar",
        "cuerpo": (
            "El 10 de julio, el cohete Larga Marcha 10B realizó su vuelo inaugural y logró recuperar su "
            "primera etapa mediante un aterrizaje controlado en el mar, convirtiéndose en el segundo país "
            "del mundo —tras SpaceX— en recuperar un propulsor de clase orbital. El avance es un hito "
            "en el programa chino de cohetes reutilizables, pieza clave para reducir costes de acceso "
            "al espacio y acelerar el programa lunar tripulado antes de 2030."
        ),
        "fuente_label": "La Jornada — China desafía a la NASA",
        "fuente_url": "https://www.jornada.com.mx/2026/08/03/politica/005n1pol",
    },
    {
        "emoji": "🌙",
        "titulo": "Chang'e-7 y el programa espacial 2026: China acelera hacia la Luna",
        "cuerpo": (
            "China presenta un calendario de misiones sin precedentes: la misión Chang'e-7 al polo sur "
            "lunar prevista para agosto (con rover y sonda saltadora para buscar hielo), la misión "
            "Tianwen-2 hacia un asteroide, y operación continua de la estación Tiangong. El objetivo "
            "es llevar astronautas chinos a la superficie lunar antes de 2030."
        ),
        "fuente_label": "La Jornada — China acelera para llevar astronautas a la Luna",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/08/03/politica/china-acelera-para-llevar-astronautas-a-la-luna",
    },
    {
        "emoji": "🧠",
        "titulo": "Kimi K3 y la autosuficiencia en chips de IA: China al 40% en solo 5 años",
        "cuerpo": (
            "El 16 de julio, Moonshot AI lanzó Kimi K3, su nuevo modelo de razonamiento avanzado. El "
            "lanzamiento se produce en un contexto en el que la autosuficiencia de China en chips de IA "
            "ha pasado de prácticamente cero en 2021 a aproximadamente el 40% en 2026, mostrando la "
            "aceleración del ecosistema tecnológico chino en uno de los sectores más estratégicos del siglo."
        ),
        "fuente_label": "The Objective — La estrategia IA de China",
        "fuente_url": "https://theobjective.com/internacional/2026-07-28/estrategia-ia-china-logica-implicaciones/",
    },
    {
        "emoji": "🌐",
        "titulo": "WAICO: el primer organismo intergubernamental de IA del mundo, con China al frente",
        "cuerpo": (
            "Durante la WAIC 2026 se presentó WAICO (World AI Cooperation Organization), el primer "
            "organismo intergubernamental dedicado exclusivamente a la gobernanza de la inteligencia "
            "artificial. Impulsado con el respaldo de China, busca que los países en desarrollo tengan "
            "voz en cómo se regulan y distribuyen los beneficios de la IA a escala global."
        ),
        "fuente_label": "Diario Red — China desafía el control tecnológico de EE.UU.",
        "fuente_url": "https://www.diario-red.com/articulo/internacional/china-desafia-control-tecnologico-ee-uu-modelo-global-abierto-inteligencia-artificial/20260719040429073168.html",
    },
    {
        "emoji": "🤝",
        "titulo": "México y China estrechan lazos en IA, robótica y semiconductores",
        "cuerpo": (
            "El 23 de julio, la Secretaría de Ciencia, Humanidades, Tecnología e Innovación de México "
            "formalizó una alianza con China en inteligencia artificial, robótica y electromovilidad. "
            "La cooperación incluye proyectos conjuntos en semiconductores y señala una tendencia "
            "creciente: los países latinoamericanos buscan a China como socio preferente en el desarrollo tecnológico."
        ),
        "fuente_label": "La Jornada — México y China impulsan alianza en IA y robótica",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/07/23/ciencias/mexico-y-china-impulsan-alianza-en-inteligencia-artificial-robotica-y-electromovilidad",
    },
    {
        "emoji": "📦",
        "titulo": "Exportaciones chinas +20,8% en junio: primer mes con más de 1 millón de coches exportados",
        "cuerpo": (
            "Las exportaciones de China se dispararon un 20,8% interanual en junio de 2026, impulsadas "
            "por la demanda récord de semiconductores (+122% interanual) y vehículos eléctricos. Este fue "
            "el primer mes en que China exportó más de 1 millón de vehículos (1,037 millones). En el "
            "primer semestre, las exportaciones de turismos alcanzaron 4,4 millones de unidades, un 72% "
            "más que el año anterior."
        ),
        "fuente_label": "Infobae — Exportaciones chinas crecen 20,8% gracias a chips y eléctricos",
        "fuente_url": "https://www.infobae.com/america/agencias/2026/07/14/las-exportaciones-chinas-crecen-un-208-interanual-en-junio-gracias-a-chips-o-electricos/",
    },
    {
        "emoji": "📊",
        "titulo": "Politburó julio 2026: hoja de ruta económica para el segundo semestre",
        "cuerpo": (
            "La reunión del Politburó de julio estableció las prioridades para el segundo semestre de "
            "2026: consolidar el crecimiento impulsado por tecnología, mantener el apoyo al consumo "
            "interno, y acelerar la transición digital en los sectores productivos. La economía china "
            "sigue su hoja de ruta de crecimiento estable y de calidad."
        ),
        "fuente_label": "CGTN — China's July 2026 Politburo meeting and world economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-31/What-China-s-July-2026-Politburo-meeting-means-for-world-economy-1PdJ7rNrPBC/p.html",
    },
    {
        "emoji": "⚓",
        "titulo": "China controla el 72% de los pedidos navales mundiales",
        "cuerpo": (
            "Los astilleros chinos captaron 1.131 de los 1.481 buques encargados en todo el mundo, "
            "representando el 72% del mercado global de construcción naval. El país continúa siendo "
            "el líder indiscutible de este sector, con una capacidad productiva y competitividad en "
            "costes sin parangón en el mundo."
        ),
        "fuente_label": "China.org.cn — El ecosistema industrial impulsa el crecimiento",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-07/30/content_118626156.htm",
    },
    {
        "emoji": "🌿",
        "titulo": "Hito histórico: renovables superan el 40% de la electricidad en China",
        "cuerpo": (
            "Por primera vez, las energías renovables suministraron más del 40% de la electricidad de "
            "China durante el primer semestre de 2026 (~2 billones de kWh, +9% interanual). A partir del "
            "1 de agosto de 2026 entran en vigor nuevas normativas con metas obligatorias de consumo "
            "renovable para industrias clave, acelerando la transición energética del país."
        ),
        "fuente_label": "Energías Renovables — China supera el 40% de generación renovable",
        "fuente_url": "https://www.energias-renovables.com/panorama/china-supera-por-primera-vez-el-40-20260803",
    },
    {
        "emoji": "☀️",
        "titulo": "Solar térmica de concentración: 24 plantas en operación, 26 en construcción",
        "cuerpo": (
            "China opera ya 24 plantas de energía solar térmica de concentración y tiene otras 26 en "
            "construcción, sumando 3,2 gigavatios de capacidad. El nivel de componentes fabricados "
            "localmente supera el 95% y los costes de construcción se han reducido a 15.000 yuanes por "
            "kilovatio, un ejemplo de cómo China ha logrado dominar e industrializar tecnología verde de vanguardia."
        ),
        "fuente_label": "China.org.cn — China logra nuevo avance en energía verde",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-07/31/content_118627767.htm",
    },
    {
        "emoji": "💰",
        "titulo": "Franja y la Ruta: récord de $20.100 millones en inversión verde en el primer semestre",
        "cuerpo": (
            "En el primer semestre de 2026, la iniciativa de la Franja y la Ruta alcanzó un récord "
            "histórico de 20.100 millones de dólares en financiación para proyectos de energía verde, "
            "superando el total registrado en todo 2025. China se consolida como el mayor inversor en "
            "infraestructura sostenible del mundo en desarrollo."
        ),
        "fuente_label": "Xinhua — Innovación tecnológica gana impulso en China en 2026",
        "fuente_url": "https://spanish.news.cn/20260312/609871a2816b42efaf0f7d9ac3b5ff7a/c.html",
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
    title = f"China Al Dia — Semana 28 Jul - 4 Ago 2026"
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
