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
        "emoji": "🚀",
        "titulo": "Shenzhou-23: China envía a un astronauta por un año al espacio en carrera hacia la Luna",
        "cuerpo": (
            "El 24 de mayo de 2026, China lanzó con éxito la misión Shenzhou-23 desde el Centro de "
            "Lanzamiento de Satélites de Jiuquan. Un taikonauta permanecerá 365 días en la Estación "
            "Espacial China (Tiangong), el período más largo de la historia del programa espacial chino. "
            "El objetivo: preparar al cuerpo humano para los viajes interplanetarios de cara al aterrizaje "
            "lunar tripulado antes de 2030. La CNSA confirmó también el lanzamiento de Chang'e-7 en agosto, "
            "rumbo al polo sur lunar donde se sospecha la existencia de agua en forma de hielo, y los "
            "ensayos del cohete reutilizable Larga Marcha-10, pieza clave del programa lunar."
        ),
        "fuente_label": "Infobae — Shenzhou-23: un año en órbita, paso decisivo hacia la Luna",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/24/un-ano-en-orbita-china-da-un-paso-decisivo-en-su-programa-lunar-con-el-lanzamiento-de-la-mision-shenzhou-23/",
    },
    {
        "emoji": "🧠",
        "titulo": "Kimi K2.6 supera a GPT-5 y Claude en benchmarks: la IA china marca nuevos récords globales",
        "cuerpo": (
            "Moonshot AI (respaldada por Alibaba) lanzó Kimi K2.6, el modelo de lenguaje de código abierto "
            "más avanzado de China. En SWE-Bench Pro —la prueba estándar de resolución de problemas reales "
            "de software— obtiene 58,6 puntos, frente a los 57,7 de GPT-5.4 y los 53,4 de Claude Opus 4.6, "
            "situándose como el modelo más capaz del mundo en este segmento. Su característica estrella es "
            "la ejecución autónoma sostenida: puede mantener procesos complejos de larga duración sin "
            "intervención humana. Otros modelos chinos también destacan: DeepSeek V4 Pro (87 puntos en el "
            "índice global), GLM-5.1 de Zhipu AI y Qwen3.5 de Alibaba."
        ),
        "fuente_label": "Javadex — Kimi K2.5: el modelo open-source que supera a Claude y GPT-5",
        "fuente_url": "https://www.javadex.es/blog/kimi-k2-5-moonshot-ai-mejor-modelo-open-source-benchmarks-claude-gpt-5-gemini-2026",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree aprobada para cotizar en bolsa: primer fabricante de robots inteligentes en el STAR Market",
        "cuerpo": (
            "El 1 de junio de 2026, la Bolsa de Shanghái aprobó la solicitud de Unitree Robotics (Hangzhou) "
            "para cotizar en el mercado STAR, convirtiéndose en la primera empresa de inteligencia incorporada "
            "(embodied intelligence) en entrar al índice. El proceso duró solo 73 días desde la presentación "
            "—el más rápido bajo el canal fast-track aprobado a mediados de 2025 por la CSRC para empresas "
            "de alta tecnología—. Unitree, reconocida globalmente por sus robots cuadrúpedos y humanoides, "
            "cuenta ya con más de 5.000 unidades humanoides enviadas a clientes reales. La cotización abre "
            "una nueva era para el sector de la robótica china en los mercados de capital."
        ),
        "fuente_label": "Panda Perspectives — China Weekly Wrap: mercados, macro y robótica",
        "fuente_url": "https://pandaperspectives.substack.com/p/china-weekly-wrap-markets-macro-and-2ed/comments",
    },
    {
        "emoji": "🏫",
        "titulo": "China abre la primera 'escuela para robots humanoides' del mundo en Shanghai",
        "cuerpo": (
            "En julio de 2026 abrirá en Shanghái el primer centro de entrenamiento heterogéneo de robots "
            "humanoides del mundo: más de 100 tipos de robots de más de una docena de fabricantes distintos "
            "entrenarán simultáneamente en el mismo espacio, compartiendo datos y experiencias. El sistema "
            "genera 50.000 datos de entrenamiento diarios y funciona como plataforma abierta de intercambio "
            "entre fabricantes. La iniciativa refleja la estrategia china de acelerar la madurez de la "
            "inteligencia incorporada no solo compitiendo entre empresas, sino creando ecosistemas "
            "colaborativos de entrenamiento a escala nacional."
        ),
        "fuente_label": "WWWhatsnew — Primera escuela para robots humanoides en Shanghai",
        "fuente_url": "https://wwwhatsnew.com/2026/05/27/centro-entrenamiento-robots-humanoides-shanghai-china-2026/",
    },
    {
        "emoji": "🏭",
        "titulo": "China lidera el mercado global de robots humanoides: el 85% de las unidades son chinas",
        "cuerpo": (
            "Los robots humanoides chinos representan aproximadamente el 85% de las unidades entregadas "
            "a nivel mundial. De los más de 13.000 humanoides despachados en el último año, AGIBOT y "
            "Unitree enviaron más de 5.000 unidades cada una. Una planta tecnológica en Guangdong ya "
            "produce un robot humanoide completamente funcional cada 30 minutos. China impulsa además la "
            "primera plataforma nacional de gestión del ciclo de vida completo de humanoides —con más de "
            "200 modelos registrados y 28.000 robots catalogados— para garantizar trazabilidad desde la "
            "producción hasta el desmantelamiento."
        ),
        "fuente_label": "LatinUS — Robots humanoides: el ambicioso plan de China para liderar el mercado global",
        "fuente_url": "https://latinus.us/estilo-de-vida/2026/6/6/robots-humanoides-el-ambicioso-plan-de-china-para-liderar-el-mercado-global-175426.html",
    },
    {
        "emoji": "⚖️",
        "titulo": "Nueva ley china de secretos comerciales: protección de datos, algoritmos y extraterritorialidad",
        "cuerpo": (
            "El 1 de junio de 2026 entraron en vigor las nuevas reglas de la SAMR sobre secretos "
            "comerciales, con importantes novedades para la economía digital: extienden la protección a "
            "datos y algoritmos de IA, introducen requisitos de confidencialidad para el trabajo remoto "
            "y la colaboración internacional, y habilitan la aplicación extraterritorial de la ley en "
            "casos que afecten al mercado chino. Las multas pueden alcanzar los 5 millones de yuanes "
            "(aproximadamente 725.000 USD). La medida fortalece el marco legal para empresas de IA y "
            "tecnología que operan en o con China, incrementando la seguridad jurídica de la innovación digital."
        ),
        "fuente_label": "China Research Group Weekly — Secretos comerciales y economía digital",
        "fuente_url": "https://chinaresearchgroupweekly.substack.com/p/crg-weekly-major-tech-deal-blocked/comments",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior de China crece un 15% en Q1 2026: el ritmo más rápido en cinco años",
        "cuerpo": (
            "El comercio exterior chino registró un crecimiento del 15% en el primer trimestre de 2026, "
            "el ritmo más elevado en cinco años. Las exportaciones de bienes crecieron un 18,3% interanual "
            "en enero-febrero (primer crecimiento de doble dígito desde marzo de 2023), y el superávit "
            "comercial en ese período superó los 213.600 millones de dólares. Los principales motores: "
            "maquinaria (+24,3%), semiconductores (+66,5%) y productos electrónicos ligados a la IA. "
            "El PIB creció un 5% interanual en Q1, por encima de las previsiones y el ritmo más rápido "
            "en tres trimestres."
        ),
        "fuente_label": "CGTN Español — Comercio exterior de China crece 15% en el primer trimestre",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-16/2044593566811017217/index.html",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD apunta a 1,3 millones de vehículos eléctricos exportados en 2026",
        "cuerpo": (
            "BYD, el mayor fabricante de vehículos eléctricos del mundo, aspira a vender 1,3 millones "
            "de coches fuera de China en 2026, un crecimiento del 25% frente al objetivo anterior. La "
            "compañía opera ya fábricas de ensamblaje en Hungría y Brasil, con una tercera planta europea "
            "en planificación, y prevé abrir una planta en Karachi (Pakistán) con capacidad inicial de "
            "50.000 vehículos anuales. Las exportaciones chinas de vehículos eléctricos e híbridos "
            "crecieron un 140% interanual en marzo 2026 (349.000 unidades, récord histórico), impulsadas "
            "por la demanda de Asia-Pacífico y América Latina."
        ),
        "fuente_label": "Bloomberg Línea — BYD aspira a vender 1,3 millones de coches fuera de China en 2026",
        "fuente_url": "https://www.bloomberglinea.com/negocios/el-gigante-de-los-vehiculos-electricos-byd-aspira-a-vender-13-millones-de-coches-fuera-de-china-en-2026/",
    },
    {
        "emoji": "☀️",
        "titulo": "Sol artificial EAST: China y la IA aceleran la carrera de la fusión nuclear limpia",
        "cuerpo": (
            "El reactor de fusión EAST (el 'sol artificial' chino) de la Academia China de Ciencias logró "
            "en 2026 una densidad de plasma que la comunidad científica consideraba previamente imposible, "
            "publicado en Science Advances. El dispositivo puede generar temperaturas de hasta 100 millones "
            "de grados centígrados —seis veces más caliente que el núcleo del Sol real—. La integración "
            "de la IA como herramienta de control y simulación está acelerando significativamente el ritmo "
            "de los experimentos. China avanza en paralelo en su plan de doblar su energía no fósil para "
            "2035, con una inversión de 1 billón de yuanes anuales en infraestructura de red."
        ),
        "fuente_label": "ATB Digital — Fusión nuclear: el sol artificial de China y la IA cambian el ritmo",
        "fuente_url": "https://www.atb.com.bo/2026/02/21/fusion-nuclear-por-que-el-sol-artificial-de-china-y-la-ia-estan-cambiando-el-ritmo-de-esta-carrera-energetica/",
    },
    {
        "emoji": "🎬",
        "titulo": "28ª edición del Festival Internacional de Cine de Shanghai con presencia española",
        "cuerpo": (
            "Del 12 al 21 de junio de 2026 se celebra la 28ª edición del Festival Internacional de Cine "
            "de Shanghai (SIFF), el único festival de largometrajes competitivos de categoría A en China "
            "(certificado por la FIAPF). El jurado está presidido por la leyenda del cine de Hong Kong "
            "Tony Leung Chiu-wai. Los premios Cáliz de Oro cubren categorías de competencia principal, "
            "nuevos talentos asiáticos, cortometrajes, animación y documentales. El festival incluye un "
            "FOCUS SPAIN el 21 de junio, con cuatro producciones españolas seleccionadas por el ICAA y "
            "el ICEX, reflejo del creciente interés cultural bilateral entre China y España."
        ),
        "fuente_label": "ICAA / Ministerio de Cultura — Visionado Shanghai International Film Festival 2026",
        "fuente_url": "https://www.cultura.gob.es/cultura/areas/cine/promocion-internacionalizacion/visionados/actualizaciones-visionados/2026/shanghai-26.html",
    },
    {
        "emoji": "🌏",
        "titulo": "APEC 2026 en Shenzhen: China impulsa gobernanza global de la IA y cadenas de suministro",
        "cuerpo": (
            "El 18 y 19 de noviembre de 2026, Shenzhen acogerá la 33ª Cumbre de Líderes Económicos del "
            "APEC, bajo el lema 'Construir una comunidad Asia-Pacífico para prosperar juntos'. A lo largo "
            "del año se celebrarán más de 300 reuniones y eventos del APEC en distintas ciudades chinas. "
            "Los tres ejes temáticos centrales son: gobernanza de la IA centrada en el bien común, "
            "resiliencia de las cadenas de suministro global e infraestructura digital. Será la tercera "
            "vez que China acoge la cumbre (tras 2001 en Shanghái y 2014 en Pekín)."
        ),
        "fuente_label": "APEC — China Unveils APEC 2026 Theme and Priorities in Shenzhen",
        "fuente_url": "https://www.apec.org/press/news-releases/2025/china-unveils-apec-2026-theme-and-priorities-in-shenzhen",
    },
    {
        "emoji": "🗺️",
        "titulo": "XV Plan Quinquenal (2026-2030): IA, 6G, robótica y biotech como pilares del futuro chino",
        "cuerpo": (
            "El nuevo plan quinquenal sitúa las 'Nuevas Fuerzas Productivas de Calidad' en el centro de "
            "la estrategia nacional. Los ejes son: IA Plus (aplicar la IA como infraestructura transversal "
            "a toda la economía), 6G, robótica, biotecnología y economía de baja altitud (drones). Las "
            "industrias emergentes —circuitos integrados, robots inteligentes y drones— suman ya casi "
            "6 billones de yuanes y aspiran a 10 billones para 2030. El presupuesto en Ciencia y Tecnología "
            "creció un 7,1% hasta 1,3 billones de yuanes. China fija crecimiento del PIB entre 4,5% y 5% "
            "para 2026, y proyecta que la economía digital represente el 12,5% del PIB."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · Semana del 13 al 19 de junio de 2026 · Publicado: {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, cultura y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 13-19 Junio 2026"
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
