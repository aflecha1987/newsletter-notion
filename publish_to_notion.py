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
        "titulo": "China rompe récord histórico de comercio exterior: 25,47 billones de yuanes en el primer semestre",
        "cuerpo": (
            "El comercio exterior de China creció un 16,9% interanual en el primer semestre de 2026, según datos "
            "de la Administración General de Aduanas. El valor total de importaciones y exportaciones alcanzó los "
            "25,47 billones de yuanes (≈ 3,75 billones de dólares), superando por primera vez la barrera de los "
            "25 billones en un primer semestre. Las exportaciones sumaron 14,73 billones de yuanes (+13,4%), "
            "manteniendo su crecimiento durante 11 trimestres consecutivos, mientras las importaciones crecieron "
            "un impresionante +22,1%. El comercio con América Latina creció un 16,2% y con África un 19,6%."
        ),
        "fuente_label": "People's Daily Español — Comercio exterior de China crece 16,9% en primer semestre 2026",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0715/c31620-20477940.html",
    },
    {
        "emoji": "💾",
        "titulo": "China produce sus primeros equipos de litografía DUV: paso clave hacia la autosuficiencia en chips",
        "cuerpo": (
            "China habría comenzado la producción de equipos nacionales de litografía por ultravioleta profundo "
            "(DUV) de inmersión, según Reuters. De confirmarse su rendimiento industrial, el avance representaría "
            "un salto histórico en la estrategia de Pekín para liberarse de la dependencia de proveedores "
            "extranjeros de equipos para la fabricación de semiconductores. Los fabricantes chinos de chips "
            "también presentaron en la mayor conferencia de IA del país el Huawei Atlas 950 SuperPoD, "
            "descrito como el mayor supernodo de IA industrial del mundo."
        ),
        "fuente_label": "Destino Panamá — China da un paso clave hacia la autosuficiencia en chips",
        "fuente_url": "https://destinopanama.com.pa/2026/07/china-da-un-paso-clave-hacia-la-autosuficiencia-en-chips/",
    },
    {
        "emoji": "🤖",
        "titulo": "Huawei triplicará la producción de chips Ascend: 600.000 unidades IA en 2026",
        "cuerpo": (
            "Huawei planea fabricar aproximadamente 600.000 chips Ascend 910C en 2026, el doble del nivel de "
            "2025. Los fabricantes chinos de chips de IA en conjunto apuntan a triplicar la producción total "
            "del país este año, reduciendo la dependencia de Nvidia. En la conferencia de IA más grande de "
            "China celebrada en julio, decenas de empresas mostraron sus soluciones para clientes que no "
            "pueden acceder a tecnología norteamericana, consolidando el ecosistema de IA chino como "
            "alternativa global."
        ),
        "fuente_label": "Gulf News — Huawei to double output of AI chip as Nvidia wavers in China",
        "fuente_url": "https://gulfnews.com/technology/huawei-to-double-output-of-top-ai-chip-as-nvidia-wavers-in-china-1.500287469",
    },
    {
        "emoji": "⚛️",
        "titulo": "Física cuántica: China reconocida en París por el primer satélite cuántico del mundo",
        "cuerpo": (
            "En una ceremonia celebrada en París el 17 de julio de 2026, fue distinguido el físico de la "
            "Universidad de Ciencia y Tecnología de China cuyo equipo lanzó en 2016 el primer satélite "
            "cuántico del mundo (Micius). El hito marcó el inicio de una era de comunicaciones cuánticas "
            "intercontinentales. Diez años después, China sigue siendo la potencia global líder en "
            "criptografía cuántica y comunicaciones de larga distancia basadas en la mecánica cuántica."
        ),
        "fuente_label": "Tricontinental — Noticias de China No. 32",
        "fuente_url": "https://thetricontinental.org/es/asia/noticias-de-china-no-32/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD se posiciona para reconquistar el título de mayor fabricante de vehículos eléctricos puros",
        "cuerpo": (
            "BYD entregó 557.090 vehículos de batería pura en el segundo trimestre de 2026, posicionándose "
            "para retomar el título de fabricante mundial más vendedor de vehículos completamente eléctricos. "
            "La compañía avanza con su estrategia de expansión internacional con fábricas en Brasil, México "
            "y Europa, y proyecta vender 1,3 millones de vehículos fuera de China en 2026. Europa, "
            "América del Norte y ASEAN representarán aproximadamente un tercio de las ventas exteriores cada una."
        ),
        "fuente_label": "Reporte Asia — BYD Global impulsa la expansión eléctrica en América Latina",
        "fuente_url": "https://reporteasia.com/autos/2026/02/24/byd-global-impulsa-la-expansion-electrica-en-america-latina/",
    },
    {
        "emoji": "⚡",
        "titulo": "La capacidad solar supera al carbón por primera vez en la historia de China",
        "cuerpo": (
            "2026 es el año en que la energía solar de China supera por primera vez a la energía de carbón "
            "en capacidad instalada. Según el Global Electricity Review de Ember, China concentra "
            "aproximadamente la mitad de la capacidad eólica y solar instalada del mundo: más de 641 GW "
            "eólicos y más de 1.200 GW solares. Para finales de 2026, eólica y solar representarán "
            "conjuntamente la mitad de la capacidad total instalada del país, consolidando a China como "
            "la mayor potencia de energías renovables del planeta."
        ),
        "fuente_label": "Ember — Global Electricity Review 2026",
        "fuente_url": "https://ember-energy.org/es/analisis/global-electricity-review-2026/",
    },
    {
        "emoji": "☀️",
        "titulo": "24 plantas de energía solar térmica operativas: 3,2 GW de potencia almacenable",
        "cuerpo": (
            "Según anunció el Consejo de Electricidad de China el 16 de julio, el país cuenta ya con "
            "24 plantas de energía solar térmica (CSP) en funcionamiento, con otras 26 en construcción, "
            "sumando 3,2 gigavatios de capacidad. A diferencia de la solar fotovoltaica convencional, "
            "estas plantas capturan el calor solar en sales fundidas, permitiendo generar electricidad "
            "estable y despachable incluso de noche, lo que las convierte en una solución clave para "
            "la estabilidad de la red eléctrica."
        ),
        "fuente_label": "Tricontinental — Noticias de China No. 32",
        "fuente_url": "https://thetricontinental.org/es/asia/noticias-de-china-no-32/",
    },
    {
        "emoji": "🌙",
        "titulo": "Chang'e-7: China se prepara para explorar el polo sur lunar y buscar agua",
        "cuerpo": (
            "La misión Chang'e-7 avanza hacia su lanzamiento en 2026 con el objetivo de explorar el polo "
            "sur de la Luna, donde se sospecha la presencia de agua en forma de hielo en cráteres de sombra "
            "permanente. La sonda incluye un orbitador, módulo de aterrizaje, rover y una mini-sonda "
            "saltadora capaz de adentrarse en los cráteres más profundos. China planea llevar un astronauta "
            "a la Luna antes de 2030, y la misión Chang'e-7 es un paso fundamental en esa hoja de ruta."
        ),
        "fuente_label": "Chanboox — China mandó una misión para ampliar la experimentación en órbita",
        "fuente_url": "https://www.chanboox.com/2026/05/26/china-mando-una-mision-que-busca-ampliar-el-tiempo-de-experimentacion-en-orbita/",
    },
    {
        "emoji": "🛸",
        "titulo": "China construye la industria satelital más ágil del mundo: hasta 5.000 satélites en emergencia",
        "cuerpo": (
            "Un informe publicado el 29 de julio revela que China está preparando una industria espacial "
            "capaz de fabricar entre 4.100 y 5.000 satélites ante situaciones de emergencia. El número "
            "de empresas chinas activas en el espacio creció de unas pocas docenas a más de 600 compañías "
            "desde la apertura a la inversión privada en 2014. La Universidad de Ciencias de la Academia "
            "China (UCAS) acaba de inaugurar su Escuela de Exploración Espacial, la primera de su tipo "
            "en el país."
        ),
        "fuente_label": "Espacio Tech — China prepara industria espacial de alto rendimiento",
        "fuente_url": "https://www.espaciotech.net/2026/07/29/china-prepara-una-industria-espacial-capaz-de-fabricar-entre-4-100-y-5-000-de-satelites-durante-una-guerra",
    },
    {
        "emoji": "🚄",
        "titulo": "El tren más rápido del mundo entra en servicio: CR450 une Pekín-Shanghái en menos de 2h30",
        "cuerpo": (
            "El CR450, el tren bala más rápido construido hasta la fecha, comienza su despliegue operacional "
            "completo en 2026. Circulará a velocidades de crucero superiores a los 400 km/h, reduciendo el "
            "trayecto entre Pekín y Shanghái (1.300 km) a menos de 2 horas y 30 minutos. China ya supera "
            "los 50.000 kilómetros de red ferroviaria de alta velocidad, más que el resto del mundo "
            "combinado, y exporta su tecnología a América Latina, Europa y Asia."
        ),
        "fuente_label": "Excélsior — China supera los 50 mil kilómetros de trenes de alta velocidad",
        "fuente_url": "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico",
    },
    {
        "emoji": "🌊",
        "titulo": "Tren submarino bajo el estrecho de Bohai: 40 minutos entre Dalian y Yantai",
        "cuerpo": (
            "China avanza en uno de sus proyectos de infraestructura más ambiciosos: un tren de alta "
            "velocidad submarino que atravesará el estrecho de Bohai a 300 km/h, conectando las ciudades "
            "de Dalian y Yantai en 40 minutos (frente a las 6 horas actuales por carretera). El proyecto, "
            "valorado en unos 36.000 millones de dólares, incorporará sensores inteligentes para detectar "
            "filtraciones y presión, ventilación inteligente y centros de monitoreo gestionados por IA."
        ),
        "fuente_label": "El Tiempo — China acelera bajo el mar: el tren bala submarino",
        "fuente_url": "https://www.eltiempo.com/mundo/asia/china-acelera-bajo-el-mar-el-tren-bala-submarino-que-superara-los-250-km-h-y-unira-dos-ciudades-clave-en-tiempo-record-3553175",
    },
    {
        "emoji": "🤝",
        "titulo": "Xi Jinping y el presidente de Kazajistán firman acuerdos bilaterales en Shanghai",
        "cuerpo": (
            "El 16 de julio, Xi Jinping se reunió con el presidente de Kazajistán en Shanghai, donde ambos "
            "mandatarios presenciaron la firma de múltiples acuerdos bilaterales en economía, comercio, "
            "transporte, finanzas y comunicación. Xi Jinping destacó el potencial de la asociación "
            "estratégica integral permanente entre los dos países, abogando por alinear sus estrategias "
            "de desarrollo en energía, conectividad y las llamadas nuevas fuerzas productivas de calidad."
        ),
        "fuente_label": "Observatorio de Política China — Cronología julio 2026",
        "fuente_url": "https://www.politica-china.org/cronologia-opch-121/",
    },
    {
        "emoji": "🌍",
        "titulo": "Wang Yi en Europa: gira por Dinamarca, Finlandia y Noruega para fortalecer lazos",
        "cuerpo": (
            "Del 2 al 8 de julio, el ministro de Asuntos Exteriores de China, Wang Yi, visitó Dinamarca, "
            "Finlandia y Noruega para fortalecer la cooperación bilateral en comercio, innovación, "
            "transición ecológica y multilateralismo. China también presentó propuestas concretas para "
            "consolidar el Área de Libre Comercio China-ASEAN 3.0 y el acuerdo RCEP en la Reunión de "
            "Ministros de Asuntos Exteriores China-ASEAN, buscando fortalecer el multilateralismo frente "
            "a las tensiones comerciales globales."
        ),
        "fuente_label": "Observatorio de Política China — Resumen de política exterior julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-67/",
    },
    {
        "emoji": "👷",
        "titulo": "30 millones de trabajadores de plataformas digitales ya cuentan con seguro laboral en toda China",
        "cuerpo": (
            "Desde el 1 de julio de 2026, el seguro de accidentes laborales para trabajadores de "
            "plataformas digitales (repartidores, conductores y similares) se extendió a todas las "
            "31 regiones de nivel provincial de China. El sistema, financiado por las plataformas y "
            "complementado por el Estado, ya cubre a casi 30 millones de personas, convirtiéndose en "
            "el programa de protección social para trabajadores de la economía de plataformas más "
            "grande del mundo."
        ),
        "fuente_label": "Tricontinental — Noticias de China No. 32",
        "fuente_url": "https://thetricontinental.org/es/asia/noticias-de-china-no-32/",
    },
    {
        "emoji": "🧬",
        "titulo": "Biotecnología china: el 28% de los acuerdos globales de licencias farmacéuticas vienen de China",
        "cuerpo": (
            "Las empresas chinas de biotecnología han pasado de desarrollar productos 'me-too' a generar "
            "activos diferenciados de primer orden. En 2024, aproximadamente el 28% de los acuerdos de "
            "licencias cerrados por grandes farmacéuticas globales provinieron de biotechs chinas, con un "
            "valor total superior a 41.000 millones de dólares. China ya representa cerca del 30% de la "
            "actividad biofarmacéutica global, y sus empresas son cada vez más protagonistas en ensayos "
            "clínicos internacionales. La feria CMEF 2026 concluyó en Shanghai como el mayor escaparate "
            "mundial de innovación médica."
        ),
        "fuente_label": "PR Newswire — CMEF 2026 concluye en Shanghai",
        "fuente_url": "https://www.prnewswire.com/news-releases/cmef-2026-concluye-en-shanghai-un-escenario-global-para-los-avances-medicos-y-las-tendencias-futuras-302759219.html",
    },
]


def build_blocks():
    today = "30 de julio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, infraestructura y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 24-30 Julio 2026"
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
