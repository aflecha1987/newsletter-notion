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
    """sources: list of (label, url)"""
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
    # --- PORTADA ---
    {
        "seccion": "PORTADA DE LA SEMANA",
        "emoji": "🏗️",
        "titulo": "China anuncia una inversión histórica de 295.000 millones de dólares en centros de datos de IA",
        "cuerpo": (
            "El 9 de junio, Bloomberg reveló que China prepara un plan de 2 billones de yuanes "
            "(~295.000 millones de dólares) para construir en los próximos cinco años una red nacional "
            "interconectada de centros de datos de IA. El proyecto, coordinado por la Comisión Nacional "
            "de Desarrollo y Reforma, convertirá a China Mobile y China Telecom en los grandes operadores "
            "de la infraestructura. Al menos el 80% de la tecnología (chips de IA incluidos) será de "
            "fabricantes nacionales, con Huawei como proveedor principal. Cuando se sumen las mejoras "
            "en la red eléctrica, el coste total podría alcanzar los 5 billones de yuanes. El objetivo: "
            "que para 2028 todos los centros de datos del país queden integrados en un único sistema coherente."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout"),
            ("Tech Startups", "https://techstartups.com/2026/06/09/china-unveils-295-billion-plan-to-build-a-nationwide-ai-data-center-network-and-reduce-reliance-on-u-s-chips/"),
            ("China Money Network", "https://www.chinamoneynetwork.com/2026/06/09/china-to-invest-295-billion-in-nationwide-data-center-expansion"),
        ],
    },
    # --- TECNOLOGÍA ---
    {
        "seccion": "TECNOLOGÍA E INTELIGENCIA ARTIFICIAL",
        "emoji": "🤖",
        "titulo": "La industria de robots humanoides china pasa del escaparate al mercado real",
        "cuerpo": (
            "El sector chino de robots humanoides ha dejado atrás la fase de demostración tecnológica para "
            "entrar de lleno en la comercialización real. La startup Robotera captó más de 200 millones de "
            "dólares liderados por SF Group y comenzó entregas de miles de unidades en el Q2 2026, con un "
            "crecimiento superior al 300%. Sus robots ya operan en más de 10 centros logísticos de China Post "
            "y SF Group, además de expandirse a automoción y electrónica. Vbot captó 73 millones de dólares "
            "en ronda Pre-A para aumentar su capacidad a más de 2.500 unidades mensuales en junio. "
            "Las expediciones domésticas de humanoides en China pasaron de 18.000 unidades en 2025 a "
            "una proyección de 62.500 unidades en 2026."
        ),
        "fuentes": [
            ("Global Times", "https://www.globaltimes.cn/page/202606/1362565.shtml"),
            ("The AI Insider – Robotera", "https://theaiinsider.tech/2026/05/08/chinas-humanoid-robot-maker-robotera-raises-over-usd-200m-in-new-funding-round/"),
            ("The AI Insider – Vbot", "https://theaiinsider.tech/2026/05/11/report-chinese-humanoid-robot-startup-vbot-raises-usd-73m-in-pre-a-funding/"),
        ],
    },
    {
        "seccion": None,
        "emoji": "📈",
        "titulo": "Unitree Robotics sale a bolsa: Nvidia se alía con el fabricante chino de robots",
        "cuerpo": (
            "La startup china de robótica Unitree Robotics —elegida por Nvidia para integrar su plataforma "
            "de humanoides— ha recibido luz verde de la Comisión de Cotización de la Bolsa de Shanghái para "
            "su OPV en el mercado STAR. Unitree planea captar 4.200 millones de yuanes. La alianza estratégica "
            "con Nvidia subraya que los fabricantes occidentales de IA ven en las empresas chinas de robótica "
            "socios tecnológicos de primer nivel."
        ),
        "fuentes": [
            ("CNBC", "https://www.cnbc.com/2026/06/01/nvidia-unitree-humanoid-robotics-system-researchers.html"),
        ],
    },
    {
        "seccion": None,
        "emoji": "🛰️",
        "titulo": "China lanza un instituto de computación espacial basada en IA",
        "cuerpo": (
            "Pekín ha creado un instituto estatal de investigación centrado en el cómputo de inteligencia "
            "artificial desde el espacio, integrando satélites de bajo consumo con modelos de IA ligeros. "
            "La iniciativa apunta a extender la infraestructura de computación china más allá de la Tierra, "
            "dotando a los satélites de capacidad de procesamiento en órbita para aplicaciones críticas "
            "—observación de la Tierra, telecomunicaciones y defensa— sin depender de centros de datos terrestres."
        ),
        "fuentes": [
            ("ChinaTechNews", "https://www.chinatechnews.com/2026/06/05/123104-china-launches-space-computing-hub-as-spacex-gears-up-for-historic-ipo"),
        ],
    },
    # --- ECONOMÍA ---
    {
        "seccion": "ECONOMÍA",
        "emoji": "💰",
        "titulo": "Las startups chinas captaron el 60% de la financiación asiática en el Q1 2026",
        "cuerpo": (
            "Las empresas emergentes con sede en China atrajeron 16.500 millones de dólares en el primer "
            "trimestre de 2026, representando el 60% de toda la inversión de riesgo asiática del período. "
            "Los sectores más activos fueron IA aplicada, robótica, semiconductores, tecnología industrial, "
            "hardware inteligente y software empresarial. La cifra consolida a China como el ecosistema de "
            "startups más dinámico de Asia y uno de los más activos del mundo."
        ),
        "fuentes": [
            ("Mean.CEO Blog", "https://blog.mean.ceo/startups-china-news-june-2026/"),
        ],
    },
    {
        "seccion": None,
        "emoji": "🚗",
        "titulo": "BYD bate su propio récord de exportaciones: 160.644 unidades en mayo (+80%)",
        "cuerpo": (
            "BYD cerró mayo de 2026 con 160.644 unidades exportadas, un incremento del 80,4% interanual "
            "y el mejor mes de su historia en ventas internacionales. En total, China vendió 377.000 "
            "vehículos eléctricos e híbridos en el extranjero durante mayo. BYD apunta a 1,3 millones "
            "de exportaciones en 2026 (+24% frente a 2025). La compañía está redirigiendo su expansión "
            "hacia el Sudeste Asiático, América Latina y Oriente Medio, mercados con menor presión "
            "arancelaria y alta demanda de electromovilidad asequible."
        ),
        "fuentes": [
            ("Global China EV", "https://www.globalchinaev.com/post/byd-leads-chinas-record-may-nev-month-with-377000-units-and-surging-exports"),
            ("CnEVPost", "https://cnevpost.com/2026/06/01/byd-may-2026-sales/"),
            ("IEA Global EV Outlook 2026", "https://www.iea.org/reports/global-ev-outlook-2026/manufacturing-and-trade"),
        ],
    },
    # --- ENERGÍA ---
    {
        "seccion": "ENERGÍA LIMPIA",
        "emoji": "⚡",
        "titulo": "Las energías solar y eólica superan el 52% de la capacidad eléctrica de China",
        "cuerpo": (
            "A cierre de febrero de 2026, la capacidad instalada de electricidad limpia en China alcanzó "
            "el 52% del total, superando por primera vez la capacidad fósil. En el primer semestre de 2026, "
            "las nuevas instalaciones solares crecieron un 107% interanual hasta 210 millones de kW, y las "
            "eólicas un 99% hasta 50 millones de kW. En 2024, China aportó el 31% de toda la inversión "
            "mundial en renovables (625.000 millones de dólares) e instaló más turbinas eólicas y paneles "
            "solares que el resto del mundo juntos."
        ),
        "fuentes": [
            ("Ember Energy", "https://ember-energy.org/latest-updates/wind-and-solar-generate-over-a-quarter-of-chinas-electricity-for-the-first-month-on-record/"),
            ("Sustainability Times", "https://www.sustainability-times.com/energy/china-shatters-global-energy-records-historic-surge-in-solar-and-wind-power-redefines-the-future-of-clean-electricity/"),
            ("Carbon Brief", "https://www.carbonbrief.org/china-briefing-5-february-2026-clean-energys-share-of-economy-record-renewables-thawing-relations-with-uk/"),
        ],
    },
    # --- ESPACIO ---
    {
        "seccion": "ESPACIO",
        "emoji": "🚀",
        "titulo": "Chang'e-7 en rampa de lanzamiento: exploradores de agua lunar para agosto de 2026",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 han llegado al cosmódromo de Wenchang para las "
            "pruebas previas al despegue, previsto para agosto de 2026. La misión —compuesta por "
            "orbitador, módulo de aterrizaje, rover y una sonda mini-saltadora— explorará el polo "
            "sur lunar en busca de hielo de agua en cráteres de sombra permanente que no han visto "
            "la luz solar en miles de millones de años. Lleva 21 cargas científicas, entre ellas "
            "6 internacionales (Italia, Rusia, Hawái). Es el paso previo a Chang'e-8 (2028), que "
            "probará el uso de recursos lunares in situ, clave para la base lunar tripulada antes de 2030."
        ),
        "fuentes": [
            ("SpaceNews", "https://spacenews.com/chinas-change-7-arrives-at-spaceport-for-lunar-south-pole-exploration-mission/"),
            ("Space.com", "https://www.space.com/astronomy/moon/chinas-next-moonshot-change-could-search-the-lunar-south-pole-for-water-this-year"),
            ("Planetary.org", "https://www.planetary.org/space-missions/change-7"),
        ],
    },
    # --- DIPLOMACIA ---
    {
        "seccion": "DIPLOMACIA Y COMERCIO",
        "emoji": "🌏",
        "titulo": "Shenzhen se prepara para la cumbre APEC de noviembre: tecnología y libre comercio",
        "cuerpo": (
            "China acogerá la cumbre del APEC el 18-19 de noviembre en Shenzhen, la tercera vez que "
            "el país organiza el foro (tras 2001 y 2014). La ciudad —símbolo del milagro económico "
            "chino y capital de la innovación— está desplegando demostraciones de transporte autónomo, "
            "drones de pasajeros y robots humanoides en servicios públicos para recibir a los líderes "
            "de 21 economías. La agenda se centra en gobernanza de la IA para el bien común, resiliencia "
            "de las cadenas de suministro y digitalización. China presenta la cumbre como una oportunidad "
            "para reforzar el libre comercio multilateral frente al proteccionismo."
        ),
        "fuentes": [
            ("Diario Financiero", "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de"),
            ("La Jornada", "https://www.jornada.com.mx/2026/05/06/economia/017n1eco"),
            ("CNN Chile", "https://www.cnnchile.com/mundo/china-se-prepara-para-la-apec-2026-el-gigante-asiatico-apuesta-por-la-tecnologia-y-la-tradicion/"),
        ],
    },
]


def build_blocks():
    today = "10 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Día · {today} · Semana del 4 al 10 de junio de 2026", "🇨🇳"),
        p(
            "Recopilación de las noticias más relevantes de China esta semana: "
            "tecnología, economía, energía limpia, espacio y diplomacia.",
        ),
        divider(),
    ]

    current_section = None
    for n in NOTICIAS:
        if n["seccion"] and n["seccion"] != current_section:
            current_section = n["seccion"]
            blocks.append(h1(current_section))

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
    title = "China Al Día — Semana 4-10 Junio 2026"
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
