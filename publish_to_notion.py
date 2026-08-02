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

MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]


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
        "emoji": "🤖",
        "titulo": "Alibaba lanza Qwen 3.8: el segundo modelo de IA más potente del mundo, con pesos abiertos",
        "cuerpo": (
            "El 19 de julio, Alibaba anunció Qwen 3.8, un modelo de lenguaje con 2,4 billones de parámetros "
            "—el segundo más poderoso del mundo, solo por detrás de Claude Fable 5 de Anthropic—. "
            "La gran apuesta diferenciadora: Qwen 3.8 es open-weight, es decir, sus pesos se publican "
            "abiertamente, lo que pone capacidades de frontera al alcance de desarrolladores e investigadores "
            "de todo el planeta a un coste radicalmente menor. Este lanzamiento confirma que la brecha entre "
            "la IA china y la estadounidense se ha cerrado casi por completo. Junto a Qwen 3.8, la startup "
            "Moonshot AI también presentó nuevos modelos en la Conferencia Mundial de IA celebrada en Shanghai."
        ),
        "fuente_label": "Merca2 — Alibaba Qwen 3.8 desafía a EEUU",
        "fuente_url": "https://www.merca2.es/2026/07/20/qwen-3-8-alibaba-desafia-eeuu-2420994/",
    },
    {
        "emoji": "📋",
        "titulo": "China aprueba su Plan Maestro de IA 2026: inversión récord y soberanía tecnológica",
        "cuerpo": (
            "Pekín aprobó su Plan Maestro de Inteligencia Artificial para 2026, consagrando la doctrina "
            "IA Plus —integrar la IA como infraestructura transversal en toda la economía—, los enjambres "
            "de agentes autónomos y la robótica inteligente como pilares del desarrollo nacional. China "
            "destina ya 3,93 billones de yuanes a investigación y desarrollo, equivalente al 2,8% de su PIB, "
            "con la meta de que el 70% de los sectores productivos incorporen IA antes de 2027 y el 90% "
            "antes de 2030. Las industrias relacionadas con IA superarán los 10 billones de yuanes para 2030."
        ),
        "fuente_label": "Moncloa — China Plan Maestro IA 2026",
        "fuente_url": "https://www.moncloa.com/2026/07/12/china-plan-maestro-ia-2026-3398625/",
    },
    {
        "emoji": "🌐",
        "titulo": "WAIC 2026 en Shanghai: China propone una nueva gobernanza mundial de la IA",
        "cuerpo": (
            "La Conferencia Mundial de Inteligencia Artificial (WAIC) 2026 reunió en Shanghai del 17 al 20 "
            "de julio a las mayores figuras del sector tecnológico global. El presidente Xi Jinping advirtió "
            "que la IA no debe estar dominada por un solo país e instó a construir una arquitectura "
            "internacional plural para gobernarla. Empresas como Alibaba, Baidu, Moonshot AI y decenas de "
            "startups presentaron sus últimos modelos y aplicaciones. El evento consolidó a Shanghai como "
            "capital mundial de la innovación en IA."
        ),
        "fuente_label": "El Cronista — La cumbre que define el futuro de la IA",
        "fuente_url": "https://www.cronista.com/columnistas/la-cumbre-que-puede-definir-el-futuro-de-la-inteligencia-artificial-y-del-poder-mundial/",
    },
    {
        "emoji": "🦾",
        "titulo": "China supera los 100.000 robots humanoides en 2026 — BYD presenta los suyos en agosto",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de la Información de China confirmó que la producción "
            "nacional de robots humanoides superará las 100.000 unidades en 2026, convirtiendo al país en el "
            "primer productor mundial de este tipo de máquinas. La gran sorpresa: BYD, el gigante de los "
            "vehículos eléctricos, anunció que presentará sus primeros robots humanoides en agosto en sus "
            "centros de experiencia Di Space, intensificando la rivalidad con Tesla y su Optimus. Según el "
            "Centro Nacional de Innovación en Robótica Humanoide de Shanghai, China ya lidera en fabricación, "
            "datasets y entornos de entrenamiento de inteligencia corpórea."
        ),
        "fuente_label": "CGTN — China's humanoid robot output set to exceed 100,000 in 2026",
        "fuente_url": "https://news.cgtn.com/news/2026-07-08/China-s-output-of-humanoid-robots-set-to-exceed-100-000-in-2026-1OBFKOQ9WUg/p.html",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior crece 16,9% en el primer semestre de 2026 — exportaciones de junio +27%",
        "cuerpo": (
            "El intercambio comercial de China alcanzó los 25,47 billones de yuanes (unos 3,75 billones de "
            "dólares) en el primer semestre de 2026, superando por primera vez los 25 billones en ese período. "
            "Las exportaciones de junio se dispararon un 27% interanual, el mayor avance en cuatro meses, muy "
            "por encima del 19% previsto por los analistas. El motor principal fue el hardware para centros de "
            "datos de IA: los componentes electrónicos y de cómputo crecieron un 56,6%. El comercio con "
            "América Latina creció un 16,2% y con África un 19,6%, consolidando el papel de China como "
            "socio comercial global prioritario."
        ),
        "fuente_label": "People's Daily Español — Comercio exterior de China crece 16,9% en H1 2026",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0715/c31620-20477940.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 lista para despegar: lanzamiento al polo sur lunar abre el 24 de agosto",
        "cuerpo": (
            "La misión Chang'e-7 está preparada para su lanzamiento, con la ventana oficial abierta del "
            "24 al 31 de agosto de 2026. La sonda explorará el polo sur de la Luna en busca de depósitos "
            "de agua en forma de hielo dentro de cráteres en sombra permanente. La misión incluye un "
            "orbitador, un satélite repetidor, un módulo de aterrizaje, un rover y una mini sonda saltadora "
            "capaz de adentrarse en zonas inaccesibles para vehículos convencionales. Chang'e-7 es un paso "
            "fundamental en el programa lunar tripulado chino, con meta de aterrizaje humano antes de 2030."
        ),
        "fuente_label": "Space Policy Online — Launch of China's Chang'e-7, window opens Aug 24, 2026",
        "fuente_url": "https://spacepolicyonline.com/events/launch-of-chinas-change-7-robotic-lunar-mission-window-opens-aug-24-2026/",
    },
    {
        "emoji": "⚡",
        "titulo": "China concentra la mitad de la capacidad eólica y solar del mundo: 1.840 GW renovables",
        "cuerpo": (
            "China ha alcanzado los 1.840 GW de capacidad instalada de energía eólica y solar, representando "
            "el 47,3% de toda la capacidad eléctrica del país y más de la mitad de la capacidad instalada en "
            "todo el mundo. Por primera vez en su historia, las energías limpias superaron al carbón y al gas "
            "en el mix eléctrico chino. La generación renovable superó el 40% del total nacional, un hito que "
            "los planificadores no esperaban hasta 2030. El país continúa construyendo macroinstalaciones de "
            "energía solar concentrada (CSP), con 24 plantas en operación y 26 más en construcción, "
            "sumando 3,2 GW de capacidad almacenable."
        ),
        "fuente_label": "El Periódico de la Energía — Renovables superan el 40% en China",
        "fuente_url": "https://elperiodicodelaenergia.com/la-generacion-de-energia-renovable-supera-por-primera-vez-el-40-del-total-en-china",
    },
    {
        "emoji": "💻",
        "titulo": "Exportaciones de alta tecnología +39%: chips e IA lideran el comercio exterior chino",
        "cuerpo": (
            "Las exportaciones chinas de productos de alta tecnología crecieron un 39% interanual en el "
            "primer semestre de 2026, impulsadas por la demanda global de infraestructura para IA. El "
            "hardware computacional —incluyendo componentes electrónicos y partes de cómputo— se disparó "
            "un 56,6%, mientras que las exportaciones de aerogeneradores y baterías de litio aumentaron "
            "un 35,6% y un 37,6% respectivamente. Los astilleros chinos captaron el 72% de los encargos "
            "mundiales de nuevos barcos en el primer semestre. China está consolidando su posición como "
            "exportador líder de las tecnologías estratégicas del siglo XXI."
        ),
        "fuente_label": "TLC Magazine México — China rompe récord de comercio exterior en H1 2026",
        "fuente_url": "https://tlcmagazinemexico.com.mx/index.php/2026/07/16/china-rompe-record-de-comercio-exterior-en-el-primer-semestre-de-2026/",
    },
]


def fecha_es(d):
    return f"{d.day} de {MESES_ES[d.month - 1]} de {d.year}"


def build_blocks():
    today = fecha_es(date.today())
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
    title = "China Al Dia — Semana 28 Jul - 2 Ago 2026"
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
