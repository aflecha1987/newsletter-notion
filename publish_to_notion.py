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
        "emoji": "🌍",
        "titulo": "China aplica arancel cero a 53 países africanos: el mayor gesto de apertura comercial del siglo",
        "cuerpo": (
            "Desde el 1 de mayo de 2026, China aplica arancel cero al 100% de los productos procedentes "
            "de los 53 países africanos con los que mantiene relaciones diplomáticas, convirtiéndose en "
            "la primera gran economía en ofrecer acceso pleno y unilateral a todo un continente. El primer "
            "cargamento bajo esta medida fueron 24 toneladas de manzanas sudafricanas que pasaron aduana "
            "en Shenzhen en tiempo récord. En 2025, el comercio bilateral China-África alcanzó los 348.080 "
            "millones de dólares, y en el primer trimestre de 2026 ya creció un 26,8% interanual hasta "
            "92.160 millones. La medida estará vigente hasta 2028 y consolida a China como el mayor socio "
            "comercial del continente africano, muy por delante de Europa y Estados Unidos."
        ),
        "fuente_label": "Xinhua Español — China autoriza primer lote bajo política de arancel cero",
        "fuente_url": "http://spanish.xinhuanet.com/20260501/f20605fdb3a54b20a4a203426b5257d5/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "DeepSeek V4: China lanza el modelo de IA más potente sin necesitar chips Nvidia",
        "cuerpo": (
            "El 24 de abril, DeepSeek presentó V4, su nuevo modelo de inteligencia artificial, en dos "
            "versiones: V4-Pro (1,6 billones de parámetros, 49.000 millones activos) y V4-Flash (284.000 "
            "millones de parámetros, 13.000 millones activos). Ambos soportan una ventana de contexto de "
            "1 millón de tokens y están optimizados para chips Huawei Ascend, reduciendo la dependencia "
            "de hardware estadounidense. En benchmarks de conocimiento mundial, V4-Pro supera a todos los "
            "modelos de código abierto y solo es ligeramente superado por Gemini-3.1-Pro. El coste de uso "
            "es de apenas 1,74 dólares por millón de tokens de entrada —una fracción de sus competidores—. "
            "La semana de su lanzamiento, el Big Fund del gobierno chino abrió una ronda de inversión que "
            "podría doblar la valoración de DeepSeek hasta los 45.000 millones de dólares."
        ),
        "fuente_label": "Euronews — DeepSeek lanza V4, todo lo que debes saber",
        "fuente_url": "https://www.euronews.com/next/2026/04/24/chinas-deepseek-releases-new-ai-model-v4-heres-everything-to-know-as-the-ai-race-speeds-up",
    },
    {
        "emoji": "🧠",
        "titulo": "Kimi K2.6 de Moonshot AI: el modelo open source chino que supera a GPT-5.5 en programación",
        "cuerpo": (
            "Moonshot AI lanzó Kimi K2.6, un modelo de código abierto con 1 billón de parámetros, "
            "ventana de contexto de 256.000 tokens y capacidad multimodal nativa. Su característica "
            "más llamativa: puede coordinar hasta 300 subagentes en secuencias de 4.000 pasos "
            "encadenados, convirtiéndolo en una herramienta excepcional para tareas de agentes "
            "autónomos complejos. En benchmarks independientes de codificación y razonamiento, K2.6 "
            "supera a GPT-5.5 y Claude Opus. La licencia Modified MIT permite a desarrolladores de "
            "todo el mundo usar, modificar y distribuir el modelo libremente. Esta es la segunda gran "
            "sorpresa china del mes en IA, y refuerza la tendencia de que el software de IA chino de "
            "código abierto está marcando el ritmo global."
        ),
        "fuente_label": "Kimi K2 — MoonshotAI GitHub y análisis K2.6",
        "fuente_url": "https://github.com/MoonshotAI/Kimi-K2",
    },
    {
        "emoji": "⚡",
        "titulo": "DeepSeek impulsa la revolución energética: más de 200 empresas estatales chinas lo integran",
        "cuerpo": (
            "La adopción de DeepSeek en el sector energético chino está siendo masiva. Longyuan Power, "
            "State Grid, China Southern Power Grid, CHN Energy, State Power Investment Corporation y "
            "China Huadian ya han integrado sus plataformas internas con DeepSeek. En total, más de "
            "200 grandes empresas líderes del país han incorporado el modelo en sus operaciones. La "
            "empresa Longyuan Power lo usa para optimización de parques eólicos y predicción de "
            "producción solar. Esta integración acelerada refleja la ventaja estratégica de DeepSeek: "
            "al ser un modelo de código abierto eficiente, puede desplegarse en infraestructuras "
            "privadas sin depender de servicios cloud externos ni hardware restringido por sanciones."
        ),
        "fuente_label": "PV Tech — China's state energy actors embrace DeepSeek AI",
        "fuente_url": "https://www.pv-tech.org/chinas-state-energy-actors-embrace-deepseek-ai-to-accelerate-digital-transformation/",
    },
    {
        "emoji": "🚫",
        "titulo": "China bloquea la compra de Manus por Meta: Pekín protege su sector IA por primera vez",
        "cuerpo": (
            "El 27 de abril, la Comisión Nacional de Desarrollo y Reforma (NDRC) de China bloqueó la "
            "adquisición de Manus —la startup de agentes IA con raíces chinas— por parte de Meta. Es "
            "la primera vez que China emite una decisión pública bloqueando inversión extranjera en su "
            "sector de inteligencia artificial, marcando un hito en la política de seguridad tecnológica "
            "del país. Manus, lanzada a principios de 2026, se había convertido en viral globalmente "
            "por su capacidad de ejecutar tareas autónomas complejas en internet. La decisión señala "
            "que China considera sus startups de IA como activos estratégicos nacionales que no deben "
            "pasar a manos extranjeras."
        ),
        "fuente_label": "USCC China Bulletin — May 5, 2026",
        "fuente_url": "https://www.uscc.gov/trade-bulletins/china-bulletin-may-5-2026",
    },
    {
        "emoji": "🏭",
        "titulo": "Tech Week Shanghai 2026: China se convierte en la capital mundial del dato",
        "cuerpo": (
            "Del 6 al 8 de mayo, el Shanghai New International Expo Centre acogió la primera edición "
            "de Tech Week Shanghai – Global Data Week, un evento que apunta a convertirse en la "
            "referencia mundial del sector de datos, inteligencia artificial e infraestructura digital. "
            "La ciudad de Shanghái ya es el mayor hub de datos de Asia-Pacífico y el evento reunió a "
            "líderes tecnológicos de más de 60 países. En paralelo, el presidente Xi Jinping celebró "
            "un seminario en Shanghái en el que subrayó la necesidad de fortalecer la investigación "
            "básica como motor de innovación, reafirmando el papel de la ciudad como epicentro de la "
            "estrategia científica y tecnológica china."
        ),
        "fuente_label": "ChinaTech Bridge — Tech Week Shanghai 2026",
        "fuente_url": "https://chinatechbridge.com/shows/21/38.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Tiangong amplía su misión: China planea dominar el espacio cuando cierre la ISS",
        "cuerpo": (
            "Con el cierre de la Estación Espacial Internacional (ISS) previsto por la NASA para 2030, "
            "China acelera la expansión de Tiangong, su propia estación en órbita terrestre baja. Los "
            "planes incluyen aumentar la capacidad de astronautas a bordo, incorporar nuevos módulos "
            "de laboratorio y abrir la estación a astronautas de países asociados, especialmente de "
            "Asia, África y América Latina. En 2026, el programa espacial chino también tiene en "
            "marcha la misión Chang'e-7 (polo sur lunar, lanzamiento en agosto), el acercamiento de "
            "Tianwen-2 a su asteroide objetivo y dos misiones Shenzhou tripuladas. China será el único "
            "país con estación espacial operativa a partir de 2030."
        ),
        "fuente_label": "PanamaPost — China hace planes para dominar el espacio",
        "fuente_url": "https://panampost.com/oriana-rivas/2026/05/01/china-hace-planes-para-dominar-el-espacio/",
    },
    {
        "emoji": "📈",
        "titulo": "Análisis económico y diplomacia marcan la semana en China: indicadores por encima de lo previsto",
        "cuerpo": (
            "El Buró Político del Comité Central del Partido Comunista de China analizó esta semana la "
            "situación económica del país, concluyendo que la economía inició 2026 con resultados "
            "positivos y con indicadores clave por encima de lo previsto. Las prioridades definidas "
            "son: construir cadenas industriales seguras y resilientes, aplicar una política fiscal "
            "más proactiva, una política monetaria acomodaticia con enfoque preciso y ampliar la "
            "demanda interna. En el plano diplomático, el canciller Wang Yi habló con el Secretario "
            "de Estado Marco Rubio, subrayando que la cuestión de Taiwán es el mayor riesgo en las "
            "relaciones bilaterales y que la diplomacia de jefes de Estado es el 'ancla' de la "
            "relación China-EE.UU."
        ),
        "fuente_label": "Prensa Latina — Análisis económico y política exterior marcan semana en China",
        "fuente_url": "https://www.prensa-latina.cu/2026/05/02/analisis-economico-y-politica-exterior-marcan-semana-en-china/",
    },
    {
        "emoji": "🍊",
        "titulo": "China abre su mercado a los cítricos africanos con arancel cero y nuevas medidas sanitarias",
        "cuerpo": (
            "Como parte de la aplicación del arancel cero a África, China ha acelerado los procedimientos "
            "sanitarios y fitosanitarios para facilitar la importación de cítricos de países como "
            "Sudáfrica, Marruecos, Egipto y Kenia. El portal fruticola.com reportó esta semana avances "
            "concretos en protocolos de importación de naranja, limón y pomelo. El sector agrícola "
            "africano ve en esta apertura una oportunidad histórica: China consume más de 30 millones "
            "de toneladas de cítricos al año y, con el arancel cero, los productores africanos pasan "
            "de competir en condiciones desventajosas a tener acceso preferencial al mayor mercado "
            "de consumo del mundo. Es un cambio de paradigma para la agricultura exportadora africana."
        ),
        "fuente_label": "Portal Frutícola — China impulsa exportaciones de cítricos africanos",
        "fuente_url": "https://www.portalfruticola.com/noticias/2026/05/06/china-citricos-africa/",
    },
    {
        "emoji": "💰",
        "titulo": "China invirtió más de 8.600 millones de dólares en América Latina en 2025",
        "cuerpo": (
            "La inversión extranjera directa china hacia América Latina y el Caribe alcanzó más de "
            "8.600 millones de dólares en 2025, generando más de 36.000 empleos en la región, según "
            "datos publicados esta semana por La Jornada. Aunque representa una caída del 12% respecto "
            "a 2024, la cifra consolida a China como uno de los principales inversores en la región. "
            "Los sectores preferidos siguen siendo la minería, infraestructura, energías renovables "
            "y telecomunicaciones. Brasil, Chile, Perú y Argentina concentran la mayor parte. "
            "La tendencia para 2026 apunta a más inversión en energía limpia y manufactura de alta "
            "tecnología, especialmente baterías para vehículos eléctricos y componentes solares."
        ),
        "fuente_label": "La Jornada — La inversión de China en América Latina hasta 2025",
        "fuente_url": "https://www.jornada.com.mx/2026/05/06/economia/016a1eco?partner=rss",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana (1-7 mayo 2026): comercio, inteligencia artificial, espacio y economia.", bold=False),
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
    title = "China Al Dia — Semana 1-7 Mayo 2026"
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
