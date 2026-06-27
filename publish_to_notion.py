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
    """Renders multiple source links as a single paragraph block."""
    rich_text = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(sources):
        if i > 0:
            rich_text.append({"type": "text", "text": {"content": " · "}})
        rich_text.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
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
        "emoji": "🌏",
        "titulo": "'China Opportunity 2.0': Li Qiang redibuja el papel de China en la economía global",
        "cuerpo": (
            "El Premier Li Qiang abrió el 24 de junio el XVII Foro de Verano de Davos en Dalian ante "
            "más de 1.800 líderes de 90 países. Rechazó el término 'China Shock 2.0' y lo rebautizó como "
            "'China Opportunity 2.0': los avances tecnológicos chinos —desde la IA de código abierto "
            "hasta los vehículos eléctricos— no son una amenaza sino una oportunidad de crecimiento para "
            "el mundo. Li destacó que los modelos de IA de código abierto chinos han sido descargados más "
            "de 10.000 millones de veces en todo el mundo, y que instalaciones como la estación espacial "
            "Tiangong, los laboratorios de fusión nuclear y las instalaciones cuánticas están abiertas a "
            "la colaboración internacional."
        ),
        "fuentes": [
            ("CGTN", "https://news.cgtn.com/news/2026-06-24/Chinese-premier-addresses-opening-plenary-of-Summer-Davos-1Oeclq4bICQ/index.html"),
            ("Xinhua", "https://english.news.cn/20260624/36979bf7fe1f4fa5b8e38954079c0593/c.html"),
            ("WEF", "https://www.weforum.org/press/2026/06/premier-li-qiang-calls-for-collaborative-innovation-and-stability-to-strengthen-global-growth/"),
        ],
    },
    {
        "emoji": "🖥️",
        "titulo": "China invierte $295.000 millones en una red nacional de centros de datos de IA",
        "cuerpo": (
            "El gobierno chino está ultimando un plan para invertir 2 billones de yuanes (~295.000 millones "
            "de dólares) en los próximos cinco años en la construcción de una red interconectada de centros "
            "de datos de IA en todo el país. El plan, encabezado por la Comisión Nacional de Desarrollo y "
            "Reforma, exige que al menos el 80% de la tecnología (chips, servidores, redes) provenga de "
            "fabricantes nacionales como Huawei, consolidando la autosuficiencia tecnológica. La iniciativa "
            "posiciona a China para competir directamente con Estados Unidos en capacidad de cómputo para "
            "IA a escala nacional."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout"),
        ],
    },
    {
        "emoji": "🤖",
        "titulo": "8.500 robots IA tomarán las riendas de la red eléctrica china",
        "cuerpo": (
            "La Corporación Estatal de la Red Eléctrica (State Grid) ha anunciado una inversión de "
            "6.800 millones de yuanes (~1.000 millones de dólares) para adquirir 8.500 robots con "
            "inteligencia artificial en 2026, encargados de inspección y mantenimiento de la red eléctrica. "
            "El despliegue incluye ~5.000 perros robot para patrullar subestaciones y líneas en zonas "
            "montañosas, además de robots humanoides y de doble brazo para tareas de alto riesgo en líneas "
            "de ultra-alta tensión. La hoja de ruta prevé operación totalmente autónoma de la red para 2030. "
            "Empresas como Unitree Robotics, Deep Robotics y AgiBot participan en el suministro."
        ),
        "fuentes": [
            ("Interesting Engineering", "https://interestingengineering.com/ai-robotics/china-8500-robots-power-grid"),
            ("TechRadar", "https://www.techradar.com/ai-platforms-assistants/the-future-has-arrived-chinas-power-grid-will-soon-be-run-by-an-army-of-humanoid-robots-and-robot-dogs-as-state-announces-usd1-billion-investment-in-8-500-robo-helpers"),
            ("SCMP", "https://www.scmp.com/economy/china-economy/article/3351323/china-plans-invest-billions-robot-army-run-its-power-grid"),
        ],
    },
    {
        "emoji": "🎓",
        "titulo": "China elimina 12.200 carreras universitarias y las reemplaza con IA y robótica",
        "cuerpo": (
            "En la mayor reforma educativa de su historia moderna, China ha eliminado más de 12.200 "
            "programas universitarios —más del 30% del total— que considera obsoletos frente a la "
            "economía digital. En paralelo ha introducido más de 10.000 nuevas titulaciones en IA, "
            "robótica, computación avanzada, ingeniería de semiconductores y economía de baja altitud. "
            "Nueve universidades ofrecen ya grados especializados en inteligencia encarnada (embodied "
            "intelligence). Con 12,7 millones de graduados en 2026 —la mayor cohorte de la historia— "
            "el objetivo es crear una generación capaz no solo de usar la IA, sino de desarrollarla y "
            "comercializarla."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/newsletters/2026-06-22/china-s-ai-programs-for-students-eliminate-12-000-university-degrees"),
            ("Gizmodo ES", "https://es.gizmodo.com/china-aplica-una-reestructuracion-educativa-al-eliminar-12-200-carreras-universitarias-en-cinco-anos-y-reemplazarlas-con-ia-robotica-e-inteligencia-encarnada-2000242247"),
        ],
    },
    {
        "emoji": "🤝",
        "titulo": "China y EE.UU. avanzan en reducción recíproca de aranceles",
        "cuerpo": (
            "El 25 de junio, Pekín confirmó que continuarán las conversaciones con Washington en el marco "
            "del nuevo Consejo de Comercio bilateral para reducir aranceles de forma recíproca. El comercio "
            "exterior de la región Beijing-Tianjin-Hebei alcanzó los 2,09 billones de yuanes en los primeros "
            "cinco meses de 2026, con crecimiento por cinco meses consecutivos. El contexto de apertura "
            "comercial se vio reforzado en el Foro de Dalian, donde líderes empresariales globales señalaron "
            "que la estabilidad en las relaciones sino-americanas es una condición necesaria para el "
            "crecimiento económico mundial."
        ),
        "fuentes": [
            ("Xinhua", "https://english.news.cn/20260625/385dd3ae7fb948a986e75fed78d85807/c.html"),
            ("Beijing Gov", "https://english.beijing.gov.cn/latest/news/"),
        ],
    },
    {
        "emoji": "🚗",
        "titulo": "NIO ES9: 10.000 entregas en solo un mes — el SUV de lujo chino arrasa",
        "cuerpo": (
            "El 26 de junio, NIO anunció que su SUV insignia ES9 superó las 10.000 unidades entregadas "
            "en su primer mes en el mercado, un hito histórico para la marca de vehículos eléctricos de "
            "lujo. El logro refleja tanto la madurez del mercado chino de NEV (donde los vehículos de "
            "nueva energía ya suponen más del 50% de las ventas nuevas) como la creciente preferencia "
            "de los consumidores por opciones premium locales frente a marcas extranjeras. En paralelo, "
            "BYD y Xpeng han acelerado sus planes de integración de robots humanoides en sus líneas de "
            "producción, fusionando sus capacidades en VE y robótica."
        ),
        "fuentes": [
            ("CnEVPost", "https://cnevpost.com/"),
            ("SCMP EVs", "https://www.scmp.com/business/china-evs"),
            ("IEA EV Outlook 2026", "https://www.iea.org/reports/global-ev-outlook-2026/manufacturing-and-trade"),
        ],
    },
    {
        "emoji": "🌐",
        "titulo": "Davos de Verano cierra: China lidera el modelo de integración IA-trabajo del mundo",
        "cuerpo": (
            "El XVII Foro Anual de los Nuevos Campeones concluyó el 25 de junio con una declaración "
            "conjunta que convoca a gobiernos y empresas a convertir la innovación tecnológica en empleos "
            "y competitividad real. El WEF y sus socios lanzaron varias iniciativas: un blueprint para la "
            "transición hacia la IA en el trabajo, proyectos piloto de colaboración humano-IA en "
            "manufactura china, y programas de salud digital impulsados por IA. El organismo advirtió que "
            "el 40% del empleo global está expuesto a la IA y que China lidera con su iniciativa 'IA Plus' "
            "el modelo de integración productiva más avanzado del mundo."
        ),
        "fuentes": [
            ("WEF", "https://www.weforum.org/press/2026/06/summer-davos-concludes-in-dalian-with-call-to-scale-innovation-into-growth-jobs-and-competitiveness/"),
            ("CGTN", "https://news.cgtn.com/news/2026-06-26/VHJhbnNjcmlwdDkxMjY2/index.html"),
            ("Arise News", "https://www.arise.tv/wef-dalian-2026-ai-takes-center-stage-as-leaders-chart-the-future-of-work-and-innovation/"),
        ],
    },
    {
        "emoji": "⚡",
        "titulo": "La ventaja silenciosa de China en IA: energía limpia y barata en abundancia",
        "cuerpo": (
            "Un análisis publicado esta semana subraya que la principal ventaja competitiva de China "
            "en la carrera de la IA no son los chips ni los algoritmos, sino su abundante energía barata "
            "y limpia. Con la mayor capacidad instalada de solar y eólica del mundo, China construye "
            "centros de datos a un ritmo que crece al 30% anual desde 2016. Esta combinación —energía "
            "renovable masiva + autosuficiencia en hardware + talento ingenieril— convierte a China en el "
            "país con menores costes operativos para escalar modelos de IA a nivel global, cerrando "
            "rápidamente la brecha con Estados Unidos."
        ),
        "fuentes": [
            ("Al Jazeera", "https://www.aljazeera.com/economy/2026/5/28/chinas-secret-weapon-in-ai-race-with-us-lots-of-cheap-energy"),
        ],
    },
]


def build_blocks():
    today = "27 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, IA, energia y sociedad.", bold=False),
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

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Semana 21-27 junio 2026 · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 21-27 Junio 2026"
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
