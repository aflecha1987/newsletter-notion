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
        "emoji": "⚛️",
        "titulo": "Jiuzhang 4.0: China establece un nuevo récord mundial en computación cuántica",
        "cuerpo": (
            "El 14 de mayo, científicos de la Universidad de Ciencia y Tecnología de China (USTC) publicaron "
            "en la revista Nature el desarrollo de Jiuzhang 4.0, que resuelve el problema de muestreo Gaussian "
            "Boson a una velocidad 10⁵⁴ veces superior a la del superordenador más potente del mundo. Su "
            "muestra de datos más compleja tarda apenas 25 microsegundos —menos que un parpadeo—, mientras "
            "que El Capitan necesitaría más de 10⁴² años para alcanzar el mismo resultado. El equipo "
            "manipuló estados cuánticos de hasta 3.050 fotones, un salto enorme frente a los 255 fotones "
            "de Jiuzhang 3.0. En paralelo, Pekín fundó el Instituto de Sichuan para la industrialización "
            "de la computación cuántica, señalando que el siguiente paso es convertir esta ciencia en "
            "productos reales de mercado."
        ),
        "fuente_label": "CGTN — Jiuzhang 4.0 sets world record",
        "fuente_url": "https://news.cgtn.com/news/2026-05-14/China-s-new-quantum-computing-prototype-Jiuzhang-4-0-sets-world-record-1N98LbBWTao/p.html",
    },
    {
        "emoji": "🤝",
        "titulo": "Cumbre Trump-Xi en Pekín: acuerdos históricos y apertura de mercados",
        "cuerpo": (
            "Del 13 al 15 de mayo, Donald Trump visitó Pekín en una cumbre histórica entre las dos mayores "
            "economías del mundo. Xi Jinping se comprometió a comprar 200 aviones Boeing, productos agrícolas "
            "por al menos 17.000 millones de dólares anuales durante 2026-2028, además de petróleo y soja "
            "estadounidenses. Xi se reunió también con los CEO tecnológicos que acompañaron a Trump —Elon Musk, "
            "Jensen Huang y Tim Cook— transmitiéndoles que China seguirá abriéndose al mundo de los negocios. "
            "Trump invitó a Xi a visitar EE.UU. en septiembre, apuntando a una consolidación del deshielo "
            "entre ambas potencias con impacto positivo en los mercados globales."
        ),
        "fuente_label": "CNBC — Xi tells Musk, Tim Cook and other CEOs: China will open wider",
        "fuente_url": "https://www.cnbc.com/2026/05/14/xi-china-open-us-business-ai-chips.html",
    },
    {
        "emoji": "💨",
        "titulo": "China enciende la turbina eólica marina más grande del mundo: 20 MW, 242 metros de altura",
        "cuerpo": (
            "El 16 de mayo, Mingyang Smart Energy activó en el Mar de China Meridional la turbina eólica "
            "marina más potente del mundo: 20 megavatios de capacidad, 242 metros de altura y palas de "
            "128 metros de longitud que barren un área equivalente a más de dos campos de fútbol. La "
            "instalación puede resistir vendavales de hasta 79,8 m/s y abastecerá a unos 96.000 hogares "
            "al año. Los científicos detectaron además que la turbina genera alteraciones microclimáticas "
            "en su entorno inmediato, un fenómeno novedoso que se encuentra bajo estudio. China lidera ya "
            "la instalación de energía eólica marina a nivel mundial, con planes de triplicar su capacidad "
            "instalada antes de 2030."
        ),
        "fuente_label": "Canal 26 — China activa la turbina eólica marina más grande del mundo",
        "fuente_url": "https://www.canal26.com/internacionales/2026/05/16/energia-renovable-a-gran-escala-china-activa-la-turbina-eolica-marina-mas-grande-del-mundo-capaz-de-abastecer-a-96000-hogares/",
    },
    {
        "emoji": "☀️",
        "titulo": "China inaugura la mayor granja solar marina del planeta",
        "cuerpo": (
            "El 17 de mayo, China inauguró la mayor planta fotovoltaica marina jamás construida: 2,3 millones "
            "de paneles solares instalados sobre el océano, en 2.934 plataformas de acero ancladas con "
            "11.736 pilotes al lecho marino. La infraestructura combina la generación de energía limpia con "
            "la acuicultura, aprovechando el espacio marítimo de forma eficiente, y puede resistir tifones, "
            "oleaje extremo y formación de hielo marino. En una sola semana, China ha activado así los dos "
            "proyectos de energía marina más grandes del mundo, confirmando su dominio absoluto en la "
            "transición energética global."
        ),
        "fuente_label": "Chicanoticias — China inaugura gigantesca granja solar marina",
        "fuente_url": "https://www.chicanoticias.com/2026/05/17/china-granja-solar/",
    },
    {
        "emoji": "🤖",
        "titulo": "China convierte los robots con IA en núcleo de su estrategia nacional",
        "cuerpo": (
            "Según el informe de mayo de la Federación Internacional de Robótica (IFR), China ha colocado "
            "oficialmente los robots impulsados por IA en el centro de su estrategia industrial nacional "
            "dentro del XV Plan Quinquenal. El país cuenta con un stock operativo de 2 millones de robots "
            "industriales —4,5 veces más que Japón— y representa el 54% de las instalaciones globales anuales. "
            "La nueva estrategia apunta a robots con inteligencia incorporada que trabajen junto a humanos "
            "en fábricas, hospitales y servicios para personas mayores. China domina el mercado emergente "
            "de humanoides, con startups que ya firman contratos reales mientras sus rivales estadounidenses "
            "siguen en fase de I+D."
        ),
        "fuente_label": "IFR — China Makes AI-powered Robots Core of National Strategy",
        "fuente_url": "https://ifr.org/ifr-press-releases/news/china-makes-ai-powered-robots-core-of-national-strategy",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 lista para lanzamiento: China buscará agua en el polo sur lunar",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 han llegado a la Base Espacial de Wenchang para iniciar "
            "las pruebas previas al lanzamiento, previsto para agosto de 2026. La misión incluye un orbitador, "
            "un módulo de aterrizaje, un rover y una sonda mini-saltadora diseñada para explorar cráteres en "
            "sombra permanente del polo sur lunar, donde se sospecha la existencia de agua en forma de hielo. "
            "En paralelo, la sonda Tianwen-2 llega a su asteroide en julio de 2026, y la CNSA planifica las "
            "misiones tripuladas Shenzhou-23 y ensayos del cohete reutilizable Larga Marcha 10, pieza clave "
            "del programa lunar tripulado antes de 2030."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🚌",
        "titulo": "BYD lleva 121 autobuses eléctricos a Sudamérica: la primera ciudad 100% eléctrica",
        "cuerpo": (
            "BYD enviará 121 autobuses eléctricos que convertirán a una ciudad sudamericana en la primera de "
            "la región con transporte público 100% eléctrico. La compañía, mayor fabricante mundial de "
            "vehículos de nuevas energías, apunta a 1,3 millones de ventas en el exterior en 2026 (+15% "
            "respecto a su objetivo anterior), con fábricas ya operativas en Brasil, México y Europa. Al "
            "cierre de marzo de 2026, China contaba con 21,48 millones de puntos de recarga para VE "
            "(+46,9% interanual), frente a 1,17 millones en Europa, consolidando la mayor infraestructura "
            "de movilidad eléctrica del mundo."
        ),
        "fuente_label": "El Cronista — China enviará 121 colectivos eléctricos a Sudamérica",
        "fuente_url": "https://www.cronista.com/informacion-gral/china-enviara-121-colectivos-electricos-y-convertira-a-esta-ciudad-latinoamericana-en-la-primera-con-transporte-100-electrico-de-sudamerica/",
    },
    {
        "emoji": "📈",
        "titulo": "La inversión digital empresarial en China crece un 10,8% y lidera el mundo en IA",
        "cuerpo": (
            "Las empresas chinas aceleraron su transformación digital: el gasto en tecnología digital creció "
            "un 10,8% interanual en los primeros dos meses de 2026. La manufactura de alta tecnología avanzó "
            "un 12,5% en el primer trimestre, con robots industriales disparándose un 33% y circuitos "
            "integrados un 24%. China cuenta ya con 602 millones de usuarios de IA generativa —más de la "
            "mitad del total mundial— y las patentes relacionadas con IA crecieron un 31,2% interanual en "
            "Q1 2026. El PIB creció un 5% interanual en el primer trimestre, superando las previsiones, "
            "con el comercio exterior avanzando un 15% en el mismo período."
        ),
        "fuente_label": "Xinhua — Innovación tecnológica gana impulso en China",
        "fuente_url": "https://spanish.news.cn/20260312/609871a2816b42efaf0f7d9ac3b5ff7a/c.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "XV Plan Quinquenal (2026-2030): IA, 6G, robots y biotech como pilares del futuro chino",
        "cuerpo": (
            "El nuevo plan quinquenal sitúa las Nuevas Fuerzas Productivas de Calidad en el núcleo del "
            "modelo de desarrollo chino. Metas clave: IA Plus (integrar la IA en el 70% de la economía "
            "para 2027 y el 90% para 2030), 6G (investigación activa y 500.000 nuevas estaciones 5G-A), "
            "robótica e industrias emergentes que suman 6 billones de yuanes y apuntan a 10 billones en "
            "2030. El presupuesto en Ciencia y Tecnología crece un 7,1% hasta 1,3 billones de yuanes, y "
            "se invertirá 1 billón de yuanes anuales en la red eléctrica para duplicar la energía no fósil "
            "de cara a 2035. China no solo quiere liderar estas tecnologías: quiere que sean el motor de su "
            "desarrollo económico para las próximas dos décadas."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · Semana 13-19 mayo 2026 · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: computacion cuantica, diplomacia, energia renovable, robotica, espacio y economia.", bold=False),
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
    title = "China Al Dia — Semana 13-19 Mayo 2026"
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
