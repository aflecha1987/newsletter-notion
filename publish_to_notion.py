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
        if i > 0:
            rich.append({"type": "text", "text": {"content": " · "}})
        rich.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
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

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


NOTICIAS = [
    {
        "emoji": "🤝",
        "titulo": "Cumbre histórica Trump-Xi en Pekín: acuerdos comerciales billonarios y nueva era diplomática",
        "cuerpo": (
            "El presidente Donald Trump visitó Pekín del 14 al 15 de mayo con una delegación sin precedentes "
            "(Elon Musk, Tim Cook, Jensen Huang) para reunirse con Xi Jinping. Los acuerdos incluyen la compra "
            "china de al menos 17.000 millones de dólares anuales en productos agrícolas estadounidenses "
            "(2026-2028), la adquisición de 200 aviones Boeing, acuerdos sobre tierras raras estratégicas "
            "(itrio, escandio, neodimio, indio) y la creación del U.S.-China Board of Trade y el "
            "U.S.-China Board of Investment para continuar las negociaciones arancelarias. El ministro "
            "de Exteriores Wang Yi calificó la reunión de histórica con resultados sustanciales."
        ),
        "fuentes": [
            ("CNBC", "https://www.cnbc.com/2026/05/18/us-china-announce-deals-after-trump-xi-summit.html"),
            ("Xinhua", "https://english.news.cn/20260517/d50300c5f44b418eaf63dc9a0494e856/c.html"),
            ("CNN", "https://www.cnn.com/2026/05/18/china/xi-trump-trade-agreements-china-visit-intl-hnk"),
        ],
    },
    {
        "emoji": "🌞",
        "titulo": "Hito histórico: la energía solar supera al carbón en China por primera vez",
        "cuerpo": (
            "En 2026, la capacidad instalada de energía solar en China superará por primera vez la del carbón, "
            "según el China Electricity Council. A finales de año, las energías no fósiles representarán el "
            "63% de la capacidad instalada total del país, frente al 31% del carbón. La capacidad conjunta "
            "de eólica y solar ya superó 1,9 billones de kW en marzo de 2026 (+28,1% interanual), y China "
            "prevé añadir más de 400 millones de kW en nuevas instalaciones a lo largo del año — más de "
            "300 millones de ellos de energías renovables."
        ),
        "fuentes": [
            ("China Daily", "https://www.chinadaily.com.cn/a/202604/29/WS69f15f2ca310d6866eb461b9.html"),
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-02-03/china-s-solar-power-capacity-on-course-to-surpass-coal-this-year"),
            ("Yale E360", "https://e360.yale.edu/digest/china-solar-coal-2026"),
        ],
    },
    {
        "emoji": "🌍",
        "titulo": "La ONU elogia el liderazgo climático de China: \"Donde China lidera, el mundo sigue\"",
        "cuerpo": (
            "El secretario ejecutivo de la CMNUCC, Simon Stiell, pronunció un discurso en Pekín durante la "
            "semana de la cumbre Trump-Xi, alabando la transición energética china como sobrecogedora. "
            "Destacó que las inversiones chinas en energía limpia casi se duplicaron en una década, "
            "superando los 625.000 millones de dólares solo en 2024, y que China es responsable de haber "
            "reducido a la mitad las proyecciones de aumento de temperatura global en los últimos diez años. "
            "En 2025, la capacidad eólica y solar instalada de forma nueva superó los 430 millones de kW "
            "(+22% interanual), superando por primera vez a la térmica."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-05-14/un-climate-chief-lavishes-praise-on-china-as-trump-meets-xi"),
            ("ONU Noticias", "https://news.un.org/es/story/2026/05/1541448"),
            ("Global Times", "https://www.globaltimes.cn/page/202605/1361026.shtml"),
        ],
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4: 1,6 billones de parámetros sobre chips Huawei — independencia tecnológica total",
        "cuerpo": (
            "DeepSeek presentó su modelo V4 con 1,6 billones de parámetros y ventana de contexto de 1 millón "
            "de tokens, completamente optimizado para el chip Huawei Ascend 950PR — sin depender de Nvidia. "
            "Es el primer gran modelo de frontera del mundo diseñado nativamente para chips chinos. "
            "V4-Pro cuesta 3,48 USD por millón de tokens de salida; V4-Flash solo 0,28 USD. "
            "El anuncio disparó los pedidos de Ascend de ByteDance, Tencent y Alibaba en días. "
            "Huawei proyecta enviar 750.000 unidades del Ascend 950PR en 2026 y aspira al 60% del mercado "
            "de aceleradores de IA en China antes de finales de año."
        ),
        "fuentes": [
            ("Fortune", "https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/"),
            ("Tom's Hardware", "https://www.tomshardware.com/tech-industry/artificial-intelligence/deepseek-launches-1-6-trillion-parameter-v4-on-huawei-chips-as-us-escalates-ai-theft-accusations"),
            ("Technology.org", "https://www.technology.org/2026/04/29/huawei-ascend-950-orders-surge-as-deepseek-v4-drives-chinese-cloud-giants-to-buy/"),
        ],
    },
    {
        "emoji": "🦾",
        "titulo": "Unitree Robotics solicita OPA de 610 millones de dólares: el fabricante de humanoides más vendido del mundo va a bolsa",
        "cuerpo": (
            "Unitree Robotics, el fabricante de robots humanoides más vendido del mundo en 2025, presentó "
            "formalmente su solicitud de salida a bolsa en el STAR Market de la Bolsa de Shanghái para "
            "captar 4.200 millones de yuanes (610 millones de dólares). Los fondos se destinarán a "
            "desarrollo de modelos de IA, nuevos productos y expansión de plantas. Fundada en Hangzhou "
            "en 2016, la empresa facturó 1.710 millones de yuanes en 2025 (frente a 392M en 2024) y "
            "generó un beneficio neto de 600 millones de yuanes. Esta semana, más de 100 robots "
            "humanoides fueron exhibidos en Hong Kong, con 4 de los 5 fabricantes más vendidos del mundo."
        ),
        "fuentes": [
            ("Rest of World", "https://restofworld.org/2026/unitree-china-humanoid-robot-shanghai-ipo/"),
            ("CNBC", "https://www.cnbc.com/2026/03/20/unitree-plans-shanghai-ipo-testing-interest-in-humanoid-robots.html"),
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-03-20/chinese-robot-maker-unitree-seeks-610-million-in-shanghai-ipo"),
        ],
    },
    {
        "emoji": "🤖",
        "titulo": "China convierte la IA robótica en pilar de la estrategia nacional: informe IFR mayo 2026",
        "cuerpo": (
            "Según el informe publicado el 6 de mayo por la International Federation of Robotics (IFR), "
            "China ha situado oficialmente los robots con inteligencia artificial como eje estructural "
            "de toda su estrategia económica nacional, pasando de ser un objetivo de nicho a convertirse "
            "en el tejido conector de la modernización del país. El nuevo plan quinquenal (2026-2030) "
            "habla explícitamente de inteligencia encarnada (embodied intelligence) como palanca de "
            "crecimiento, promoviendo robots de alta gama integrados con IA frente a la automatización "
            "industrial tradicional."
        ),
        "fuentes": [
            ("RoboticsTomorrow", "https://www.roboticstomorrow.com/news/2026/05/06/china-makes-ai-powered-robots-core-of-national-strategy-%E2%80%93-ifr-reports/26521/"),
            ("The Diplomat", "https://thediplomat.com/2026/03/chinas-new-five-year-plan-prioritizes-robotics-the-world-should-pay-attention/"),
        ],
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate récord de exportaciones en abril: +70,9% interanual rumbo al liderazgo global",
        "cuerpo": (
            "En abril de 2026, BYD exportó 134.542 vehículos de pasajeros, un aumento del 70,9% "
            "respecto al año anterior, estableciendo un nuevo récord histórico mensual de exportaciones. "
            "El gigante chino mantiene su objetivo de 1,5 millones de ventas en el exterior en 2026. "
            "A nivel global, BYD se convirtió en 2025 en el número 1 mundial en ventas de vehículos "
            "100% eléctricos, superando a Tesla por primera vez en la historia, con 2,26 millones de "
            "BEV vendidos. Los vehículos eléctricos chinos ahorrarán más de 28.000 millones de dólares "
            "en importaciones de petróleo en 2026, con el crudo por encima de los 100 dólares."
        ),
        "fuentes": [
            ("Electric Cars Report", "https://electriccarsreport.com/2026/05/byd-april-2026-sales-overseas-surge-offsets-china-slowdown/"),
            ("CNBC", "https://www.cnbc.com/2026/01/02/chinas-byd-to-overtake-tesla-as-worlds-top-ev-seller-for-first-time.html"),
        ],
    },
    {
        "emoji": "🛸",
        "titulo": "Brazo robótico espacial y robot humanoide controlado desde la órbita: nuevos hitos de China en el espacio",
        "cuerpo": (
            "El satélite Yuxing-3 06, lanzado el 16 de marzo desde Jiuquan, completó con éxito las "
            "primeras pruebas orbitales del primer brazo robótico flexible diseñado para reparar "
            "satélites en órbita, desarrollado por Suzhou Sanyuan Aerospace Technology. "
            "En paralelo, un laboratorio de GuoXing Aerospace y la Universidad Jiao Tong de Shanghái "
            "demostró por primera vez el control remoto de un robot humanoide desde el espacio, "
            "integrando un agente de IA, procesamiento orbital y un robot terrestre en un sistema "
            "de control cerrado y autónomo."
        ),
        "fuentes": [
            ("Interesting Engineering (brazo)", "https://interestingengineering.com/ai-robotics/china-flexible-space-robotic-arm"),
            ("Interesting Engineering (humanoide)", "https://interestingengineering.com/innovation/china-humanoid-robot-control-using-space-inference"),
        ],
    },
    {
        "emoji": "🚀",
        "titulo": "Tianwen-2: China lanza su primera misión de regreso de muestras de un asteroide — finales de mayo",
        "cuerpo": (
            "La misión Tianwen-2 está prevista para ser lanzada a finales de mayo de 2026, "
            "convirtiéndose en la primera misión china de regreso de muestras desde un asteroide y "
            "la segunda en su historia de exploración interplanetaria profunda (tras Tianwen-1 a "
            "Marte en 2020). La sonda llegará a su destino en julio de 2026, desde donde enviará "
            "imágenes y eventualmente muestras inéditas de un cuerpo primordial del Sistema Solar. "
            "Más adelante en el año, está previsto el lanzamiento de Chang'e-7 hacia el polo sur "
            "lunar en busca de hielo de agua, previsto para agosto de 2026."
        ),
        "fuentes": [
            ("China in Space", "https://www.china-in-space.com/p/change-7-to-start-searching-for-lunar"),
            ("Planetary.org", "https://www.planetary.org/space-missions/change-7"),
        ],
    },
]


def build_blocks():
    today = date.today().strftime("%-d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Día · Semana del 14 al 21 de mayo de 2026", "🇨🇳"),
        p(
            "Recopilación de las noticias más relevantes de China esta semana: "
            "diplomacia, energía, IA, robótica, vehículos eléctricos y espacio.",
            bold=False,
        ),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        blocks.append(p_links(n["fuentes"]))
        blocks.append(divider())

    blocks.append(p(
        "China al Día · Newsletter semanal en español · Fuentes internacionales verificadas",
        bold=True,
    ))
    return blocks


def create_notion_page():
    title = "China Al Día — Semana 14-21 Mayo 2026"
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

    print(f"Creando página en Notion: '{title}'")
    print(f"Noticias incluidas: {len(NOTICIAS)}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "").replace("-", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id}")
    print(f"\n¡Listo!")
    print(f"URL: {page_url}")
    return page_url


if __name__ == "__main__":
    create_notion_page()
