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
        "titulo": "Jiuzhang 4.0: China pulveriza el récord mundial de computación cuántica",
        "cuerpo": (
            "El 13 de mayo, científicos de la Universidad de Ciencia y Tecnología de China (USTC) "
            "publicaron en la revista Nature los resultados de Jiuzhang 4.0, manipulando estados cuánticos "
            "de hasta 3.050 fotones —doce veces más que el modelo anterior— y resolviendo el problema del "
            "muestreo bosónico gaussiano a una velocidad 10⁵⁴ veces superior a la del superordenador más "
            "potente del mundo. La muestra más compleja tarda apenas 25 microsegundos en generarse. El "
            "resultado abre la puerta a procesadores de computación cuántica tolerantes a fallos a escala "
            "de billones de cúbits, consolidando a China como potencia mundial en esta tecnología."
        ),
        "fuente_label": "CGTN — Jiuzhang 4.0 takes optical quantum computing to new heights",
        "fuente_url": "https://news.cgtn.com/news/2026-05-17/China-s-Jiuzhang-4-0-takes-optical-quantum-computing-to-new-heights-1NdSw6Shfos/p.html",
    },
    {
        "emoji": "🍵",
        "titulo": "Robots humanoides trabajan en los campos de té de Fujian",
        "cuerpo": (
            "Como preludio a los Juegos Mundiales de Robots Humanoides 2026 (Pekín, 22-26 agosto), "
            "decenas de robots completaron la cadena completa de producción de té blanco en las montañas "
            "de Fuding, Fujian: cosecha selectiva, transporte por senderos de montaña, marchitado, tostado "
            "con control de temperatura por imagen térmica y prensado final. Cada etapa exigió habilidades "
            "distintas: destreza fina para no dañar las hojas, equilibrio en terreno irregular y "
            "monitorización constante. China representa ya casi el 80% de las ventas mundiales de robots "
            "humanoides."
        ),
        "fuente_label": "Interesting Engineering — China tests humanoid robots in tea farms",
        "fuente_url": "https://interestingengineering.com/ai-robotics/china-tests-humanoid-robots-in-tea-farms-before-the-2026-world-robot-games",
    },
    {
        "emoji": "🏫",
        "titulo": "China crea 'escuelas de robots' para prepararlos para el mundo laboral",
        "cuerpo": (
            "Las autoridades municipales de varias ciudades chinas están financiando centros de "
            "entrenamiento laboral para robots humanoides. En estos centros, los robots aprenden mediante "
            "repetición supervisada: una mano robótica necesita unas 10.000 repeticiones para dominar una "
            "nueva habilidad. Las capacidades entrenadas incluyen doblar ropa, fregar platos, gestión de "
            "almacén y tareas de línea de montaje. El plan estratégico nacional fija como meta que los "
            "robots humanoides representen un sector de 10 billones de yuanes para 2030, y los "
            "policymakers los identifican como el siguiente gran vector exportador de China."
        ),
        "fuente_label": "CNBC — Job training for robots: How China is getting machines ready to join the workforce",
        "fuente_url": "https://www.cnbc.com/2026/05/21/china-robots-humanoid-job-training.html",
    },
    {
        "emoji": "💾",
        "titulo": "Chips IA: China produce a 7nm y las grandes tecnológicas escalan producción propia",
        "cuerpo": (
            "China ha logrado producir procesadores a 7 nanómetros a pesar de las restricciones de "
            "exportación de semiconductores de Washington, socavando la estrategia occidental de contención "
            "tecnológica. En paralelo, Alibaba anunció que sus chips GPU propios de T-Head están en "
            "producción masiva a escala comercial, mientras Tencent indicó que la producción de sus chips "
            "domésticos para IA se acelerará este año. Los analistas señalan que China está construyendo "
            "una cadena de suministro de semiconductores alternativa e independiente con una velocidad "
            "que ha sorprendido al sector."
        ),
        "fuente_label": "CNBC — China AI chips ramp up as Nvidia H200 access unclear",
        "fuente_url": "https://www.cnbc.com/2026/05/14/china-ai-chips-nvidia.html",
    },
    {
        "emoji": "🤝",
        "titulo": "Xi a los CEOs de Silicon Valley: 'La puerta de China se abrirá aún más'",
        "cuerpo": (
            "Durante la visita del presidente Trump a China a mediados de mayo, Xi Jinping se reunió con "
            "los principales ejecutivos tecnológicos de EE.UU. y les trasladó que China dará la bienvenida "
            "a una mayor cooperación mutuamente beneficiosa. El mensaje llegó en un contexto de "
            "desescalada comercial: ambos países acordaron que China comprará al menos 17.000 millones de "
            "dólares anuales en productos agrícolas estadounidenses durante 2026, 2027 y 2028. Los modelos "
            "de IA de compañías como Alibaba ya compiten con los de las principales firmas de EE.UU. en "
            "varios benchmarks."
        ),
        "fuente_label": "CNBC — Xi tells Musk, Tim Cook and other CEOs: China will 'open wider'",
        "fuente_url": "https://www.cnbc.com/2026/05/14/xi-china-open-us-business-ai-chips.html",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD y los eléctricos chinos: 400.000 unidades exportadas solo en abril",
        "cuerpo": (
            "Las exportaciones chinas de vehículos eléctricos e híbridos enchufables alcanzaron las "
            "400.000 unidades en abril, la cifra mensual más alta jamás registrada, con un crecimiento "
            "interanual superior al 120%. BYD lidera la expansión global, con un objetivo de 1,5 millones "
            "de vehículos exportados en 2026, un 15-24% por encima de su meta anterior, y acaba de "
            "presentar su nueva línea GT eléctrica bajo la sub-marca Fangchengbao para los mercados de "
            "lujo internacionales. Con China liderando, los analistas prevén que casi uno de cada tres "
            "coches vendidos globalmente en 2026 será eléctrico."
        ),
        "fuente_label": "Bloomberg Línea — BYD confía en superar un 15% su objetivo de exportaciones",
        "fuente_url": "https://www.bloomberglinea.com/negocios/byd-confia-en-que-las-exportaciones-de-2026-superaran-en-un-15-su-anterior-objetivo/",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar china supera al carbón en capacidad instalada",
        "cuerpo": (
            "En 2026, China alcanzó un punto de inflexión energética sin precedentes: por primera vez en "
            "su historia, la capacidad instalada de energía solar supera a la del carbón. La potencia "
            "renovable en funcionamiento supera ya los 1,6 teravatios, con 448 gigavatios adicionales en "
            "construcción —la mitad del total mundial—. Las energías no fósiles representarán el 63% de "
            "la capacidad instalada a finales de 2026, y la generación solar más eólica ya alcanza el "
            "22% de la electricidad producida, superando la media de la OCDE. El almacenamiento en "
            "baterías creció un 75% en 2025."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🚀",
        "titulo": "China podría llevar astronautas a la Luna en 2027: la carrera se acelera",
        "cuerpo": (
            "Jared Isaacman, administrador de la NASA, declaró esta semana que China podría lanzar "
            "misiones tripuladas a la Luna tan pronto como en 2027. La CNSA ya tiene los módulos de la "
            "misión Chang'e-7 en la base espacial de Wenchang, preparando el lanzamiento para agosto de "
            "2026, que explorará el polo sur lunar buscando hielo de agua con una sonda saltadora. La "
            "futura misión Chang'e-8 llevará un robot 'obrero' con IA para tomar decisiones autónomas "
            "en tiempo real, sentando las bases de la primera estación internacional de investigación "
            "lunar antes de 2030."
        ),
        "fuente_label": "Espacio Tech — Isaacman: China lanzará misiones tripuladas a la Luna en 2027",
        "fuente_url": "https://www.espaciotech.net/2026/05/21/jared-isaacman-asegura-que-china-lanzara-misiones-tripuladas-a-la-luna-en-2027/",
    },
    {
        "emoji": "🏥",
        "titulo": "Más de 250 quioscos de salud digital con IA en el metro de Shanghái",
        "cuerpo": (
            "China ha desplegado más de 250 quioscos de diagnóstico inteligente en estaciones de metro, "
            "centros comerciales y zonas de alta afluencia de Shanghái, combinando biomedicina avanzada "
            "con Medicina Tradicional China. Los dispositivos miden presión arterial, frecuencia cardíaca, "
            "saturación de oxígeno y temperatura; sus algoritmos de IA analizan rasgos faciales, color y "
            "textura de la lengua y el pulso digital mediante sensores de presión multicapa, integrando "
            "diagnóstico occidental y tradicional en un solo sistema accesible para millones de ciudadanos."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional China",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Semana del 18 al 24 de mayo de 2026. Recopilacion de las noticias mas relevantes de China: computacion cuantica, robotica, energia, economia y espacio.", bold=False),
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
    title = "China Al Dia — Semana 18-24 Mayo 2026"
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
