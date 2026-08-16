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
        "emoji": "📦",
        "titulo": "China bate todos sus récords comerciales: exportaciones +23,9 % en julio impulsadas por la IA",
        "cuerpo": (
            "Los datos de aduanas publicados esta semana confirman que las exportaciones chinas crecieron "
            "un 23,9 % interanual en julio, superando las previsiones del consenso (22,2 %). El motor "
            "de este crecimiento son los componentes tecnológicos vinculados a la inteligencia artificial: "
            "las exportaciones de semiconductores registraron un crecimiento del 116,6 % interanual, "
            "mientras que los envíos de buques (+92,4 %) y automóviles (+60,4 %) también batieron marcas. "
            "El total de importaciones y exportaciones de China entre enero y julio alcanza ya los "
            "4,4 billones de dólares, un incremento del 17,3 % respecto al mismo período de 2025."
        ),
        "fuente_label": "Forbes España — Exportaciones chinas +23,9 % en julio",
        "fuente_url": "https://forbes.es/ultima-hora/996226/las-exportaciones-chinas-crecieron-un-239-en-julio-aupadas-por-las-ventas-tecnologicas/",
    },
    {
        "emoji": "🤖",
        "titulo": "China domina el 90 % del mercado mundial de robots humanoides",
        "cuerpo": (
            "Según un análisis de Rest of World y datos de WAIC 2026, las empresas chinas controlan ya "
            "el 90 % del mercado global de robots humanoides. Unitree y AgiBot lideran el sector "
            "replicando el playbook de los vehículos eléctricos: producción masiva, economías de escala "
            "y costes un 40-60 % inferiores a sus competidores occidentales. El gobierno nacional ha "
            "fijado el objetivo de 100.000 robots humanoides desplegados en fábricas e instalaciones "
            "para 2027. Hoy, operar a entre un 30 y 50 % de la eficiencia humana es suficiente para "
            "que muchas empresas los adopten en tareas de almacén y logística."
        ),
        "fuente_label": "Rest of World — China winning the humanoid robot race",
        "fuente_url": "https://restofworld.org/2026/china-humanoid-robots-unitree-agibot-tesla-optimus/",
    },
    {
        "emoji": "☀️",
        "titulo": "China lanza dos alianzas industriales para la energía solar espacial",
        "cuerpo": (
            "Durante la feria SNEC 2026 en Shanghai, China constituyó dos nuevas alianzas industriales "
            "para acelerar la energía solar basada en el espacio y las tecnologías de perovskita. La "
            "Space Energy Development Alliance agrupa a empresas de paneles solares, almacenamiento, "
            "hidrógeno, centros de datos e industria aeroespacial. Ya en mayo de 2026, el proyecto "
            "Zhuri (Perseguir el Sol) logró la primera transmisión inalámbrica de potencia en microondas "
            "de uno a muchos blancos en movimiento simultáneamente, convirtiendo a China en el único "
            "país con un sistema completo de este tipo."
        ),
        "fuente_label": "SAURenergy — China lanza alianzas de energía solar espacial",
        "fuente_url": "https://www.saurenergy.com/solar-energy-news/china-launches-two-space-energy-alliances-to-advance-space-based-solar-technologies-11902998",
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e-7 lista en Wenchang: ventana de lanzamiento abre el 24 de agosto",
        "cuerpo": (
            "La misión lunar Chang'e-7 de China ha completado su traslado al cosmódromo de Wenchang y "
            "está en preparación final para su lanzamiento a bordo de un Long March 5. La ventana de "
            "lanzamiento abre el 24 de agosto de 2026 y se extiende hasta el 31. La misión incluye un "
            "orbitador, un módulo de aterrizaje, un rover y una sonda 'saltarina' diseñada para descender "
            "a cráteres permanentemente en sombra del polo sur lunar en busca de hielo de agua. Chang'e-7 "
            "es el precursor de la Chang'e-8 (2029) y ambas son pilares de la futura Base Internacional "
            "de Investigación Lunar de cara al alunizaje tripulado previsto para 2030."
        ),
        "fuente_label": "SpaceNews — Chang'e-7 arrives at Wenchang for lunar south pole mission",
        "fuente_url": "https://spacenews.com/chinas-change-7-arrives-at-spaceport-for-lunar-south-pole-exploration-mission/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD exporta un récord de 179.841 vehículos en julio, +124 % interanual",
        "cuerpo": (
            "BYD cerró julio de 2026 con sus mejores cifras de exportación en la historia de la compañía: "
            "179.841 vehículos enviados al exterior, un 124,3 % más que en julio de 2025 y 5.000 unidades "
            "por encima de su anterior récord de junio. Las ventas globales totales alcanzaron 419.211 "
            "unidades, un +21,8 % interanual, con el crecimiento impulsado casi íntegramente desde los "
            "mercados internacionales. BYD ha revisado al alza su objetivo anual de exportaciones a "
            "1,5 millones de vehículos para 2026, frente a los 1,05 millones exportados en 2025."
        ),
        "fuente_label": "CleanTechnica — BYD Achieves Record Exports With 124% Growth",
        "fuente_url": "https://cleantechnica.com/2026/08/04/byd-achieves-record-exports-with-124-growth/",
    },
    {
        "emoji": "🌏",
        "titulo": "China presidirá APEC 2026 en Shenzhen: reunión de altos funcionarios en Dalian este mes",
        "cuerpo": (
            "China ejerce este año la presidencia de la Cooperación Económica Asia-Pacífico (APEC) con "
            "la cumbre de líderes programada en Shenzhen los días 18 y 19 de noviembre. En agosto, los "
            "representantes de las 21 economías miembro se reúnen en Dalian para las reuniones de altos "
            "funcionarios. La agenda prioritaria de China incluye la creación del Área de Libre Comercio "
            "de Asia-Pacífico (FTAAP), la digitalización del comercio y la integración de cadenas de "
            "suministro regionales. El comercio de China con las economías APEC representó el 57,8 % "
            "de su comercio exterior total en 2025."
        ),
        "fuente_label": "Empresa Exterior — China asume la presidencia de APEC 2026",
        "fuente_url": "https://empresaexterior.com/art/101322/china-asume-la-presidencia-de-apec-2026-con-el-objetivo-de-impulsar-el-area-de-libre-comercio-de-asia-pacifico-ftaap",
    },
    {
        "emoji": "🚄",
        "titulo": "Tren maglev chino marca un nuevo récord: 800 km/h desde cero en 5,3 segundos",
        "cuerpo": (
            "En el Laboratorio Donghu, en la provincia de Hubei, un prototipo de tren de levitación "
            "magnética alcanzó los 800 km/h en apenas 5,3 segundos, estableciendo un nuevo récord "
            "mundial de aceleración. La pista de pruebas, de un kilómetro de longitud, opera en un "
            "tubo de vacío parcial para eliminar la resistencia aerodinámica. Más allá del transporte, "
            "los investigadores apuntan a aplicaciones en lanzamiento de satélites y sistemas de "
            "proyectiles hipersónicos de bajo coste. China cuenta ya con más de 50.000 kilómetros de "
            "red ferroviaria de alta velocidad convencional, la mayor del mundo."
        ),
        "fuente_label": "Yahoo Noticias — Tren maglev chino alcanza 800 km/h en 5,3 segundos",
        "fuente_url": "https://es-us.noticias.yahoo.com/tren-experimental-chino-alcanza-los-800-kmh-en-segundos-y-habria-establecido-un-nuevo-record-mundial-225623515.html",
    },
    {
        "emoji": "🏗️",
        "titulo": "La mayor tuneladora del mundo completa 11,18 km bajo el río Yangtsé en 23 meses",
        "cuerpo": (
            "Tras 23 meses de perforación ininterrumpida, la tuneladora de 4.000 toneladas más grande "
            "del mundo ha completado los 11,18 kilómetros del túnel ferroviario que une la isla Chongming "
            "con Shanghai, reduciendo el trayecto entre ambos puntos a 17 minutos. El proyecto forma "
            "parte de la línea de alta velocidad Shenzhen-Jiangmen, de 116 km, que cuando esté operativa "
            "conectará las dos ciudades en menos de una hora. La tuneladora retomará el tramo final, "
            "con 1,8 km restantes, a finales de agosto, con el calendario apuntando a la perforación "
            "completa a finales de 2026."
        ),
        "fuente_label": "ECOticias — Tuneladora completa 11,18 km bajo el río Yangtsé",
        "fuente_url": "https://www.ecoticias.com/hoyeco/tras-23-meses-de-excavacion-sin-parar-la-mayor-tuneladora-ferroviaria-del-mundo-de-4-000-toneladas-completa-1118-kilometros-bajo-el-yangtse-y-reduce-a-17-minutos-el-trayecto-chongming-shanghai/38243/",
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

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Semana 10-16 Ago 2026 · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 10-16 Ago 2026"
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
