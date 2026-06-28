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

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}


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
        "titulo": "Davos de Verano en Dalian: China impulsa la innovación global a gran escala",
        "cuerpo": (
            "Del 23 al 25 de junio, Dalian acogió la XVII Reunión Anual de los Nuevos Campeones del "
            "Foro Económico Mundial bajo el lema 'Innovar a gran escala'. Más de 1.700 participantes "
            "de 90+ países debatieron cómo la IA y la transformación tecnológica están rediseñando "
            "el crecimiento económico mundial. El primer ministro Li Qiang presentó el concepto "
            "'Oportunidad China 2.0', defendiendo los avances tecnológicos del país como una "
            "oportunidad global, no una amenaza. El foro cerró con un consenso: la innovación es más "
            "necesaria que nunca en un contexto de cambio acelerado, y China desempeña un papel clave."
        ),
        "fuente_label": "Xinhua Español — Davos de Verano concluye en Dalian",
        "fuente_url": "http://spanish.xinhuanet.com/20260625/f887ae7ad4d849c280c904c695b009e9/c.html",
    },
    {
        "emoji": "🏭",
        "titulo": "La IA debuta en la 4ª Exposición Internacional de Cadenas de Suministro de China (CISCE)",
        "cuerpo": (
            "Del 22 al 26 de junio, Pekín acogió la 4ª CISCE con 228 empresas de 11 países y el "
            "debut de una zona dedicada exclusivamente a la inteligencia artificial. La sección de "
            "'tecnología digital inteligente' mostró el ecosistema completo de la IA: desde la "
            "recopilación de datos hasta aplicaciones en el mundo real. Apple, Walmart, Schneider "
            "Electric y SAP demostraron cómo la IA está redefiniendo la manufactura, el retail y "
            "la salud digital. Las seis grandes cadenas del evento: manufactura avanzada, agricultura "
            "verde, tecnología digital, vida saludable, vehículo inteligente y energía limpia."
        ),
        "fuente_label": "CGTN Español — Exposición Internacional de Cadenas de Suministro de China",
        "fuente_url": "https://espanol.cgtn.com/2026/06/15/ARTI1781490625242419",
    },
    {
        "emoji": "🧠",
        "titulo": "China lanza silla de ruedas controlada por la mente: el BCI sale del laboratorio",
        "cuerpo": (
            "China aprobó en marzo su primer BCI (interfaz cerebro-computadora) invasivo para uso "
            "comercial, declarándolo industria estratégica del futuro. En junio llega al mercado una "
            "silla de ruedas controlada por señales cerebrales para pacientes con ELA y enfermedad "
            "de la neurona motora. Tianjin presentó su Plan de Acción BCI 2026-2030 e inauguró un "
            "clúster industrial dedicado a la tecnología cerebral. El objetivo nacional: avances "
            "técnicos significativos para 2027 y dos o tres empresas BCI de clase mundial antes de "
            "2030, compitiendo directamente con Neuralink de Elon Musk."
        ),
        "fuente_label": "People's Daily Español — Tianjin impulsa su estatus como potencia BCI",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0616/c31616-20467940.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23: la primera astronauta de Hong Kong y un año completo en el espacio",
        "cuerpo": (
            "La misión Shenzhou-23, operativa en junio en la estación Tiangong, incluye a Lai Ka-ying, "
            "la primera astronauta procedente de Hong Kong en la historia del programa espacial chino. "
            "Uno de los tres tripulantes permanecerá un año completo en órbita —hito sin precedentes— "
            "para estudiar los efectos de la microgravedad en el organismo humano. La misión realiza "
            "más de 100 proyectos científicos en biología, medicina espacial, ciencia de materiales "
            "y física de fluidos. Paso clave hacia el objetivo de llevar astronautas chinos a la "
            "Luna antes de 2030."
        ),
        "fuente_label": "Infobae — China da un paso decisivo con la misión Shenzhou-23",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/24/un-ano-en-orbita-china-da-un-paso-decisivo-en-su-programa-lunar-con-el-lanzamiento-de-la-mision-shenzhou-23/",
    },
    {
        "emoji": "🔬",
        "titulo": "China lidera la investigación científica mundial: crecimiento del 22,4% en producción",
        "cuerpo": (
            "Según el Nature Index 2026, China es el país que más contribuye a la investigación "
            "científica de alta calidad, siendo la única nación entre las 10 potencias científicas "
            "principales que registró crecimiento de doble dígito: +22,4% entre 2024 y 2025. En el "
            "Foro Zhongguancun 2026 en Pekín se presentaron 21 avances en cuatro ejes: ciencia "
            "mundial, economía, necesidades nacionales y salud. Las áreas estrella fueron IA, "
            "aeroespacial, circuitos integrados y medicina preventiva."
        ),
        "fuente_label": "UnoTV — China lidera la investigación científica mundial en 2026",
        "fuente_url": "https://www.unotv.com/ruta-a-china/china-lidera-investigacion-cientifica-mundial-nature-index-2026/",
    },
    {
        "emoji": "📈",
        "titulo": "El comercio exterior chino se dispara en junio: récord impulsado por acuerdo con EE.UU.",
        "cuerpo": (
            "El comercio exterior de China creció un 5,2% interanual en junio 2026, duplicando el "
            "ritmo de mayo. Las exportaciones alcanzaron 2,34 billones de yuanes (≈326.000 millones "
            "de dólares), un +7,2% interanual. El motor principal fue la demanda mundial de "
            "maquinaria, electrónica y tecnología vinculada a la IA (+24,3%). El reciente acuerdo "
            "comercial China-EE.UU. catalizó esta revitalización. En el primer semestre, las "
            "importaciones crecieron un 20,5% interanual, evidenciando también la fortaleza del "
            "consumo interno chino."
        ),
        "fuente_label": "Empresa Exterior — El comercio exterior chino se dispara en junio",
        "fuente_url": "https://empresaexterior.com/art/98387/el-comercio-exterior-chino-se-dispara-en-junio-impulsado-por-el-nuevo-entendimiento-con-estados-unidos-superando-todas-las-expectativas",
    },
    {
        "emoji": "☀️",
        "titulo": "China produce más energía solar que el planeta puede instalar: el electroestado toma forma",
        "cuerpo": (
            "China ha llegado a un punto histórico: su capacidad de fabricación de paneles solares "
            "supera ya la demanda global de instalación. Por primera vez en el país, la capacidad "
            "solar instalada superó a la de carbón. Las energías renovables representan el 56% de "
            "la capacidad total instalada. En 2025, China instaló 446 GW de nueva capacidad "
            "renovable, más que el resto del mundo en conjunto, alcanzando un total superior a 2,34 "
            "TW. El historiador Adam Tooze acuñó el término 'electroestado' para describir el nuevo "
            "sistema energético chino, que busca liderar la transición energética global."
        ),
        "fuente_label": "Algoritmo Mag — China ya puede fabricar más energía solar que el planeta necesita instalar",
        "fuente_url": "https://algoritmomag.com/china-energia-solar/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD supera a Tesla: los vehículos eléctricos chinos consolidan su liderazgo mundial",
        "cuerpo": (
            "BYD encabeza el mercado mundial de vehículos eléctricos tras superar a Tesla en ventas "
            "globales. Las exportaciones chinas de VE e híbridos batieron en 2026 un nuevo récord "
            "histórico (+140% interanual en marzo). En la 4ª CISCE, la cadena de 'vehículo "
            "inteligente' fue una de las seis grandes apuestas del evento, con docenas de proveedores "
            "de componentes para coches eléctricos autónomos. China ha invertido 231.000 millones de "
            "dólares en el desarrollo de su industria de vehículos eléctricos desde 2009, y los "
            "resultados son indiscutibles."
        ),
        "fuente_label": "Ambientum — Estrategia energética de China: liderazgo y renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
    },
    {
        "emoji": "🤝",
        "titulo": "China fortalece su diplomacia económica: reuniones clave con Brasil y Austria",
        "cuerpo": (
            "En la semana del 23 al 28 de junio, China intensificó su diplomacia económica. Pan "
            "Gongsheng, gobernador del Banco Popular de China, se reunió con el ministro de Hacienda "
            "de Brasil para reforzar la coordinación macroeconómica y la cooperación financiera "
            "bilateral. El canciller Wang Yi se reunió con la ministra de Asuntos Europeos de "
            "Austria. En el Davos de Verano, el premier Li Qiang se reunió con seis jefes de "
            "gobierno de distintos continentes, consolidando el papel de China como actor central "
            "del multilateralismo económico y la gobernanza global."
        ),
        "fuente_label": "World Economic Forum — Summer Davos 2026 Day 3",
        "fuente_url": "https://www.weforum.org/stories/2026/06/summer-davos-amnc-2026-day-3-live-updates/",
    },
    {
        "emoji": "📡",
        "titulo": "XV Plan Quinquenal: 6G, robótica, IA y biotech como pilares del desarrollo 2026-2030",
        "cuerpo": (
            "El XV Plan Quinquenal (2026-2030) sitúa las 'Nuevas Fuerzas Productivas de Calidad' en "
            "el centro de la estrategia nacional. Las 10 tecnologías emergentes prioritarias: IA, "
            "robótica, 6G, computación cuántica, hidrógeno, biotecnología, materiales avanzados, "
            "economía de baja altitud (drones), semiconductores y energía de fusión. Las industrias "
            "emergentes suman ya 6 billones de yuanes y aspiran a 10 billones para 2030. El "
            "presupuesto en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones de yuanes. "
            "China no solo quiere liderar estas tecnologías: quiere que sean el motor de su "
            "desarrollo económico en las próximas dos décadas."
        ),
        "fuente_label": "Mundo Global — Oportunidad China 2.0: las 10 tecnologías emergentes más importantes",
        "fuente_url": "https://mundoglobal.org/oportunidad-china-2-0-la-inteligencia-artificial-y-las-10-tecnologias-emergentes-que-china-considera-mas-importantes-en-2026/",
    },
]


def build_blocks():
    today_obj = date.today()
    today_str = f"{today_obj.day} de {MESES[today_obj.month]} de {today_obj.year}"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today_str}", "🇨🇳"),
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
    title = "China Al Dia — Semana 22-28 Junio 2026"
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
