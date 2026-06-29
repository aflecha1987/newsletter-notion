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
        "emoji": "🌐",
        "titulo": "China presenta el concepto \"Oportunidad China 2.0\" en el Davos de Verano de Dalian",
        "cuerpo": (
            "Del 23 al 25 de junio, la ciudad costera de Dalian acogió la XVII Reunión Anual de los Nuevos "
            "Campeones del Foro Económico Mundial —el \"Davos de Verano\"— con más de 1.700 participantes "
            "de más de 90 países. El primer ministro Li Qiang inauguró el foro acuñando el término "
            "\"Oportunidad China 2.0\": la tesis de que los avances tecnológicos chinos en vehículos "
            "eléctricos, paneles solares, chips, baterías, IA y robótica no son una amenaza, sino opciones "
            "asequibles y competitivas para el mundo. La inteligencia artificial fue el eje central del "
            "encuentro, consolidando el modelo chino de \"IA+\" como referente global de crecimiento económico."
        ),
        "fuente_label": "La Jornada — Avances tecnológicos de China son una oportunidad",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/06/24/economia/avances-tecnologicos-de-china-son-una-oportunidad-no-una-amenaza-dice-el-premier-li-quiang",
    },
    {
        "emoji": "🤖",
        "titulo": "China lanza plan trienal para integrar IA en toda su infraestructura de telecomunicaciones",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de la Información publicó en junio una hoja de ruta "
            "2026-2028 para integrar la inteligencia artificial en toda la red de telecomunicaciones del "
            "país. Los objetivos concretos incluyen que las redes alcancen una fase inicial de inteligencia "
            "autónoma de alto nivel para 2028, con más de 30 casos de uso de alto valor, agentes de IA "
            "especializados y cobertura del 75% de las áreas metropolitanas con acceso a potencia de "
            "cómputo de latencia inferior a 1 milisegundo. China se posiciona así como el primer país "
            "del mundo en desplegar IA a escala de infraestructura nacional de telecomunicaciones."
        ),
        "fuente_label": "China Gov — China issues three-year plan to boost AI integration",
        "fuente_url": "https://english.www.gov.cn/news/202606/10/content_WS6a296017c6d00ca5f9a0b876.html",
    },
    {
        "emoji": "🛸",
        "titulo": "Paneles solares en órbita: China construye la primera planta energética espacial del mundo",
        "cuerpo": (
            "China avanza en un proyecto sin precedentes: una planta solar masiva en órbita geoestacionaria "
            "a 36.000 km de altitud. La energía captada se transmitiría a la Tierra mediante haces de "
            "microondas o láser y podría ser hasta 10 veces más eficiente que los paneles solares "
            "convencionales, al no verse afectada por la atmósfera ni por los ciclos día/noche. El "
            "lanzamiento del satélite de prueba está previsto para 2028. China también se convirtió este "
            "año en el primer país del mundo en superar 1 TW (1 billón de vatios) de capacidad solar "
            "instalada, con la solar a punto de superar al carbón en capacidad total instalada por "
            "primera vez en la historia."
        ),
        "fuente_label": "El Español — China construye paneles solares en el espacio a 36.000 km",
        "fuente_url": "https://www.elespanol.com/ciencia/20260413/china-cambia-estrategia-construye-paneles-solares-espacio-kilometros-trabajan-horas-dia/1003744201225_0.html",
    },
    {
        "emoji": "☀️",
        "titulo": "La energía solar china supera al carbón por primera vez en la historia",
        "cuerpo": (
            "En 2026, China está a punto de lograr un hito sin precedentes: su capacidad instalada de "
            "energía solar superará a la del carbón por primera vez. El país añadió 434 GW de renovables "
            "en 2025 —otro récord mundial— y en el Q1 2026 la capacidad total instalada rozó los 4 billones "
            "de kW. Las dos grandes empresas estatales de la red eléctrica invertirán 1 billón de yuanes "
            "anuales (unos 146.000 millones de dólares) durante el 15.º Plan Quinquenal (2026-2030) "
            "para conectar las nuevas energías a la red. China consolida su liderazgo absoluto en la "
            "transición energética global."
        ),
        "fuente_label": "CGTN — China's total installed power capacity nears 4 billion kW",
        "fuente_url": "https://news.cgtn.com/news/2026-04-20/China-s-total-installed-power-capacity-nears-4-billion-kW-in-Q1-2026-1Mv6wRFRpLO/p.html",
    },
    {
        "emoji": "📈",
        "titulo": "El comercio exterior de China sube un 20,5% interanual en los primeros cinco meses de 2026",
        "cuerpo": (
            "Las importaciones chinas crecieron un 20,5% interanual en los primeros cinco meses de 2026, "
            "superando el ritmo de crecimiento de las exportaciones y consolidando a China como segundo "
            "importador mundial por decimoséptimo año consecutivo. El PIB creció un 5% interanual en el "
            "Q1, acelerando desde el 4,5% del trimestre anterior y batiendo las previsiones del mercado. "
            "Las exportaciones, impulsadas por la demanda global de productos de IA y tecnología verde, "
            "subieron en torno al 15% en los primeros cuatro meses. China también ha concedido arancel "
            "cero a 63 países como parte de su apuesta por el libre comercio multilateral."
        ),
        "fuente_label": "WEF — The state of China's economy in 5 numbers",
        "fuente_url": "https://www.weforum.org/stories/2026/06/the-state-of-china-economy-in-five-numbers/",
    },
    {
        "emoji": "🚗",
        "titulo": "China supera los 1,5 millones de vehículos eléctricos exportados en 2026",
        "cuerpo": (
            "China alcanzó un nuevo récord histórico de exportaciones de vehículos electrificados en "
            "2026, superando el hito de 1,5 millones de unidades enviadas a nivel global. En mayo, los "
            "vehículos eléctricos coparon el top 5 de ventas en China con 950.000 enchufables vendidos "
            "en un solo mes. BYD, Geely y Chery lideran las exportaciones hacia Asia-Pacífico, Europa y "
            "América Latina, donde la demanda de movilidad sostenible y asequible no para de crecer. El "
            "mercado global de eléctricos crece un 0,9% en 2026, pero China sigue siendo el motor "
            "indiscutible con su producción y exportación récord."
        ),
        "fuente_label": "16 Válvulas — China logró otro récord de exportación de vehículos electrificados",
        "fuente_url": "https://www.16valvulas.com.ar/crecimiento-imparable-china-logro-otro-record-de-exportacion-de-vehiculos-electrificados-con-mas-de-1-5-millones-de-unidades-enviadas-a-nivel-global-en-2026/",
    },
    {
        "emoji": "🚄",
        "titulo": "El primer tren de alta velocidad privado de China supera los 100 millones de pasajeros",
        "cuerpo": (
            "El 27 de junio, la primera línea ferroviaria de alta velocidad de China gestionada con "
            "capital privado superó el hito de 100 millones de pasajeros transportados desde su apertura. "
            "El logro demuestra la madurez del modelo chino de ferrocarril de alta velocidad y su "
            "capacidad para atraer inversión privada a infraestructuras críticas. China ya cuenta con "
            "la red de alta velocidad más extensa del mundo y continúa expandiéndola a nuevos países "
            "y regiones mediante su Iniciativa de la Franja y la Ruta."
        ),
        "fuente_label": "Xinhua — Primera línea ferroviaria privada supera 100 millones de pasajeros",
        "fuente_url": "http://spanish.xinhuanet.com/20260628/05e1abf0363347dd8a8d829c5211f64c/c.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "La BRI bate récord histórico: 213.500 millones de dólares en nuevos proyectos",
        "cuerpo": (
            "La Iniciativa de la Franja y la Ruta (BRI) alcanzó en 2025 un valor récord de 213.500 "
            "millones de dólares en nuevos contratos e inversiones, marcando un giro hacia grandes "
            "proyectos de infraestructura —ferrocarriles, puertos, energía— tras años de iniciativas "
            "más pequeñas. En 2026, China ha intensificado sus esfuerzos en África (puertos, zonas "
            "industriales, telecomunicaciones), América Latina (energía, minería, logística) y Europa, "
            "con inversiones directas en el puerto del Pireo que superarán los 550 millones de euros. "
            "Más de 150 países participan actualmente en la mayor iniciativa de desarrollo global del siglo XXI."
        ),
        "fuente_label": "CKGSB — China's Belt and Road Enters a New Phase",
        "fuente_url": "https://english.ckgsb.edu.cn/knowledge/article/china-belt-and-road-enters-a-new-phase/",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou 23: China envía a la primera astronauta de Hong Kong a la estación Tiangong",
        "cuerpo": (
            "El 24 de mayo de 2026, China lanzó la misión Shenzhou 23 con tres astronautas hacia la "
            "estación espacial Tiangong. Entre ellos destaca Lai Ka-ying, nacida en Hong Kong y primera "
            "astronauta originaria de la ciudad en llegar al espacio. Uno de los tripulantes realizará "
            "una estancia de un año completo en órbita, un hito crucial en la preparación del programa "
            "de alunizaje tripulado chino antes de 2030. El lanzamiento de Chang'e-7 hacia el polo sur "
            "lunar, donde se sospecha la existencia de agua en forma de hielo, está previsto para finales "
            "de 2026."
        ),
        "fuente_label": "NPR — China launches Shenzhou 23 spacecraft",
        "fuente_url": "https://www.npr.org/2026/05/25/g-s1-124179/china-launches-shenzhou-23-spacecraft",
    },
    {
        "emoji": "🤝",
        "titulo": "40 embajadores de 27 países visitan la provincia de Hubei esta semana",
        "cuerpo": (
            "Esta semana, casi 40 enviados diplomáticos de 27 países y organizaciones internacionales "
            "—entre ellos embajadores de Argentina, España, Reino Unido, Bulgaria, Turkmenistán y "
            "Comoras— visitaron la provincia de Hubei para conocer su desarrollo cultural, económico e "
            "industrial. La visita al Museo Provincial de Hubei en Wuhan es parte de la activa diplomacia "
            "cultural que China promueve para reforzar los lazos con sus socios internacionales, "
            "mostrando la riqueza histórica y el dinamismo moderno de sus regiones interiores."
        ),
        "fuente_label": "Xinhua — Enviados diplomáticos extranjeros visitan el Museo Provincial de Hubei",
        "fuente_url": "http://spanish.xinhuanet.com/20260628/60ee2c27398f44b8a1aea2ca824a467a/c.html",
    },
]


def build_blocks():
    today = "29 de junio de 2026"
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
    title = "China Al Dia — Semana 23-29 Junio 2026"
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
