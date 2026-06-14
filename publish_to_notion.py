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
        "emoji": "📈",
        "titulo": "Exportaciones chinas de mayo se disparan un 19,4%: muy por encima de lo esperado",
        "cuerpo": (
            "El 9 de junio, las autoridades chinas publicaron los datos de comercio exterior de mayo de 2026: "
            "las exportaciones crecieron un 19,4% interanual, muy por encima de la previsión del 15% de los "
            "analistas. El total de importaciones y exportaciones en los primeros cinco meses del año alcanzó "
            "los 20,68 billones de yuanes (≈2,86 billones de dólares), un alza del 15,3%. El motor del "
            "crecimiento: tecnología de alto valor añadido y la explosión global de la demanda de productos "
            "relacionados con la IA, donde China domina la cadena de suministro."
        ),
        "fuente_label": "La Jornada — China: exportaciones escalaron 19,4% en mayo",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/06/09/economia/-china-anuncia-que-sus-exportaciones-escalaron-194-en-mayo-por-encima-de-lo-esperado",
    },
    {
        "emoji": "🤖",
        "titulo": "China lanza robots humanoides domésticos: lavan ropa, tienden camas y cuidan ancianos",
        "cuerpo": (
            "GigaAI, startup china de robótica, presentó el primer robot humanoide de uso general doméstico "
            "del país. Capaz de lavar ropa, tender camas, servir comida y asistir a personas mayores, el "
            "robot responde a los patrones de un envejecimiento demográfico acelerado que convierte al cuidado "
            "del hogar en un mercado estratégico. El Ministerio de Industria y Tecnología de la Información "
            "ha designado a los robots humanoides como industria estratégica emergente, con Shenzhen y "
            "Guangzhou como centros de fabricación. En 2026, los envíos globales de humanoides alcanzarán "
            "35.000 unidades, un incremento del 94% interanual."
        ),
        "fuente_label": "La República — China lanza robots humanoides con IA para el hogar",
        "fuente_url": "https://larepublica.pe/ciencia/2026/05/28/china-lanza-robots-humanoides-con-inteligencia-artificial-capaces-de-lavar-ropa-tender-camas-y-cuidar-a-ancianos-579712",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek y Qwen3 reducen la brecha con los modelos de IA occidentales",
        "cuerpo": (
            "Los modelos de inteligencia artificial chinos DeepSeek V4 y Qwen3-Max-Thinking han reducido "
            "significativamente la distancia con los sistemas estadounidenses en las principales evaluaciones "
            "técnicas. Alibaba, Tencent y Baidu intensifican la competencia por usuarios con campañas "
            "agresivas. China ya cuenta con 602 millones de usuarios de IA generativa —más que ningún otro "
            "país— y las patentes relacionadas con IA crecieron un 31,2% en el primer trimestre. La cuarta "
            "revolución industrial china tiene a la IA como columna vertebral."
        ),
        "fuente_label": "La Jornada — IA impulsa la cuarta revolución industrial china",
        "fuente_url": "https://www.jornada.com.mx/2026/04/20/economia/018n1eco",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD rompe récords: exportaciones +80% en mayo, rumbo a 1,5 millones de vehículos globales",
        "cuerpo": (
            "BYD vendió 160.644 vehículos fuera de China en mayo de 2026, un aumento del 80% interanual, "
            "su mejor marca histórica. En los primeros cinco meses del año, las ventas al exterior acumulan "
            "616.907 unidades (+65% vs. 2025). La empresa confía en superar su objetivo de 1,5 millones de "
            "unidades exportadas en 2026, un 15% por encima de la meta inicial. Las exportaciones "
            "representan el 42,8% de sus ventas totales mensuales. En mayo, las exportaciones totales de "
            "automóviles chinos subieron un 73%, impulsadas por el interés global en el vehículo eléctrico "
            "ante el alza del precio del combustible."
        ),
        "fuente_label": "CleanTechnica — BYD exports rose 80% year over year in May",
        "fuente_url": "https://cleantechnica.com/2026/06/07/byd-exports-rose-80-year-over-year-in-may/",
    },
    {
        "emoji": "🛤️",
        "titulo": "La BRI se reinventa: la 'Ruta de la Seda Verde' y la 'Ruta de la Seda Digital'",
        "cuerpo": (
            "La Iniciativa Belt and Road entra en 2026 en una nueva fase de 'alta calidad'. Según el FMI, "
            "China ha pivotado hacia la Ruta de la Seda Verde (energía renovable, infraestructura sostenible) "
            "y la Ruta de la Seda Digital (redes 5G, e-commerce, plataformas digitales). Las inversiones "
            "priorizan proyectos más pequeños y técnicamente especializados: en la primera mitad de 2025 se "
            "movilizaron 66.200 millones de dólares en construcción, cifra récord. La nueva BRI conecta "
            "geografías y también estándares tecnológicos, exportando el modelo de desarrollo digital chino."
        ),
        "fuente_label": "UDLAP — BRI 2026: From Expansion to Strategic High-Quality Cooperation",
        "fuente_url": "https://observatorioglobal.udlap.mx/the-belt-and-road-initiative-in-2026-from-expansion-to-strategic-high-quality-cooperation/",
    },
    {
        "emoji": "⚡",
        "titulo": "Viento y solar generan por primera vez más del 25% de la electricidad china",
        "cuerpo": (
            "Por primera vez en la historia, las energías eólica y solar generaron más de una cuarta parte "
            "de la electricidad de China durante un mes completo. En 2025, China añadió casi 500 GW de "
            "nueva capacidad renovable —el 60% del crecimiento global—, incluyendo 370 GW de solar "
            "fotovoltaica y 117 GW de eólica (un 48% más que en 2024). Para 2026, el objetivo es añadir "
            "otros 200 GW. El país lleva acumulados más de 1.000 GW de capacidad solar instalada, una "
            "cifra que parecía imposible hace apenas una década."
        ),
        "fuente_label": "Ember Energy — Wind and solar generate over a quarter of China's electricity",
        "fuente_url": "https://ember-energy.org/latest-updates/wind-and-solar-generate-over-a-quarter-of-chinas-electricity-for-the-first-month-on-record/",
    },
    {
        "emoji": "🚀",
        "titulo": "China a la Luna en 2030: la misión Chang'e-7 y el programa lunar toman forma",
        "cuerpo": (
            "China ha anunciado oficialmente que sus astronautas pisarán la Luna antes de 2030, unificando "
            "sus programas de vuelo tripulado y exploración robótica bajo una misma estrategia. La misión "
            "Chang'e-7, prevista para 2026, llevará un orbitador, módulo de aterrizaje, rover y una sonda "
            "saltadora para buscar agua helada en el polo sur lunar. En paralelo, China y Rusia avanzan en "
            "el diseño de la Estación Internacional de Investigación Lunar, cuya segunda fase constructiva "
            "arranca en 2026. La nueva carrera espacial tiene a China como principal rival de Estados Unidos."
        ),
        "fuente_label": "Espaciotech — China en la Luna para 2030",
        "fuente_url": "https://www.espaciotech.net/2026/06/09/china-en-la-luna-para-2030-que-implica-para-el-orden-espacial-internacional-y-para-los-acuerdos-artemis/",
    },
    {
        "emoji": "🌊",
        "titulo": "El buque Meng Xiang se alista para excavar 11 km bajo el fondo del océano",
        "cuerpo": (
            "China prepara la primera gran expedición del buque de investigación oceanográfica Meng Xiang, "
            "con el objetivo de perforar hasta 11 kilómetros bajo la corteza oceánica para obtener muestras "
            "del manto terrestre. Si lo consigue, será la exploración más profunda del subsuelo oceánico "
            "jamás realizada por ningún país. Las muestras podrían revelar claves sobre la formación de la "
            "Tierra, los ciclos del carbono y la vida en entornos extremos. Una apuesta científica de largo "
            "aliento que demuestra la creciente ambición investigadora de China en los océanos del mundo."
        ),
        "fuente_label": "Wikipedia — 2026 in China",
        "fuente_url": "https://en.wikipedia.org/wiki/2026_in_China",
    },
    {
        "emoji": "🏙️",
        "titulo": "China organiza la cumbre APEC 2026 en Shenzhen: IA, comercio y cadenas de suministro",
        "cuerpo": (
            "Shenzhen, capital tecnológica de China, acogerá la cumbre del Foro de Cooperación Económica "
            "Asia-Pacífico (APEC) los días 18 y 19 de noviembre de 2026. China despliega todo su potencial "
            "tecnológico en los preparativos: demostraciones de IA, infraestructura 5G y sistemas de "
            "movilidad inteligente. La agenda gira en torno a la gobernanza de la IA para el bien común, "
            "la resiliencia de las cadenas de suministro globales frente al proteccionismo y la "
            "formalización económica mediante infraestructura digital. Una cumbre que posiciona a China "
            "como arquitecta del orden económico del Pacífico."
        ),
        "fuente_label": "Diario Financiero — China despliega potencial tecnológico para APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
]


def build_blocks():
    today = "14 de junio de 2026"
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
    title = "China Al Dia — Semana 8-14 Junio 2026"
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
