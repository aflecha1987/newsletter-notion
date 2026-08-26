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
        "emoji": "⚡",
        "titulo": "China consolida el 41,2% de generación renovable y fija objetivos de consumo obligatorio",
        "cuerpo": (
            "En agosto de 2026, China confirmó que las energías renovables cubren el 41,2 % de su "
            "generación eléctrica, habiendo incorporado 117 GW en el primer semestre. El 1 de agosto "
            "entró en vigor la nueva normativa de la NDRC que fija objetivos de consumo de renovables "
            "para empresas y provincias —no solo de producción—, incluyendo por primera vez el hidrógeno "
            "y el amoníaco verde. China invierte además 20.100 millones de dólares en energía verde "
            "en el marco de la Iniciativa Franja y Ruta."
        ),
        "fuente_label": "Energías Renovables — China supera el 40% de generación renovable",
        "fuente_url": "https://www.energias-renovables.com/panorama/china-supera-por-primera-vez-el-40-20260803",
    },
    {
        "emoji": "📈",
        "titulo": "PIB del 4,7%: las nuevas fuerzas productivas aportan más del 40% al crecimiento chino",
        "cuerpo": (
            "La economía china mantiene un crecimiento estable del 4,7 %, dentro del objetivo del "
            "XV Plan Quinquenal (2026-2030). Las 'nuevas fuerzas productivas' —IA, semiconductores, "
            "vehículos eléctricos y biotecnología— aportaron más del 40 % al crecimiento total. "
            "Las patentes de IA crecieron un 34,8 % interanual y la penetración de vehículos de "
            "nueva energía alcanzó el 54,1 % de las ventas minoristas."
        ),
        "fuente_label": "Prensa Latina — Economía china estable con PIB de 4,7%",
        "fuente_url": "https://www.prensa-latina.cu/2026/08/24/economia-china-estable-con-pib-de-47-y-nuevas-fuerzas-productivas/",
    },
    {
        "emoji": "🚢",
        "titulo": "China domina el 72% de la construcción naval y lidera exportaciones verdes globales",
        "cuerpo": (
            "Los astilleros chinos captaron 1.131 de los 1.481 buques encargados en todo el mundo en "
            "el primer semestre —alrededor del 72 % del mercado global—. En paralelo, las exportaciones "
            "de aerogeneradores crecieron un +35,6 %, las de baterías de litio un +37,6 %, y las de "
            "automóviles alcanzaron 5,1 millones de unidades (+65,3 %). China consolida su liderazgo "
            "en las industrias verdes del futuro."
        ),
        "fuente_label": "Sputnik Mundo — Alta tecnología impulsa el superávit comercial de China",
        "fuente_url": "https://noticiaslatam.lat/20260820/la-modernizacion-industrial-y-la-alta-tecnologia-impulsan-el-superavit-comercial-de-china-dice-1174735241.html",
    },
    {
        "emoji": "🛰️",
        "titulo": "China lanza satélites de observación terrestre con IA integrada a bordo",
        "cuerpo": (
            "El 5 de agosto, China lanzó desde una plataforma marítima en Shandong los satélites "
            "Oriental Smart Eye 01 y 02 a bordo del cohete Smart Dragon-3. Estos satélites procesan "
            "datos con inteligencia artificial directamente en órbita, orientados a aplicaciones "
            "agrícolas, ambientales y de gestión de recursos naturales. La constelación ya tiene en "
            "funcionamiento diez modelos de IA en el espacio, incluyendo el modelo Qwen3 de Alibaba Cloud."
        ),
        "fuente_label": "EspacioTech — China lanza satélites de observación con IA a bordo",
        "fuente_url": "https://www.espaciotech.net/2026/08/05/china-lanzo-desde-el-mar-dos-satelites-que-observaran-la-tierra-con-inteligencia-artificial",
    },
    {
        "emoji": "🔬",
        "titulo": "Congreso Internacional de Ciencias Básicas en Pekín: más de 1.000 científicos del mundo",
        "cuerpo": (
            "El Congreso Internacional de Ciencias Básicas (ICBS 2026) abrió sus puertas en Pekín "
            "con más de 1.000 participantes de todo el mundo. Durante dos semanas, más de 500 sesiones "
            "académicas cubrirán desde razonamiento de modelos de IA a gran escala hasta información "
            "cuántica, visión por computadora e interacción humano-computadora. China se posiciona "
            "como sede natural del debate científico global."
        ),
        "fuente_label": "PR Newswire — Congreso Internacional de Ciencias Básicas en Pekín",
        "fuente_url": "https://www.prnewswire.com/news-releases/cctvse-inaugura-en-pekin-el-congreso-internacional-de-ciencias-basicas-302846949.html",
    },
    {
        "emoji": "👨‍🚀",
        "titulo": "La juventud china impulsa la industria aeroespacial, el mar profundo y la IA",
        "cuerpo": (
            "Un reportaje de Xinhua destaca cómo la nueva generación de científicos e ingenieros chinos "
            "protagoniza avances simultáneos en la industria aeroespacial, la exploración del mar "
            "profundo con vehículos submarinos autónomos y la innovación en IA. El promedio de edad "
            "de los líderes de proyecto en sectores estratégicos ha bajado a 35 años."
        ),
        "fuente_label": "Confirmado — Juventud china destaca en aeroespacial, mar profundo e IA",
        "fuente_url": "https://confirmado.net/juventud-china-destaca-en-industria-aeroespacial-exploracion-profunda-del-mar-e-innovacion-en-ia/",
    },
    {
        "emoji": "🏥",
        "titulo": "IA y medicina tradicional china: quioscos de diagnóstico inteligente llegan al metro",
        "cuerpo": (
            "China despliega quioscos de diagnóstico asistido por IA en estaciones de metro y puntos "
            "urbanos, combinando biomedicina avanzada con Medicina Tradicional China (MTC). Los "
            "dispositivos miden presión arterial, frecuencia cardíaca, saturación de oxígeno y "
            "temperatura; la IA aplica simultáneamente criterios de MTC: análisis facial, observación "
            "de lengua e interpretación digital del pulso. El objetivo es detectar enfermedades "
            "crónicas de forma precoz, descargando presión de los centros de salud primaria."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
    {
        "emoji": "🌏",
        "titulo": "Xi Jinping y Lula refuerzan alianza China-Brasil en el BRICS con récords comerciales",
        "cuerpo": (
            "El presidente Xi Jinping habló con el presidente Lula da Silva para estrechar la "
            "coordinación estratégica bilateral dentro del BRICS. Lula destacó récords históricos "
            "del comercio bilateral e invitó a inversiones chinas en IA, energía y recursos minerales. "
            "El Nuevo Banco de Desarrollo, con sede en Shanghái, ya ha aprobado préstamos por "
            "35.000 millones de dólares en más de 100 proyectos en el Sur Global."
        ),
        "fuente_label": "Observatorio de Política China — Resumen política exterior julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-china-miscelanea/",
    },
    {
        "emoji": "🗺️",
        "titulo": "Iniciativa Franja y Ruta bate récords: 126.400 millones de dólares en el primer semestre",
        "cuerpo": (
            "El primer semestre de 2026 registró un récord histórico en la BRI: 49.800 millones en "
            "inversiones y 76.500 millones en contratos de construcción, totalizando 126.400 millones "
            "de dólares en 186 proyectos activos. Los sectores con mayor crecimiento son energía "
            "limpia, minería crítica y nuevas tecnologías (5G, centros de datos, IA). Las empresas "
            "líderes son PowerChina, CCCC y State Construction Engineering."
        ),
        "fuente_label": "Green Finance & Development Center — BRI 2026 H1",
        "fuente_url": "https://greenfdc.org/chinas-investment-and-construction-engagement-in-the-belt-and-road-initiative-bri-2026-h1/",
    },
    {
        "emoji": "🌞",
        "titulo": "Plan quinquenal de renovables 2026-2030: objetivo del 50% de energía limpia",
        "cuerpo": (
            "El 23 de julio, la NDRC y la NEA presentaron el XV Plan Quinquenal de Energías Renovables. "
            "El objetivo es que las renovables cubran el 50 % de la mezcla energética para 2030. "
            "El plan incluye por primera vez el hidrógeno y el amoníaco verde como fuentes computables. "
            "La capacidad renovable total ya es de 2.455 GW, más del 60 % del parque de generación nacional."
        ),
        "fuente_label": "Ecosistema Startup — China fija meta del 50% renovable para 2030",
        "fuente_url": "https://ecosistemastartup.com/china-marca-renewables-como-fuente-principal-50-en-2030/",
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
    title = "China Al Dia — Semana 19-26 Ago 2026"
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
