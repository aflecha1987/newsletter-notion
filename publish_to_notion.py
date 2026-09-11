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
        "emoji": "☀️",
        "titulo": "La energía solar supera al carbón en China: un punto de inflexión histórico para el planeta",
        "cuerpo": (
            "Al cierre de julio de 2026, la capacidad fotovoltaica instalada de China alcanzó "
            "1.286 millones de kilovatios, superando por primera vez a la del carbón (1.285 millones de kW) "
            "y convirtiéndose en la mayor fuente de generación eléctrica del país por potencia instalada. "
            "La generación solar creció un 15,5 % interanual en los primeros siete meses del año, llegando "
            "a 802.400 millones de kWh. La solar representa ya el 31,5 % de la capacidad instalada total. "
            "El hito convierte a China en el país que más rápido ha transformado su matriz energética "
            "en la historia moderna."
        ),
        "fuente_label": "Bloomberg / Energy Connects — Solar supera al carbón como mayor fuente instalada",
        "fuente_url": "https://www.energyconnects.com/news/renewables/2026/september/solar-surpasses-coal-as-china-s-top-source-of-power-capacity/",
    },
    {
        "emoji": "🤖",
        "titulo": "Conferencia Mundial de Robótica 2026 en Pekín: China envía el 97 % de los robots humanoides del planeta",
        "cuerpo": (
            "Del 19 al 23 de agosto, la Conferencia Mundial de Robótica 2026 reunió en Pekín a 373 "
            "empresas que exhibieron más de 3.000 productos, incluyendo 311 debuts mundiales. El informe "
            "presentado en el evento reveló que China envió más de 40.000 robots humanoides en el primer "
            "semestre de 2026, el 97 % del total mundial. Los robots ya operan en plantas de CATL, Bosch "
            "y varios fabricantes de automóviles. El tema del encuentro: 'Simbiosis humano-robot: "
            "convergencia de producción y demanda'."
        ),
        "fuente_label": "TechNode — China's Humanoid Robot Boom: Moving Beyond the Show Floor",
        "fuente_url": "https://technode.com/2026/09/02/chinas-humanoid-robot-boom-i-moving-beyond-the-show-floor/",
    },
    {
        "emoji": "💾",
        "titulo": "DeepSeek desarrolla su propio chip de IA: China avanza hacia la soberanía total en semiconductores",
        "cuerpo": (
            "La startup china DeepSeek está desarrollando su propio chip de IA para inferencia, "
            "trabajando con socios externos de diseño y reforzando la contratación de ingenieros en "
            "semiconductores. El objetivo es reducir la dependencia de Nvidia (bloqueada por sanciones "
            "estadounidenses) y de los chips Ascend de Huawei. La noticia impactó en Wall Street, donde "
            "las acciones de Nvidia cayeron ante la señal de que la empresa de IA más eficiente del "
            "mundo fabrica sus propios chips, amenazando el modelo de hardware occidental."
        ),
        "fuente_label": "Expansión MX — DeepSeek desarrolla chip de IA propio sin depender de Nvidia",
        "fuente_url": "https://expansion.mx/tecnologia/2026/07/07/deepseek-desarrolla-chip-de-ia-no-depende-de-nvidia",
    },
    {
        "emoji": "🚗",
        "titulo": "China lanza arquitectura de 1.000 V que carga un vehículo eléctrico en 5 minutos",
        "cuerpo": (
            "Geely Holding Group presentó una nueva arquitectura eléctrica de 1.000 voltios que promete "
            "reducir el tiempo de carga a 5 minutos para 200 km de autonomía. El sistema es compatible "
            "con varias marcas del grupo (Volvo, Zeekr, Lynk & Co, Polestar) y podría llegar a coches "
            "de gama media antes de 2028. China también tiene más de 100 millones de coches eléctricos "
            "interconectados a la red como baterías móviles V2G, y fija el objetivo de que los NEV "
            "representen el 70 % de las ventas de turismos para 2030."
        ),
        "fuente_label": "Semana — Tecnología de 1.000 V que carga carros eléctricos en 5 minutos",
        "fuente_url": "https://www.semana.com/vehiculos/articulo/de-china-para-el-mundo-la-tecnologia-de-1000-v-que-promete-cargar-carros-electricos-en-5-minutos/202623/",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones de China se disparan un 25 % en agosto: autos +47 %, computadoras +49 %",
        "cuerpo": (
            "Las exportaciones chinas alcanzaron los 401.440 millones de dólares en agosto de 2026, "
            "un 25 % más que en agosto del año anterior. Los automóviles lideraron con un alza del "
            "47,1 %, seguidos de computadoras y componentes (+49,4 % acumulado enero-agosto) y los "
            "buques (+29,8 %). El comercio exterior total en los primeros ocho meses del año creció "
            "17,6 % interanual, superando 34,78 billones de yuanes (5,13 billones de dólares). "
            "El dato contradice a quienes apostaban a que los aranceles frenarían el dinamismo exportador chino."
        ),
        "fuente_label": "Prensa Latina — China con fuerte crecimiento del comercio exterior hasta agosto",
        "fuente_url": "https://www.prensa-latina.cu/2026/09/09/china-con-fuerte-crecimiento-del-comercio-exterior-hasta-agosto/",
    },
    {
        "emoji": "🌐",
        "titulo": "China amplía cooperación económica con más de 140 países en múltiples frentes globales",
        "cuerpo": (
            "Durante la semana del 8 al 11 de septiembre, China anunció la ampliación de acuerdos de "
            "cooperación económica y comercial con socios estratégicos de África, Latinoamérica y el "
            "Sudeste Asiático. Los acuerdos incluyen financiamiento de infraestructura verde, "
            "transferencia tecnológica en 5G y acceso preferencial al mercado chino para productos "
            "agrícolas de países en desarrollo. Más de 140 naciones participan en la red de "
            "cooperación global promovida por China en 2026."
        ),
        "fuente_label": "Prensa Latina — China amplía cooperación económica a nivel internacional",
        "fuente_url": "https://www.prensa-latina.cu/2026/09/10/china-amplia-cooperacion-economica-y-comercial-a-nivel-internacional/",
    },
    {
        "emoji": "⚡",
        "titulo": "Energía renovable supera el 41 % de generación eléctrica: China lidera la transición energética",
        "cuerpo": (
            "Los datos del primer semestre de 2026 confirman que las energías renovables representaron "
            "el 41,2 % de la generación eléctrica de China, primera vez en la historia que superan "
            "el 40 % en un semestre completo. La participación del carbón cayó al 49,7 %, también "
            "por primera vez por debajo del 50 %. El 73,9 % de la nueva potencia añadida en el semestre "
            "fue renovable (117 GW). La capacidad renovable total alcanzó 2.455 GW, más del 60 % "
            "del parque nacional de generación."
        ),
        "fuente_label": "La República Perú — China marca un antes y un después en la energía mundial",
        "fuente_url": "https://larepublica.pe/mundo/2026/09/05/china-marca-un-antes-y-un-despues-en-la-energia-mundial-la-capacidad-solar-instalada-supera-por-primera-vez-a-la-del-carbon-196220",
    },
    {
        "emoji": "🌿",
        "titulo": "China, superpotencia verde: 225.000 millones de dólares para tecnología limpia global",
        "cuerpo": (
            "China se ha convertido en el mayor inversor mundial en tecnología verde, con 225.000 "
            "millones de dólares comprometidos en 2026 para proyectos de energía limpia fuera de sus "
            "fronteras. La ofensiva abarca desde parques solares en el Sahel hasta plantas hidroeléctricas "
            "en Asia Central y redes eléctricas inteligentes en América Latina. Las exportaciones de "
            "paneles solares chinos representan el 80 % del mercado global, y sus aerogeneradores el 60 %. "
            "El Fondo de Inversión en Energía Verde del Cinturón y la Ruta superó los 50.000 millones."
        ),
        "fuente_label": "El Español — China se alza como superpotencia verde: 225.000 millones de dólares",
        "fuente_url": "https://www.elespanol.com/ciencia/20260331/china-alza-superpotencia-verde-millones-dolares-hacer-tecnologia-mundo/1003744187286_0.html",
    },
    {
        "emoji": "📋",
        "titulo": "Plan Quinquenal 2026-2030: IA, autosuficiencia tecnológica y energía limpia como prioridades nacionales",
        "cuerpo": (
            "El XV Plan Quinquenal (2026-2030) establece como prioridades: autosuficiencia en "
            "semiconductores e IA, industrialización de la robótica, seguridad energética mediante "
            "renovables y desarrollo de nuevas infraestructuras digitales. El plan prevé que la "
            "inversión en I+D supere el 3 % del PIB para 2030 (desde el 2,6 % actual), con énfasis "
            "en biotecnología, computación cuántica, materiales avanzados e inteligencia artificial. "
            "El objetivo final: que China sea reconocida internacionalmente como líder en innovación "
            "antes de 2035."
        ),
        "fuente_label": "The Conversation — 2026-2030: cinco años en los que China busca consolidar su poder global",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
    },
    {
        "emoji": "💊",
        "titulo": "Biotech china bate récords: 60.000 millones en acuerdos de licencias en el primer trimestre",
        "cuerpo": (
            "Mientras la atención global se concentra en la IA y los robots, China construye en "
            "paralelo una potencia farmacéutica global. Las empresas biotech chinas firmaron acuerdos "
            "de licencia transfronteriza por un valor récord de 60.000 millones de dólares solo en "
            "el primer trimestre de 2026. China compite ahora en oncología de precisión, terapias CAR-T, "
            "edición genética y biofármacos, captando el 39 % de los ensayos clínicos globales, "
            "más que EE.UU. y la UE combinados."
        ),
        "fuente_label": "Gizmodo ES — China y su silenciosa exportación biotecnológica",
        "fuente_url": "https://es.gizmodo.com/todos-miraban-a-deepseek-y-a-los-robots-humanoides-pero-china-estaba-preparando-una-exportacion-mucho-mas-silenciosa-ahora-sus-medicamentos-empiezan-a-llenar-las-carteras-de-las-farmaceuticas-occide-2000249516",
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
    title = "China Al Dia — Semana 5-11 Sep 2026"
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
