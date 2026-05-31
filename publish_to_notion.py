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
        "titulo": "Shenzhou-23: China lanza a su primera astronauta de Hong Kong y prepara un año en órbita",
        "cuerpo": (
            "El 24 de mayo a las 23:08 (hora de Pekín), China lanzó con éxito la misión Shenzhou-23 desde "
            "el Centro de Lanzamiento de Jiuquan, en el desierto de Gobi. La nave lleva a bordo al "
            "comandante Zhu Yangzhu, al piloto Zhang Zhiyuan y a la especialista Lai Ka-ying, quien con "
            "43 años se convirtió en la primera astronauta originaria de Hong Kong en viajar al espacio. "
            "Uno de los tripulantes permanecerá 365 días en órbita, batiendo el récord nacional de "
            "estancia continua. La misión acerca a China un paso más a su objetivo de lograr un alunizaje "
            "tripulado antes de 2030."
        ),
        "fuente_label": "Infobae — Un año en órbita: China da un paso decisivo en su programa lunar",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/24/un-ano-en-orbita-china-da-un-paso-decisivo-en-su-programa-lunar-con-el-mision-shenzhou-23/",
    },
    {
        "emoji": "💻",
        "titulo": "Huawei conquista el mercado chino de chips IA: el CEO de Nvidia admite que ha cedido ese espacio",
        "cuerpo": (
            "Jensen Huang, CEO de Nvidia, declaró esta semana que su empresa ha 'cedido en gran medida' "
            "el mercado chino de chips de IA a Huawei: 'Huawei es muy, muy fuerte. Tendrá un año "
            "extraordinario y su ecosistema local de chips lo está haciendo muy bien, porque nosotros "
            "nos hemos retirado de ese mercado'. Paralelamente, Huawei presentó su nueva técnica de "
            "fabricación 'LogicFolding', con la que proyecta alcanzar para 2031 una capacidad equivalente "
            "a un proceso de 1,4 nanómetros. El mercado chino de chips IA podría alcanzar los 67.000 "
            "millones de dólares en 2030, con empresas nacionales cubriendo el 86% de la demanda."
        ),
        "fuente_label": "CNBC — Nvidia says it has largely conceded China's AI chip market to Huawei",
        "fuente_url": "https://www.cnbc.com/2026/05/21/nvidia-jensen-huang-china-ai-chip-market-huawei.html",
    },
    {
        "emoji": "🌐",
        "titulo": "600 millones de usuarios de IA generativa y presencia china en 170 países",
        "cuerpo": (
            "China ha alcanzado los 600 millones de usuarios de IA generativa en 2026, un crecimiento del "
            "142% respecto a 2025, impulsado en buena parte por el lanzamiento de DeepSeek V4 y la "
            "adopción acelerada en ByteDance, Tencent y Alibaba. Las proveedoras chinas de nube lograron "
            "un crecimiento de triple dígito en ingresos de IA en el exterior, y las empresas chinas de IA "
            "ya tienen presencia comercial en más de 170 países y regiones, consolidando el liderazgo "
            "global de China en inteligencia artificial aplicada."
        ),
        "fuente_label": "SCMP — China takes confident strides to develop more AI innovation in 2026",
        "fuente_url": "https://www.scmp.com/tech/tech-war/article/3338528/tech-war-china-takes-confident-strides-develop-more-ai-innovation-2026",
    },
    {
        "emoji": "🤝",
        "titulo": "China invertirá 1.100 millones de dólares en Serbia: IA, robots y vehículos eléctricos",
        "cuerpo": (
            "El 27 de mayo, China anunció una inversión adicional de 1.100 millones de dólares en Serbia, "
            "destinada a proyectos de fabricación de componentes para automóviles, robots humanoides, "
            "energía e inteligencia artificial. La operación consolida la presencia china en Europa del "
            "Este como plataforma de producción y acceso al mercado europeo, en el marco de una estrategia "
            "de diversificación de su cadena de valor global."
        ),
        "fuente_label": "Bloomberg — China to Invest $1.1 Billion in Serbia in AI, Robots and Cars",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-05-27/china-to-invest-1-1-billion-in-serbia-in-ai-robots-and-cars",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD exporta más de 400.000 vehículos en abril: un récord sin precedentes",
        "cuerpo": (
            "Solo en el mes de abril de 2026, las exportaciones chinas de vehículos eléctricos e híbridos "
            "enchufables superaron las 400.000 unidades, una cifra sin precedentes en la historia de la "
            "industria. BYD lidera con un objetivo anual de 1,5 millones de exportaciones (+15%), con "
            "plantas ya operativas en Tailandia, Uzbekistán y Brasil, y su primera fábrica europea en "
            "Hungría lista para iniciar producción. La firma además presentó su apuesta por los "
            "trenes autónomos, diversificando su cartera más allá del automóvil eléctrico."
        ),
        "fuente_label": "Bloomberg Línea — BYD confía en superar su objetivo de exportaciones 2026",
        "fuente_url": "https://www.bloomberglinea.com/negocios/byd-confia-en-que-las-exportaciones-de-2026-superaran-en-un-15-su-anterior-objetivo/",
    },
    {
        "emoji": "🏙️",
        "titulo": "Plan Nacional de Renovación Urbana 2026-2030: ciudades más inteligentes y habitables",
        "cuerpo": (
            "El Consejo de Estado chino aprobó su Plan Nacional de Renovación Urbana para el período del "
            "15.º Plan Quinquenal (2026-2030), con objetivos y medidas de política para modernizar las "
            "ciudades del país. El programa prioriza la rehabilitación de barrios antiguos, la mejora de "
            "infraestructuras de servicios básicos y la integración de tecnologías inteligentes en la "
            "gestión urbana, beneficiando a cientos de millones de ciudadanos."
        ),
        "fuente_label": "CGTN — China news latest",
        "fuente_url": "https://www.cgtn.com/china",
    },
    {
        "emoji": "🌏",
        "titulo": "La 8.ª Feria de Chongqing atrae inversión europea récord y refuerza la cooperación con Latinoamérica",
        "cuerpo": (
            "Del 21 al 24 de mayo, Chongqing acogió la 8.ª Feria Internacional de China Occidental para "
            "la Inversión y el Comercio (WCIFIT), con destacada presencia de empresas de Alemania, Países "
            "Bajos, Italia y otros países europeos. Paralelamente, el 28 de mayo Tarija (Bolivia) fue sede "
            "del Foro 'Bolivia: Hacia el Mundo con China', trazando las líneas de cooperación comercial, "
            "transición energética y desarrollo logístico entre ambas naciones, reflejando el creciente "
            "vínculo entre China y América Latina."
        ),
        "fuente_label": "Xinhua — Noticias de China",
        "fuente_url": "https://spanish.xinhuanet.com/",
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
    title = "China Al Dia — Semana 25-31 Mayo 2026"
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
