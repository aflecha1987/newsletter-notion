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
        "emoji": "🚗",
        "titulo": "BYD domina el 10% del mercado eléctrico de la UE y bate récords de exportación",
        "cuerpo": (
            "BYD vendió más de 160.000 vehículos en el exterior durante mayo de 2026, un 80% más "
            "que en el mismo mes del año anterior. La compañía china acapara ya uno de cada diez "
            "eléctricos puros vendidos en la Unión Europea en 2026, duplicando su cuota interanual. "
            "En los primeros cuatro meses del año, las entregas en Europa se dispararon un 144% "
            "interanual hasta las 101.221 unidades. Su objetivo para el año: 1,5 millones de "
            "vehículos exportados, un 15% por encima del objetivo anterior. La logística ya acompaña "
            "esa ambición: el BYD Explorer No.1, un buque Ro-Ro de 199 metros con capacidad para "
            "7.000 coches, zarpó el 1 de junio desde Singapur hacia Southampton."
        ),
        "fuente_label": "Bloomberg Línea — BYD confía en superar su objetivo de exportaciones 2026",
        "fuente_url": "https://www.bloomberglinea.com/negocios/byd-confia-en-que-las-exportaciones-de-2026-superaran-en-un-15-su-anterior-objetivo/",
    },
    {
        "emoji": "🤖",
        "titulo": "Alibaba y Baidu presentan modelos de IA que compiten con los mejores del mundo",
        "cuerpo": (
            "China consolida su posición en la carrera global de la inteligencia artificial con "
            "dos lanzamientos de peso: Alibaba lanzó Qwen 3.7 Max (puesto 11 del ranking global "
            "LLM Stats), con soporte multimodal para texto, foto y video, y capacidad para analizar "
            "vídeos de hasta dos horas. Baidu presentó ERNIE 5.1, que ocupa el primer puesto entre "
            "todos los modelos chinos en el ranking de texto de LMArena y el cuarto global. Ambos "
            "modelos están disponibles en la nube y vía API. DeepSeek V4 Pro Max, con licencia "
            "abierta MIT y contexto de un millón de tokens, sigue liderando entre los modelos "
            "open-source y comprime la brecha con los gigantes estadounidenses."
        ),
        "fuente_label": "Bloomberg Línea — Alibaba actualiza su modelo de IA y eleva la presión sobre DeepSeek",
        "fuente_url": "https://www.bloomberglinea.com/tecnologia/alibaba-actualiza-su-modelo-de-ia-y-eleva-la-presion-sobre-deepseek/",
    },
    {
        "emoji": "⚡",
        "titulo": "State Grid invertirá 1.000 millones de dólares en 8.500 robots para la red eléctrica",
        "cuerpo": (
            "La empresa estatal State Grid Corporation of China ha anunciado la compra de 8.500 "
            "robots con inteligencia artificial en 2026, con una inversión de 6.800 millones de "
            "yuanes (~1.000 millones de dólares). El plan incluye 500 robots humanoides para "
            "trabajar con líneas en tensión (presupuesto: 2.500 millones de yuanes) y 3.000 robots "
            "de doble brazo para operar equipos y gestionar fallos (1.800 millones de yuanes). "
            "El objetivo es reducir riesgos laborales y detectar averías antes de que se conviertan "
            "en un problema, en un contexto en que la red eléctrica china soporta una demanda "
            "creciente por el auge de las renovables y la electrificación del transporte."
        ),
        "fuente_label": "Ecoticias — China prepara millones de robots para la red eléctrica",
        "fuente_url": "https://www.ecoticias.com/hoyeco/china-desafia-las-normas-a-un-nivel-que-nadie-puede-imaginar-prepara-millones-de-robots-para-que-se-encarguen-de-la-red-electrica-del-pais-evitando-el-error-humano-y-transformando-la-energia-para-sie/35733/",
    },
    {
        "emoji": "☀️",
        "titulo": "Histórico: la energía solar supera al carbón como primera fuente de capacidad en China",
        "cuerpo": (
            "Un hito sin precedentes: en 2026, la capacidad solar instalada en China supera por "
            "primera vez a la del carbón, con más de 1,38 teravatios frente a los 1,23 TW del "
            "carbón. China añadirá alrededor de 300 GW de nueva capacidad eólica y solar solo en "
            "2026, tras haber instalado un récord de casi 500 GW en 2025 (más del 60% del "
            "crecimiento global). La energía eólica y solar ya generan más de un cuarto de toda "
            "la electricidad del país. En paralelo, avanza la construcción de una planta solar "
            "espacial en órbita geosincrónica: las primeras pruebas comenzarán en 2028, con el "
            "objetivo de alcanzar 2 GW de capacidad para 2050."
        ),
        "fuente_label": "IEA Global Energy Review 2026 — Solar PV and Wind",
        "fuente_url": "https://www.iea.org/reports/global-energy-review-2026/technology-solar-pv-and-wind",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior de China: +15,3% interanual en enero-mayo, récord histórico",
        "cuerpo": (
            "El comercio exterior chino acumula 20,68 billones de yuanes en los primeros cinco "
            "meses de 2026, con un crecimiento del 15,3% interanual —el ritmo más rápido en cinco "
            "años—. El comercio con los países de la ASEAN creció un 16,6%, con la Unión Europea "
            "un 10,3%, y con los países africanos un 18,2%. Las exportaciones registran subidas de "
            "doble dígito en prácticamente todos los destinos, reflejando la posición insustituible "
            "de China en las cadenas de suministro globales y el avance firme de su manufactura de "
            "alto valor añadido."
        ),
        "fuente_label": "CGTN Español — Comercio exterior de China crece 15% en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-16/2044593566811017217/index.html",
    },
    {
        "emoji": "🏭",
        "titulo": "IV Exposición Internacional de la Cadena de Suministro: 500+ empresas en Pekín",
        "cuerpo": (
            "Del 22 al 26 de junio se celebra en Pekín la cuarta edición de la Exposición "
            "Internacional de la Cadena de Suministro de China, con más de 500 empresas nacionales "
            "y extranjeras inscritas. El evento se ha convertido en plataforma clave para la "
            "cooperación internacional en cadenas industriales. Esta edición está marcada por las "
            "prioridades del 15.º Plan Quinquenal: manufactura avanzada, semiconductores, energías "
            "limpias y digitalización. La expo refleja la apuesta de China por abrir sus cadenas "
            "de suministro al mundo mientras refuerza su liderazgo industrial."
        ),
        "fuente_label": "CGTN Español — Más de 500 empresas inscritas en la Expo Cadena de Suministro 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-03-02/2028294317752307713/index.html",
    },
    {
        "emoji": "💾",
        "titulo": "Qingdao estrena el primer centro de datos prefabricado del mundo",
        "cuerpo": (
            "El 6 de junio entró en funcionamiento en Qingdao lo que se presenta como la primera "
            "base prefabricada del mundo para centros de computación de alta densidad. La tecnología, "
            "desarrollada por una empresa china, convierte la infraestructura energética de los "
            "centros de datos en módulos prefabricados listos para instalar, reduciendo "
            "drásticamente los tiempos y costes de construcción. Este tipo de innovación en "
            "infraestructura digital es clave para sostener el explosivo crecimiento de la demanda "
            "computacional generada por la IA generativa y los modelos de lenguaje masivos."
        ),
        "fuente_label": "Xataka — Compañía china convierte su energía en piezas prefabricadas para centros de datos",
        "fuente_url": "https://www.xataka.com/energia/centros-datos-tienen-problema-fondo-compania-china-acaba-convertir-su-energia-piezas-prefabricadas",
    },
    {
        "emoji": "🚀",
        "titulo": "2026: el año más intensivo de la historia del programa espacial chino",
        "cuerpo": (
            "La Agencia Espacial Nacional China (CNSA) tiene previstas para 2026 misiones sin "
            "precedentes: el lanzamiento de Chang'e-7 (agosto), que buscará agua en los cráteres "
            "oscuros del polo sur lunar; el acercamiento de Tianwen-2 a su asteroide objetivo; la "
            "misión tripulada Shenzhou-23; y los ensayos del cohete reutilizable Larga Marcha 10, "
            "pieza angular del programa lunar tripulado antes de 2030. El programa espacial "
            "comercial también acelera, con múltiples startups chinas compitiendo en lanzamientos "
            "y constelaciones de satélites de observación."
        ),
        "fuente_label": "Universe Today — China's Space Programme Prepares for Its Busiest Year Yet",
        "fuente_url": "https://www.universetoday.com/articles/chinas-space-programme-prepares-for-its-busiest-year-yet",
    },
    {
        "emoji": "🎬",
        "titulo": "Festival Internacional de Cine de Shanghai celebra su 28ª edición con IA y cine global",
        "cuerpo": (
            "Del 12 al 21 de junio, Shanghai acogió la 28ª edición del Festival Internacional de "
            "Cine de Shanghai (SIFF), uno de los festivales más importantes de Asia y referente "
            "del cine global. La edición de 2026 reunió producciones de más de 80 países e integró "
            "por primera vez una sección dedicada al cine generado con inteligencia artificial. "
            "El festival consolida el creciente peso del soft power cultural chino en el panorama "
            "internacional y Shanghai como capital cultural de Asia."
        ),
        "fuente_label": "CGTN Español — Festival Internacional de Cine de Shanghai 2026",
        "fuente_url": "https://espanol.cgtn.com/",
    },
]


def build_blocks():
    today = "21 de junio de 2026"
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
    title = "China Al Dia — Semana 15-21 Junio 2026"
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
