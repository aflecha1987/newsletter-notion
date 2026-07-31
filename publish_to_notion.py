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
        "emoji": "💾",
        "titulo": "China inicia producción en masa de máquinas DUV de litografía propias: independencia en semiconductores",
        "cuerpo": (
            "El 27 de julio, TrendForce y Tom's Hardware confirmaron que un fabricante estatal radicado en "
            "Shanghái ha comenzado la producción en masa de máquinas de litografía DUV por inmersión de "
            "fabricación totalmente china. Las primeras unidades serán entregadas este mismo año a SMIC, "
            "Hua Hong y CXMT. Los sistemas operan a una longitud de onda de 193 nanómetros y permiten "
            "fabricar chips lógicos y de memoria sin depender de ASML. La noticia sacudió los mercados: "
            "las acciones de ASML cayeron bruscamente y el índice Kospi de Corea del Sur suspendió "
            "brevemente la negociación al desplomarse casi un 11%. Para China, supone el paso más "
            "significativo hacia la autosuficiencia en equipos de fabricación de chips desde que EE.UU. "
            "impuso las restricciones de exportación de tecnología avanzada."
        ),
        "fuente_label": "Tom's Hardware — China begins mass production of homegrown DUV lithography machines",
        "fuente_url": "https://www.tomshardware.com/tech-industry/semiconductors/china-begins-mass-production-of-domestic-immersion-duv-lithography-machines",
    },
    {
        "emoji": "🤖",
        "titulo": "Plan Maestro de IA 2026: China consolida la doctrina IA Plus con presupuesto récord",
        "cuerpo": (
            "En julio de 2026, China aprobó su decimoquinto Plan Quinquenal consagrando la doctrina "
            "IA Plus —aplicar la inteligencia artificial como infraestructura transversal a toda la "
            "economía— junto con los enjambres inteligentes y los agentes autónomos como pilares del "
            "desarrollo nacional. Las cifras son contundentes: 295.000 robots industriales instalados "
            "en un solo año, representando el 54% del total mundial. El objetivo es que el 70% de los "
            "procesos productivos integren IA para 2027, y el 90% para 2030. Las industrias de IA del "
            "país apuntan a superar los 10 billones de yuanes en valor para esa fecha."
        ),
        "fuente_label": "Moncloa — China Plan Maestro IA 2026",
        "fuente_url": "https://www.moncloa.com/2026/07/12/china-plan-maestro-ia-2026-3398625/",
    },
    {
        "emoji": "🏙️",
        "titulo": "WAIC 2026 Shanghai: robots humanoides y el nacimiento de una nueva era tecnológica",
        "cuerpo": (
            "Del 17 al 20 de julio se celebró en Shanghái la Conferencia Mundial de Inteligencia "
            "Artificial 2026 bajo el lema 'Alianza en la IA para un futuro más brillante'. Más de "
            "1.400 invitados internacionales y 200 proveedores presentaron sus últimas innovaciones. "
            "El protagonismo fue para los robots humanoides: se estima que la producción anual china "
            "de estos robots superará las 100.000 unidades en 2026, con decenas de modelos operando "
            "ya en fábricas reales. El presidente de Kazajistán, Tokayev, visitó China especialmente "
            "para asistir al evento. La conferencia reafirmó el liderazgo de Shanghái como capital "
            "global de la IA."
        ),
        "fuente_label": "Xinhua — Conferencia Mundial de IA 2026 en Shanghai",
        "fuente_url": "http://spanish.xinhuanet.com/20260720/debb96dbb6c04901bf5d683c6b1d87dc/c.html",
    },
    {
        "emoji": "🦾",
        "titulo": "China lidera la robótica mundial: 70% de ventas globales de robots cuadrúpedos, 400+ modelos humanoides",
        "cuerpo": (
            "China se ha consolidado como el mayor mercado y productor mundial de robótica avanzada. "
            "Los robots cuadrúpedos chinos representan cerca del 70% de las ventas mundiales, y el "
            "país cuenta con más de 400 modelos de robots humanoides, más de la mitad de todos los "
            "disponibles en el globo. Changzhou se ha convertido en la capital de la robótica "
            "inteligente, con un ecosistema de proveedores, fabricantes y centros I+D sin parangón. "
            "La inteligencia artificial ha dejado de ser un añadido y se ha convertido en el sistema "
            "nervioso central de toda esta maquinaria industrial."
        ),
        "fuente_label": "People's Daily Español — Changzhou impulsa el futuro de la robótica inteligente",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0722/c31616-20480488.html",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China crece un 4,7% en H1 2026: manufactura de alta tecnología como motor",
        "cuerpo": (
            "La economía china cerró el primer semestre de 2026 con un crecimiento del 4,7% interanual. "
            "El motor sigue siendo la manufactura tecnológica, la exportación de vehículos de nueva "
            "energía y la inversión en sectores de alta tecnología. Cada hora salen de las cadenas de "
            "montaje 2.000 vehículos de nueva energía, y cada día se registran varios miles de patentes "
            "de invención. Cada minuto, el tren de alta velocidad Fuxing recorre 5,8 km y 600 "
            "contenedores salen de los puertos. La manufactura china ocupa el primer puesto mundial "
            "por decimosexto año consecutivo."
        ),
        "fuente_label": "Banco Mundial — Rebalancing Growth: China Economic Update",
        "fuente_url": "https://www.worldbank.org/en/news/press-release/2026/07/07/rebalancing-growth-china-economic-update",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de coches chinos baten récords: 905.000 unidades en un mes y BYD apunta a 1,5M en 2026",
        "cuerpo": (
            "Las exportaciones de automóviles de China registraron en 2026 el mejor dato mensual de "
            "su historia, superando las 905.000 unidades en un solo mes, más que todo lo exportado en "
            "el año 2019. BYD lidera con cerca de 175.000 unidades exportadas en junio, apuntando a "
            "1,5 millones de vehículos exportados en todo 2026, un 15% por encima de su objetivo "
            "inicial. En el segundo trimestre, BYD entregó 557.090 unidades puramente eléctricas, "
            "superando a Tesla (480.126) en ese segmento. La empresa también desarrolla sus propios "
            "semiconductores para reducir dependencia externa."
        ),
        "fuente_label": "Motor16 — Exportaciones coches chinos 2026 récord",
        "fuente_url": "https://www.motor16.com/las-ultimas-noticias/exportaciones-coches-chinos-2026-record/",
    },
    {
        "emoji": "☀️",
        "titulo": "Zhuri logra 1.180 W de energía solar desde el espacio: China lidera la revolución energética orbital",
        "cuerpo": (
            "China se convirtió esta semana en el primer país en demostrar de forma práctica la "
            "transmisión de energía solar captada desde el espacio exterior. El proyecto Zhuri logró "
            "una potencia de 1.180 vatios recibidos en tierra, superando cualquier demostración previa "
            "de energía solar espacial. El programa sigue una hoja de ruta escalonada: demostrador en "
            "órbita baja en 2026, prototipo de 0,5 MW en órbita geoestacionaria en 2030, y una planta "
            "piloto de 20 MW en 2035. La energía solar espacial puede generar electricidad las 24 horas "
            "del día sin pérdidas atmosféricas."
        ),
        "fuente_label": "Ecosistema Startup — Zhuri: China logra 1.180W de energía solar espacial",
        "fuente_url": "https://ecosistemastartup.com/zhuri-china-logra-1-180w-de-energia-solar-espacial-en-2026/",
    },
    {
        "emoji": "🌞",
        "titulo": "24 plantas termosolares en operación y 26 en construcción: China escala la energía CSP",
        "cuerpo": (
            "El Consejo de Electricidad de China confirmó el 16 de julio que el país opera actualmente "
            "24 plantas de energía solar de concentración (CSP) y tiene otras 26 en construcción, con "
            "una capacidad total en construcción de 3,2 gigavatios. Este tipo de instalaciones almacenan "
            "el calor solar en sales fundidas, permitiendo generar electricidad incluso de noche, lo que "
            "las convierte en un complemento ideal para la red eléctrica. La apuesta china por las CSP "
            "se enmarca en el plan de duplicar su capacidad de energía limpia para 2035, con una "
            "inversión de 1 billón de yuanes anuales en infraestructura eléctrica."
        ),
        "fuente_label": "Pressenza — El comienzo de una nueva era tecnológica",
        "fuente_url": "https://www.pressenza.com/es/2026/07/el-comienzo-de-una-nueva-era-tecnologica-la-semana-en-que-los-mercados-descubrieron-que-china-ya-no-esta-persiguiendo-a-occidente/",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 lista para agosto: la exploración del polo sur lunar más cerca que nunca",
        "cuerpo": (
            "Los módulos de la misión Chang'e-7 completaron su traslado a la Base Espacial de Wenchang "
            "y superaron las pruebas previas al lanzamiento, programado para agosto de 2026. La misión "
            "incluye un orbitador, un módulo de aterrizaje, un rover y una sonda mini-saltadora diseñada "
            "para explorar cráteres en sombra permanente del polo sur lunar, donde los científicos "
            "sospechan la existencia de agua en forma de hielo. El éxito sería un paso decisivo en la "
            "preparación del programa lunar tripulado chino antes de 2030. En paralelo, avanza el "
            "cohete reutilizable Larga Marcha 10 y la misión Tianwen-2 a su asteroide objetivo."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🤝",
        "titulo": "China y ASEAN: comercio supera 1 billón de dólares y se acelera el libre comercio 3.0",
        "cuerpo": (
            "El 23 de julio, el canciller Wang Yi participó en la reunión de cancilleres China-ASEAN "
            "en Filipinas. Tras superar en 2025 la barrera de 1 billón de dólares en comercio bilateral, "
            "Wang Yi pidió acelerar la negociación de la Zona de Libre Comercio China-ASEAN 3.0 para "
            "profundizar la integración económica regional. Por otro lado, China registró las primeras "
            "solicitudes bajo sus nuevas regulaciones de inversión extranjera directa, vigentes desde "
            "el 1 de julio, que refuerzan la protección de las inversiones chinas en el exterior y "
            "establecen mecanismos frente a medidas discriminatorias de terceros países."
        ),
        "fuente_label": "Observatorio de Política China — Resumen política exterior julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-67/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
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
    title = "China Al Dia — Semana 24-31 Julio 2026"
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
