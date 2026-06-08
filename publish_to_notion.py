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
        "titulo": "China lanza el cohete Long March 12B: el más alto en completar su vuelo inaugural",
        "cuerpo": (
            "El 1 de junio, el cohete portador Larga Marcha 12B completó con éxito su vuelo inaugural "
            "desde la Zona de Innovación Aeroespacial Comercial de Dongfeng, poniendo en órbita un lote "
            "de satélites polares de la constelación Qianfan. Con 72 metros de altura y un diámetro de "
            "4,37 metros, es el cohete más alto en completar su primer vuelo en China. Tiene una capacidad "
            "de carga de 20 toneladas y puede desplegar 36 satélites en una sola misión. Tardó solo "
            "21 meses desde la concepción hasta el vuelo, una velocidad sin precedentes en el sector."
        ),
        "fuente_label": "Xinhua — China hits new milestone in space solar power project",
        "fuente_url": "https://english.news.cn/20260518/1a8b6d6c735b487aafc14c17bf686175/c.html",
    },
    {
        "emoji": "🧠",
        "titulo": "Kimi K2.5 de Moonshot AI rivaliza con GPT-5.2 y Claude 4.5",
        "cuerpo": (
            "Moonshot AI presentó Kimi K2.5, un modelo multimodal de código abierto con 1 billón de "
            "parámetros. Según la empresa, ofrece resultados comparables a GPT-5.2, Claude 4.5 Opus y "
            "Gemini 3 Pro en tareas de razonamiento, comprensión de imágenes y vídeos, programación y "
            "amplitud de contexto. En paralelo, Alibaba Cloud lanzó Qwen3-Max-Thinking. China ya cuenta "
            "con 602 millones de usuarios de IA generativa —más de la mitad de los usuarios globales— "
            "y lidera en número de patentes de IA, con un crecimiento del 31,2% interanual en Q1 2026."
        ),
        "fuente_label": "Infobae — Los nuevos modelos de IA de China reducen la brecha con EE.UU.",
        "fuente_url": "https://www.infobae.com/america/agencias/2026/01/27/los-nuevos-modelos-de-ia-de-china-reducen-la-brecha-con-estados-unidos/",
    },
    {
        "emoji": "🏆",
        "titulo": "China asciende al puesto 9 mundial en innovación, el avance más rápido en una década",
        "cuerpo": (
            "El Informe del Índice Nacional de Innovación 2025, presentado en el Foro Zhongguancun 2026 "
            "en Pekín, sitúa a China en el puesto 9 mundial, siendo el país con mayor progreso en los "
            "últimos diez años. Entre los hitos del año: los robots industriales crecieron un 28% "
            "interanual, los circuitos integrados un 10,9% y la manufactura de alta tecnología un 9,4%. "
            "En robótica, China registró la mayor densidad de robots por trabajador de cualquier país "
            "en desarrollo, consolidándose como la fábrica inteligente del mundo."
        ),
        "fuente_label": "Xinhua — Innovación tecnológica gana impulso en China durante primeros meses de 2026",
        "fuente_url": "https://spanish.news.cn/20260312/609871a2816b42efaf0f7d9ac3b5ff7a/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Robots humanoides: China domina el 90% del mercado global",
        "cuerpo": (
            "China controla cerca del 90% de los robots humanoides vendidos en el mundo y aumentará su "
            "producción en un 94% en 2026. Dos empresas lideran el mercado: Unitree (49,3% de cuota, "
            "con capacidad para 75.000 humanoides/año) y AgiBot (30,4%). Una nueva fábrica en Guangdong "
            "produce un robot humanoide cada 30 minutos, con estimaciones de 10.000 unidades anuales. "
            "Morgan Stanley prevé que las ventas de humanoides en China se dupliquen hasta las 28.000 "
            "unidades este año. El sector ha pasado de la fase demo a la adopción operativa real en "
            "manufactura, logística y retail."
        ),
        "fuente_label": "TechCrunch — Why China's humanoid robot industry is winning the early market",
        "fuente_url": "https://techcrunch.com/2026/02/28/why-chinas-humanoid-robot-industry-is-winning-the-early-market/",
    },
    {
        "emoji": "⚡",
        "titulo": "Instalada la mayor estación conversora offshore del mundo en Guangdong",
        "cuerpo": (
            "La estación conversora offshore 'Haifengzhixin' (Corazón de la Brisa Marina) completó su "
            "instalación en Yangjiang, Guangdong, tras un viaje de 1.090 millas náuticas. Es la mayor "
            "estación conversora offshore del mundo, parte de un proyecto de energía eólica marina de "
            "alta tensión en corriente continua. El proyecto refuerza la ambición de China de duplicar "
            "su energía no fósil para 2035, plan anunciado en abril por la Comisión Nacional de "
            "Desarrollo y Reforma, que contempla 1 billón de yuanes anuales de inversión en redes "
            "durante el 15.º Plan Quinquenal."
        ),
        "fuente_label": "Bloomberg — China Lifts Green Push With Plan to Double Clean Energy by 2035",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-17/china-lifts-green-push-with-plan-to-double-clean-energy-by-2035",
    },
    {
        "emoji": "☀️",
        "titulo": "China lanza dos alianzas de energía solar espacial en SNEC 2026 en Shanghái",
        "cuerpo": (
            "En la 19.ª Exposición Internacional de Energía Fotovoltaica SNEC 2026 celebrada en Shanghái, "
            "se presentaron dos nuevas alianzas industriales enfocadas en la energía solar desde el espacio: "
            "la Space Energy Development Alliance, que agrupa a empresas de solar, almacenamiento de "
            "energía, hidrógeno, infraestructura de carga y aeroespacial. La iniciativa apunta a desarrollar "
            "plantas solares orbitales capaces de recoger más energía en un año que todo el petróleo en "
            "la Tierra. China ya lanzó un prototipo en 2025 y planifica su primera estación comercial "
            "para la década de 2030."
        ),
        "fuente_label": "Saurenergy — China Launches Two Space Energy Alliances",
        "fuente_url": "https://www.saurenergy.com/solar-energy-news/china-launches-two-space-energy-alliances-to-advance-space-based-solar-technologies-11902998",
    },
    {
        "emoji": "🌊",
        "titulo": "El Canal Pinglu completa la conexión de agua: abrirá en septiembre de 2026",
        "cuerpo": (
            "El Canal Pinglu —eje del Corredor Logístico Occidental China-ASEAN— alcanzó la conexión "
            "plena de agua y entró en fase de puesta en marcha hidráulica. El canal de 134,2 km, ubicado "
            "en Guangxi, está previsto para abrir a la navegación en septiembre de 2026. Es una obra "
            "estratégica del Plan Quinquenal que reducirá el tiempo de tránsito de mercancías entre el "
            "interior de China y el Golfo de Tonkín de semanas a días, reforzando los lazos comerciales "
            "con el Sudeste Asiático."
        ),
        "fuente_label": "Pandaily — China Achieves Major Breakthroughs in Aerospace, Clean Energy, and Infrastructure",
        "fuente_url": "https://pandaily.com/china-aerospace-clean-energy-breakthroughs-jun2026",
    },
    {
        "emoji": "📡",
        "titulo": "5G-A cubre ya 330 ciudades chinas: China planifica el salto al 6G",
        "cuerpo": (
            "A cierre de marzo de 2026, China contaba con 4.958 millones de estaciones base 5G, con la "
            "tecnología 5G-Advanced (5G-A) cubriendo 330 ciudades. Los usuarios de IoT alcanzaron los "
            "2.948 millones —casi tres veces la población del país—. El sector de telecomunicaciones "
            "creció un 13,6% interanual en Q1 2026. China planifica el despliegue de 500.000 nuevas "
            "estaciones 5G-A antes de 2030, mientras avanza en la investigación del 6G como motor "
            "económico global post-2030."
        ),
        "fuente_label": "Xinhua — China boosts digital technology in push for modernization",
        "fuente_url": "http://www.shanghainews.net/news/279002526/china-boosts-digital-technology-in-push-for-modernization",
    },
    {
        "emoji": "📈",
        "titulo": "PIB crece un 5% en Q1 2026 y comercio exterior sube un 15%",
        "cuerpo": (
            "La economía china mantiene el rumbo: el PIB creció un 5% en el primer trimestre —superando "
            "las previsiones— y el comercio exterior aumentó un 15% interanual. Las exportaciones de "
            "bienes crecieron un 18,3% en enero-febrero, el primer crecimiento de doble dígito desde "
            "2023. La manufactura de alta tecnología subió un 12,5%, con robots industriales (+33%) y "
            "circuitos integrados (+24%) como motores principales. La Asamblea Popular Nacional fijó el "
            "objetivo de crecimiento en entre el 4,5% y el 5% para el conjunto del año."
        ),
        "fuente_label": "CGTN Español — Comercio exterior de China aumenta 15% en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-15/2044294393639481345/index.html",
    },
    {
        "emoji": "🏥",
        "titulo": "IA y Medicina Tradicional China: quioscos de diagnóstico inteligente en el metro",
        "cuerpo": (
            "China despliega quioscos de diagnóstico asistido por IA en estaciones de metro y espacios "
            "urbanos, combinando tecnología biomédica con la Medicina Tradicional China. Los dispositivos "
            "miden presión arterial, frecuencia cardíaca, saturación de oxígeno y temperatura, mientras "
            "la IA aplica criterios de la medicina tradicional: análisis facial, observación de la lengua "
            "e interpretación digital del pulso mediante sensores multicapa. La Comisión Nacional de Salud "
            "promueve la integración de IA en los servicios médicos como parte de la estrategia nacional "
            "de salud digital."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional China",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
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
    title = "China Al Dia — Semana 2-8 Junio 2026"
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
