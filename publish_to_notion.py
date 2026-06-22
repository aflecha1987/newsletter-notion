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
        "titulo": "Robots humanoides en fábricas reales: China lanza programa nacional de despliegue industrial",
        "cuerpo": (
            "El Gobierno chino ha puesto en marcha un programa nacional para acelerar la integración de robots "
            "humanoides e inteligencia artificial encarnada en industrias reales, con un calendario de obligado "
            "cumplimiento: los gobiernos locales y empresas estatales deben presentar sus planes de implementación "
            "antes de que termine junio y reportar avances en noviembre. Una fábrica de robots inaugurada en Pekín "
            "a finales de abril ya ha entregado 300 unidades a clientes reales en pocas semanas, con el objetivo "
            "de producir 10.000 unidades para finales de 2026 y medio millón anuales para 2030. Cada robot sale "
            "de la línea aproximadamente cada 30 minutos —un 50% más rápido que los métodos tradicionales—. "
            "El despliegue abarca manufactura, logística, retail, sanidad, inspección industrial y emergencias."
        ),
        "fuente_label": "SCMP — China fast tracks humanoid robots and embodied AI into industry",
        "fuente_url": "https://www.scmp.com/economy/china-economy/article/3356629/china-fast-tracks-humanoid-robots-and-embodied-ai-industry-under-nationwide-programme",
    },
    {
        "emoji": "💰",
        "titulo": "China invertirá $295.000 millones en centros de datos de IA en todo el país",
        "cuerpo": (
            "China prepara un despliegue masivo de infraestructura de inteligencia artificial: un plan de "
            "2 billones de yuanes (aproximadamente 295.000 millones de dólares) a cinco años para construir "
            "centros de datos de IA a escala nacional. El plan exige que al menos el 80% de la tecnología "
            "—incluyendo chips de IA— provenga de proveedores nacionales como Huawei, marginando de facto "
            "a Nvidia. El objetivo es propulsar el sector de IA chino y superar a Estados Unidos en capacidad "
            "computacional. Es la mayor apuesta de infraestructura tecnológica anunciada por un gobierno en "
            "la historia reciente."
        ),
        "fuente_label": "Bloomberg — China Plans $295 Billion Investment to Build Nationwide AI Data Centers",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4 y Huawei: el chip Ascend 950 valida su primer modelo de IA de frontera",
        "cuerpo": (
            "DeepSeek, la startup china que sacudió Silicon Valley con sus modelos de bajo coste, lanzó "
            "un avance de su nuevo modelo V4 optimizado específicamente para los chips Ascend 950 de Huawei, "
            "marcando un hito: es la primera vez que un modelo de IA de nivel de frontera valida los chips "
            "nacionales chinos a escala. La respuesta del mercado fue inmediata: ByteDance, Tencent y Alibaba "
            "se lanzaron a realizar nuevos pedidos de chips Ascend 950 a Huawei. Este momento representa un "
            "punto de inflexión en la independencia tecnológica de China, con el ecosistema de IA chino "
            "funcionando plenamente sobre hardware nacional."
        ),
        "fuente_label": "Capacity Global — DeepSeek V4 triggers scramble for Huawei AI chips",
        "fuente_url": "https://capacityglobal.com/news/deepseek-v4-triggers-scramble/",
    },
    {
        "emoji": "📡",
        "titulo": "Plan IA+ telecomunicaciones 2026-2028: redes autónomas e inteligentes en tres años",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de la Información publicó en junio un plan trienal para "
            "integrar la inteligencia artificial en las redes de comunicación del país. Las metas incluyen: "
            "redes de telecomunicaciones con autonomía inteligente de alto nivel para 2028, más de 30 casos "
            "de uso de alto valor, y cobertura de al menos el 75% de las áreas metropolitanas con acceso a "
            "potencia computacional con latencia inferior a un milisegundo. China quiere que su red sea la "
            "más inteligente y autónoma del mundo antes de que acabe la década."
        ),
        "fuente_label": "Gobierno de China — Plan IA integración telecomunicaciones",
        "fuente_url": "https://english.www.gov.cn/news/202606/10/content_WS6a296017c6d00ca5f9a0b876.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Tianwen-2 llega al asteroide Kamoʻoalewa: China, a punto de su primer muestreo asteroidal",
        "cuerpo": (
            "La sonda Tianwen-2 de la Agencia Espacial Nacional China (CNSA) llegó al asteroide 469219 "
            "Kamoʻoalewa el 7 de junio, un objeto de entre 40 y 100 metros de diámetro que es una de las "
            "siete cuasi-lunas conocidas de la Tierra. El descenso para recoger muestras de la superficie "
            "está previsto para el 4 de julio, empleando una técnica de perforación nunca antes usada en "
            "misiones espaciales. Las muestras regresarán a la Tierra en 2027. Tras esta misión, Tianwen-2 "
            "pondrá rumbo al cometa de cinturón principal 311P/PanSTARRS, al que llegará en enero de 2035. "
            "Es la primera misión de retorno de muestras asteroidal de China, y solo la tercera de la historia."
        ),
        "fuente_label": "Scientific American — China's Tianwen-2 spacecraft arrives at Earth's quasi-moon",
        "fuente_url": "https://www.scientificamerican.com/article/chinas-tianwen-2-spacecraft-arrives-at-one-of-earths-mysterious-quasi-moons/",
    },
    {
        "emoji": "⚡",
        "titulo": "Solar y eólica superan al carbón en capacidad instalada: un hito histórico para China",
        "cuerpo": (
            "Por primera vez en la historia, la energía solar y eólica combinadas han superado al carbón "
            "en capacidad instalada en China. A febrero de 2026, China contaba con 1,23 teravatios (TW) "
            "de capacidad solar y 650 GW de capacidad eólica, que juntas representan casi la mitad de la "
            "capacidad eléctrica total del país. En el primer semestre de 2026, las nuevas instalaciones "
            "solares crecieron un 107,1% interanual hasta los 210 GW, y las eólicas un 98,9% hasta los "
            "50 GW. China acumula ya cerca del 30% de la capacidad eléctrica mundial total, que roza los "
            "4.000 millones de kilovatios."
        ),
        "fuente_label": "Mercom India — China Installed 1.2 TW of Solar, 650 GW of Wind Capacity",
        "fuente_url": "https://www.mercomindia.com/china-installed-1-2-tw-of-solar-650-gw-of-wind-capacity-as-of-february-2026",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de vehículos eléctricos chinos: casi 900.000 unidades en cuatro meses",
        "cuerpo": (
            "China exportó 278.081 vehículos eléctricos en abril de 2026, llevando el total acumulado del "
            "año a 893.852 unidades en los cuatro primeros meses, más del doble que el mismo período de 2025. "
            "Los principales destinos son Rusia, Brasil y los Emiratos Árabes Unidos, con Asia como región "
            "importadora líder (110.613 unidades), seguida de Europa (83.813) y América Latina (52.897). "
            "La intensa competencia en el mercado doméstico ha convertido la exportación en el motor de "
            "crecimiento prioritario para BYD, Geely y los grandes fabricantes chinos de nueva energía."
        ),
        "fuente_label": "Al Jazeera — China's EV exports surge 40 percent in April",
        "fuente_url": "https://www.aljazeera.com/economy/2026/5/27/chinas-ev-exports-surge-40-percent-in-april",
    },
    {
        "emoji": "📈",
        "titulo": "Perspectivas económicas de China: exportaciones al +15% y relaciones con EE.UU. más estables",
        "cuerpo": (
            "Según el informe de perspectivas de China de BBVA Research para junio de 2026, las exportaciones "
            "chinas crecen en torno al 15% en los primeros cuatro meses del año. Unas relaciones comerciales "
            "con EE.UU. más estables tras la reciente cumbre bilateral en Pekín apoyan el panorama exterior. "
            "El Banco Popular de China mantendrá una postura de espera sin nuevas bajadas de tipos previstas "
            "para el resto del año. China mantiene su objetivo de crecimiento del PIB en el rango del "
            "4,5-5% para 2026, respaldado por una manufactura de alta tecnología que sigue acelerando y "
            "unas exportaciones con sólida tracción internacional."
        ),
        "fuente_label": "BBVA Research — China Economic Outlook June 2026",
        "fuente_url": "https://www.bbvaresearch.com/en/publicaciones/china-economic-outlook-june-2026/",
    },
    {
        "emoji": "⚓",
        "titulo": "El portaaviones Fujian completa ejercicios en el Pacífico y avanza hacia capacidad operativa plena",
        "cuerpo": (
            "El portaaviones Fujian, el más moderno y avanzado de la Armada china, regresó a su base en "
            "Qingdao el 16 de junio tras completar aproximadamente dos semanas de ejercicios en el Pacífico. "
            "El Fujian es el primer portaaviones chino equipado con un sistema de catapulta electromagnética "
            "(EMALS) de desarrollo propio, equivalente al del USS Gerald R. Ford. El proceso de adiestramiento "
            "intensivo se aceleró desde comienzos de 2026, con el objetivo declarado de alcanzar la "
            "capacidad operativa plena antes de finales de año, consolidando la proyección naval de China "
            "en el Indo-Pacífico."
        ),
        "fuente_label": "Zona Militar — El portaaviones Fujian regresa tras ejercicios en el Pacífico",
        "fuente_url": "https://www.zona-militar.com/2026/06/16/el-mas-moderno-portaaviones-de-la-armada-de-china-regreso-a-puerto-tras-completar-nuevas-ejercitaciones-en-el-pacifico/",
    },
]


def build_blocks():
    today = "22 de junio de 2026"
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
    title = "China Al Dia — Semana 16-22 Junio 2026"
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
