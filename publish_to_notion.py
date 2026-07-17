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
        "emoji": "🎤",
        "titulo": "Xi Jinping inaugura la WAIC 2026: 'La IA debe ser una sinfonía, no un solo'",
        "cuerpo": (
            "El 17 de julio, el presidente Xi Jinping abrió la Conferencia Mundial sobre Inteligencia "
            "Artificial (WAIC 2026) en Shanghái con un mensaje que resonó a nivel global: el desarrollo "
            "de la IA no debe ser un monopolio de un solo país, sino 'una sinfonía de cooperación "
            "internacional'. Xi celebró los avances de China en IA de bajo costo y accesible, e instó "
            "al mundo a adoptar un enfoque inclusivo y colaborativo. La conferencia, que se extiende "
            "del 17 al 20 de julio, reúne a centenares de líderes de la industria y de gobiernos para "
            "debatir la gobernanza global de la IA."
        ),
        "fuente_label": "Bloomberg — Xi Vows to Make AI for All at China's Top Tech Summit",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-07-17/xi-vows-to-make-ai-for-all-in-debut-at-china-s-top-tech-summit",
    },
    {
        "emoji": "📦",
        "titulo": "Comercio exterior de China bate récord histórico: 25,47 billones de yuanes en el primer semestre",
        "cuerpo": (
            "El comercio exterior de China creció un 16,9% interanual en el primer semestre de 2026, "
            "alcanzando un valor total de 25,47 billones de yuanes (aprox. 3,75 billones de dólares), "
            "superando por primera vez la barrera de los 25 billones en ese período. Las exportaciones "
            "sumaron 14,73 billones de yuanes (+13,4%) mientras las importaciones alcanzaron 10,74 "
            "billones (+22,1%), con 11 trimestres consecutivos de crecimiento exportador. Los sectores "
            "estrella: tecnología, manufactura avanzada, vehículos eléctricos y equipos industriales."
        ),
        "fuente_label": "People's Daily Español — Comercio exterior crece 16,9% en primer semestre 2026",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0715/c31620-20477940.html",
    },
    {
        "emoji": "🚗",
        "titulo": "China supera por primera vez 1 millón de vehículos exportados en un solo mes",
        "cuerpo": (
            "En junio de 2026, China exportó 1,037 millones de vehículos, un hito histórico que consolida "
            "al país como la primera potencia exportadora de automóviles del mundo. Los vehículos eléctricos "
            "e híbridos enchufables ya representan más de la mitad de las exportaciones. BYD lideró el "
            "ranking con 175.349 unidades exportadas en junio (+94,7% interanual), y sus exportaciones "
            "acumuladas en el primer semestre alcanzaron 789.367 unidades (+68%). Se proyecta que China "
            "exporte cerca de 10 millones de vehículos en todo 2026."
        ),
        "fuente_label": "Somos Eléctricos — China rompe todos los récords: ya exporta más de 1 millón de vehículos al mes",
        "fuente_url": "https://www.somoselectricos.com/coches-electricos/china-rompe-todos-records-exporta-mas-1-millon-vehiculos-mes/20260710095025058096.html",
    },
    {
        "emoji": "🤖",
        "titulo": "La IA se convierte en el nuevo motor de la industria china: más de 6.200 empresas y 1,2 billones de yuanes",
        "cuerpo": (
            "La inteligencia artificial está reconfigurando la segunda economía del mundo. En 2025, el "
            "sector principal de IA en China superó los 1,2 billones de yuanes (aprox. 176.700 millones "
            "de dólares) y cuenta con más de 6.200 empresas. En el primer semestre de 2026, las ventas "
            "de dispositivos inteligentes portátiles se duplicaron, y las de tiendas automatizadas "
            "crecieron más del 20%. iFlytek ya equipa con IA más de 50.000 escuelas; robots asistenciales "
            "operan en residencias geriátricas de Shenzhen; y la IA se despliega en hospitales de Pekín "
            "para diagnóstico asistido."
        ),
        "fuente_label": "Xinhua — IA emerge como nuevo motor de crecimiento para las industrias chinas",
        "fuente_url": "http://spanish.xinhuanet.com/20260716/1a7d8f8da7fc4c3ca583fa6c6a2f3683/c.html",
    },
    {
        "emoji": "💾",
        "titulo": "CXMT busca recaudar 10.000 millones de dólares para liderar los chips de memoria para IA",
        "cuerpo": (
            "CXMT (ChangXin Memory Technologies), pieza clave en la estrategia de autosuficiencia "
            "semiconductora de China, lanzó una ronda de financiación que podría superar los 10.000 "
            "millones de dólares. La empresa, especializada en chips de memoria DRAM, busca escalar "
            "masivamente su capacidad productiva para satisfacer la demanda creciente del sector de "
            "inteligencia artificial. China apuesta por CXMT como respuesta estratégica a las "
            "restricciones de exportación de chips de memoria impuestas por EE.UU."
        ),
        "fuente_label": "The Wire China — Daily Roundup July 15 2026",
        "fuente_url": "https://www.thewirechina.com/2026/07/15/the-daily-roundup-july-15-2026/",
    },
    {
        "emoji": "🧠",
        "titulo": "China aprueba su plan maestro de IA para 2026: inversión récord y control tecnológico total",
        "cuerpo": (
            "El gobierno chino aprobó su plan maestro de inteligencia artificial para 2026, con una "
            "inversión récord que refuerza su apuesta por el control tecnológico nacional. El plan "
            "establece que la IA se integre en el 70% de la economía productiva para 2027 y el 90% "
            "para 2030. Las industrias de IA apuntan a superar los 10 billones de yuanes para 2030. "
            "Se prioriza el desarrollo de modelos de lenguaje propios, chips de IA nacionales y "
            "aplicaciones industriales en manufactura, logística, salud y educación."
        ),
        "fuente_label": "Moncloa — China aprueba su plan maestro de IA para 2026",
        "fuente_url": "https://www.moncloa.com/2026/07/12/china-plan-maestro-ia-2026-3398625/",
    },
    {
        "emoji": "☀️",
        "titulo": "China logra hito en energía solar espacial: transmisión inalámbrica al 20,8% de eficiencia",
        "cuerpo": (
            "La Universidad de Xidian logró un avance significativo en el proyecto de energía solar "
            "espacial 'Zhuri' (Perseguir el Sol): su sistema de prueba terrestre alcanzó una eficiencia "
            "de transmisión inalámbrica del 20,8% a 100 metros, suministrando 1.180 vatios de potencia "
            "y cargando múltiples objetivos en movimiento simultáneamente. El objetivo final es desplegar "
            "una planta solar a 36.000 km en órbita geoestacionaria que transmita energía continuamente "
            "a la Tierra, sin importar las condiciones meteorológicas."
        ),
        "fuente_label": "CGTN — China advances space solar power breakthrough",
        "fuente_url": "https://news.cgtn.com/news/2026-05-19/China-advances-space-solar-power-breakthrough-1NgRg7RgnpC/p.html",
    },
    {
        "emoji": "🛸",
        "titulo": "La nave espacial reutilizable 'Dragón Divino' libera un nuevo objeto misterioso en órbita",
        "cuerpo": (
            "La misteriosa nave espacial reutilizable china conocida como 'Dragón Divino' volvió a captar "
            "la atención mundial al liberar un nuevo objeto en el espacio cuya función permanece sin revelar. "
            "La nave, comparable al X-37B estadounidense, lleva varios meses en órbita realizando "
            "experimentos clasificados. China planifica para 2026 el acercamiento de la sonda Tianwen-2 "
            "a su asteroide objetivo, dos misiones tripuladas Shenzhou y ensayos del cohete reutilizable "
            "Larga Marcha 10, pieza clave del programa lunar tripulado antes de 2030."
        ),
        "fuente_label": "Gizmodo ES — La enigmática nave reutilizable de China libera otro objeto en el espacio",
        "fuente_url": "https://es.gizmodo.com/la-enigmatica-nave-reutilizable-de-china-libera-otro-objeto-en-el-espacio-y-alimenta-las-sospechas-sobre-su-programa-orbital-2000243625",
    },
    {
        "emoji": "🚇",
        "titulo": "China planea el primer tren bala submarino del mundo: unirá Dalian y Yantai bajo el Mar de Bohai",
        "cuerpo": (
            "China avanza en el diseño del túnel submarino del Estrecho de Bohai, un megaproyecto que "
            "conectaría las ciudades de Dalian y Yantai mediante un corredor ferroviario de alta velocidad "
            "bajo el mar. El tren alcanzaría 250 km/h en su trayecto submarino, reduciendo drásticamente "
            "los tiempos de viaje. Este proyecto, si se materializa, sería el primer tren bala submarino "
            "del mundo. China ya opera la red ferroviaria de alta velocidad más extensa del planeta con "
            "47.000 km de vías."
        ),
        "fuente_label": "La Silla Rota — El nuevo tren submarino de alta velocidad en China",
        "fuente_url": "https://lasillarota.com/mundo/2026/5/7/el-nuevo-tren-submarino-de-alta-velocidad-en-china-apunta-transformar-el-transporte-moderno-598155.html",
    },
    {
        "emoji": "🌐",
        "titulo": "La Nueva Ruta de la Seda en 2026: calidad sobre cantidad y la 'Seda Verde'",
        "cuerpo": (
            "La Iniciativa de la Franja y la Ruta (BRI) entra en 2026 en una nueva fase de cooperación "
            "de alta calidad, alejándose de los megaproyectos de infraestructura para enfocarse en "
            "inversiones más sostenibles, tecnológicas y verdes. La 'Seda Verde' y la 'Seda Digital' "
            "son ahora los ejes: energías renovables, telecomunicaciones y conectividad digital. En julio, "
            "el gobierno chino publicó un informe de avance detallando los resultados de más de una "
            "década de cooperación con más de 150 países y organizaciones internacionales."
        ),
        "fuente_label": "UDLAP — Belt and Road Initiative in 2026: From Expansion to Strategic High-Quality Cooperation",
        "fuente_url": "https://observatorioglobal.udlap.mx/the-belt-and-road-initiative-in-2026-from-expansion-to-strategic-high-quality-cooperation/",
    },
    {
        "emoji": "🏥",
        "titulo": "China fusiona IA con Medicina Tradicional: quioscos de diagnóstico inteligente en el metro",
        "cuerpo": (
            "China despliega quioscos de diagnóstico asistido por inteligencia artificial en estaciones "
            "de metro y puntos urbanos estratégicos, integrando tecnología biomédica de vanguardia con "
            "los principios de la Medicina Tradicional China (MTC). Los dispositivos miden presión "
            "arterial, frecuencia cardíaca, saturación de oxígeno y temperatura corporal; mientras la "
            "IA aplica criterios de la MTC —análisis facial, observación de lengua e interpretación "
            "digital del pulso— mediante sensores multicapa. La Comisión Nacional de Salud promueve "
            "esta integración como parte de la estrategia de salud digital nacional."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional China",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
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
    title = "China Al Dia — Semana 11-17 Julio 2026"
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
