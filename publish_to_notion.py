#!/usr/bin/env python3
"""
Publica la newsletter semanal de China Al Dia en Notion.
Uso: NOTION_TOKEN=<token> PARENT_PAGE_ID=<id> python publish_to_notion.py
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
        "titulo": "Kimi K3: el modelo de codigo abierto mas grande del mundo sacude Silicon Valley",
        "cuerpo": (
            "El 17 de julio, la startup Moonshot AI lanzo Kimi K3, un modelo de inteligencia artificial "
            "con 2,8 billones de parametros — el modelo de codigo abierto mas grande jamas publicado —, "
            "con rendimiento que casi iguala a OpenAI y Anthropic. Alibaba presento simultaneamente Qwen 3.8. "
            "Los mercados financieros reaccionaron: las acciones de Alibaba cayeron un 4% y los grandes "
            "tecnologicos de EE.UU. sufrieron el golpe. Los analistas apuntan que China ya no persigue a "
            "Occidente en IA, sino que en ciertos segmentos ha tomado la delantera."
        ),
        "fuente_label": "CNBC — Moonshot AI Kimi K3 rivals OpenAI, Anthropic",
        "fuente_url": "https://www.cnbc.com/2026/07/17/moonshot-ai-kimi-k3-model-openai-anthropic-china.html",
    },
    {
        "emoji": "🌐",
        "titulo": "China crea la primera organizacion mundial de IA con 29 paises: sede en Shanghai",
        "cuerpo": (
            "El 16 de julio, en la Conferencia Mundial de IA de Shanghai, representantes de 29 paises "
            "firmaron el acuerdo para crear la Organizacion Mundial de Cooperacion en Inteligencia "
            "Artificial, con sede permanente en Shanghai. China incorporo la gobernanza global de la IA "
            "como pilar del XV Plan Quinquenal (2026-2030) con una inversion de 3,93 billones de yuanes. "
            "La apuesta de Pekin es construir un orden tecnologico global alternativo al hegemonico "
            "occidental, reduciendo la brecha digital con los paises del Sur Global."
        ),
        "fuente_label": "El Imparcial — China presenta plan global de IA",
        "fuente_url": "https://www.elimparcial.com/mundo/2026/07/17/china-presenta-plan-global-de-inteligencia-artificial-para-reducir-la-brecha-digital-y-crea-con-29-paises-una-organizacion-con-sede-en-shanghai/",
    },
    {
        "emoji": "💾",
        "titulo": "CXMT: el mayor IPO chino de chips sacude los mercados globales de semiconductores",
        "cuerpo": (
            "ChangXin Memory Technologies (CXMT), el mayor fabricante chino de memoria DRAM, debuto en "
            "el Mercado STAR de Shanghai recaudando 9.800 millones de dolares, con sus acciones subiendo "
            "un 466% en el primer dia. CXMT produce en masa chips con proceso de 16 nanometros sin "
            "necesitar tecnologia EUV, y ya surte a Xiaomi, Oppo, Vivo, Lenovo, Alibaba Cloud y "
            "ByteDance. El 'efecto CXMT' golpeo las acciones de Micron, SK Hynix y Nvidia: China esta "
            "reconstruyendo su cadena tecnologica completa de semiconductores."
        ),
        "fuente_label": "SCMP — The CXMT shock",
        "fuente_url": "https://www.scmp.com/business/china-business/article/3362256/cxmt-shock-how-chinas-viable-alternatives-punch-nvidia-micron-sk-hynix-shares",
    },
    {
        "emoji": "🦾",
        "titulo": "BYD presenta su primer robot humanoide: el gigante del EV entra en la robotica",
        "cuerpo": (
            "BYD, el mayor fabricante de vehiculos electricos del mundo, presento su primer robot "
            "humanoide en sus centros Di Space a principios de agosto, capaz de interactuar con visitantes "
            "de forma autonoma. En paralelo, XPeng comenzo la produccion en serie de su robot IRON, "
            "con meta de mas de 1.000 unidades al mes para finales de 2026. Los fabricantes chinos de "
            "EVs aprovechan el 70% de solapamiento tecnologico entre vehiculos inteligentes y robots "
            "humanoides para crear una segunda linea de crecimiento."
        ),
        "fuente_label": "SCMP — BYD debut first humanoid robots August",
        "fuente_url": "https://www.scmp.com/business/china-business/article/3362362/byd-debut-first-humanoid-robots-august-rivalry-tesla-intensifies",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD y Huawei se alian en conduccion autonoma: el Bao 8 lidera la fusion EV-Tech",
        "cuerpo": (
            "BYD firmo un acuerdo con Huawei para integrar el sistema de conduccion autonoma Qiankun "
            "de la empresa tecnologica en sus SUVs todoterreno Fangchengbao. El Bao 8 sera el primer "
            "modelo BYD con tecnologia Huawei incorporada. La alianza entre el mayor fabricante chino "
            "de coches electricos y el gigante tecnologico marca una nueva fase en la integracion de "
            "la industria automovilistica y tecnologica en China."
        ),
        "fuente_label": "Yahoo Tech — China's BYD and Huawei autonomous driving",
        "fuente_url": "https://tech.yahoo.com/transportation/articles/chinas-byd-huaweis-advanced-autonomous-034303960.html",
    },
    {
        "emoji": "⚡",
        "titulo": "Hito historico: las renovables superan el 40% de la electricidad china por primera vez",
        "cuerpo": (
            "En el primer semestre de 2026, las energias renovables representaron el 41,2% de la "
            "generacion electrica total de China — superando el 40% por primera vez en la historia — "
            "mientras que el carbon cayo por debajo del 50%, otro hito sin precedentes. La capacidad "
            "instalada de eolica y solar crecio un 16,8% interanual, con generacion combinada de mas "
            "de 1,2 billones de kWh. Una startup de Shanghai tambien anuncio un avance en la produccion "
            "de combustibles de aviacion sostenibles a partir de CO2 e hidrogeno verde."
        ),
        "fuente_label": "Global Times — China renewables top 40%, coal falls below 50%",
        "fuente_url": "https://www.globaltimes.cn/page/202607/1367207.shtml",
    },
    {
        "emoji": "📈",
        "titulo": "La IA como nuevo motor economico: PIB Q2 crece 4,3% impulsado por high-tech",
        "cuerpo": (
            "La economia china crecio un 4,3% interanual en el segundo trimestre de 2026, con la "
            "electronica e informatica aportando mas de la mitad de la expansion trimestral. Hefei, "
            "corazon de la industria china de chips de memoria, trabaja a plena capacidad para abastecer "
            "la demanda global de hardware de IA. El PMI Compuesto subio a su maximo de 3 meses en "
            "julio. CGTN califico la innovacion como el principal motor de crecimiento del primer "
            "semestre de 2026."
        ),
        "fuente_label": "CGTN — Innovation seen as key growth engine H1 2026",
        "fuente_url": "https://news.cgtn.com/news/2026-07-30/VHJhbnNjcmlwdDkxNzQw/index.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e 7 lista para agosto: China busca agua en el polo sur de la Luna",
        "cuerpo": (
            "Todos los modulos de la mision Chang'e 7 llegaron a la Base Espacial de Wenchang listos "
            "para el lanzamiento previsto en agosto de 2026. La mision incluye un orbitador, lander, "
            "rover y una sonda mini-saltadora disenada para explorar crateres en sombra permanente del "
            "polo sur lunar en busca de hielo de agua. China se consolida como el principal rival de "
            "EE.UU. en el liderazgo de la exploracion espacial global, con misiones como Tianwen-2 "
            "(asteroide) y Shenzhou-23 (tripulada) tambien en marcha."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🚄",
        "titulo": "China supera los 50.000 km de alta velocidad ferroviaria: la red mas extensa del mundo",
        "cuerpo": (
            "La red ferroviaria de alta velocidad china supero los 50.000 kilometros en operacion, "
            "consolidandola como la mas extensa del planeta. Se inauguro la Estacion de Chongqing Este, "
            "la terminal ferroviaria de alta velocidad mas grande del mundo (1,22 millones de m2). "
            "El nuevo prototipo CR450, el tren comercial mas rapido sobre rieles, podria iniciar "
            "operaciones a finales de 2026. China tambien avanza en un tren submarino a traves del "
            "Mar de Bohai a 250 km/h."
        ),
        "fuente_label": "Excelsior — China supera los 50 mil km de trenes de alta velocidad",
        "fuente_url": "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico",
    },
]


def build_blocks():
    blocks = [
        callout("Newsletter semanal · China Al Dia · Semana del 28 jul - 3 ago 2026", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio e infraestructura.", bold=False),
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
    title = "China Al Dia — Semana 28 Jul - 3 Ago 2026"
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
