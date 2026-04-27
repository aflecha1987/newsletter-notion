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
        "emoji": "🧠",
        "titulo": "DeepSeek lanza V4: el mayor modelo open-weight del mundo con 1,6 billones de parámetros",
        "cuerpo": (
            "El 24 de abril, DeepSeek presentó su nueva generación de modelos de IA, sacudiendo de nuevo "
            "la industria global. El modelo V4 Pro cuenta con 1,6 billones de parámetros —el mayor modelo "
            "open-weight del mundo—, con ventana de contexto de 1 millón de tokens. DeepSeek asegura que "
            "V4 Pro supera a GPT-5.2 de OpenAI y a Gemini 3.0 Pro de Google en varios benchmarks de "
            "razonamiento y programación. El modelo se ha desplegado en colaboración con Huawei, cuyos "
            "chips Ascend 950 alimentan los clústeres mediante la tecnología 'Supernode', avanzando en "
            "la independencia tecnológica de China. Los precios son disruptivos: 0,145 $/millón de tokens "
            "input para el Pro —hasta 7 veces más barato que ChatGPT— y está disponible como código abierto."
        ),
        "fuente_label": "CNBC — DeepSeek V4 LLM preview open-source AI competition",
        "fuente_url": "https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html",
    },
    {
        "emoji": "🏆",
        "titulo": "Stanford HAI 2026: China ha eliminado la ventaja de EE.UU. en inteligencia artificial",
        "cuerpo": (
            "El Índice de Inteligencia Artificial 2026 del Instituto HAI de la Universidad de Stanford, "
            "publicado el 13 de abril, concluye que China ha eliminado la ventaja que Estados Unidos "
            "mantenía en IA. Por primera vez, las publicaciones científicas de China sobre IA superan "
            "en número e impacto a las estadounidenses, y el país asiático lidera en patentes de IA a "
            "nivel global. La brecha en capacidades de los modelos se ha cerrado significativamente en "
            "el último año, impulsada por empresas como DeepSeek, Baidu, Alibaba y Zhipu AI, y por la "
            "intensa integración de la IA en sectores productivos. En el Q1 2026, las patentes de IA "
            "crecieron un 31,2% interanual y China cuenta con 602 millones de usuarios de IA generativa."
        ),
        "fuente_label": "SiliconANGLE — Stanford HAI 2026 AI Index: China erases US lead",
        "fuente_url": "https://siliconangle.com/2026/04/13/stanford-hais-2026-ai-index-reveals-china-u-s-now-neck-neck-race-global-dominance/",
    },
    {
        "emoji": "✈️",
        "titulo": "Xpeng en Auto China 2026: coches voladores, robot IRON y tres modelos de robotaxi",
        "cuerpo": (
            "En el Salón del Automóvil de Pekín 2026, Xpeng presentó su ecosistema de 'IA física': "
            "su robot humanoide de nueva generación IRON entrará en producción masiva en el Q4 de 2026, "
            "comenzando como recepcionistas y asistentes de ventas. El 'Land Aircraft Carrier' (coche "
            "volador) iniciará producción masiva en 2027, con más de 7.000 pedidos ya confirmados. "
            "Además, la compañía lanzará tres modelos de robotaxi en 2026 e iniciará pruebas en Guangzhou. "
            "La arquitectura VLA 2.0 (visual-lingüística-acción) dota de inteligencia unificada a todos "
            "sus vehículos y robots, posicionando a Xpeng como referente global de la movilidad inteligente."
        ),
        "fuente_label": "Technology.org — Xpeng plans flying car mass production 2027, humanoid robots Q4 2026",
        "fuente_url": "https://www.technology.org/2026/04/23/xpeng-plans-flying-car-mass-production-for-2027-humanoid-robots-by-late-2026/",
    },
    {
        "emoji": "🤖",
        "titulo": "China controla el 90% del mercado global de robots humanoides",
        "cuerpo": (
            "Un informe de CNBC confirma que las empresas chinas fabrican y envían más robots humanoides "
            "que ningún otro país del mundo, controlando aproximadamente el 90% del mercado global. "
            "Compañías como Unitree y Agibot lideran el segmento, mientras los fabricantes de coches "
            "eléctricos como BYD, Xpeng y Geely aceleran su entrada en robótica. Rest of World señala "
            "que China está aplicando 'el mismo guion que con los vehículos eléctricos': fabricación "
            "masiva, reducción agresiva de costes e integración vertical de la cadena de suministro. "
            "Los inversores chinos apuestan fuerte con valoraciones más contenidas que en EE.UU., "
            "priorizando la presencia real en el mercado sobre la especulación."
        ),
        "fuente_label": "CNBC — China ships more humanoid robots than the U.S.",
        "fuente_url": "https://www.cnbc.com/2026/04/21/china-humanoid-robots-us-investors.html",
    },
    {
        "emoji": "🛡️",
        "titulo": "China activa escudo tecnológico: veta la inversión estadounidense no autorizada en startups de IA",
        "cuerpo": (
            "El gobierno chino instruyó esta semana a sus principales startups de inteligencia artificial "
            "—incluidas Moonshot AI y StepFun— para que rechacen capital de inversores estadounidenses "
            "sin autorización previa del Estado. La medida forma parte de una estrategia para salvaguardar "
            "la propiedad intelectual y el control estratégico de sus tecnologías clave. En paralelo, "
            "China redujo sus tenencias de bonos del Tesoro de EE.UU. a 757.000 millones de dólares, "
            "consolidando su tendencia de diversificación de reservas y alejamiento progresivo del dólar "
            "como eje de sus reservas internacionales."
        ),
        "fuente_label": "Ámbito — China blindará sus empresas tecnológicas de inversiones de EE.UU.",
        "fuente_url": "https://www.ambito.com/economia/china-blindara-sus-empresas-tecnologicas-las-inversiones-estadounidenses-n6270546",
    },
    {
        "emoji": "⚡",
        "titulo": "China resiste la crisis del petróleo gracias a su estrategia de electrificación masiva",
        "cuerpo": (
            "Un análisis de CNN publicado el 21 de abril concluye que China está en posición de fortaleza "
            "ante la volatilidad del petróleo gracias a su apuesta por la electrificación. El país produce "
            "ya el 85% de los paneles solares del mundo y el 60% de los vehículos eléctricos globales. "
            "Nuevas cifras confirman que China genera más electricidad renovable que cualquier otra nación "
            "y que la demanda de petróleo para transporte tocó su pico en 2025. La estrategia de "
            "'electroestado' —impulsar la seguridad energética a través de renovables— está "
            "dando sus frutos frente a las tensiones globales en los mercados de energía."
        ),
        "fuente_label": "CNN en Español — Fortaleza energética China: resistir crisis petrolera",
        "fuente_url": "http://cnnespanol.cnn.com/2026/04/21/ciencia/fortaleza-energetica-china-resistir-crisis-petrolera-trax",
    },
    {
        "emoji": "🌐",
        "titulo": "Semana de grandes hitos: robots, VE y DeepSeek protagonizan siete días históricos",
        "cuerpo": (
            "Global Times resume la semana del 21 al 27 de abril como 'un período de grandes saltos "
            "tecnológicos': robots humanoides corriendo medias maratones y dominando el mercado global, "
            "exportaciones de vehículos eléctricos en máximos históricos (+140% interanual en marzo), "
            "el lanzamiento de DeepSeek V4 como el mayor modelo open-weight del mundo, y Xpeng "
            "anunciando coches voladores y robots humanoides en producción masiva antes de 2027. "
            "Además, en el Foro Zhongguancun 2026, la Academia China de Ciencias presentó avances "
            "en el procesador RISC-V Xiangshan y el sistema operativo Ruyi, el primero nativo compatible "
            "con el estándar internacional RVA23 de alto rendimiento."
        ),
        "fuente_label": "Global Times — A week of breakthroughs highlights China's tech advances",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359843.shtml",
    },
]


def build_blocks():
    today = date.today().strftime("%d de abril de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Semana del 21 al 27 de abril de 2026 · DeepSeek V4, Stanford HAI, Xpeng Auto China, robots humanoides y mas.", bold=False),
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
    title = "China Al Dia — Semana 21-27 Abril 2026"
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
