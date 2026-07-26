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

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


NOTICIAS = [
    {
        "emoji": "🌐",
        "titulo": "WAIC 2026: 29 países fundan la primera organización multilateral de inteligencia artificial",
        "cuerpo": (
            "La Conferencia Mundial de Inteligencia Artificial (WAIC 2026) concluyó en Shanghái con un "
            "hito histórico: 29 países firmaron el acuerdo constitutivo de la Organización Mundial para "
            "la Cooperación en Inteligencia Artificial, el primer organismo multilateral de su tipo. "
            "El presidente Xi Jinping defendió un modelo global basado en la cooperación, el acceso "
            "equitativo y la participación de los países en desarrollo, y anunció la creación de un "
            "centro internacional de cooperación en IA junto a la CELAC. La conferencia reunió a más "
            "de 400 empresas y 350 modelos de IA de decenas de naciones."
        ),
        "fuentes": [
            ("CGTN Español", "https://espanol.cgtn.com/2026/07/19/ARTI1784426596140231"),
            ("Diario Red", "https://www.diario-red.com/articulo/internacional/china-desafia-control-tecnologico-ee-uu-modelo-global-abierto-inteligencia-artificial/20260719040429073168.html"),
        ],
    },
    {
        "emoji": "🤖",
        "titulo": "China lidera el 70% del mercado global de robots cuadrúpedos y supera los 400 modelos humanoides",
        "cuerpo": (
            "El sector robótico chino alcanzó una posición de dominio sin precedentes: los robots "
            "cuadrúpedos fabricados en China representaron cerca del 70% de las ventas mundiales. El "
            "país cuenta con más de 400 modelos de robots humanoides, superando la mitad de todos los "
            "productos disponibles a nivel global. Estos avances, presentados durante la WAIC 2026, "
            "reflejan la aceleración de la economía inteligente como eje central del 15.º Plan Quinquenal."
        ),
        "fuentes": [
            ("Prensa Latina", "https://www.prensa-latina.cu/2026/07/20/china-con-liderazgo-en-robotica-inteligente-ia-y-otras-industrias/"),
            ("TechXplore", "https://techxplore.com/news/2026-07-shanghai-science-forum-photos-china.html"),
        ],
    },
    {
        "emoji": "💻",
        "titulo": "Supercomputación espacial y 2.185 EFLOPS: la infraestructura de IA de China alcanza nuevas cotas",
        "cuerpo": (
            "En la WAIC 2026, empresas chinas presentaron un superclúster de IA de 100.000 tarjetas "
            "totalmente fabricado en China y sistemas de infraestructura integrados tierra-espacio para "
            "computación con IA. La capacidad de computación inteligente de China ya alcanzó 2.185 EFLOPS "
            "a finales de junio. Este despliegue masivo sitúa al país en posición de competir con los "
            "mayores centros de datos del mundo, con la ventaja adicional de extender la red al espacio "
            "para mayor flexibilidad y resiliencia global."
        ),
        "fuentes": [
            ("Global Times", "https://www.globaltimes.cn/page/202607/1366311.shtml"),
            ("CGTN", "https://news.cgtn.com/news/2026-07-20/China-s-high-tech-sector-gains-momentum-in-first-half-of-2026-1OVBxolqoqk/p.html"),
        ],
    },
    {
        "emoji": "🔬",
        "titulo": "IA científica autónoma: de predecir erupciones solares al descubrimiento de fármacos anticáncer",
        "cuerpo": (
            "La inteligencia artificial china da saltos cualitativos en investigación científica. "
            "Avances recientes: completó la disposición sin defectos de 2.024 qubits en 60 milisegundos; "
            "descubrió y validó de forma autónoma nuevos objetivos terapéuticos contra el cáncer; logró "
            "predicción de erupciones solares de clase X con 100% de acierto activando automáticamente "
            "telescopios; y analizó el cambio climático global en minutos en lugar de días. La IA "
            "científica china pasa de ser herramienta asistente a motor de descubrimiento autónomo."
        ),
        "fuentes": [
            ("36kr International", "https://eu.36kr.com/en/p/3884022753882115"),
            ("Global Times", "https://www.globaltimes.cn/page/202605/1361310.shtml"),
        ],
    },
    {
        "emoji": "📊",
        "titulo": "Patentes de IA en China: +34,8% interanual en el primer semestre de 2026",
        "cuerpo": (
            "El dinamismo innovador de China se refleja en sus datos de propiedad intelectual: las "
            "autorizaciones de patentes vinculadas a inteligencia artificial crecieron un 34,8% "
            "interanual en el primer semestre de 2026, y las relacionadas con industrias estratégicas "
            "emergentes avanzaron un 15,6%. La industria central de IA del país acumula un valor "
            "superior al billón de yuanes, impulsada por el mandato político de modernizar China "
            "mediante la ciencia y la tecnología."
        ),
        "fuentes": [
            ("Prensa Latina", "https://www.prensa-latina.cu/2026/07/13/china-reporta-alza-en-indicadores-de-consumo-e-innovacion-tecnologica/"),
            ("China.org.cn", "http://spanish.china.org.cn/txt/2026-07/09/content_118590390.htm"),
        ],
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China crece un 4,7% en el primer semestre de 2026: 9,7 billones de dólares",
        "cuerpo": (
            "La Oficina Nacional de Estadísticas de China confirmó un crecimiento del PIB del 4,7% "
            "interanual en el primer semestre de 2026, con un producto interior bruto de 69,57 "
            "billones de yuanes (aproximadamente 9,7 billones de dólares). La producción industrial "
            "de grandes empresas avanzó un 5,4% y el sector servicios un 5,2%. Las autoridades "
            "mantendrán en el segundo semestre políticas orientadas a ampliar la demanda interna y "
            "consolidar nuevos motores de crecimiento, con estabilidad como objetivo central."
        ),
        "fuentes": [
            ("Prensa Latina", "https://www.prensa-latina.cu/2026/07/15/economia-china-crece-47-por-ciento-en-primer-semestre/"),
            ("Trading Economics", "https://es.tradingeconomics.com/china/gdp-growth-annual"),
        ],
    },
    {
        "emoji": "🤝",
        "titulo": "México y China estrechan lazos en IA, robótica y semiconductores",
        "cuerpo": (
            "México y China firmaron acuerdos de cooperación científica en inteligencia artificial, "
            "robótica y semiconductores. China también manifestó su interés en expandir la cooperación "
            "en infraestructura verde con México, identificando sectores de inversión conjunta en "
            "energías limpias y conectividad digital. El acercamiento refleja la creciente influencia "
            "de China en América Latina como socio tecnológico y económico prioritario para la región."
        ),
        "fuentes": [
            ("Excélsior", "https://www.excelsior.com.mx/nacional/mexico-y-china-estrechan-lazos-cientificos-inteligencia-artificial-robotica-y-semiconductores"),
            ("Forbes México", "https://forbes.com.mx/china-ve-potencial-para-crecer-cooperacion-en-infraestructura-verde-con-mexico/"),
        ],
    },
    {
        "emoji": "🚀",
        "titulo": "Tianwen-2: China recogerá muestras de un asteroide antes de que acabe julio",
        "cuerpo": (
            "La misión china Tianwen-2 está en camino de recoger aproximadamente 1 kg de muestras "
            "del asteroide objetivo. La sonda liberará la cápsula de muestras hacia la Tierra en un "
            "sobrevuelo en 2027 y, a continuación, continuará su viaje durante 7 años hasta alcanzar "
            "un cometa. China sería así el tercer país en traer muestras de un asteroide a la Tierra, "
            "en el marco del ambicioso programa espacial que también prepara una misión tripulada "
            "lunar antes de 2030."
        ),
        "fuentes": [
            ("South China Morning Post", "https://www.scmp.com/topics/chinas-space-programme"),
            ("National Science Review", "https://academic.oup.com/nsr/article/13/1/nwaf335/8248510"),
        ],
    },
    {
        "emoji": "☀️",
        "titulo": "La energía solar de China superará al carbón en capacidad instalada por primera vez en 2026",
        "cuerpo": (
            "China está a punto de alcanzar un hito histórico: se prevé que la capacidad instalada "
            "de energía solar supere por primera vez a la del carbón en 2026, y que la eólica y la "
            "solar representen conjuntamente la mitad de la capacidad total de generación eléctrica "
            "a finales de año. Además, a partir de agosto entrarán en vigor nuevas reglas que "
            "obligarán a provincias e industrias clave —acero, cemento, centros de datos, redes 5G— "
            "a cumplir objetivos concretos de consumo de energías renovables, consolidando a China "
            "como el primer gran electroestado del mundo."
        ),
        "fuentes": [
            ("El Periódico de la Energía", "https://elperiodicodelaenergia.com/china-preve-que-la-capacidad-instalada-de-energia-solar-supere-al-carbon-en-2026/"),
            ("Ecoportal", "https://www.ecoportal.net/energia/china-electroestado-energia-limpia/"),
        ],
    },
    {
        "emoji": "🏥",
        "titulo": "CMEF 2026: la mayor feria médica del mundo reúne a 300.000 profesionales de 150 países en Shanghái",
        "cuerpo": (
            "La 93.ª edición de la Feria Internacional de Equipos Médicos de China (CMEF) concluyó "
            "en Shanghái bajo el lema 'Fusión de la innovación, evolución sin límites', reuniendo a "
            "más de 300.000 participantes de más de 150 países. Los temas centrales fueron la IA en "
            "la atención sanitaria, las interfaces cerebro-computadora, los dispositivos para la "
            "economía plateada (envejecimiento de la población) y los avances regulatorios. China "
            "se posiciona como hub global de innovación médica y diagnóstico por imagen de vanguardia."
        ),
        "fuentes": [
            ("PR Newswire", "https://www.prnewswire.com/news-releases/cmef-2026-concluye-en-shanghai-un-escenario-global-para-los-avances-medicos-y-las-tendencias-futuras-302759219.html"),
        ],
    },
    {
        "emoji": "🩺",
        "titulo": "IA y Medicina Tradicional China: quioscos de diagnóstico inteligente llegan al metro",
        "cuerpo": (
            "China despliega quioscos de diagnóstico asistido por IA en estaciones de metro y puntos "
            "urbanos, integrando tecnología biomédica avanzada con la Medicina Tradicional China. "
            "Los dispositivos miden presión arterial, frecuencia cardíaca, saturación de oxígeno y "
            "temperatura, mientras la IA aplica criterios clásicos: análisis facial, observación de "
            "la lengua e interpretación del pulso mediante sensores multicapa. La Comisión Nacional "
            "de Salud impulsa esta integración como parte de la estrategia nacional de salud digital."
        ),
        "fuentes": [
            ("Mundo Global", "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/"),
            ("Consalud", "https://www.consalud.es/salud35/analisis/la-industria-biomedica-china-acelera-su-transformacion-el-capital-en-i-d-impulsa-un-nuevo-modelo-de-crecimiento.html"),
        ],
    },
    {
        "emoji": "🗺️",
        "titulo": "La Iniciativa Cinturón y Ruta evoluciona: hacia la Ruta de la Seda Verde y Digital en 2026",
        "cuerpo": (
            "En 2026, la Iniciativa Cinturón y Ruta (BRI) entra en una nueva fase estratégica de "
            "calidad sobre cantidad. El Consejo Asesor del Foro BRI se reunió en Urumqi para definir "
            "las prioridades frente a la incertidumbre global. Los nuevos pilares son la Green Silk "
            "Road (energías renovables e infraestructura sostenible), la Digital Silk Road (redes 5G "
            "y comercio electrónico) y la cooperación en IA con el Sur Global. La BRI sigue siendo "
            "el principal mecanismo de China para fortalecer lazos económicos con más de 150 países socios."
        ),
        "fuentes": [
            ("CGTN", "https://news.cgtn.com/news/2026-07-17/VHJhbnNjcmlwdDkxNjA4/index.html"),
            ("UDLAP Observatory", "https://observatorioglobal.udlap.mx/the-belt-and-road-initiative-in-2026-from-expansion-to-strategic-high-quality-cooperation/"),
            ("Observatorio de Política China", "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-65/"),
        ],
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, energia y salud.", bold=False),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        for label, url in n["fuentes"]:
            blocks.append(p_link(label, url))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 20-26 Julio 2026"
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
