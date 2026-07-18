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
        "titulo": "Xi Jinping debuta en el WAIC y lanza la primera alianza global de IA con 29 países",
        "cuerpo": (
            "El presidente chino compareció por primera vez ante la Conferencia Mundial de Inteligencia "
            "Artificial (WAIC 2026) celebrada en Shanghái del 17 al 20 de julio, señal inequívoca de que "
            "China eleva su apuesta por liderar la gobernanza global de la IA. Xi declaró: 'El desarrollo "
            "de la IA no debe ser el solo de un único país, sino la sinfonía de la cooperación internacional.' "
            "El día anterior, 29 países firmaron la creación de la Organización Mundial de Cooperación en "
            "IA (WAICO), con sede en Shanghái, cuyos miembros fundadores incluyen Indonesia, Brasil, "
            "Malasia, Sudáfrica, Rusia y Pakistán. China anunció 5.000 plazas de formación en IA para "
            "países en desarrollo y la extensión de un sistema de alerta meteorológica con IA a 30 países. "
            "El evento reunió a 1.400 participantes y 1.100 empresas expositoras —Microsoft, Google, "
            "Huawei, Alibaba— con 3.000 productos presentados, más de 300 de ellos debutando mundialmente."
        ),
        "fuente_label": "CGTN — Discurso de Xi Jinping en el WAIC 2026",
        "fuente_url": "https://news.cgtn.com/news/2026-07-17/Full-text-Xi-s-keynote-speech-at-the-2026-WAIC-opening-ceremony-1OQSfeoRvUs/p.html",
    },
    {
        "emoji": "🧠",
        "titulo": "Kimi K3: el mayor modelo de código abierto del mundo sacude los mercados globales",
        "cuerpo": (
            "La startup china Moonshot AI presentó Kimi K3, un modelo de lenguaje con 2,8 billones de "
            "parámetros —un 75% más grande que el modelo más avanzado de DeepSeek y el mayor modelo de "
            "pesos abiertos publicado hasta la fecha—. Sus pesos se publicarán antes del 27 de julio, "
            "siguiendo la misma estrategia que convirtió a DeepSeek en fenómeno global. En pruebas "
            "independientes, Kimi K3 lidera el ranking de programación de interfaces web de la plataforma "
            "Arena, superando a los modelos de OpenAI y Anthropic. Los mercados vivieron un nuevo 'momento "
            "DeepSeek', con caídas en el sector de semiconductores y nuevas dudas sobre si las "
            "multimillonarias inversiones occidentales en IA generarán la rentabilidad esperada."
        ),
        "fuente_label": "Xataka — Kimi K3 lidera ranking de programación",
        "fuente_url": "https://www.xataka.com/robotica-e-ia/nuevo-modelo-chino-kimi-k3-numero-uno-frontend-code-arena-esta-desatando-locura-internet",
    },
    {
        "emoji": "🏭",
        "titulo": "La IA transforma la industria china: de las minas a los hospitales",
        "cuerpo": (
            "La inteligencia artificial se ha convertido en el motor fiable de la transformación industrial "
            "china, reconfigurando sectores completos: fábricas que operan de noche sin personal, minas con "
            "monitoreo de seguridad en tiempo real, aulas con herramientas de IA y hospitales con diagnóstico "
            "asistido. Solo iFlytek reporta que sus tableros interactivos con IA se utilizan en más de "
            "50.000 escuelas y benefician a 130 millones de profesores y alumnos. En los primeros cinco "
            "meses del año, las ventas de dispositivos inteligentes portátiles se duplicaron interanualmente, "
            "y la inversión en IA y robótica humanoide creció un 118,4% interanual en el primer semestre."
        ),
        "fuente_label": "Cubadebate — China acelera su transformación industrial con la IA",
        "fuente_url": "http://www.cubadebate.cu/noticias/2026/07/17/china-acelera-su-transformacion-industrial-con-la-ia-como-motor-del-crecimiento/",
    },
    {
        "emoji": "🦾",
        "titulo": "Robots humanoides chinos salen al mundo para aprender a ser humanos",
        "cuerpo": (
            "China envió robots humanoides a entornos reales —calles, parques, centros comerciales— para "
            "que aprendan comportamientos humanos a partir de la observación. En paralelo, en julio entró "
            "en pleno funcionamiento la primera 'escuela para robots humanoides' de China, en Shanghái, "
            "con la participación de Boston Dynamics, Agility Robotics, Unitree y Pudu Robotics: 100 modelos "
            "distintos generan 50.000 datos diarios en una plataforma de intercambio entre fabricantes. "
            "La inversión en robótica humanoide creció un 118,4% interanual en el primer semestre de 2026."
        ),
        "fuente_label": "The Japan Times — China robots learning to be human",
        "fuente_url": "https://www.japantimes.co.jp/business/2026/07/16/china-robots-how-to-be-human/",
    },
    {
        "emoji": "💙",
        "titulo": "Robots compañeros con IA emocional: reconocen 20 emociones con 90% de precisión",
        "cuerpo": (
            "Una empresa china presentó una nueva línea de robots humanoides de compañía capaces de "
            "reconocer más de 20 matices emocionales con una precisión superior al 90%, gracias al primer "
            "gran modelo de IA emocional del mundo. Diseñados para el apoyo afectivo y la asistencia "
            "doméstica, los robots ya acumulan más de 10.000 pedidos anticipados, con una producción "
            "prevista de 50.000 unidades en 2026. El desarrollo se enmarca en la estrategia china de "
            "convertir la robótica social en un sector exportable de alto valor añadido."
        ),
        "fuente_label": "TV BRICS — Robots humanoides con IA emocional",
        "fuente_url": "https://tvbrics.com/es/news/china-presenta-robots-humanoides-de-compa-a-para-ofrecer-apoyo-emocional-y-asistencia-en-el-hogar/",
    },
    {
        "emoji": "📦",
        "titulo": "Comercio exterior de China crece un 16,9% en el primer semestre de 2026",
        "cuerpo": (
            "El valor total de las importaciones y exportaciones de China alcanzó los 25,47 billones de "
            "yuanes en el primer semestre del año, un aumento del 16,9% interanual. Las exportaciones "
            "ascendieron a 14,73 billones de yuanes (+13,4%), impulsadas principalmente por los productos "
            "tecnológicos, que se dispararon un 27% interanual solo en junio. Las sólidas exportaciones, "
            "catalizadas por el auge de la IA, compensaron la debilidad relativa de la demanda interna, "
            "que continúa siendo el 'eslabón débil' de la economía china en este período."
        ),
        "fuente_label": "People's Daily — Comercio exterior crece 16,9% en H1 2026",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0715/c31620-20477940.html",
    },
    {
        "emoji": "🌐",
        "titulo": "China potencia la digitalización del BRICS con la red 5G más grande del mundo",
        "cuerpo": (
            "China ofrece a los países del BRICS su experiencia en infraestructura digital, plataformas "
            "de comercio electrónico y coordinación de la innovación. Con más de 5 millones de estaciones "
            "base 5G —la red más extensa del planeta—, China está lista para exportar su modelo de "
            "transformación digital. Las adjudicaciones para proyectos de infraestructura digital crecieron "
            "un 23% interanual en el primer semestre. El plan quinquenal 2026-2030 sitúa la cooperación "
            "tecnológica con el Sur Global como una prioridad estratégica de primer orden."
        ),
        "fuente_label": "TeleSUR — China potencia al BRICS con infraestructura digital",
        "fuente_url": "https://www.telesurtv.net/china-potencia-brics-experiencia-infraestructura-digital/",
    },
    {
        "emoji": "☀️",
        "titulo": "China alcanza un nuevo hito en energía solar espacial: transmisión de 1.180 vatios",
        "cuerpo": (
            "El equipo del proyecto Zhuri (Caza del Sol) de la Universidad de Xidian logró transmitir "
            "1.180 vatios de energía de forma inalámbrica a 100 metros de distancia con una eficiencia "
            "del 20,8%, cargando múltiples objetivos en movimiento simultáneamente. El sistema también "
            "demostró la carga inalámbrica de drones a 30 metros a 30 km/h. El proyecto apunta a construir "
            "una matriz solar de 1 km de ancho en órbita geoestacionaria a 36.000 km de altitud, capaz "
            "de abastecer tanto misiones espaciales como la red eléctrica terrestre de forma continua, "
            "sin interrupciones por nubes o ciclos día-noche."
        ),
        "fuente_label": "CGTN — China advances space solar power breakthrough",
        "fuente_url": "https://news.cgtn.com/news/2026-05-19/China-advances-space-solar-power-breakthrough-1NgRg7RgnpC/p.html",
    },
    {
        "emoji": "⚡",
        "titulo": "Energía inteligente china: de los proyectos piloto al despliegue comercial a gran escala",
        "cuerpo": (
            "La industria de energía inteligente de China ha superado la fase de pilotos y entrado en "
            "despliegue comercial masivo, con la IA aplicada a la previsión de generación renovable, "
            "la gestión de redes y la optimización del consumo industrial. China abre nuevas vías de "
            "cooperación internacional en este campo, especialmente con países del Sur Global que buscan "
            "electrificarse con tecnologías limpias. El XV Plan Quinquenal asigna más de 1 billón de "
            "yuanes anuales a inversión en infraestructura de red eléctrica renovable."
        ),
        "fuente_label": "People's Daily — China's smart energy push",
        "fuente_url": "https://en.people.cn/n3/2026/0714/c90000-20477405.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "El XV Plan Quinquenal (2026-2030): cinco años para consolidar el liderazgo tecnológico global",
        "cuerpo": (
            "China ha fijado su hoja de ruta para 2026-2030: consolidar su poder global mediante la "
            "tecnología, la autosuficiencia y la proyección exterior. Los ejes son la IA Plus (IA como "
            "infraestructura transversal), el 6G, la robótica, la biotecnología y la economía de baja "
            "altitud (drones). El presupuesto en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones "
            "de yuanes. El objetivo: que el 70% de la economía productiva incorpore IA para 2027, y el "
            "90% para 2030, con las industrias de IA superando los 10 billones de yuanes en valor."
        ),
        "fuente_label": "The Conversation — 2026-2030: China consolida su poder global",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, IA, economia, robotica y energia.", bold=False),
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
    title = "China Al Dia — Semana 11-18 Julio 2026"
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
