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
        "emoji": "📈",
        "titulo": "Alta tecnología e industrialización impulsan el mayor superávit comercial de la historia de China",
        "cuerpo": (
            "El 20 de agosto, Sputnik Mundo publicó un análisis destacando que la modernización "
            "industrial y la alta tecnología son los principales motores del récord de superávit "
            "comercial chino en 2026. Las exportaciones de productos manufacturados de alto valor "
            "agregado —vehículos eléctricos, maquinaria de precisión, equipos de energía renovable— "
            "han desplazado definitivamente a los productos de bajo coste como motor del comercio "
            "exterior. La estrategia 'China 2.0' está produciendo resultados: el país exporta cada "
            "vez más inteligencia incorporada en sus productos."
        ),
        "fuente_label": "Sputnik Mundo — La modernización industrial impulsa el superávit comercial de China",
        "fuente_url": "https://noticiaslatam.lat/20260820/la-modernizacion-industrial-y-la-alta-tecnologia-impulsan-el-superavit-comercial-de-china-dice-1174735241.html",
    },
    {
        "emoji": "🤖",
        "titulo": "AGIBOT entrega su robot humanoide número 15.000: China produce el 88,7 % del total mundial",
        "cuerpo": (
            "En junio de 2026, la empresa china AGIBOT entregó su robot número 15.000 directamente "
            "a una fábrica de Shanghai para uso en líneas de producción. En 2025, China acaparó el "
            "88,7 % de los envíos globales de robots humanoides, y el Ministerio de Industria y "
            "Tecnología de la Información espera que la producción total de robots humanoides supere "
            "las 100.000 unidades en 2026. La industria robótica china ya no es un laboratorio de "
            "investigación: es la cadena de suministro del planeta."
        ),
        "fuente_label": "Educatronica — Industria de la inteligencia artificial en China 2026",
        "fuente_url": "https://educatronica.org/2026/04/12/industria-inteligencia-artificial-china-2026/",
    },
    {
        "emoji": "🧠",
        "titulo": "Plan AI+: China integra la inteligencia artificial como infraestructura transversal de la sociedad",
        "cuerpo": (
            "China lanzó el ambicioso Plan AI+, que busca usar la inteligencia artificial como "
            "infraestructura transversal aplicada a todos los sectores productivos y de servicios. "
            "Las metas son claras: incorporar IA en el 70 % de la sociedad para 2027 y en el "
            "90 % para 2030. Los sectores prioritarios incluyen salud, educación, logística, "
            "agricultura, energía y seguridad vial. El plan incluye subsidios para pymes que adopten "
            "soluciones de IA y un fondo público de 200.000 millones de yuanes para investigación "
            "en IA aplicada."
        ),
        "fuente_label": "Mundo Global — Las 10 tecnologías emergentes más importantes de China en 2026",
        "fuente_url": "https://mundoglobal.org/oportunidad-china-2-0-la-inteligencia-artificial-y-las-10-tecnologias-emergentes-que-china-considera-mas-importantes-en-2026/",
    },
    {
        "emoji": "🚀",
        "titulo": "China recupera con éxito el primer estadio de un cohete portador en plataforma marítima",
        "cuerpo": (
            "China ha abierto un nuevo capítulo en el desarrollo de cohetes reutilizables al recuperar "
            "con éxito el primer estadio de un cohete portador tras un retorno vertical histórico sobre "
            "una plataforma marítima. El logro coloca a China a la par de SpaceX en tecnología de "
            "reutilización de lanzadores, con el objetivo de reducir el coste de acceso al espacio en "
            "un 60-80 % en los próximos años. La empresa CASIC y varios actores privados compiten "
            "por liderar este mercado emergente en China."
        ),
        "fuente_label": "AICAD — Las 3 grandes innovaciones tecnológicas de China del 2026",
        "fuente_url": "https://www.aicad.es/las-3-grandes-innovaciones-tecnologicas-de-china-del-2026",
    },
    {
        "emoji": "💡",
        "titulo": "Innovación inteligente: la IA china abre nuevas posibilidades para una vida mejor",
        "cuerpo": (
            "El 19 de agosto, china.org.cn publicó un especial sobre cómo la innovación inteligente "
            "china está mejorando la calidad de vida. Entre los casos destacados: tutores de IA que "
            "personalizan el aprendizaje para millones de estudiantes, sistemas de gestión inteligente "
            "del tráfico que reducen los tiempos de desplazamiento urbano en un 30 %, y plataformas "
            "de IA aplicadas a la agricultura de precisión que optimizan el uso de agua y fertilizantes. "
            "China está pasando de exportar tecnología a exportar modelos de vida."
        ),
        "fuente_label": "China.org.cn — Innovación inteligente abre nuevas posibilidades para una vida mejor",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-08/19/content_118656289.htm",
    },
    {
        "emoji": "🌱",
        "titulo": "China y Jordania forjan una alianza verde: EVs y energía renovable lideran el comercio bilateral",
        "cuerpo": (
            "El Rey de Jordania realizó una visita de Estado a China del 18 al 24 de agosto, centrando "
            "la agenda en la transición hacia una economía verde. El comercio bilateral de bienes de "
            "consumo verdes ha irrumpido como el nuevo motor de crecimiento: vehículos eléctricos "
            "chinos se venden ahora masivamente en Amman, mientras Jordania exporta minerales críticos "
            "estratégicos para las baterías. El acuerdo prevé también la instalación de parques "
            "solares en el desierto jordano con tecnología y financiación chinas."
        ),
        "fuente_label": "CGTN — China-Jordan ties go green: EVs, renewable energy drive new trade boom",
        "fuente_url": "https://news.cgtn.com/news/2026-08-18/China-Jordan-ties-go-green-EVs-renewable-energy-drive-new-trade-boom-1PI13rs2zAI/p.html",
    },
    {
        "emoji": "🏭",
        "titulo": "China aprueba los planes quinquenales de descarbonización industrial más ambiciosos del mundo",
        "cuerpo": (
            "En junio de 2026, el gobierno chino aprobó los planes quinquenales para la "
            "descarbonización industrial, con objetivos vinculantes para nueve sectores clave: "
            "acero, aluminio electrolítico, cemento, vidrio plano, refino de petróleo, etileno, "
            "amoníaco sintético, metanol y generación termoeléctrica. A partir de agosto, las "
            "empresas tendrán objetivos obligatorios de consumo de energía limpia. El plan "
            "también prevé una 'campaña intensiva de ahorro energético y descarbonización' entre "
            "2026 y 2028 en toda la industria pesada."
        ),
        "fuente_label": "Carbon Brief — China Briefing 25 June 2026: Five-year plans passed",
        "fuente_url": "https://www.carbonbrief.org/china-briefing-25-june-2026-five-year-plans-passed-critical-mineral-tensions-industrial-decarbonisation-plan",
    },
    {
        "emoji": "⚡",
        "titulo": "El carbón cae por debajo del 50 % de la generación eléctrica china por primera vez en la historia",
        "cuerpo": (
            "Los datos del primer semestre de 2026 confirman un hito sin precedentes: la cuota del "
            "carbón en la generación eléctrica de China cayó al 49,7 %, por debajo del 50 % por "
            "primera vez. Las renovables —solar, eólica e hidráulica— representaron ya el 41,2 % "
            "de la electricidad generada. China incorporó 117 GW de nueva potencia renovable en "
            "solo seis meses, el 73,9 % de toda la nueva capacidad eléctrica instalada en el período. "
            "La capacidad renovable total alcanzó 2.455 GW, más del 60 % del parque nacional."
        ),
        "fuente_label": "IndexBox — China's Renewable Energy Share Reaches 41.2% in First Half of 2026",
        "fuente_url": "https://www.indexbox.io/blog/renewable-energy-hits-412-of-chinas-electricity-in-h1-2026/",
    },
    {
        "emoji": "🔬",
        "titulo": "La autosuficiencia científica y tecnológica: el nuevo pilar del desarrollo soberano de China",
        "cuerpo": (
            "China está priorizando la autosuficiencia en ciencia y tecnología como condición del "
            "desarrollo soberano. El país ha incrementado el gasto en I+D hasta el 2,6 % del PIB, "
            "con el objetivo de alcanzar el 3 % para 2030. Las áreas más sensibles —semiconductores, "
            "sistemas operativos, motores de avión, software industrial— reciben financiación estatal "
            "prioritaria. El mensaje es claro: China quiere innovar sin depender de proveedores "
            "externos que puedan imponer restricciones geopolíticas."
        ),
        "fuente_label": "China.org.cn — Autosuficiencia científica y tecnológica como pilar del desarrollo",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-07/20/content_118607233.htm",
    },
    {
        "emoji": "💼",
        "titulo": "La inversión empresarial en tecnología digital crece un 10,8 % en China en 2026",
        "cuerpo": (
            "Según datos de Xinhua, la cantidad gastada por las empresas chinas en la adquisición y "
            "desarrollo de tecnología digital aumentó un 10,8 % interanual en los dos primeros meses "
            "de 2026. El dato refleja una aceleración de la inversión privada en transformación "
            "digital, impulsada por los incentivos del Plan AI+ y la competencia entre empresas por "
            "adoptar modelos de lenguaje y automatización inteligente en sus procesos productivos "
            "y logísticos. China digitaliza su economía a un ritmo sin precedentes."
        ),
        "fuente_label": "Xinhua en español — Innovación tecnológica gana impulso en China en 2026",
        "fuente_url": "https://spanish.news.cn/20260312/609871a2816b42efaf0f7d9ac3b5ff7a/c.html",
    },
    {
        "emoji": "🌍",
        "titulo": "China consolida su liderazgo global: 5 años para ser la primera potencia tecnológica del mundo",
        "cuerpo": (
            "Un análisis de The Conversation repasa cómo China planea consolidar su poder global "
            "entre 2026 y 2030 mediante la tecnología, la autosuficiencia y la proyección exterior. "
            "La hoja de ruta incluye: dominio en IA generativa y modelos fundacionales, liderazgo "
            "en fabricación de semiconductores maduros, control de la cadena de suministro de "
            "minerales críticos y expansión de los estándares tecnológicos chinos (6G, IA, "
            "vehículos autónomos) como norma internacional."
        ),
        "fuente_label": "The Conversation — 2026-2030: cinco años para consolidar el poder global de China",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · Semana 15-22 Ago 2026 · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, energia, ciencia y cooperacion internacional.", bold=False),
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
    title = "China Al Dia — Semana 15-22 Ago 2026"
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
