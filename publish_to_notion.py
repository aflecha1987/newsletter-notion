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

def p_links(sources):
    """sources: list of (label, url) tuples"""
    rich = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(sources):
        rich.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
        if i < len(sources) - 1:
            rich.append({"type": "text", "text": {"content": " · "}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}}

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
        "emoji": "📡",
        "titulo": "China lanza un programa piloto nacional para acelerar el 6G",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de la Información (MIIT) lanzó el 4 de junio un "
            "programa piloto conjunto ministerio-provincias para acelerar la innovación y el desarrollo "
            "del 6G, sentando las bases para su futura implantación comercial. El programa integra redes "
            "de comunicación con inteligencia artificial, internet satelital y tecnologías de detección "
            "inalámbrica. China ya acumula más de 300 tecnologías clave en 6G y apunta a la "
            "comercialización para 2030, convirtiéndose en el primer país en definir su estándar global."
        ),
        "fuentes": [
            ("24 News HD", "https://www.24newshd.tv/04-Jun-2026/china-launches-pilot-program-accelerate-6g-innovation-development"),
            ("China Daily", "https://www.chinadaily.com.cn/a/202601/21/WS69704a8ca310d6866eb34f27.html"),
            ("CGTN", "https://news.cgtn.com/news/2026-03-29/VHJhbnNjcmlwdDg5ODg0/index.html"),
        ],
    },
    {
        "emoji": "💾",
        "titulo": "China exporta chips por valor de 103.500 millones de dólares en solo 4 meses",
        "cuerpo": (
            "En los primeros cuatro meses de 2026, China exportó 117.000 millones de circuitos integrados "
            "por un valor de 103.500 millones de dólares, un incremento del 83,7% interanual. Los módulos "
            "ópticos y chips chinos se han convertido en eslabones críticos de la cadena de suministro "
            "global de IA. SMIC, el mayor fabricante de chips de China, registró una utilización de "
            "capacidad del 93,1% en Q1 2026, con ingresos récord proyectados superiores a 11.000 "
            "millones de dólares en el año. SMIC también inició producción en piloto de su proceso de "
            "5 nm para socios como Huawei y Alibaba."
        ),
        "fuentes": [
            ("Xinhua", "https://english.news.cn/20260607/f2149e761e3b4317bf03bb21569cc1b8/c.html"),
            ("CNBC", "https://www.cnbc.com/2026/04/03/chinese-chip-firms-record-revenue-ai-boom-us-curbs.html"),
            ("Enkiai", "https://enkiai.com/ai-market-intelligence/smic-ai-chip-strategy-2026-inside-chinas-5nm-power-play/"),
        ],
    },
    {
        "emoji": "🚀",
        "titulo": "El primer robot astronauta humanoide del mundo: China lo llevará al espacio",
        "cuerpo": (
            "Engine AI, empresa china de robótica con sede en Shenzhen, anunció el programa Humanoid Robot "
            "Astronaut Exploration Program en alianza con Beijing Interstellar Human Spaceflight Technology. "
            "El robot PM01 —1,38 m de altura, 40 kg, articulaciones que imitan el movimiento humano, "
            "rotación de cintura hasta 320 grados— se convertirá en el primer humanoide en el espacio. "
            "Integra chips NVIDIA Jetson Orin e Intel N97, sensores de alta precisión y toma de decisiones "
            "autónoma. China ya tiene un asistente de IA operativo en su estación espacial Tiangong."
        ),
        "fuentes": [
            ("Interesting Engineering", "https://interestingengineering.com/ai-robotics/worlds-first-humanoid-robot-astronaut-china"),
            ("CnEV Post", "https://cnevpost.com/2026/01/26/chinese-firm-launches-effort-to-send-humanoid-robot-into-space/"),
            ("Electrek", "https://electrek.co/2026/01/28/bot-space-race-humanoid-robots-connect-to-satellite-prep-for-space-launch/"),
        ],
    },
    {
        "emoji": "🤖",
        "titulo": "AGIBOT WORLD CHALLENGE 2026: la competición global de IA encarnada",
        "cuerpo": (
            "El AGIBOT WORLD CHALLENGE 2026 se presentó en el ICRA 2026, la mayor conferencia de robótica "
            "del mundo, con dos pistas: Reasoning to Action (planificación y ejecución de tareas físicas) "
            "y World Model (predicción de cambios en el entorno físico). Participaron equipos de la "
            "Academia China de Ciencias, Tsinghua, USTC, Alibaba y vivo. China produce el 85% de los "
            "robots humanoides instalados globalmente, a aproximadamente la mitad del coste de sus "
            "competidores occidentales, consolidando su liderazgo en IA encarnada."
        ),
        "fuentes": [
            ("TradingView News", "https://www.tradingview.com/news/eqs:09f22872d094b:0-agibot-world-challenge-2026-advances-embodied-ai-competition-from-simulation-to-real-robot-testing-at-icra-2026/"),
            ("CNBC", "https://www.cnbc.com/2026/06/03/humanoid-robots-trillion-dollar-ai-market.html"),
            ("Rest of World", "https://restofworld.org/2026/china-ai-robotics-training-data/"),
        ],
    },
    {
        "emoji": "🧠",
        "titulo": "China capta talento de IA de EE.UU. para construir su próxima super-app",
        "cuerpo": (
            "Yao Shunyu, ex científico jefe de IA en OpenAI, se incorporó a Tencent con el objetivo "
            "explícito de crear una organización de AGI a largo plazo en China. Las empresas chinas han "
            "apostado por un modelo de IA aplicada —fábricas, electrónica de consumo, salud— capturando "
            "talento de primer nivel global. En paralelo, Zhipu AI (Knowledge Atlas) y MiniMax se "
            "incorporaron al Hang Seng Tech Index el 8 de junio, atrayendo entre 1.250 y 1.750 millones "
            "de dólares en flujos de inversión pasiva. Las startups chinas de IA levantaron 16.500 "
            "millones de dólares solo en Q1 2026."
        ),
        "fuentes": [
            ("CNBC", "https://www.cnbc.com/2026/06/05/china-may-move-toward-us-path-on-ai-as-firms-poach-employees.html"),
            ("SCMP", "https://www.scmp.com/tech/tech-war/article/3338528/tech-war-china-takes-confident-strides-develop-more-ai-innovation-2026"),
            ("Mean.CEO Blog", "https://blog.mean.ceo/startups-china-news-june-2026/"),
        ],
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate su récord: más de 160.000 exportaciones solo en mayo de 2026",
        "cuerpo": (
            "BYD publicó sus cifras de mayo de 2026: 376.990 vehículos eléctricos (NEV) vendidos "
            "globalmente, con exportaciones superiores a 160.000 unidades, nuevos máximos históricos. "
            "La empresa apunta a vender 1,3 millones de unidades fuera de China en 2026, un 24% más "
            "que el año anterior, con plantas ya operativas en Tailandia, Uzbekistán y Brasil, y la "
            "apertura próxima de su primera fábrica europea. Las exportaciones chinas de vehículos "
            "de nueva energía son el motor más dinámico del comercio exterior del país."
        ),
        "fuentes": [
            ("Global China EV", "https://www.globalchinaev.com/post/byd-leads-chinas-record-may-nev-month-with-377000-units-and-surging-exports"),
            ("Rest of World", "https://restofworld.org/2026/china-ev-exports-competition-price/"),
            ("Atlantic Council", "https://www.atlanticcouncil.org/blogs/energysource/chinese-electric-vehicle-exports-rise-amid-the-oil-crisis-posing-a-dilemma-for-importing-countries/"),
        ],
    },
    {
        "emoji": "⚡",
        "titulo": "China instala el 50% de toda la energía eólica y solar del mundo",
        "cuerpo": (
            "En 2025, China instaló más de la mitad de toda la energía eólica y solar añadida "
            "globalmente: 370 GW fotovoltaicos y 117 GW eólicos nuevos (+22% interanual). La capacidad "
            "acumulada de energía renovable supera ya los 1,84 billones de kilovatios —el 47,3% de toda "
            "la capacidad instalada del país—, superando por primera vez a la energía térmica. En 2024, "
            "en China se instalaron más aerogeneradores y paneles solares que en todo el resto del mundo "
            "combinado. El viento y el sol generaron el 26% de toda la electricidad china en abril 2025."
        ),
        "fuentes": [
            ("Blitz India Media", "https://blitzindiamedia.com/world/china-renewable-energy-milestone-2026-wind-solar-357gw/"),
            ("Ember Energy", "https://ember-energy.org/latest-updates/wind-and-solar-generate-over-a-quarter-of-chinas-electricity-for-the-first-month-on-record/"),
            ("IEA", "https://www.iea.org/reports/global-energy-review-2026/technology-solar-pv-and-wind"),
        ],
    },
    {
        "emoji": "🛰️",
        "titulo": "Pekín inaugura el Instituto de Computación Inteligente Espacial",
        "cuerpo": (
            "Pekín puso en marcha el Beijing Space Intelligent Computing Research Institute, un centro "
            "estatal de investigación especializado en inteligencia artificial aplicada al espacio. "
            "Ubicado en E-Town —el hub tecnológico que alberga las principales empresas chinas de "
            "robótica e IA—, el instituto se centra en chips de computación espacial, comunicaciones "
            "láser entre satélites, energía espacial y estándares de seguridad espacial. La iniciativa "
            "refuerza el papel de China como líder en la convergencia entre la carrera espacial y la "
            "revolución de la inteligencia artificial."
        ),
        "fuentes": [
            ("SCMP", "https://www.scmp.com/tech/big-tech/article/3356102/china-launches-space-computing-hub-spacex-gears-historic-ipo"),
        ],
    },
]


def build_blocks():
    semana = "1 al 7 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · Semana del {semana}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio y sociedad.", bold=False),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        blocks.append(p_links(n["fuentes"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 1-7 Junio 2026"
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
