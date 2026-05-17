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
        "emoji": "🤝",
        "titulo": "Cumbre histórica Trump-Xi en Pekín: China anuncia apertura para empresas tecnológicas",
        "cuerpo": (
            "Los días 13 y 14 de mayo de 2026, Donald Trump y Xi Jinping se reunieron en Pekín en la "
            "primera visita de un presidente estadounidense a China en más de una década. Xi recibió a "
            "Elon Musk, Tim Cook y otros CEOs con el mensaje de que China 'abrirá más' sus puertas a "
            "los negocios. Los acuerdos preliminares incluyen la creación de un Consejo de Inversión "
            "conjunto, la adquisición china de 200 aviones Boeing, la ampliación del comercio agrícola "
            "y pasos concretos para estabilizar las relaciones arancelarias entre las dos primeras "
            "economías del mundo. Ambas potencias reconocieron que la IA y la tecnología serán el "
            "campo de competición del siglo XXI, pero optaron por el diálogo frente al conflicto."
        ),
        "fuente_label": "CNBC — Xi tells Musk, Tim Cook and other CEOs: China will 'open wider'",
        "fuente_url": "https://www.cnbc.com/2026/05/14/xi-china-open-us-business-ai-chips.html",
    },
    {
        "emoji": "🧠",
        "titulo": "El plan IA de Xi: 'inteligencia artificial' aparece más de 50 veces en el Plan Quinquenal",
        "cuerpo": (
            "El análisis del 15.º Plan Quinquenal (2026-2030) revela que el término 'inteligencia "
            "artificial' aparece más de 50 veces. La estrategia 'IA Plus' busca que la IA sea "
            "infraestructura transversal para toda la economía: acelerar la autonomía tecnológica "
            "en todos los sectores, transformar industrias tradicionales y crear nuevos escenarios "
            "de consumo. El plan apunta a que el 70% de la economía productiva integre IA para 2027 "
            "y el 90% para 2030. China ya cuenta con 602 millones de usuarios de IA generativa "
            "—más de la mitad del total mundial—. Las industrias de IA superarán los 10 billones "
            "de yuanes para 2030."
        ),
        "fuente_label": "El Grand Continent — Bastidores del plan de IA de Xi para transformar China",
        "fuente_url": "https://legrandcontinent.eu/es/2026/05/13/bastidores-del-plan-ia-de-xi-para-transformar-china/",
    },
    {
        "emoji": "🤖",
        "titulo": "China encarga 8.500 robots con IA para gestionar la red eléctrica más grande del mundo",
        "cuerpo": (
            "China ha encargado 8.500 robots con inteligencia artificial para gestionar su red eléctrica "
            "nacional, con una inversión de 1.000 millones de dólares solo en 2026. Estos robots "
            "sustituirán a operarios en tareas de alto riesgo: mantenimiento de torres de alta tensión, "
            "subestaciones aisladas y líneas en zonas de difícil acceso. La producción total de robots "
            "con IA en China crecerá un 94% este año, con Unitree Robotics ampliando su capacidad a "
            "75.000 robots humanoides y 115.000 cuadrúpedos anuales. 2026 es considerado el año de "
            "inflexión en que la robótica china pasa de la demostración tecnológica a la "
            "comercialización masiva."
        ),
        "fuente_label": "La Jornada — China apuesta a robots con IA para todo tipo de labores",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/05/10/economia/china-apuesta-a-robots-con-inteligencia-artificial-para-todo-tipo-de-labores",
    },
    {
        "emoji": "🔬",
        "titulo": "China lidera el 90% de las tecnologías cruciales del siglo XXI, según Nature",
        "cuerpo": (
            "Un estudio publicado en la revista Nature concluye que China lidera la investigación en "
            "el 90% de las tecnologías consideradas cruciales para el futuro, un vuelco dramático "
            "respecto a principios de siglo. Los campos donde China domina incluyen energías renovables, "
            "semiconductores en nodos maduros, materiales avanzados, biotecnología y computación cuántica. "
            "El presupuesto en Ciencia y Tecnología creció un 10% en 2026 hasta 426.000 millones de "
            "yuanes, con énfasis especial en investigación básica. Las startups chinas de biotech "
            "lideran globalmente el desarrollo de fármacos de primera generación, según la revista "
            "Science."
        ),
        "fuente_label": "Nature — China leads research in 90% of crucial technologies",
        "fuente_url": "https://www.nature.com/articles/d41586-025-04048-7",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar supera al carbón en capacidad instalada en China",
        "cuerpo": (
            "2026 es el año del cambio de era energética en China: la capacidad instalada de energía "
            "solar ha superado por primera vez a la del carbón, según el Consejo de Electricidad de "
            "China. Junto con la eólica, las renovables representarán la mitad de toda la capacidad "
            "eléctrica del país a finales de 2026. China añadirá este año más de 300 GW de nueva "
            "energía renovable, equivalente a toda la potencia instalada de Alemania. En paralelo, "
            "el país instaló el mayor aerogenerador marino del mundo, de 20 megavatios, capaz de "
            "abastecer a 44.000 hogares. El parque solar del desierto de Kubuqi también está "
            "reverdeciendo tierras áridas mientras genera energía."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "⚛️",
        "titulo": "El 'sol artificial' chino rompe la barrera de fusión nuclear que se creía infranqueable",
        "cuerpo": (
            "El reactor de fusión EAST (conocido como el 'sol artificial' chino) ha superado el "
            "Límite de Greenwald —la barrera de densidad máxima del plasma considerada infranqueable "
            "durante décadas— alcanzando densidades de 1,3 a 1,65 veces por encima del límite. "
            "Los investigadores lograron controlar con precisión el calentamiento del plasma, la "
            "inyección de combustible y la interacción plasma-pared, entrando en un 'régimen libre "
            "de densidad' teóricamente predicho pero nunca antes observado. El logro, publicado en "
            "Science y aclamado por la comunidad científica internacional, abre la puerta a reactores "
            "de fusión mucho más eficientes y acerca la energía de fusión comercial a la realidad."
        ),
        "fuente_label": "IFLScience — China's Artificial Sun Exceeds The Greenwald Limit For The First Time",
        "fuente_url": "https://www.iflscience.com/chinas-artificial-sun-exceeds-the-greenwald-limit-for-the-first-time-breaking-nuclear-fusion-density-record-82202",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 se prepara para explorar el polo sur de la Luna: lanzamiento en agosto de 2026",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 han llegado a la Base Espacial de Wenchang para "
            "las pruebas finales previas al lanzamiento, programado para agosto de 2026. La misión "
            "incluye un orbitador, un módulo de aterrizaje, un rover y una innovadora sonda "
            "mini-saltadora capaz de explorar los cráteres en sombra permanente del polo sur lunar, "
            "donde podría existir agua en forma de hielo. En paralelo, China avanza con la prueba del "
            "cohete reutilizable Larga Marcha 10, pieza clave del programa de alunizaje tripulado "
            "antes de 2030, y la misión Tianwen-2 hacia el asteroide 2016 HO3 ya ha pasado por su "
            "maniobra de acercamiento."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🌾",
        "titulo": "China y EE.UU. acuerdan ampliar comercio agrícola y crear Consejo de Inversión bilateral",
        "cuerpo": (
            "Tras la cumbre de Pekín, los comunicados del 16 de mayo confirman que China y Estados "
            "Unidos acordaron ampliar el comercio agrícola con reducciones arancelarias específicas y "
            "abordar barreras no arancelarias. La compra de 200 aviones Boeing y el acceso ampliado "
            "para empresas tecnológicas estadounidenses son los elementos más concretos. Ambas partes "
            "crearán un Consejo de Inversión y un Consejo Comercial permanentes para seguir negociando "
            "reducciones arancelarias recíprocas. Analistas señalan que, aunque los acuerdos son "
            "'preliminares', representan la mayor distensión comercial entre las dos economías más "
            "grandes del mundo desde 2020."
        ),
        "fuente_label": "La Jornada — China y EU acuerdan ampliar comercio agrícola",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/05/16/economia/china-y-eu-acuerdan-ampliar-comercio-agricola",
    },
    {
        "emoji": "🎓",
        "titulo": "China impulsa la fusión entre educación, ciencia y talento como motor de innovación",
        "cuerpo": (
            "El 7 de mayo, el Gobierno chino presentó su plan para integrar de forma orgánica educación, "
            "ciencia y tecnología, y formación de talento. El plan incluye la creación de centros de "
            "innovación universitaria, la expansión de programas de doctorado aplicado y la atracción "
            "de científicos de la diáspora china. El presupuesto en educación para 2026 asciende a "
            "192.480 millones de yuanes (+5% interanual). El Ministerio de Ciencia y Tecnología "
            "confirma que los jóvenes científicos que regresan al país son ya el principal motor "
            "de los avances en IA, biotecnología y computación cuántica."
        ),
        "fuente_label": "CGTN — China advances fusion of education, sci-tech and talent",
        "fuente_url": "https://news.cgtn.com/news/2026-05-07/China-advances-fusion-of-education-sci-tech-and-talent-1MWXxIaoSGs/share_amp.html",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio y ciencia.", bold=False),
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
    title = "China Al Dia — Semana 11-17 Mayo 2026"
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
