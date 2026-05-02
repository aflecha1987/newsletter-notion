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

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


NOTICIAS = [
    {
        "emoji": "🚗",
        "titulo": "El Salón del Automóvil de Pekín 2026 reescribe el futuro de la movilidad eléctrica",
        "cuerpo": (
            "El Beijing Auto Show 2026 (Auto China), celebrado del 24 de abril al 3 de mayo, se ha "
            "convertido en el mayor salón del automóvil del mundo: 1.451 vehículos expuestos, 181 debuts "
            "mundiales y 71 concepts en 380.000 m². Los NEV representan más del 80% de los modelos "
            "presentados. BYD presentó el Denza Z, un hypercar eléctrico descapotable de más de 1.000 CV "
            "destinado a Europa, junto con la batería Blade de 2ª generación y carga en menos de 10 minutos. "
            "XPeng lanzó el GX SUV con 750 km de autonomía y hardware L4 por $58.000. Geely presentó el "
            "EVA Cab, el primer robotaxi autónomo sin conductor con arquitectura cuántica L4 hecho en China. "
            "Xiaomi sorprendió con el Aero GT, un concept eléctrico de alto rendimiento. El show recibió "
            "cerca de 1 millón de visitantes, batiendo el récord del salón del automóvil más visitado del mundo."
        ),
        "fuente_label": "Electrek — Beijing Auto Show 2026: a glimpse at the future of the auto industry",
        "fuente_url": "https://electrek.co/2026/04/26/beijing-auto-show-2026-insane-glimpse-future-auto-industry/",
    },
    {
        "emoji": "🤖",
        "titulo": "DeepSeek V4 corre en chips Huawei y cuesta 10 veces menos que GPT-5.5",
        "cuerpo": (
            "El 24 de abril, DeepSeek lanzó V4 Pro y V4 Flash: la primera IA de frontera china "
            "construida para ejecutarse nativamente en chips Huawei Ascend 950PR en lugar de NVIDIA. "
            "V4 Pro tiene 1,6 billones de parámetros, es open source (licencia MIT), con ventana de "
            "contexto de 1 millón de tokens y precios 10 veces menores que GPT-5.5. En días, ByteDance, "
            "Tencent y Alibaba iniciaron pedidos masivos del chip Ascend 950PR. Huawei prevé enviar "
            "750.000 unidades este año. El Ascend 950PR supera en 2,87 veces al NVIDIA H20 en FP4 y ofrece "
            "1,56 PFLOPS. Este lanzamiento marca la ruptura definitiva de China con la dependencia del "
            "ecosistema CUDA de NVIDIA, construyendo una pila de IA soberana de principio a fin."
        ),
        "fuente_label": "Fortune — DeepSeek V4: rock-bottom prices and deep integration with Huawei chips",
        "fuente_url": "https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/",
    },
    {
        "emoji": "🦾",
        "titulo": "XPeng IRON: el robot humanoide más humano del mundo entra en producción en 2026",
        "cuerpo": (
            "En el Salón del Automóvil de Pekín, XPeng presentó la versión casi lista para producción "
            "de su robot humanoide IRON. Mide menos de 170 cm con estructura esqueleto-músculo-piel, "
            "más de 60 articulaciones y manos con 22 grados de libertad. Funciona con tres chips IA "
            "Turing propios (2.250 TOPS) y el modelo VLA 2.0. La empresa apunta a producir más de "
            "1.000 unidades al mes hacia finales de 2026, en escenarios comerciales como centros "
            "comerciales, tiendas y exposiciones. IRON fue cortado en público para demostrar que no "
            "había ninguna persona dentro: sus movimientos son tan fluidos que generó incredulidad "
            "entre el público. Es el exponente más avanzado de la ola de humanoides chinos listos para el mercado."
        ),
        "fuente_label": "Humanoids Daily — XPeng debuts Most Human-Like Iron Robot",
        "fuente_url": "https://www.humanoidsdaily.com/news/xpeng-debuts-most-human-like-iron-robot-details-vlt-brain-and-2026-production-goal",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar de China supera por primera vez a la del carbón",
        "cuerpo": (
            "En 2026, China alcanza un punto de inflexión energético sin precedentes: la capacidad "
            "instalada de energía solar supera por primera vez a la del carbón. A finales de marzo, "
            "la capacidad eólica y solar combinada alcanzó 1.900 millones de kW (+28,1% interanual), "
            "representando ya el 40% de toda la electricidad generada. Se espera que en 2026 China "
            "añada más de 300 GW de nueva energía renovable sobre un total de 400 GW de nueva capacidad. "
            "A finales de año, las renovables representarán el 50% de la capacidad instalada total del "
            "país. China está en camino de alcanzar su objetivo de pico de emisiones antes de 2030 y "
            "neutralidad de carbono antes de 2060, mientras lidera al mismo tiempo el mercado de "
            "fabricación de paneles solares con más del 80% de la producción mundial."
        ),
        "fuente_label": "China Daily — Solar capacity to outshine coal power in 2026",
        "fuente_url": "https://www.chinadaily.com.cn/a/202604/29/WS69f15f2ca310d6866eb461b9.html",
    },
    {
        "emoji": "🔋",
        "titulo": "China domina el 75% de las baterías del mundo: el nuevo eje geopolítico del siglo XXI",
        "cuerpo": (
            "China controla más del 75% de la producción mundial de baterías de litio y domina toda "
            "la cadena de valor: desde minerales críticos hasta la celda final. El Auto Show de Pekín "
            "2026 reforzó este liderazgo con el debut de la batería Blade de segunda generación de BYD, "
            "con carga ultrarrápida de menos de 10 minutos y mayor densidad energética, acompañada de "
            "una red de 20.000 puntos de carga rápida. En paralelo, China lidera la instalación de "
            "almacenamiento energético a escala de red (BESS), clave para estabilizar la integración "
            "de renovables. Varios analistas ya califican el dominio chino de las baterías como el "
            "'nuevo petróleo' del siglo XXI, con implicaciones geopolíticas que van mucho más allá del sector automotriz."
        ),
        "fuente_label": "El Ecosistema Startup — China domina las baterías: la geopolítica energética en 2026",
        "fuente_url": "https://ecosistemastartup.com/china-domina-las-baterias-la-geopolitica-energetica-en-2026/",
    },
    {
        "emoji": "📈",
        "titulo": "PMI manufacturero: 50,3 en abril — China sigue en expansión industrial",
        "cuerpo": (
            "El PMI manufacturero de China se situó en 50,3 en abril de 2026, superando el umbral de "
            "50 que marca la frontera entre expansión y contracción. El dato consolida la tendencia "
            "positiva de un primer trimestre sólido: PIB +5% interanual, exportaciones de bienes de "
            "alta tecnología +18,3%, comercio exterior total +15% (el ritmo más rápido en cinco años). "
            "El motor ha sido la manufactura de alta tecnología, cuya producción creció un 12,5% en "
            "Q1, con robots industriales y circuitos integrados disparándose un 33% y 24% respectivamente. "
            "China consolida su posición como la fábrica del mundo más sofisticada tecnológicamente, "
            "lejos ya del modelo de mano de obra barata de décadas anteriores."
        ),
        "fuente_label": "CGTN Español — El comercio exterior de China crece un 15% en el primer trimestre",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-16/2044593566811017217/index.html",
    },
    {
        "emoji": "🏆",
        "titulo": "China lidera patentes de IA globales: 602 millones de usuarios de IA generativa",
        "cuerpo": (
            "Un informe publicado esta semana confirma que China es el primer país del mundo en "
            "solicitudes de patentes de IA, con un crecimiento interanual del 31,2% en el primer "
            "trimestre de 2026. China cuenta ya con 602 millones de usuarios de IA generativa, más "
            "del 50% del total global. El 26 de abril, China Media Group (CMG) lanzó la Gala de "
            "Ciencia y Tecnología 2026, el evento nacional que celebra los grandes avances del año. "
            "Las industrias de IA del país superaron el billón de yuanes en valor en 2025 y apuntan "
            "a superar los 10 billones en 2030. China impulsa activamente su iniciativa AI Plus para "
            "que el 70% de la economía productiva esté integrada con IA antes de 2027."
        ),
        "fuente_label": "Global Times — From robots to EVs to AI: a week of breakthroughs highlights China's tech",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359843.shtml",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 en la rampa de lanzamiento: China apunta al polo sur lunar en agosto",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 han llegado a la Base Espacial de Wenchang, "
            "iniciando las pruebas finales previas al lanzamiento previsto para agosto de 2026. La "
            "misión incluye un orbitador, módulo de aterrizaje, rover y una mini-sonda saltadora "
            "diseñada para explorar cráteres en sombra permanente del polo sur lunar, donde se "
            "sospecha la presencia de agua en forma de hielo. Además, la CNSA tiene previstas para "
            "2026 la misión Tianwen-2 a su asteroide objetivo, las misiones tripuladas Shenzhou-23, "
            "y los ensayos del cohete reutilizable Larga Marcha 10, pieza clave del programa lunar "
            "tripulado antes de 2030. China consolida su posición como segunda potencia espacial mundial."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🌐",
        "titulo": "China y España refuerzan lazos estratégicos: visita de Sánchez a Pekín",
        "cuerpo": (
            "El presidente del Gobierno de España, Pedro Sánchez, realizó una visita oficial a China "
            "del 11 al 15 de abril, consolidando la asociación estratégica entre ambos países. Las "
            "conversaciones se centraron en comercio bilateral, cooperación tecnológica e inversiones "
            "en energías renovables. En el marco de su política exterior activa, China también celebró "
            "el octavo diálogo diplomático China-Australia y confirmó que será la sede de la 33.ª "
            "Reunión de Líderes del APEC en noviembre de 2026, considerado el evento diplomático más "
            "importante del año. La iniciativa de aranceles cero para todos los países africanos con "
            "relaciones diplomáticas refuerza el liderazgo de China como socio del Sur Global."
        ),
        "fuente_label": "Observatorio de Política China — Resumen política exterior 24-30 abril 2026",
        "fuente_url": "https://www.politica-china.org/resumen-politica-exterior-miscelanea-8/",
    },
    {
        "emoji": "⚡",
        "titulo": "5G-A cubre 330 ciudades y China planea 500.000 nuevas estaciones antes de 2030",
        "cuerpo": (
            "A cierre de marzo de 2026, China contaba con 4.958 millones de estaciones base 5G, con "
            "la tecnología 5G-Advanced (5G-A) cubriendo 330 ciudades. Los usuarios de IoT alcanzaron "
            "los 2.948 millones, casi tres veces la población china. El sector de fabricación de "
            "equipos electrónicos y comunicaciones creció un 13,6% interanual en Q1. China planifica "
            "el despliegue de 500.000 nuevas estaciones 5G-A antes de 2030, mientras avanza en la "
            "investigación del 6G, previsto como nuevo motor de crecimiento económico global a partir "
            "de esa fecha. La conectividad digital se consolida como infraestructura crítica para la "
            "economía inteligente que el nuevo plan quinquenal pone en el centro del desarrollo nacional."
        ),
        "fuente_label": "Xinhua / Shanghai News — China boosts digital technology in push for modernization",
        "fuente_url": "http://www.shanghainews.net/news/279002526/china-boosts-digital-technology-in-push-for-modernization",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today} · Semana 27 abr – 2 may 2026", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, IA, vehiculos electricos, energia renovable, espacio y diplomacia.", bold=False),
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
    title = "China Al Dia — Semana 27 Abril – 2 Mayo 2026"
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
