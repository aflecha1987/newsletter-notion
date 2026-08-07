#!/usr/bin/env python3
"""
Publica la newsletter de China Al Dia en Notion.
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

def p_links(sources):
    """sources: list of (label, url) tuples"""
    rich_text = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(sources):
        rich_text.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
        if i < len(sources) - 1:
            rich_text.append({"type": "text", "text": {"content": " · "}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def callout(text, emoji="📌"):
    return {"object": "block", "type": "callout",
            "callout": {"icon": {"type": "emoji", "emoji": emoji},
                        "rich_text": [{"type": "text", "text": {"content": text}}]}}

def quote(text):
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def section_header(text):
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": text},
                                         "annotations": {"color": "blue_background"}}]}}


NOTICIAS = [
    # ─── PORTADA ──────────────────────────────────────────────────────────────
    {
        "seccion": "🗞️  PORTADA DEL DÍA",
        "emoji": "📈",
        "titulo": "Exportaciones de China superan previsiones en julio: +23,9 % impulsadas por el auge global de la IA",
        "cuerpo": (
            "China publicó hoy sus datos de comercio exterior de julio: las exportaciones crecieron un "
            "23,9 % interanual, alcanzando los 397.850 millones de dólares y superando la previsión del "
            "mercado del 22,88 %. Las importaciones subieron un 27,5 % hasta 285.350 millones. El superávit "
            "comercial se situó en 112.500 millones de dólares. El motor fue la demanda global de productos "
            "de alta tecnología vinculados a la infraestructura de IA —chips, servidores, baterías y "
            "componentes de energía limpia—. El dato de julio modera respecto al récord del +27 % de junio, "
            "el ritmo más rápido desde octubre de 2021."
        ),
        "fuentes": [
            ("CNBC", "https://www.cnbc.com/2026/08/07/china-july-trade-exports-imports-surplus-imbalance-tariffs-.html"),
            ("Reuters / Investing.com", "https://ca.investing.com/news/economy-news/chinas-july-exports-beat-expectations-on-robust-hightech-demand-4785325"),
            ("SCMP", "https://www.scmp.com/economy/economic-indicators/article/3363236/chinas-exports-hold-firm-july-despite-trade-and-geopolitical-headwinds"),
        ],
    },
    # ─── TECNOLOGÍA E IA ──────────────────────────────────────────────────────
    {
        "seccion": "🤖  TECNOLOGÍA E INTELIGENCIA ARTIFICIAL",
        "emoji": "🌐",
        "titulo": "China crea la WAICO: nueva organización internacional de IA con 29 países fundadores",
        "cuerpo": (
            "Durante la Conferencia Mundial de IA (WAIC 2026) en Shanghái, el presidente Xi Jinping "
            "anunció la World Artificial Intelligence Cooperation Organization (WAICO), la primera "
            "organización internacional de gobernanza en IA, con sede en Shanghái. Los 29 países fundadores "
            "incluyen Brasil, Rusia, Sudáfrica, Indonesia y Pakistán. La conferencia reunió a más de "
            "1.100 empresas y mostró más de 3.000 productos —300 por primera vez en el mundo— y consolida "
            "a China como centro de la gobernanza global de la IA y alternativa a los marcos occidentales."
        ),
        "fuentes": [
            ("RadioNodo AI", "https://radionodo.ai/nace-waico-china-crea-una-nueva-organizacion-internacional-de-inteligencia-artificial/"),
            ("La Ecuación Digital", "https://www.laecuaciondigital.com/tecnologias/inteligencia-artificial/china-gobernanza-global-ia-waic/"),
            ("Mundo Global", "https://mundoglobal.org/13-claves-para-entender-la-waic-2026-la-conferencia-con-la-que-china-quiere-mostrar-el-futuro-de-la-inteligencia-artificial/"),
        ],
    },
    {
        "seccion": None,
        "emoji": "🔬",
        "titulo": "Xi Jinping subraya la innovación científica como motor de la modernización china",
        "cuerpo": (
            "El presidente Xi Jinping reiteró ayer que la innovación científico-tecnológica es la clave "
            "para la modernización del país, en el marco del Plan Quinquenal 2026-2030 que busca convertir "
            "a China en una potencia científica global para 2035. Xi llamó a integrar mejor la investigación "
            "universitaria con la industria y acelerar la formación de nuevas generaciones de científicos de "
            "élite. El período 2026-2030 es descrito como 'fase crucial' para alcanzar la autosuficiencia "
            "en semiconductores, aviación, biotecnología y computación cuántica."
        ),
        "fuentes": [
            ("CGTN", "https://news.cgtn.com/news/2026-08-06/Xi-underscores-sci-tech-innovation-to-advance-China-s-modernization-1PmbnQr21fW/p.html"),
            ("Xinhua ES", "http://spanish.xinhuanet.com/20260708/351fa1e6395b401dace4f81c1f581872/c.html"),
        ],
    },
    {
        "seccion": None,
        "emoji": "🦾",
        "titulo": "Producción de robots humanoides superará 100.000 unidades en 2026",
        "cuerpo": (
            "Según el Ministerio de Industria y Tecnología, la producción de robots humanoides en China "
            "superará las 100.000 unidades en 2026, el mayor volumen mundial. El gobierno fijó el objetivo "
            "de 10.000 robots humanoides en uso comercial antes de que termine el año —en manufactura, "
            "logística, sanidad y emergencias—. Empresas como AGIBOT (A3 Ultra), Unitree Robotics, Engine AI "
            "y Galbot lideran el sector. Más de la mitad de los 400+ modelos de robots humanoides existentes "
            "en el mundo son de origen chino."
        ),
        "fuentes": [
            ("CGTN", "https://news.cgtn.com/news/2026-07-08/China-s-output-of-humanoid-robots-set-to-exceed-100-000-in-2026-1OBFKOQ9WUg/p.html"),
            ("Caixin Global", "https://www.caixinglobal.com/2026-06-10/china-targets-10000-humanoid-robots-in-commercial-use-by-end-2026-102452656.html"),
            ("Interesting Engineering", "https://interestingengineering.com/ai-robotics/china-agibot-humanoid-robot"),
        ],
    },
    # ─── ESPACIO Y CIENCIA ────────────────────────────────────────────────────
    {
        "seccion": "🛰️  ESPACIO Y CIENCIA",
        "emoji": "🌕",
        "titulo": "Chang'e-6 revoluciona la cartografía lunar: primer mapa geológico de la cara oculta",
        "cuerpo": (
            "China presentó la versión más completa del mapa geológico global de la Luna, actualizado "
            "con las muestras inéditas de la misión Chang'e-6 —la primera en traer material de la cara "
            "oculta del satélite—. El nuevo mapa ofrece resolución sin precedentes en zonas jamás exploradas "
            "in situ y corrige errores en modelos anteriores basados solo en teledetección. El logro "
            "posiciona a China como la principal potencia en exploración lunar activa de cara a las "
            "misiones tripuladas previstas antes de 2030."
        ),
        "fuentes": [
            ("Canal 26", "https://www.canal26.com/ciencia-y-espacio/2026/08/06/la-mision-change-6-permitio-obtener-las-primeras-muestras-de-la-cara-oculta-de-la-luna-y-mejorar-su-mapa-geologico/"),
            ("Astroaventura", "https://astroaventura.net/aeroespacial/objetivo-2030-los-grandes-avances-de-china-para-llevar-astronautas-a-caminar-sobre-la-superficie-de-la-luna/"),
        ],
    },
    {
        "seccion": None,
        "emoji": "⚛️",
        "titulo": "Zuchongzhi 3.0 y satélites QKD: China a la vanguardia de la computación cuántica",
        "cuerpo": (
            "El ordenador cuántico chino Zuchongzhi 3.0 demostró en 2026 una ventaja computacional que "
            "deja a los superordenadores convencionales más rápidos del mundo a años de distancia. "
            "Simultáneamente, China despliega una constelación de 4 satélites QKD en órbita baja para "
            "comunicaciones 'inhackeables' basadas en las leyes de la física cuántica. El programa cuántico "
            "avanza en paralelo al de semiconductores como estrategia dual para garantizar la soberanía "
            "tecnológica independientemente del acceso a chips extranjeros."
        ),
        "fuentes": [
            ("Tech Biz Hub", "https://techbizhub.com/news/china-tech-advancement-2026-global-innovation"),
            ("Medium", "https://medium.com/@harshduhan/the-great-eclipse-how-chinas-2026-breakthroughs-are-casting-a-shadow-over-the-west-4d1e326476a7"),
        ],
    },
    # ─── ECONOMÍA ─────────────────────────────────────────────────────────────
    {
        "seccion": "💼  ECONOMÍA Y MERCADOS",
        "emoji": "📊",
        "titulo": "Bolsa de Shanghái cierra al alza: índice compuesto en 3.911 puntos (+0,27 %)",
        "cuerpo": (
            "El Índice Compuesto de Shanghái cerró hoy en 3.911 puntos, ganando un 0,27 % respecto a "
            "la sesión anterior, impulsado por los sólidos datos comerciales de julio. El mercado "
            "bursátil chino mantiene tendencia alcista en 2026 gracias a la narrativa de la IA, el "
            "liderazgo en robótica y las exportaciones récord. El sector tecnológico y de semiconductores "
            "ha liderado las ganancias este año."
        ),
        "fuentes": [
            ("Trading Economics", "https://tradingeconomics.com/china/stock-market"),
        ],
    },
    {
        "seccion": None,
        "emoji": "🎬",
        "titulo": "China-Brasil: diplomacia cultural en el V Festival de Cine del Año Cultural Bilateral",
        "cuerpo": (
            "En el marco del Año Cultural China-Brasil 2026, se celebró hoy en Río de Janeiro la "
            "ceremonia de clausura del V Festival de Cine Chino-Brasileño, uno de los intercambios "
            "culturales sur-sur más activos del mundo. La iniciativa forma parte de la estrategia "
            "de diplomacia cultural que China despliega en Latinoamérica, África y Asia, con más de "
            "40 acuerdos de cooperación tecnológica y cultural firmados en 2026."
        ),
        "fuentes": [
            ("China Boss News", "https://shannonbrandao.substack.com/sitemap/2026"),
        ],
    },
    # ─── ENERGÍA ──────────────────────────────────────────────────────────────
    {
        "seccion": "⚡  ENERGÍA Y MEDIO AMBIENTE",
        "emoji": "☀️",
        "titulo": "Plantas CSP: 24 en operación, 26 en construcción, costes reducidos a la mitad en una década",
        "cuerpo": (
            "China opera ya 24 plantas de energía solar de concentración (CSP) con otras 26 en "
            "construcción, sumando 3,2 GW de capacidad total. Los costes de construcción se han reducido "
            "a la mitad en una década, hasta los 15.000 yuanes (~2.200 dólares) por kilovatio. La CSP "
            "complementa la solar fotovoltaica y la eólica garantizando suministro firme en horas "
            "nocturnas y días nublados, resolviendo el principal talón de Aquiles de las energías "
            "intermitentes y abriendo camino a la exportación de esta tecnología."
        ),
        "fuentes": [
            ("Tricontinental", "https://thetricontinental.org/es/asia/noticias-de-china-no-32/"),
            ("The Conversation", "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464"),
        ],
    },
]


def build_blocks():
    today = date.today().strftime("%-d de %B de %Y")
    blocks = [
        callout(f"Newsletter diaria · China Al Día · {today}", "🇨🇳"),
        p("Recopilación de las noticias más relevantes de China hoy: tecnología, economía, espacio y sociedad."),
        divider(),
    ]

    current_section = None
    for n in NOTICIAS:
        if n.get("seccion") and n["seccion"] != current_section:
            current_section = n["seccion"]
            blocks.append(section_header(current_section))

        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        blocks.append(p_links(n["fuentes"]))
        blocks.append(divider())

    blocks.append(p("China al Día · Newsletter diaria en español · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    today = date.today()
    title = f"China Al Día — {today.strftime('%-d de %B de %Y')}"
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

    print(f"Creando página en Notion: '{title}'")
    print(f"Noticias incluidas: {len(NOTICIAS)}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "").replace("-", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id}")
    print(f"\n¡Listo!")
    print(f"URL: {page_url}")
    return page_url


if __name__ == "__main__":
    create_notion_page()
