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
        "titulo": "WRC 2026: la XI Conferencia Mundial de Robots convierte Pekín en la capital global de la robótica",
        "cuerpo": (
            "La XI Conferencia Mundial de Robots (WRC 2026), celebrada en Pekín del 19 al 23 de agosto "
            "bajo el lema 'Simbiosis Humano-Robot, Convergencia Producción-Demanda', reunió a más de "
            "300 expositores con más de 3.000 productos, incluyendo más de 300 debuts mundiales. "
            "El Concurso Mundial de Robots 2026 congregó a más de 10.000 competidores de más de "
            "6.000 equipos procedentes de más de 20 países. El robot humanoide Tiangong Omni demostró "
            "en vivo su capacidad para caminar sobre postes, subir escaleras y gatear. La competición "
            "ha dejado de ser sobre cuerpos mecánicos: ahora se centra en los modelos de IA encarnada "
            "que dan vida a los robots."
        ),
        "fuente_label": "Science & Technology Daily — Robotics Wows the World at WRC 2026",
        "fuente_url": "https://www.stdaily.com/web/English/2026-08/22/content_567828.html",
    },
    {
        "emoji": "🏅",
        "titulo": "2os Juegos Mundiales de Robots Humanoides en el Estadio Olímpico de Pekín",
        "cuerpo": (
            "El 22 de agosto, el Estadio Nacional de Patinaje de Velocidad de Pekín fue escenario de "
            "la 2a edicion de los Juegos Mundiales de Robots Humanoides. Los robots de las principales "
            "companias chinas compitieron en atletismo, baloncesto, natacion y obstaculos. "
            "China consolida asi su posicion de liderazgo absoluto en la robotica humanoide: sus "
            "empresas acaparan mas del 55 % de los expositores en eventos tecnologicos internacionales, "
            "incluyendo los de EE.UU."
        ),
        "fuente_label": "Gulf News — World's first humanoid robot games begin in China",
        "fuente_url": "https://gulfnews.com/amp/story/sport/worlds-first-humanoid-robot-games-begin-in-china-1.500234339",
    },
    {
        "emoji": "🦾",
        "titulo": "UBTech produce su robot humanoide número 1.000: el Walker S2 entra en producción industrial",
        "cuerpo": (
            "La empresa china de robótica UBTech alcanzó un hito histórico al ensamblar su robot "
            "humanoide número 1.000, el Walker S2, completando la transición de la fase de demostración "
            "tecnológica a la producción industrial a gran escala. El Walker S2 se despliega en líneas "
            "de fabricación de automóviles, logística y asistencia hospitalaria. China prevé alcanzar "
            "100.000 robots humanoides desplegados para 2027, según el Plan de Acción Nacional para "
            "Robots Humanoides 2025."
        ),
        "fuente_label": "SCMP — China fast-tracks humanoid robots and embodied AI into industry",
        "fuente_url": "https://www.scmp.com/economy/china-economy/article/3356629/china-fast-tracks-humanoid-robots-and-embodied-ai-industry-under-nationwide-programme",
    },
    {
        "emoji": "🔬",
        "titulo": "China logra récord mundial de eficiencia solar con paneles de perovskita a escala industrial",
        "cuerpo": (
            "Un equipo de la Universidad de Nankín liderado por Hairen Tan, en colaboración con "
            "Renshine Solar, publicó en Nature (12 de agosto) el desarrollo de un panel de perovskita "
            "de 0,72 metros cuadrados con una eficiencia certificada del 22,0 %, récord mundial para "
            "hardware de perovskita a escala de metro. En condiciones reales, los paneles generaron "
            "un 3,42 % más de electricidad que los de silicio en marzo, un 3,79 % más en abril y "
            "un 5,81 % más en mayo. La brecha se amplía con la temperatura, lo que les da especial "
            "relevancia en climas cálidos y aplicaciones espaciales."
        ),
        "fuente_label": "Interesting Engineering — China's record perovskite solar panels outdo silicon",
        "fuente_url": "https://interestingengineering.com/energy/china-record-perovskite-solar-panels-silicon",
    },
    {
        "emoji": "🛰️",
        "titulo": "Alas solares espaciales plegables 'Nebula': el prototipo chino que cabe en un termo",
        "cuerpo": (
            "Yanhe Solar finalizó el prototipo de ingeniería de sus alas solares espaciales 'Nebula', "
            "de enrollamiento flexible, fabricadas sobre un sustrato de poliimida totalmente flexible "
            "de 0,1 mm de grosor. El diseño permite plegarlas hasta el diametro de un termo durante "
            "el lanzamiento y desplegarlas en orbita mediante un mecanismo pasivo, reduciendo el peso "
            "entre un 25 % y un 30 % respecto a las soluciones convencionales y logrando una ratio "
            "de almacenamiento de 35x. La tecnologia esta disenada para la proxima generacion de "
            "estaciones de energia solar espacial."
        ),
        "fuente_label": "TaiYang News — China Solar PV News Snippets August 2026",
        "fuente_url": "https://taiyangnews.info/markets/china-solar-pv-news-snippets-august-18-2026",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones de China en julio 2026: +23,9 % impulsadas por IA y alta tecnología",
        "cuerpo": (
            "Las exportaciones chinas de julio crecieron un 23,9 % interanual, superando las previsiones "
            "del mercado (Reuters estimaba +22,2 %), impulsadas por la demanda global de productos "
            "relacionados con la inteligencia artificial y los semiconductores. Las importaciones "
            "aumentaron un 27,5 %. En el acumulado del primer semestre (en yuanes), el comercio "
            "exterior total creció un 16,9 %, con exportaciones de 14,73 billones de yuanes (+13,4 %). "
            "El comercio con la ASEAN creció un 20 %, con la UE un 9,5 %, con América Latina un 15,4 % "
            "y con África un 18,9 %."
        ),
        "fuente_label": "CNBC — China's exports growth beats estimates in July, AI-driven shipments surge",
        "fuente_url": "https://www.cnbc.com/2026/08/07/china-july-trade-exports-imports-surplus-imbalance-tariffs-.html",
    },
    {
        "emoji": "🤝",
        "titulo": "China y Corea del Sur retoman negociaciones del TLC: 16a ronda en Pekín el 31 de agosto",
        "cuerpo": (
            "El 31 de agosto, China y Corea del Sur abrieron en Pekín la 16a ronda de negociaciones "
            "para ampliar su Tratado de Libre Comercio bilateral, extendiendo su alcance a los sectores "
            "de servicios e inversión. El acuerdo original, centrado en bienes, se firmó en 2015; "
            "esta ronda busca profundizar la integración en tecnología digital, cadenas de suministro, "
            "electromovilidad e intercambios culturales. El TLC ampliado podría convertirse en uno "
            "de los bloques comerciales más grandes de Asia."
        ),
        "fuente_label": "UPI — South Korea, China resume FTA services and investment talks in Beijing",
        "fuente_url": "https://www.upi.com/Top_News/World-News/2026/08/31/South-Korea-China-resume-FTA-services-investment-talks-in-Beijing/2661788219142/",
    },
    {
        "emoji": "💡",
        "titulo": "China acelera su plan de autosuficiencia tecnológica: IA encarnada, 6G, cuántica y fusión nuclear",
        "cuerpo": (
            "El gobierno chino reafirmó su estrategia de autosuficiencia tecnológica 2026-2030, con "
            "metas concretas en inteligencia artificial encarnada (que impulsa los robots humanoides), "
            "comunicaciones 6G, biofabricación, interfaces cerebro-computador, hidrógeno verde y "
            "energía de fusión nuclear. Según el plan, las industrias relacionadas con la IA "
            "alcanzarán más de 10 billones de yuanes de valor para 2030. China lanzará nuevos "
            "proyectos de centros de datos y coordinará la distribución de capacidad computacional "
            "a nivel nacional."
        ),
        "fuente_label": "Yahoo News — China vows to accelerate technological self-reliance, AI push",
        "fuente_url": "https://www.yahoo.com/news/articles/china-vows-accelerate-technological-self-014121650.html",
    },
    {
        "emoji": "📊",
        "titulo": "PIB de China +4,7 % en el primer semestre; manufactura de alta tecnología +13,8 %",
        "cuerpo": (
            "El PIB de China creció un 4,7 % interanual en el primer semestre de 2026, con la "
            "producción industrial aumentando un 5,3 % entre enero y julio. La manufactura de alta "
            "tecnología lideró el crecimiento con un +13,8 %, mientras que la producción de equipos "
            "avanzó un 9,7 %. La economía 'nueva' (IA, biotecnología, robótica, semiconductores, "
            "energía limpia) marca el paso, posicionando a China como el principal motor de innovación "
            "industrial del planeta."
        ),
        "fuente_label": "Mundo Ejecutivo — China 2026: alta tecnología amortigua desaceleración económica",
        "fuente_url": "https://mundoejecutivocdmx.com/tecnologia/china-alta-tecnologia-desaceleracion-economia/",
    },
    {
        "emoji": "💻",
        "titulo": "Apple evalúa integrar chips de memoria CXMT (fabricación china) en sus productos",
        "cuerpo": (
            "El 20 de agosto, el COO de Apple, Sabih Khan, declinó confirmar informes que señalaban "
            "que la compañía estaba probando chips de memoria de ChangXin Memory Technologies (CXMT), "
            "el fabricante chino de DRAM que completó su IPO por 8.600 millones de dólares en julio. "
            "Si Apple adoptara chips CXMT, supondría una validación histórica del ecosistema de "
            "semiconductores chino en el mercado premium global, en plena guerra tecnológica con "
            "Washington. Analistas señalan que los chips CXMT compiten en precio y calidad con los "
            "de Samsung y SK Hynix."
        ),
        "fuente_label": "CNBC — From Apple to Ford: How Chinese tech is becoming harder for global companies to ignore",
        "fuente_url": "https://www.cnbc.com/2026/08/14/china-tech-global-appeal-apple-ford-catl-deepseek.html",
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
    title = "China Al Dia — Semana 25 Ago - 1 Sep 2026"
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
