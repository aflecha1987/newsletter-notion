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

def p_links(links):
    """links: list of (label, url) tuples"""
    rich_text = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(links):
        rich_text.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
        if i < len(links) - 1:
            rich_text.append({"type": "text", "text": {"content": " · "}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text}}

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
        "titulo": "Unitree Robotics: primera empresa de robots humanoides en cotizar en bolsa",
        "cuerpo": (
            "El 1 de junio, la Bolsa de Shanghái (STAR Market) aprobó la salida a bolsa de Unitree Robotics, "
            "la mayor empresa del mundo en ventas de robots humanoides. La compañía busca captar 4.200 millones "
            "de yuanes (~620 millones de dólares) mediante la emisión de al menos 40,4 millones de nuevas "
            "acciones. Unitree se convierte en la primera empresa de robots humanoides en cotizar en el mercado "
            "A-share chino, un hito que marca la madurez de la industria. Casi en paralelo, su rival AGIBOT "
            "superó las 10.000 unidades producidas, consolidando el llamado 'duopolio de los humanoides chinos'. "
            "En la misma semana, Nvidia anunció su alianza con Unitree: el robot H2 —de casi 1,80 m— combinado "
            "con el hardware Jetson Thor de Nvidia (GPU Blackwell) será el primer sistema robótico que el "
            "fabricante de chips comercialice a institutos de investigación de Stanford, ETH Zurich y otros "
            "centros punteros del mundo."
        ),
        "fuentes": [
            ("CNBC", "https://www.cnbc.com/2026/06/01/nvidia-unitree-humanoid-robotics-system-researchers.html"),
            ("Rest of World", "https://restofworld.org/2026/unitree-china-humanoid-robot-shanghai-ipo/"),
            ("TechTimes", "https://www.techtimes.com/articles/317632/20260602/unitree-ipo-cleared-agibot-hits-10000-units-china-humanoid-robot-duopoly-takes-shape.htm"),
        ],
    },
    {
        "emoji": "🚗",
        "titulo": "BYD exportaciones récord en mayo: +80% interanual, 160.644 unidades",
        "cuerpo": (
            "BYD publicó sus datos de mayo y la cifra internacional fue histórica: 160.644 unidades exportadas, "
            "un incremento del 80% interanual, representando el 42% de todas sus ventas de NEV en el mes. El "
            "total de entregas en mayo fue de 383.453 vehículos, recuperando el crecimiento positivo tras nueve "
            "meses consecutivos de caída en ventas globales. La compañía mantiene su objetivo de 1,3 millones de "
            "vehículos vendidos fuera de China en 2026, un 25% por encima de su resultado de 2025. En la misma "
            "semana, la marca Leapmotor también estableció su propio récord histórico de exportaciones mensuales, "
            "otra muestra de que el sector EV chino avanza en bloque hacia la conquista de mercados internacionales."
        ),
        "fuentes": [
            ("Electrive", "https://www.electrive.com/2026/06/02/byd-records-first-sales-increase-in-eight-months/"),
            ("Bloomberg Línea", "https://www.bloomberglinea.com/negocios/byd-vuelve-a-crecer-ventas-suben-por-primera-vez-en-nueve-meses-gracias-a-la-demanda-internacional/"),
            ("Car News China", "https://carnewschina.com/2026/06/01/china-ev-global-sales-in-may-2026-leapmotor-new-historical-record-byd-stopped-falling-yoy/"),
        ],
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23: la primera astronauta hongkonesa y un año en órbita",
        "cuerpo": (
            "La misión tripulada Shenzhou-23, lanzada el 24 de mayo desde Jiuquan, completó su acoplamiento a "
            "la estación Tiangong en menos de cuatro horas. La tripulación: Zhu Yangzhu (comandante), Zhang "
            "Zhiyuan (piloto) y Li Jiaying, también conocida como Lai Ka-ying, excomisaria de la Policía de "
            "Hong Kong, que se convierte en la primera astronauta procedente de Hong Kong del programa chino. "
            "Por primera vez en la historia, un astronauta chino realizará una estancia de un año completo en "
            "órbita, un hito clave de cara al entrenamiento para misiones lunares tripuladas antes de 2030. "
            "En paralelo, los astronautas de Shenzhou-21 aterrizaron el 29 de mayo tras 210 días en el espacio."
        ),
        "fuentes": [
            ("El Español", "https://www.elespanol.com/omicrono/defensa-y-espacio/20260524/china-lanza-exito-mision-espacial-ambiciosa-nave-shenzhou-23-viaja-rumbo-estacion-tiangong/1003744257663_0.html"),
            ("El Financiero", "https://www.elfinanciero.com.mx/ciencia/2026/05/29/astronautas-de-mision-china-shenzhou-21-vuelven-a-la-tierra-estuvieron-210-dias-en-orbita/"),
            ("Vanguardia", "https://www.vanguardia.com/mundo/2026/05/24/mision-shenzhou-23-avanza-con-exito-astronautas-chinos-ya-estan-en-la-estacion-tiangong/"),
        ],
    },
    {
        "emoji": "⚡",
        "titulo": "Histórico: la capacidad solar china supera al carbón por primera vez",
        "cuerpo": (
            "2026 marca un punto de inflexión en la historia energética de China: la capacidad instalada de "
            "energía solar supera por primera vez a la del carbón, consolidando a China como la mayor potencia "
            "solar del planeta. En 2026 se añadirán más de 300 GW de capacidad renovable. Para dar escala al "
            "dato: China instaló en 2025 más capacidad eólica que todo lo que Estados Unidos ha instalado en "
            "toda su historia. La barata electricidad resultante es además la ventaja secreta de China en la "
            "carrera de la IA: sus centros de datos crecen al 30% anual, respaldados por energía renovable y "
            "asequible sin parangón en el mundo. En el primer semestre de 2025, la energía eólica y solar ya "
            "generaron 2.073 TWh, superando por primera vez la suma de nuclear, hidráulica y bioenergía juntas."
        ),
        "fuentes": [
            ("Ecoticias", "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez"),
            ("Al Jazeera", "https://www.aljazeera.com/economy/2026/5/28/chinas-secret-weapon-in-ai-race-with-us-lots-of-cheap-energy"),
            ("Ember", "https://ember-energy.org/es/analisis/global-electricity-review-2026/"),
        ],
    },
    {
        "emoji": "📈",
        "titulo": "La IA catapulta a Zhongji Innolight al primer puesto del índice CSI 300",
        "cuerpo": (
            "La empresa de transceivers ópticos Zhongji Innolight, proveedor clave de Nvidia para centros de "
            "datos de IA, se convirtió esta semana en la compañía con mayor ponderación del índice CSI 300 "
            "—el indicador principal de la bolsa china—, con un 5,3% del total, desbancando al gigante de "
            "baterías CATL. El movimiento refleja el reajuste del mercado hacia los beneficiarios directos "
            "del boom de la IA en China. En el ámbito de los startups, las empresas chinas de IA captaron "
            "alrededor de 16.500 millones de dólares en el Q1 2026, liderado por firmas como StepFun, "
            "Moonshot AI y Galaxy Bot. El modelo DeepSeek-V4, lanzado en abril, opera con respaldo del "
            "hardware Ascend 950 de Huawei, con 1,6 billones de parámetros y hasta un millón de palabras "
            "de contexto, demostrando que la IA china avanza con independencia tecnológica real."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-06-04/ai-boom-propels-china-optical-maker-to-top-weighting-on-csi-300"),
            ("Blog Mean CEO", "https://blog.mean.ceo/startups-china-news-june-2026/"),
            ("CNN", "https://www.cnn.com/2026/04/24/tech/chinas-ai-deepseek-v4-intl-hnk"),
        ],
    },
    {
        "emoji": "🚙",
        "titulo": "Nio lanza el L60 renovado con chip propio de 5nm y LiDAR el 11 de junio",
        "cuerpo": (
            "La submarca familiar de Nio abrió los pedidos anticipados del L60 renovado en el Salón del "
            "Automóvil de Shenzhen, con fecha de lanzamiento oficial fijada para el 11 de junio. El vehículo "
            "incorpora LiDAR en el techo y el chip de conducción autónoma de 5nm desarrollado en casa por Nio, "
            "una apuesta clara por la soberanía tecnológica. Xpeng, por su parte, mantiene su plan de comenzar "
            "la producción en masa de robots humanoides IRON a finales de 2026. China también publicó su plan "
            "de estandarización del sector automóvil 2026, con nuevas normativas de seguridad para sistemas de "
            "IA en vehículos de conducción autónoma, reforzando su posición como árbitro global de los "
            "estándares del vehículo inteligente."
        ),
        "fuentes": [
            ("South China Morning Post", "https://www.scmp.com/economy/china-economy/article/3355063/china-unveils-auto-industry-blueprint-set-ev-ai-vehicle-and-semiconductor-standards"),
            ("CNN Business", "https://www.cnn.com/2026/05/02/business/beijing-auto-show-china-evs-intl-hnk"),
        ],
    },
]


def build_blocks():
    today = "6 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: robotica, vehiculos electricos, espacio, energia y mercados financieros.", bold=False),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        if "fuentes" in n:
            blocks.append(p_links(n["fuentes"]))
        elif "fuente_label" in n:
            blocks.append(p_link(n["fuente_label"], n["fuente_url"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 1-6 Junio 2026"
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
