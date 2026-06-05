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
        "titulo": "China lanza el cohete reutilizable Long March 12B en vuelo inaugural sorpresa",
        "cuerpo": (
            "El 1 de junio de 2026 a las 08:40 UTC, China lanzó el cohete Long March 12B desde Jiuquan "
            "sin emitir ningún aviso previo, poniendo en órbita satélites de la megaconstelación Qianfan "
            "(Mil Velas). El Long March 12B es un vehículo propulsado por queroseno y oxígeno líquido, "
            "diseñado para recuperar su primera etapa mediante aterrizaje propulsivo similar al Falcon 9 "
            "de SpaceX. La misión confirma que China ya opera cohetes reutilizables con cargas útiles "
            "comerciales reales, marcando un hito en la carrera espacial del país."
        ),
        "fuente_label": "SpaceNews — China conducts surprise launch of Long March 12B",
        "fuente_url": "https://spacenews.com/china-conducts-surprise-launch-of-long-march-12b-delivers-qianfan-satellites-on-debut-flight/",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree Robotics: primera empresa de robots humanoides en cotizar en bolsa",
        "cuerpo": (
            "El 1 de junio, la Bolsa de Shanghai aprobó la OPI de Unitree Robotics, convirtiéndola en "
            "la primera empresa de 'IA encarnada' admitida en el mercado A-share de China. La compañía "
            "busca recaudar 4.200 millones de yuanes (~616 millones USD) con una valoración de 6.200 "
            "millones USD. NVIDIA además ha designado su robot H2 Plus como plataforma de referencia "
            "para el proyecto GR00T de humanoides de código abierto. Más de 46 empresas de robótica "
            "chinas ya están en cola para cotizar en Hong Kong."
        ),
        "fuente_label": "Bloomberg — China Robotics Firms Line Up IPOs",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-01/china-robotics-firms-line-up-ipos-to-pitch-next-phase-of-ai",
    },
    {
        "emoji": "💡",
        "titulo": "Huawei anuncia ruptura tecnológica en diseño de chips con arquitectura LogicFolding",
        "cuerpo": (
            "Huawei anunció que sus chips Kirin de próxima generación utilizarán la arquitectura "
            "LogicFolding, que apila circuitos 2D en estructuras 3D verticales para mejorar rendimiento "
            "sin depender del encogimiento de transistores. La compañía proyecta alcanzar una densidad "
            "equivalente a procesos de 1,4 nm para 2031 —la frontera tecnológica global esperada para "
            "esa fecha—. Esta tecnología también potencia la serie Ascend, que alimenta modelos de IA "
            "chinos como DeepSeek V4."
        ),
        "fuente_label": "NBC News — Huawei touts chip design breakthrough",
        "fuente_url": "https://www.nbcnews.com/world/asia/chinas-huawei-touts-chip-design-breakthrough-bid-defy-us-sanctions-rcna346783",
    },
    {
        "emoji": "🦾",
        "titulo": "China domina la IA física: datos de millones de horas de movimiento humano",
        "cuerpo": (
            "China ha construido un ecosistema masivo de datos de movimiento humano recogidos en hogares "
            "y fábricas, superando al modelo estadounidense en escala y coste. El 15° Plan Quinquenal "
            "coloca la robótica como eje del sistema industrial moderno, con empresas chinas de humanoides "
            "ya desplegando unidades en fábricas y centros comerciales con contratos reales. La revista "
            "Time calificó este mes a China como la nación que podría dominar el futuro de la IA física, "
            "con más de 46 empresas de robótica preparando su salida a bolsa."
        ),
        "fuente_label": "Time — China Could Dominate the Physical AI Future",
        "fuente_url": "https://time.com/7382151/china-dominates-the-physical-ai-race/",
    },
    {
        "emoji": "📈",
        "titulo": "Las exportaciones chinas se disparan un 26% en abril pese a aranceles globales",
        "cuerpo": (
            "Las exportaciones chinas registraron un incremento del 26% interanual en abril de 2026, "
            "impulsadas por vehículos eléctricos, paneles solares, baterías, turbinas eólicas y "
            "semiconductores. A pesar de los aranceles estadounidenses, China diversificó sus mercados "
            "hacia Asia y Europa, donde las ventas de autos eléctricos chinos crecieron más del 30% el "
            "año anterior. El superávit comercial del país se estima en 1,2 billones de dólares anuales, "
            "el mayor de su historia."
        ),
        "fuente_label": "World Economic Forum — State of China's Economy in 5 Numbers",
        "fuente_url": "https://www.weforum.org/stories/2026/06/the-state-of-china-economy-in-five-numbers/",
    },
    {
        "emoji": "🌍",
        "titulo": "China aplica aranceles cero al 100% de los países africanos con relaciones diplomáticas",
        "cuerpo": (
            "A partir del 1 de mayo de 2026, China extendió el arancel cero al total de bienes gravables "
            "provenientes de los 53 países africanos con los que mantiene relaciones diplomáticas. Kenia, "
            "Egipto, Nigeria, Costa de Marfil y Ghana son los principales beneficiarios: sus productos "
            "(café, aguacates, cacao, vino) enfrentaban antes aranceles de entre el 8% y el 30%. La "
            "medida refuerza la apuesta de China por el crecimiento del Sur Global."
        ),
        "fuente_label": "Xinhua — China's new zero-tariff policy for Africa",
        "fuente_url": "https://english.news.cn/20260501/8ff23078c91e4d9e8e8af9cc702231d9/c.html",
    },
    {
        "emoji": "🏙️",
        "titulo": "Shenzhen se prepara para liderar la agenda tecnológica global en APEC 2026",
        "cuerpo": (
            "Shenzhen albergará la cumbre del APEC los días 18 y 19 de noviembre de 2026, con China "
            "posicionando la gobernanza de la IA, la resiliencia de cadenas de suministro y la "
            "infraestructura digital como ejes centrales. La ciudad ya despliega demostraciones de "
            "transporte autónomo, drones ('economía de baja altitud') y robots humanoides en servicios "
            "públicos. El evento proyecta a China como arquitecta de las normas tecnológicas globales "
            "para la próxima década."
        ),
        "fuente_label": "Diario Financiero — China y APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "☄️",
        "titulo": "Tianwen-2 en camino: encuentro con el asteroide Kamo'oalewa previsto para julio",
        "cuerpo": (
            "La sonda china Tianwen-2 avanza hacia su encuentro del 4 de julio con el asteroide 469219 "
            "Kamo'oalewa, en la primera misión de retorno de muestras asteroidales de China. Un nuevo "
            "estudio publicado en Nature Communications en junio cuestiona su origen lunar, sugiriendo "
            "que su superficie coincide con condritos LL muy meteorizados. Tras recoger muestras, la "
            "sonda regresará a la Tierra en noviembre de 2027 y después se dirigirá al cometa "
            "311P/PanSTARRS."
        ),
        "fuente_label": "Phys.org — Kamo'oalewa asteroid update / Tianwen-2",
        "fuente_url": "https://phys.org/news/2026-06-kamooalewa-asteroid-lunar-tianwen.html",
    },
    {
        "emoji": "⚡",
        "titulo": "China: el 60% de su capacidad eléctrica ya es renovable",
        "cuerpo": (
            "A cierre del primer trimestre de 2026, la capacidad instalada de energías renovables de "
            "China alcanzó los 2.395 GW (+22% interanual), representando el 60,4% de la capacidad "
            "eléctrica total del país. Xinhua publicó el 2 de junio un análisis detallando cómo China "
            "protege sus industrias emergentes con un suministro energético verde y seguro. El 15° Plan "
            "Quinquenal proyecta duplicar la producción de energía no fósil para 2035, con hidrógeno "
            "verde y solar de concentración como nuevos motores industriales."
        ),
        "fuente_label": "Xinhua — China striving to become energy powerhouse",
        "fuente_url": "https://english.news.cn/20260602/7d378af33ae847bead95aa9905dbd421/c.html",
    },
    {
        "emoji": "🤝",
        "titulo": "Xi Jinping y Trump abren canales diplomáticos en medio de competición tecnológica",
        "cuerpo": (
            "El presidente Xi Jinping y Donald Trump mantuvieron conversaciones formales en mayo de 2026, "
            "en un esfuerzo por sostener canales diplomáticos en medio de la intensa competición "
            "tecnológica y comercial entre ambas potencias. China reiteró su postura de resolver "
            "diferencias mediante diálogo, oponiéndose a medidas arancelarias unilaterales. El MIT "
            "destacó en junio la importancia de mantener vías diplomáticas funcionales para evitar "
            "escaladas en la rivalidad bilateral."
        ),
        "fuente_label": "Ministerio de Relaciones Exteriores de China — Xi-Trump Talks",
        "fuente_url": "https://www.fmprc.gov.cn/eng/xw/zyxw/202605/t20260514_11910330.html",
    },
    {
        "emoji": "🌏",
        "titulo": "Myanmar visita China: 76 años de amistad y comunidad de destino compartido",
        "cuerpo": (
            "El Ministro de Relaciones Exteriores de Myanmar, Tin Maung Swe, realizó una visita oficial "
            "a China del 4 al 6 de junio, celebrando 76 años de lazos diplomáticos bajo el concepto de "
            "'comunidad de destino compartido'. La visita refuerza la cooperación bilateral en "
            "infraestructura, comercio y seguridad regional, en línea con la diplomacia de vecindad del "
            "gobierno de Xi Jinping en el sudeste asiático."
        ),
        "fuente_label": "FMPRC — Myanmar Foreign Minister visits China",
        "fuente_url": "https://www.fmprc.gov.cn/eng/xw/fyrbt/202606/t20260603_11936890.html",
    },
    {
        "emoji": "🎨",
        "titulo": "350 millones de jóvenes chinos fusionan herencia tradicional con cultura digital global",
        "cuerpo": (
            "Xinhua destaca cómo los jóvenes chinos de 14 a 35 años están convirtiéndose en motor de "
            "innovación cultural, fusionando patrimonio tradicional con formatos digitales. Productos "
            "como un imán de nevera con forma de corona fénix han vendido más de un millón de unidades "
            "anuales, y una skin de videojuego inspirada en los murales de Dunhuang superó los 40 "
            "millones de ventas. En enero de 2026, los ingresos de juegos chinos en el exterior "
            "alcanzaron los 2.077 millones USD (+24% interanual)."
        ),
        "fuente_label": "Xinhua — Young Chinese breathe new life into traditional culture",
        "fuente_url": "https://english.news.cn/20260526/5c802d210a584c2989a4d5ccd3c2ea23/c.html",
    },
]


def build_blocks():
    today = date.today().strftime("%d de junio de %Y")
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
    title = "China Al Dia — Semana 1-5 Junio 2026"
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
