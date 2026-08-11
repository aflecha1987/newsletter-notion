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
    # ── SEMANA 4-11 AGO 2026 ──────────────────────────────────────────────────
    {
        "emoji": "🤖",
        "titulo": "La IA china crea una 'zona de muerte' para los fabricantes de modelos de EE.UU.",
        "cuerpo": (
            "En la primera semana de agosto, las grandes tecnologicas chinas lanzaron una avalancha de "
            "modelos de inteligencia artificial que igualan o superan a los principales sistemas "
            "estadounidenses, a un coste significativamente menor. Alibaba presento Qwen3.8-Max, que "
            "segun benchmarks independientes iguala o supera al Claude Opus de Anthropic. Moonshot AI "
            "lanzo Kimi K3, comparable a las opciones mas caras de EE.UU. pero construido con un "
            "presupuesto mucho mas reducido. ByteDance, DeepSeek y Z.ai tambien presentaron sus ultimos "
            "modelos. Bloomberg titulo: 'China's AI Blitz Creates Death Zone for Rival US Model Makers'. "
            "La aceleracion china en IA es la noticia tecnologica mas importante del verano de 2026."
        ),
        "fuente_label": "Bloomberg — China's AI Blitz Creates 'Death Zone' for Rival US Model Makers",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-08-04/china-s-ai-blitz-creates-death-zone-for-rival-us-model-makers",
    },
    {
        "emoji": "🌐",
        "titulo": "China lanza la WAICO: nueva organizacion internacional de gobernanza de IA con 29 paises fundadores",
        "cuerpo": (
            "Xi Jinping anuncio en la apertura de la WAIC 2026 (17-20 de julio, Shanghai) la creacion de "
            "la World Artificial Intelligence Cooperation Organization (WAICO), una nueva organizacion "
            "internacional para la gobernanza y cooperacion global en IA. Los 29 paises fundadores "
            "incluyen Brasil, Rusia, Sudafrica, Indonesia, Pakistan y varias naciones del bloque BRICS "
            "y OCS. EE.UU. y los principales paises europeos occidentales no participaron. En los "
            "proximos cinco anos, China proporcionara 5.000 cuotas para programas de intercambio y "
            "establecera centros de cooperacion con la ASEAN, la Liga Arabe, la Union Africana, CELAC y BRICS."
        ),
        "fuente_label": "Radionodo AI — Nace WAICO: China crea nueva organización internacional de IA",
        "fuente_url": "https://radionodo.ai/nace-waico-china-crea-una-nueva-organizacion-internacional-de-inteligencia-artificial/",
    },
    {
        "emoji": "🦾",
        "titulo": "Shanghai Electric despliega robots humanoides de nueva generacion en la WAIC 2026",
        "cuerpo": (
            "Shanghai Electric presento en la WAIC 2026 su linea de robots humanoides SUYUAN y TUOYUAN, "
            "con capacidades avanzadas de manipulacion y movilidad integradas con modelos de IA a gran "
            "escala. Ademas, lanzo 51 modelos y agentes de IA bajo la serie StarCloud Intelligent "
            "Manufacturing. El evento confirmo que China lidera globalmente en humanoides: mas de 400 "
            "modelos han sido desarrollados por empresas chinas, mas de la mitad del total mundial. Las "
            "fabricas chinas mas avanzadas ya operan con mas de 3.000 robots industriales sincronizados "
            "mediante IA, IoT y conectividad 5G."
        ),
        "fuente_label": "DiarioBitcoin — Shanghai Electric en WAIC 2026",
        "fuente_url": "https://www.diariobitcoin.com/tecnologia/shanghai-electric-despliega-robots-humanoides-y-fabricas-inteligentes-en-waic-2026/",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior de China crece un 17,3% en los primeros 7 meses de 2026",
        "cuerpo": (
            "En los primeros siete meses de 2026, las exportaciones e importaciones chinas sumaron "
            "30,13 billones de yuanes, con un crecimiento interanual del 17,3 %. Solo en julio, el "
            "comercio exterior alcanzo los 4,66 billones de yuanes (+19,2 % interanual). Las "
            "exportaciones de productos de alta tecnologia crecieron mas de un 50 % en julio, aportando "
            "casi el 60 % del incremento total. Los vehiculos electricos, las baterias de litio y las "
            "turbinas eolicas continuan siendo los grandes motores. El comercio con los paises de la "
            "Iniciativa Cinturon y Ruta crecio un 15,5 %, mientras que los intercambios con otras "
            "economias de la APEC aumentaron un 21 %."
        ),
        "fuente_label": "Brasil 247 — China vence guerra comercial con avance de 17,3% en comercio exterior",
        "fuente_url": "https://www.brasil247.com/global-times/china-tambem-derrota-trump-e-vence-guerra-comercial-com-avanco-de-173-no-comercio-exterior/",
    },
    {
        "emoji": "🌏",
        "titulo": "China acogerá la APEC 2026: cumbre del 60% del PIB mundial en Chengdu y Beijing",
        "cuerpo": (
            "China es el anfitrion de la APEC 2026, la cumbre anual que reune a las 21 economias de "
            "la cuenca del Pacifico, responsables del 60 % del PIB mundial y el 47 % del comercio "
            "global. Chengdu acogera la Semana Digital de la APEC y otros eventos previos, mientras "
            "que la cumbre de lideres tendra lugar en noviembre. El evento es una oportunidad para que "
            "China afiance su liderazgo economico regional y mundial, especialmente en economia "
            "digital, energias limpias e inteligencia artificial."
        ),
        "fuente_label": "Wikipedia — APEC China 2026",
        "fuente_url": "https://en.wikipedia.org/wiki/APEC_China_2026",
    },
    {
        "emoji": "⚡",
        "titulo": "China supera el 40% de electricidad renovable — el carbon cae del 50% por primera vez",
        "cuerpo": (
            "En el primer semestre de 2026, la generacion electrica de fuentes renovables en China "
            "supero por primera vez la barrera del 40 % (41,2 %), mientras la participacion del carbon "
            "cayo por debajo del 50 % por primera vez en un semestre completo. China instalo 117 GW de "
            "nueva capacidad renovable en esos seis meses —el 73,9 % de toda la nueva capacidad "
            "instalada—. Ya hay 24 plantas de energia solar de espejos (termosolar) en operacion, con "
            "otras 26 en construccion que suman 3,2 GW adicionales. El objetivo del gobierno es que "
            "el 50 % de la electricidad proceda de fuentes no fosiles en 2030."
        ),
        "fuente_label": "Energías Renovables — China supera por primera vez el 40% de generación eléctrica renovable",
        "fuente_url": "https://www.energias-renovables.com/panorama/china-supera-por-primera-vez-el-40-20260803",
    },
    {
        "emoji": "🛰️",
        "titulo": "China planea construir la primera fabrica espacial: modulo inflable en la estacion Tiangong",
        "cuerpo": (
            "China trabaja en un modulo inflable de hasta dos metros de diametro para instalarlo en la "
            "estacion espacial Tiangong, con el objetivo de aprovechar la microgravedad para fabricar "
            "materiales avanzados y biofarmacos imposibles de producir en la Tierra. El modulo se "
            "lanzaria plegado y se expandiria en orbita. En paralelo, China desafia a la NASA 23 anos "
            "despues de su primer viaje espacial: ya opera una estacion permanente, ha traido muestras "
            "de la cara oculta de la Luna y proyecta un alunizaje con astronautas antes de 2030."
        ),
        "fuente_label": "El Español — China busca construir fábrica en el espacio con módulo inflable",
        "fuente_url": "https://www.elespanol.com/ciencia/20260730/china-cambia-normas-busca-construir-fabrica-espacio-modulo-metros-diametro-kw/1003744337933_0.html",
    },
    {
        "emoji": "🚄",
        "titulo": "Air China inaugura vuelo diario Beijing-Ulan Bator con avion de fabricacion nacional",
        "cuerpo": (
            "A partir del 12 de agosto de 2026, Air China operara un vuelo diario de ida y vuelta "
            "entre Beijing y Ulan Bator (Mongolia) con un avion troncal de fabricacion nacional. El "
            "hito consolida la expansion de la aeronautica comercial china y la llegada del avion "
            "nacional a rutas internacionales regulares. En el frente ferroviario, China continua el "
            "despliegue de su red de trenes Maglev de alta velocidad (600-1.000 km/h), con el objetivo "
            "de conectar megaciudades como Beijing y Shanghai en apenas hora y media, y en 2026 entra "
            "en servicio el primer tren de pasajeros impulsado por hidrogeno a 250 km/h."
        ),
        "fuente_label": "Xinhua en español — Innovación tecnológica en China 2026",
        "fuente_url": "https://spanish.news.cn/20260312/609871a2816b42efaf0f7d9ac3b5ff7a/c.html",
    },
    {
        "emoji": "🌍",
        "titulo": "China y Africa celebran 70 anos de relaciones diplomaticas con nuevos acuerdos de modernizacion",
        "cuerpo": (
            "2026 marca el 70 aniversario del establecimiento de relaciones diplomaticas entre China "
            "y los paises africanos. En este marco, China impulsara la Iniciativa de Cooperacion para "
            "la Modernizacion en Africa, que incluye transferencia tecnologica, financiacion de "
            "infraestructuras limpias y formacion de talento local. Ademas, se acelera la negociacion "
            "de un acuerdo de asociacion economica entre China y el bloque africano. Este 2026, "
            "Xi Jinping ha recibido en Beijing a los lideres de EE.UU., Rusia y las principales "
            "potencias europeas, consolidando una agenda diplomatica activa."
        ),
        "fuente_label": "Observatorio Política China — Resumen de Política Exterior",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-4/",
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
    title = "China Al Dia — Semana 4-11 Ago 2026"
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
