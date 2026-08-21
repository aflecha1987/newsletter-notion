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
        "emoji": "🌕",
        "titulo": "Chang'e 7: China se prepara para ser la primera en llegar al polo sur lunar",
        "cuerpo": (
            "El 19 de agosto, China trasladó verticalmente la sonda Chang'e-7 y el cohete Long March 5 "
            "Y14 a su plataforma de lanzamiento en Wenchang, Hainan. El lanzamiento está previsto para "
            "el próximo domingo, lo que convertiría a China en el primer país en colocar una sonda en "
            "el polo sur lunar. La misión incluye un orbitador, un módulo de aterrizaje, un rover y un "
            "miniexplorador 'saltador' capaz de descender a cráteres en sombra permanente en busca de "
            "hielo de agua. Está diseñada para operar al menos ocho años e incluye instrumentos de "
            "Egipto, Baréin, Suiza, Rusia, Tailandia, Italia y Estados Unidos."
        ),
        "fuente_label": "Xinhua — China prepara el lanzamiento de la sonda Chang'e-7",
        "fuente_url": "https://english.news.cn/20260819/449ddc15c79749c5a560903d30a27cf4/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Conferencia Mundial de Robótica 2026: más de 150 nuevos productos en Beijing",
        "cuerpo": (
            "Del 19 al 23 de agosto, Beijing acoge la World Robot Conference 2026, con más de 300 "
            "empresas y 2.000 productos, con foco en humanoides listos para el trabajo real. Leju muestra "
            "humanoides que ya operan en fábricas europeas y plantas automotrices; Robotera tiene más de "
            "100 robots clasificadores en 15 almacenes de China Post; Unitree exhibe prototipos que "
            "boxean y bailan. El Ministerio de Industria se ha fijado el objetivo de instalar 10.000 "
            "humanoides en fábricas chinas antes de que finalice 2026."
        ),
        "fuente_label": "Espacio Tech — China presenta más de 150 nuevos productos robóticos en Beijing",
        "fuente_url": "https://www.espaciotech.net/2026/08/19/avanza-la-era-de-los-robots-china-presento-mas-de-150-nuevos-productos-roboticos-en-beijing/",
    },
    {
        "emoji": "🧠",
        "titulo": "Alibaba lanza Qwen3.8-27B: su modelo de IA ligero iguala a GPT y DeepSeek",
        "cuerpo": (
            "Alibaba presentó Qwen3.8-27B, un modelo de inteligencia artificial ligero que en benchmarks "
            "independientes alcanza el rendimiento de modelos mucho mayores, incluidos OpenAI, DeepSeek "
            "y Zhipu AI. El modelo es de código abierto y está diseñado para correr en hardware de "
            "consumo, democratizando el acceso a la IA de alto rendimiento. Las acciones del índice "
            "STAR 50 acumulan una subida del 29 % en lo que va de 2026, reflejo del apetito inversor "
            "por la carrera china de la IA."
        ),
        "fuente_label": "Bloomberg — China's High-Tech Boom",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-08-14/china-s-high-tech-boom-seen-failing-to-halt-slowdown-of-economy",
    },
    {
        "emoji": "🦾",
        "titulo": "El 55 % de los expositores de robótica en eventos internacionales son chinos",
        "cuerpo": (
            "Un análisis publicado esta semana revela que las empresas chinas representan ya el 55 % de "
            "todos los expositores de robots humanoides en ferias tecnológicas de primer nivel celebradas "
            "fuera de China. La cifra refleja la agresiva estrategia de internacionalización de la "
            "industria robótica del país, impulsada por una base de manufactura sin parangón y subsidios "
            "públicos estratégicos. China consolida así su liderazgo en un sector que se perfila como "
            "uno de los mayores mercados industriales de las próximas décadas."
        ),
        "fuente_label": "Yahoo Tech — Humanoid showdown: Chinese firms 55% of exhibitors",
        "fuente_url": "https://tech.yahoo.com/articles/humanoid-showdown-chinese-firms-55-095315163.html",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones chinas crecen un 23,9 % en julio, impulsadas por tecnología e IA",
        "cuerpo": (
            "Las exportaciones de China alcanzaron 397.852 millones de dólares en julio de 2026, un "
            "+23,9 % interanual. La demanda global de componentes tecnológicos ligados a la inteligencia "
            "artificial fue el principal motor. El superávit comercial mensual alcanzó 112.500 millones "
            "de dólares, el tercer mes consecutivo por encima de los 100.000 millones. El superávit "
            "acumulado en el año supera ya los 687.000 millones de dólares, un récord histórico."
        ),
        "fuente_label": "Forbes España — Exportaciones chinas crecen 23,9 % en julio",
        "fuente_url": "https://forbes.es/ultima-hora/996226/las-exportaciones-chinas-crecieron-un-239-en-julio-aupadas-por-las-ventas-tecnologicas/",
    },
    {
        "emoji": "🏭",
        "titulo": "Equipos electrónicos lideran la producción industrial china con un +19 % en julio",
        "cuerpo": (
            "En julio de 2026, la producción industrial de China creció un 4,5 % interanual, con el "
            "sector de equipos electrónicos como gran protagonista: su producción se disparó más de un "
            "19 %. El dato confirma que la transformación hacia la fabricación de alto valor está en "
            "marcha: mientras sectores tradicionales muestran señales de desaceleración, las industrias "
            "ligadas a la IA, los semiconductores y la electrónica de precisión continúan su expansión "
            "a doble dígito."
        ),
        "fuente_label": "Mundo Ejecutivo — China: alta tecnología amortigua desaceleración",
        "fuente_url": "https://mundoejecutivocdmx.com/tecnologia/china-alta-tecnologia-desaceleracion-economia/",
    },
    {
        "emoji": "🚀",
        "titulo": "53 misiones espaciales en 2026: China rompe todos sus récords de lanzamientos",
        "cuerpo": (
            "China ha completado ya 53 misiones espaciales desde enero hasta mediados de agosto de 2026, "
            "el año más activo en la historia del programa espacial chino. Muchas incorporan inteligencia "
            "artificial embarcada para procesamiento de datos en órbita y prueban tecnologías de "
            "computación espacial de próxima generación. La hoja de ruta incluye cohetes reutilizables, "
            "nuevas estaciones de lanzamiento y la ampliación de la Estación Espacial Tiangong, que "
            "sigue acogiendo tripulaciones en rotación continua."
        ),
        "fuente_label": "NASASpaceFlight — China roundup agosto 2026",
        "fuente_url": "https://www.nasaspaceflight.com/2026/08/china-roundup-20260813/",
    },
    {
        "emoji": "🌱",
        "titulo": "La alta tecnología impulsa el superávit: China consolida su nuevo modelo exportador",
        "cuerpo": (
            "Un análisis del 20 de agosto destaca que el modelo exportador de China ha completado su "
            "transición hacia productos de alto valor añadido. El 'nuevo trío' exportador —vehículos "
            "eléctricos, baterías de litio y paneles solares— continúa su expansión global, mientras "
            "la modernización industrial garantiza competitividad estructural. Tres meses consecutivos "
            "con superávit comercial superior a los 100.000 millones de dólares confirman que el modelo "
            "es sostenible y que las restricciones de terceros países no han logrado frenar el dinamismo "
            "exportador chino."
        ),
        "fuente_label": "Sputnik Mundo — La modernización industrial impulsa el superávit de China",
        "fuente_url": "https://noticiaslatam.lat/20260820/la-modernizacion-industrial-y-la-alta-tecnologia-impulsan-el-superavit-comercial-de-china-dice-1174735241.html",
    },
    {
        "emoji": "💡",
        "titulo": "Innovación inteligente en China: IA que mejora la vida cotidiana en 20 provincias",
        "cuerpo": (
            "Un especial de Xinhua publicado el 19 de agosto recorre cómo la IA y la innovación "
            "tecnológica mejoran la vida en China: desde sistemas de diagnóstico médico en zonas rurales "
            "hasta gestión inteligente del tráfico, agricultura de precisión y ciudades con redes "
            "energéticas autoadaptativas. El artículo documenta casos concretos en más de 20 provincias "
            "y sirve de balance del ambicioso plan de innovación del XIV Plan Quinquenal, cuya ejecución "
            "concluye en 2025."
        ),
        "fuente_label": "Xinhua en español — Innovación inteligente en China",
        "fuente_url": "http://spanish.xinhuanet.com/20260819/1b7ab48dc67b4bed8d7f2b803cda7a0d/c.html",
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
    title = "China Al Dia — Semana 14-21 Ago 2026"
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
