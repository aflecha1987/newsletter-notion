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
        "emoji": "🤖",
        "titulo": "China ordena 10.000 robots humanoides en trabajo real antes de fin de año",
        "cuerpo": (
            "El 10 de junio, el gobierno chino emitió una directiva exigiendo que 10.000 robots humanoides "
            "estén en uso comercial activo —en fábricas, almacenes, hospitales y operaciones de emergencia— "
            "antes del 31 de diciembre de 2026. Los gobiernos locales deben entregar planes de despliegue "
            "antes de finales de junio. La cifra no es aspiracional: es un mandato con informes de "
            "seguimiento en noviembre. Para el 18 de junio, China ya enviaba el 90% de todos los robots "
            "humanoides producidos en el mundo, y sus empresas lideran los principales benchmarks de IA "
            "encarnada. Una fábrica de robots en Pekín ya ha entregado 300 unidades a clientes reales "
            "desde su apertura en abril, apuntando a 10.000 unidades antes de fin de año."
        ),
        "fuente_label": "Caixin Global — China Targets 10,000 Humanoid Robots in Commercial Use by End-2026",
        "fuente_url": "https://www.caixinglobal.com/2026-06-10/china-targets-10000-humanoid-robots-in-commercial-use-by-end-2026-102452656.html",
    },
    {
        "emoji": "💡",
        "titulo": "Plan de 295.000 millones de dólares para una red nacional de centros de datos de IA",
        "cuerpo": (
            "El 9 de junio, Bloomberg reveló que China está diseñando un megaplan de 2 billones de yuanes "
            "(~295.000 millones de dólares) para construir una red interconectada de centros de datos de IA "
            "en todo el país, con objetivo de tenerla operativa en 2028. El plan exige que al menos el 80% "
            "de los chips utilizados sean de fabricación nacional —fundamentalmente de Huawei— cerrando "
            "efectivamente la puerta a Nvidia y AMD. Las empresas estatales China Mobile y China Telecom "
            "operarán la mayor parte de la infraestructura, financiada mediante bonos soberanos y deuda "
            "especial a largo plazo. Junto al gasto privado de Alibaba, Tencent y Baidu, China construye "
            "la mayor infraestructura pública de IA del mundo."
        ),
        "fuente_label": "Bloomberg — China Plans $295 Billion Investment to Build Nationwide AI Data Centers",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout",
    },
    {
        "emoji": "🧠",
        "titulo": "Qwen 3.7 Max: el modelo IA abierto de Alibaba que lidera benchmarks globales",
        "cuerpo": (
            "Presentado en el Alibaba Cloud Summit de Hangzhou en mayo 2026, Qwen 3.7 Max es la nueva "
            "apuesta de Alibaba por la IA de frontera de código abierto. Con una ventana de contexto de "
            "1 millón de tokens, supera a modelos globales en Terminal-Bench 2.0, SWE-Bench Pro y "
            "MCP-Atlas, y registra la tasa de alucinación más baja entre todos los modelos de frontera "
            "(22,9%). Los modelos de la familia Qwen acumulan ya cerca de 1.000 millones de descargas "
            "en Hugging Face, representando más del 50% de todas las descargas de modelos de IA abiertos "
            "a nivel mundial. El modelo supera a sus competidores occidentales en más de 15 benchmarks "
            "especializados de agentes y programación."
        ),
        "fuente_label": "Digital Applied — Qwen 3.7 Max: Alibaba's Strongest AI Model Yet",
        "fuente_url": "https://www.digitalapplied.com/blog/qwen-3-7-max-alibaba-flagship-ai-model-2026",
    },
    {
        "emoji": "💾",
        "titulo": "SMIC produce en masa chips 5nm sin litografía EUV: hito histórico",
        "cuerpo": (
            "SMIC, el mayor fabricante de chips de China, ha confirmado producción en masa de su nodo "
            "N+3 de clase 5nm sin necesidad de equipos de litografía ultravioleta extrema (EUV) —que "
            "China no puede importar por las restricciones de exportación—, utilizando en su lugar procesos "
            "avanzados de múltiple patterning con tecnología DUV. El logro fue verificado de forma "
            "independiente y en 2026 se ha entrado en fase de suministro a partners como Huawei y Alibaba "
            "para chips de IA. SMIC proyecta ingresos superiores a 11.000 millones de dólares en 2026, "
            "consolidando la autosuficiencia tecnológica de China en uno de los sectores más críticos "
            "para la economía global."
        ),
        "fuente_label": "SCMP — SMIC unveils action plan for seizing new growth opportunities",
        "fuente_url": "https://www.scmp.com/tech/big-tech/article/3348044/chinas-top-chip-foundry-smic-unveils-action-plan-seizing-new-growth-opportunities",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23: la primera astronauta de Hong Kong y el reto del año en el espacio",
        "cuerpo": (
            "El 24 de mayo, China lanzó la misión tripulada Shenzhou-23 desde Jiuquan. La tripulación "
            "la integran el comandante Zhu Yangzhu, el piloto Zhang Zhiyuan y Li Jiaying, la primera "
            "astronauta procedente de Hong Kong en la historia del programa espacial chino. El objetivo "
            "histórico de esta misión: que un miembro de la tripulación permanezca un año completo en la "
            "estación espacial Tiangong, el período de mayor duración jamás intentado por China. Los datos "
            "fisiológicos recopilados serán fundamentales para planificar las misiones lunares tripuladas "
            "previstas para antes de 2030, en el marco del programa de exploración lunar más ambicioso "
            "de la historia del país."
        ),
        "fuente_label": "Semana — China lanzó la misión espacial Shenzhou-23",
        "fuente_url": "https://www.semana.com/tecnologia/articulo/china-lanzo-la-mision-espacial-shenzhou-23-por-primera-vez-un-astronauta-permanecera-un-ano-completo-en-el-espacio/202646/",
    },
    {
        "emoji": "🛸",
        "titulo": "PM01: el primer astronauta robótico del mundo se prepara para el espacio",
        "cuerpo": (
            "La empresa china Engine AI y la compañía de turismo espacial Interstellar anunciaron el "
            "primer programa de astronauta robótico humanoide de la historia. El robot PM01 (1,38 m, "
            "40 kg) fue conectado a un satélite como prueba previa en enero de 2026. El robot incorpora "
            "sensores de entorno de alta precisión, respuesta de movimiento en milisegundos y algoritmos "
            "de decisión autónoma. Su misión en el espacio: mantenimiento de estaciones, monitorización "
            "de larga duración y operaciones en entornos de alta radiación donde los humanos no pueden "
            "operar. China avanza así en convertir la robótica de IA encarnada en el motor de su "
            "programa espacial del futuro."
        ),
        "fuente_label": "Interesting Engineering — China: World's first robot astronaut for space exploration",
        "fuente_url": "https://interestingengineering.com/ai-robotics/worlds-first-humanoid-robot-astronaut-china",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar china supera al carbón por primera vez",
        "cuerpo": (
            "En 2026, China cruza uno de los umbrales energéticos más importantes de su historia: la "
            "capacidad solar instalada supera por primera vez a la del carbón. La potencia solar "
            "instalada ya supera los 1.230 gigavatios y crece a un ritmo sin precedentes. Combinada "
            "con la eólica, la energía limpia representa ya el 50% de la capacidad total instalada del "
            "país. Para finales de año, la energía no fósil representará el 63% del mix energético "
            "nacional, dentro del marco del XV Plan Quinquenal (2026-2030). China fabrica tantos "
            "paneles solares que la industria global enfrenta una crisis de sobreoferta, consolidando "
            "al país como el lider indiscutible de la transición energética mundial."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de VE chinos baten récord histórico: 430.000 unidades en un mes",
        "cuerpo": (
            "En abril de 2026, China exportó 430.000 nuevos vehículos de energía (eléctricos e híbridos "
            "enchufables), el mejor mes de la historia, con un crecimiento del +110% interanual. En los "
            "primeros cuatro meses del año, las exportaciones acumuladas superaron las 893.000 unidades. "
            "Los principales destinos son Asia (110.000 unidades/mes), Europa (83.000) y Latinoamérica "
            "(52.000). China fabrica el 75% de todos los vehículos eléctricos del mundo, y en 2025 "
            "alcanzó un récord de 2,5 millones de VE exportados —el doble que el año anterior—. BYD, "
            "Geely y Chery lideran la conquista de los mercados internacionales."
        ),
        "fuente_label": "Al Jazeera — China's EV exports surge 40 percent in April",
        "fuente_url": "https://www.aljazeera.com/economy/2026/5/27/chinas-ev-exports-surge-40-percent-in-april",
    },
    {
        "emoji": "🎓",
        "titulo": "China elimina 12.000 carreras universitarias y apuesta por la era de la IA",
        "cuerpo": (
            "El Ministerio de Educación de China anunció la eliminación de más de 12.000 carreras "
            "universitarias obsoletas y su sustitución por nuevos programas en inteligencia artificial, "
            "semiconductores, robótica, sistemas no tripulados (drones), economía de baja altitud y "
            "tecnologías marinas inteligentes. La medida forma parte del XV Plan Quinquenal y busca "
            "garantizar que las universidades chinas formen a los ingenieros y científicos que necesita "
            "la economía inteligente de 2030. China también se prepara para ser anfitriona del APEC 2026 "
            "en Shenzhen (noviembre), donde pondrá en el centro la gobernanza global de la IA y la "
            "resiliencia de las cadenas de suministro."
        ),
        "fuente_label": "Diario Financiero — China elimina más de 12.000 carreras universitarias",
        "fuente_url": "https://www.df.cl/internacional/economia/china-elimina-mas-de-12-000-carreras-universitarias-y-acelera-formacion-en",
    },
    {
        "emoji": "🏗️",
        "titulo": "Fábricas de datos de robótica en Shanghai, Tianjin y Fujian: la infraestructura del futuro",
        "cuerpo": (
            "China ha abierto grandes instalaciones industriales de recopilación de datos para robots "
            "humanoides en Shanghai, Tianjin y Fujian. Estas 'fábricas de datos' albergan a cientos "
            "de operadores humanos que enseñan a los robots a realizar tareas cotidianas —desde doblar "
            "ropa hasta manipular componentes electrónicos—, generando datasets masivos de IA encarnada "
            "de código abierto. El objetivo es acelerar el entrenamiento de los modelos de IA que harán "
            "que los robots sean útiles en el mundo real. Esta infraestructura es considerada por los "
            "expertos como la ventaja competitiva más importante de China en la carrera global por la "
            "robótica inteligente."
        ),
        "fuente_label": "Rest of World — How China is using human labor to win the humanoid robot data race",
        "fuente_url": "https://restofworld.org/2026/china-ai-robotics-training-data/",
    },
    {
        "emoji": "📊",
        "titulo": "ITIF: China innova en espacio más rápido que ningún competidor en la historia",
        "cuerpo": (
            "Un informe del Information Technology and Innovation Foundation (ITIF) publicado el 8 de "
            "junio concluye que China publica más de tres veces más investigación de alto impacto que "
            "su competidor más cercano en tecnología espacial, robótica y defensa, y alberga 8 de las "
            "10 principales instituciones del mundo en esas disciplinas. El informe señala que China ha "
            "pasado en una década de importador de tecnología espacial a exportador neto y referencia "
            "global. La velocidad de innovación, según el ITIF, no tiene precedentes en ningún país "
            "en la historia reciente y coloca a China en una posición de liderazgo estructural en las "
            "tecnologías que definirán el siglo XXI."
        ),
        "fuente_label": "ITIF — How Innovative Is China's Space Industry? (June 8, 2026)",
        "fuente_url": "https://itif.org/publications/2026/06/08/how-innovative-is-chinas-space-industry/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de junio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, IA, espacio, energia y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 13-20 Junio 2026"
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
