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
    # ── PORTADA ──────────────────────────────────────────────────────────────
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23 en órbita: la primera astronauta de Hong Kong y una misión de un año",
        "cuerpo": (
            "El 24 de mayo, China lanzó la nave Shenzhou-23 con tres astronautas a bordo: el comandante "
            "Zhu Yangzhu, Zhang Zhiyuan y Lai Ka-ying —nacida en Hong Kong y doctora en informática "
            "forense—, que se convierte en la primera astronauta de esa ciudad en el espacio. Uno de "
            "los tres permanecerá en órbita durante un año completo —una de las estancias individuales "
            "más largas en el espacio a escala mundial—, con el objetivo de explorar los límites de la "
            "adaptabilidad humana en vuelos de larga duración. La tripulación ejecutará más de 100 "
            "experimentos científicos en ciencias de la vida, física de fluidos en microgravedad y "
            "medicina aeroespacial."
        ),
        "fuente_label": "NPR — China launches Shenzhou-23 spacecraft",
        "fuente_url": "https://www.npr.org/2026/05/25/g-s1-124179/china-launches-shenzhou-23-spacecraft",
    },
    # ── TECNOLOGÍA ────────────────────────────────────────────────────────────
    {
        "emoji": "⚛️",
        "titulo": "Origin Wukong-180: China presenta su cuarta generación de computadora cuántica",
        "cuerpo": (
            "Origin Quantum puso en línea el Origin Wukong-180, su cuarta generación de computadora "
            "cuántica superconductora, con un chip de 180 qubits computacionales (más 251 qubits de "
            "acoplamiento) y cuatro sistemas de desarrollo íntegramente nacional. La empresa calificó "
            "el hito como el primer paso sistemático para integrar la capacidad cuántica china en el "
            "ecosistema de IA: de ser 'utilizable' a ser 'práctica y accesible'. Su predecesor, el "
            "Wukong de 72 qubits, registró ya cerca de 50 millones de accesos remotos desde más de "
            "160 países."
        ),
        "fuente_label": "Quantum Computing Report — Origin Wukong-180",
        "fuente_url": "https://quantumcomputingreport.com/origin-quantum-unveils-origin-wukong-180-fourth-generation-quantum-computer/",
    },
    {
        "emoji": "🔬",
        "titulo": "Jiuzhang 4.0 bate el récord mundial de computación cuántica fotónica y lo publica en Nature",
        "cuerpo": (
            "El 14 de mayo, la Universidad de Ciencia y Tecnología de China publicó en la revista Nature "
            "los resultados del prototipo cuántico fotónico Jiuzhang 4.0, que resolvió el problema de "
            "'muestreo bosónico gaussiano' a una velocidad 10⁵⁴ veces mayor que la de la supercomputadora "
            "más potente del mundo. El sistema manipuló y detectó estados cuánticos de hasta 3.050 fotones "
            "—frente a los 255 del Jiuzhang 3.0—, con una eficiencia global del 51%, abriendo la puerta "
            "a futuros procesadores ópticos tolerantes a fallos."
        ),
        "fuente_label": "Xinhua — Jiuzhang 4.0 publicado en Nature",
        "fuente_url": "https://english.news.cn/20260514/db28783f4b34466096e9cde2dd7afecc/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "World Intelligence Expo 2026 en Tianjin: 700 empresas, 150 robots y el auge de la IA encarnada",
        "cuerpo": (
            "El 28 de mayo arrancó en Tianjin la Exposición Mundial de Inteligencia 2026, con más de "
            "700 empresas en 130.000 m² —un récord histórico—. Por primera vez, la inteligencia encarnada "
            "(embodied AI) tuvo su propio pabellón con cerca de 150 robots completos; más de 40 modelos "
            "de lenguaje grande compitieron en una zona dedicada. Un robot realizó una demostración de "
            "enhebrar una aguja ante el público, símbolo de la precisión alcanzada por la robótica china."
        ),
        "fuente_label": "CGTN — World Intelligence Expo 2026 opens in Tianjin",
        "fuente_url": "https://news.cgtn.com/news/2026-05-28/World-Intelligence-Expo-2026-opens-in-Tianjin-1NwnYH5FVJe/p.html",
    },
    # ── CIENCIA Y ESPACIO ─────────────────────────────────────────────────────
    {
        "emoji": "🌕",
        "titulo": "China acelera la carrera lunar: Shenzhou-23 ensaya maniobras para la misión tripulada a la Luna en 2030",
        "cuerpo": (
            "La misión Shenzhou-23 sirve también como banco de pruebas para el programa lunar chino: "
            "el acoplamiento autónomo rápido con el módulo central de Tiangong replica el procedimiento "
            "previsto entre la cápsula Mengzhou y el módulo de alunizaje Lanyue para la misión tripulada "
            "a la Luna en 2030. Beijing ha completado pruebas de seguridad en el cohete Long March-10 "
            "de gran capacidad. China y EE.UU. compiten activamente: NASA apunta a 2028 y China a 2030."
        ),
        "fuente_label": "Manila Times — China accelerates space ambitions",
        "fuente_url": "https://www.manilatimes.net/2026/05/30/business/science-technology/china-accelerates-space-ambitions-as-moon-race-enters-new-lap/2354660",
    },
    # ── ECONOMÍA ──────────────────────────────────────────────────────────────
    {
        "emoji": "📈",
        "titulo": "China crece un 5% en Q1 2026 y sus exportaciones se disparan un 14% interanual",
        "cuerpo": (
            "La economía china creció un 5,0% interanual en el primer trimestre de 2026, superando las "
            "previsiones del 4,8%. Las exportaciones en el primer trimestre alcanzaron los 977.600 "
            "millones de dólares (+14%), con crecimientos del 20% hacia el Sudeste Asiático, 32% hacia "
            "África y 21% hacia la UE. China registró en 2025 un superávit comercial récord de 1,19 "
            "billones de dólares, impulsado por exportaciones totales de 3,77 billones."
        ),
        "fuente_label": "CNN — China GDP Q1 2026",
        "fuente_url": "https://www.cnn.com/2026/04/15/china/china-gdp-q1-economy-growth-intl-hnk",
    },
    {
        "emoji": "🤝",
        "titulo": "Tras la cumbre Trump-Xi: China comprará USD 17.000 millones anuales en productos agrícolas de EE.UU.",
        "cuerpo": (
            "Tras la visita de estado del presidente Trump a Beijing (14-17 de mayo), ambas partes "
            "acordaron la reducción de aranceles en productos específicos, la creación de un Consejo "
            "de Comercio e Inversión bilateral y la compra por parte de China de al menos 17.000 millones "
            "de dólares anuales en productos agrícolas estadounidenses hasta 2028, incluyendo la "
            "reapertura del mercado chino a la carne vacuna y de aves. El déficit comercial de EE.UU. "
            "con China cayó un 32% interanual en 2025."
        ),
        "fuente_label": "Al Jazeera — US says China to buy billions in agricultural goods",
        "fuente_url": "https://www.aljazeera.com/economy/2026/5/18/us-says-china-to-buy-billions-in-agricultural-goods-after-trump-xi-talks",
    },
    # ── INFRAESTRUCTURA ───────────────────────────────────────────────────────
    {
        "emoji": "🚢",
        "titulo": "El segundo crucero fabricado íntegramente en China supera sus pruebas de mar: entrega en noviembre",
        "cuerpo": (
            "El 27 de mayo, el Adora Flora City regresó a Shanghái tras completar con éxito 12 días de "
            "pruebas en el Mar del Este de China. Mide 341 metros, pesa 141.900 toneladas brutas, "
            "cuenta con 2.130 cabinas y capacidad para 5.232 pasajeros. Un equipo de 937 profesionales "
            "de 12 países completó 149 verificaciones en un único viaje. Está prevista su entrega el "
            "6 de noviembre para operar rutas internacionales desde el Puerto de Nansha (Guangzhou)."
        ),
        "fuente_label": "Xinhua — China's second homegrown cruise ship completes sea trial",
        "fuente_url": "https://english.news.cn/20260527/d42395973c4f472a90fb88b86b16ffef/c.html",
    },
    {
        "emoji": "🌉",
        "titulo": "Cierre del tablero del puente Shituo sobre el Yangtze: un hito del ferrocarril a 350 km/h",
        "cuerpo": (
            "El 28-29 de mayo se completó el cierre del tablero ferroviario del puente Shituo sobre "
            "el río Yangtze (Chongqing), uno de los puentes atirantados ferroviarios más largos del "
            "mundo: 1.416,9 metros de longitud total y 608 metros de vano central. La obra forma parte "
            "de la línea de alta velocidad Chongqing-Wanzhou (251 km, 350 km/h) que reducirá el viaje "
            "entre ambas ciudades a menos de una hora. Es parte de la gran arteria Shanghái-Chengdu "
            "a lo largo del Yangtze."
        ),
        "fuente_label": "CGTN — Final section of new 1.5 km bridge over Yangtze installed",
        "fuente_url": "https://news.cgtn.com/news/2026-05-29/Final-section-of-new-1-5-km-bridge-over-Yangtze-River-installed-1Nx7NQRfIXK/p.html",
    },
    {
        "emoji": "🏗️",
        "titulo": "216.800 millones de yuanes para 336 proyectos estratégicos de infraestructura",
        "cuerpo": (
            "A finales de mayo, la Comisión Nacional de Desarrollo y Reforma asignó el segundo lote "
            "de proyectos del año, distribuyendo 216.800 millones de yuanes en bonos especiales de "
            "ultra-largo plazo para 336 proyectos de las 'Seis Redes' (ferrocarriles, carreteras, "
            "redes eléctricas, de computación, de agua y tuberías). La inversión total en infraestructura "
            "creció un 8,9% interanual en el primer trimestre de 2026."
        ),
        "fuente_label": "Xinhua — China assigns ultra-long treasury bonds for major projects",
        "fuente_url": "https://english.news.cn/20260525/24a8cb319d154c569671f5ea2a870c26/c.html",
    },
    # ── ENERGÍA ───────────────────────────────────────────────────────────────
    {
        "emoji": "🌬️",
        "titulo": "China conecta la primera turbina eólica marina de 20 MW del mundo: suficiente para 44.000 hogares",
        "cuerpo": (
            "China Three Gorges Corporation instaló y conectó a la red la primera turbina eólica marina "
            "de 20 megavatios del mundo, en las aguas de Fujian. El sistema puede generar más de 80 "
            "millones de kWh anuales, suficiente para abastecer a 44.000 hogares. Las energías limpias "
            "ya representan más del 52% de la capacidad eléctrica instalada total de China en 2026."
        ),
        "fuente_label": "Marine Insight — World's first 20 MW offshore wind turbine connected to the grid",
        "fuente_url": "https://www.marineinsight.com/know-more/worlds-first-20-megawatt-offshore-wind-turbine-connected-to-the-grid/",
    },
    # ── DIPLOMACIA ────────────────────────────────────────────────────────────
    {
        "emoji": "✈️",
        "titulo": "China amplía el acceso sin visado a cinco países de América Latina: Brasil, Argentina, Chile, Perú y Uruguay",
        "cuerpo": (
            "China extendió la política de exención de visado de 30 días a los ciudadanos de Brasil, "
            "Argentina, Chile, Perú y Uruguay, en el marco del cuarto encuentro ministerial del Foro "
            "China-CELAC en Beijing. Con esta ampliación, China ofrece entrada sin visado unilateral "
            "a 43 países. La medida va acompañada de un aumento a 24 vuelos semanales directos entre "
            "China y América Latina."
        ),
        "fuente_label": "SCMP — China expands visa-free travel to 5 Latin American nations",
        "fuente_url": "https://www.scmp.com/news/china/diplomacy/article/3310515/china-expands-visa-free-travel-5-latin-american-nations-after-summit-regional-bloc",
    },
    {
        "emoji": "🌏",
        "titulo": "China presidirá el APEC 2026: segunda reunión de altos funcionarios consolida la agenda regional",
        "cuerpo": (
            "China, como anfitrión del APEC 2026, celebró en Shanghái (18-19 de mayo) la segunda "
            "Reunión de Altos Funcionarios, sentando las bases para la reunión de líderes del segundo "
            "semestre. Beijing impulsa la agenda de la 'Zona de Libre Comercio de Asia-Pacífico' y "
            "refuerza su rol de potencia diplomática como mediador y promotor del comercio Sur-Sur."
        ),
        "fuente_label": "Observatorio de Política China — Resumen política exterior",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-4/",
    },
    # ── SOCIEDAD ──────────────────────────────────────────────────────────────
    {
        "emoji": "🏘️",
        "titulo": "Reforma histórica: China elimina la barrera del hukou para 250 millones de migrantes internos",
        "cuerpo": (
            "El Consejo de Estado emitió en mayo directrices históricas para garantizar que los "
            "residentes sin registro de hogar local (hukou) accedan a los mismos servicios públicos "
            "que los residentes registrados —una barrera que afectaba principalmente a los migrantes "
            "internos desde hace décadas—. La reforma abarca educación, vivienda, seguro social, "
            "atención médica y asistencia a mayores. Según estimaciones oficiales, puede beneficiar "
            "directamente a 250 millones de personas, pieza clave de la estrategia de 'nueva "
            "urbanización centrada en las personas' del 15.º Plan Quinquenal."
        ),
        "fuente_label": "Xinhua — China to ensure equal access to basic public services for all residents",
        "fuente_url": "https://english.news.cn/20260522/0b01863270924ccaaf34fe5335ad0ee8/c.html",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana (26-30 mayo 2026): tecnologia cuantica, espacio, economia, infraestructura, energia limpia, diplomacia y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 26-30 Mayo 2026"
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
