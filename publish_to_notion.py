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
        "emoji": "🌐",
        "titulo": "Xi Jinping lanza WAICO: China crea un bloque mundial de IA con 29 naciones",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghai acogió el Congreso Mundial de IA 2026 (WAIC). El presidente "
            "Xi Jinping anunció la fundación de la Organización Mundial de Cooperación en Inteligencia "
            "Artificial (WAICO), un organismo intergubernamental con 29 países miembros —incluyendo Brasil, "
            "Rusia, Indonesia, Pakistán, Cuba y Venezuela— con sede permanente en Shanghai. Se presentaron "
            "más de 300 nuevos productos y modelos de IA. Xi comprometió 5.000 plazas de formación en IA "
            "para países en desarrollo y seis nuevos centros de cooperación internacional en ASEAN, la Liga "
            "Árabe, la Unión Africana, CELAC, la OCS y los BRICS. El sistema de alerta meteorológica "
            "MAZU —primera solución nacional de IA del mundo en respuesta a la iniciativa de la ONU— "
            "será desplegado en 30 países."
        ),
        "fuente_label": "Xinhua (español) — Conferencia Mundial de IA 2026",
        "fuente_url": "http://spanish.xinhuanet.com/20260719/4579c53087754b21a09363efaf9f8478/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Kimi K3: China lanza el mayor modelo de IA open source del mundo (2,8 billones de parámetros)",
        "cuerpo": (
            "El 16 de julio, la startup china Moonshot AI lanzó Kimi K3, el modelo de inteligencia "
            "artificial de código abierto más grande jamás publicado, con 2,8 billones de parámetros y "
            "una ventana de contexto de un millón de tokens con capacidades de visión nativas. Su "
            "rendimiento supera al de DeepSeek y es comparable —o superior en tareas de código— a los "
            "principales modelos de OpenAI. En menos de 24 horas desde el anuncio, las acciones de sus "
            "competidores se desplomaron: Z.ai cayó un 28%, MiniMax un 16% y Alibaba un 4%. Los pesos "
            "completos del modelo se publicarán el 27 de julio."
        ),
        "fuente_label": "VentureBeat — Moonshot AI lanza Kimi K3",
        "fuente_url": "https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems",
    },
    {
        "emoji": "💡",
        "titulo": "GLM-5.2 de Zhipu AI: el primer modelo chino reconocido como igual a los grandes laboratorios de EE.UU.",
        "cuerpo": (
            "El modelo GLM-5.2 de Zhipu AI se ha convertido en el más discutido entre programadores "
            "internacionales en julio de 2026. El asesor de la Casa Blanca Marc Andreessen lo definió "
            "como 'el primer modelo de IA chino que iguala y a menudo supera a los modelos de los "
            "grandes laboratorios americanos'. Este reconocimiento, especialmente notable viniendo del "
            "ecosistema tecnológico de EE.UU., pone de manifiesto el ritmo al que China está cerrando "
            "la brecha en modelos fundacionales de inteligencia artificial."
        ),
        "fuente_label": "Malay Mail — Chinese AI models challenging Silicon Valley",
        "fuente_url": "https://www.malaymail.com/news/tech-gadgets/2026/07/17/the-chinese-ai-models-quietly-challenging-silicon-valley-in-2026/227907",
    },
    {
        "emoji": "📋",
        "titulo": "China regula agentes autónomos de IA e IA antropomórfica",
        "cuerpo": (
            "Julio de 2026 marcó un hito en la gobernanza de la IA en China con la aprobación de tres "
            "nuevas normativas que abordan la ética de la IA, los agentes autónomos y la IA antropomórfica. "
            "El marco regulador chino se posiciona como una referencia alternativa al europeo (Acta de IA "
            "de la UE), apostando por la innovación responsable sin frenar el desarrollo tecnológico. La "
            "Comisión Nacional de Desarrollo y Reforma también publicó un Plan de Acción para la "
            "Cooperación y Desarrollo de la IA con ocho iniciativas prácticas internacionales."
        ),
        "fuente_label": "IAPP — China's new AI rules: Ethics, AI agents and anthropomorphic AI",
        "fuente_url": "https://iapp.org/news/a/china-s-new-ai-rules-ethics-ai-agents-and-anthropomorphic-ai",
    },
    {
        "emoji": "🚗",
        "titulo": "China exporta más de 1 millón de vehículos en un solo mes por primera vez en la historia",
        "cuerpo": (
            "En junio de 2026, China exportó 1.037 millones de vehículos, convirtiéndose en el primer "
            "mes en la historia en superar el umbral del millón de unidades. El aumento interanual fue "
            "del 75,1%. Los vehículos de nueva energía (eléctricos e híbridos enchufables) representaron "
            "el 58,5% de las ventas internas y más de la mitad de las exportaciones. En el primer "
            "semestre, las exportaciones automotrices alcanzaron 5,1 millones de unidades (+65,3%). "
            "La consultora AlixPartners proyecta que China podría exportar 10 millones de vehículos "
            "a lo largo de todo 2026."
        ),
        "fuente_label": "Somos Eléctricos — China rompe todos los records de exportación de vehículos",
        "fuente_url": "https://www.somoselectricos.com/coches-electricos/china-rompe-todos-records-exporta-mas-1-millon-vehiculos-mes/20260710095025058096.html",
    },
    {
        "emoji": "💾",
        "titulo": "Exportaciones chinas de semiconductores: +88,7% gracias al boom de la IA global",
        "cuerpo": (
            "La demanda mundial de inteligencia artificial ha disparado las exportaciones chinas de "
            "circuitos integrados en el primer semestre de 2026: el valor de estos productos aumentó "
            "un 88,7% interanual. Las exportaciones generales de China crecieron un 27% en junio, "
            "alcanzando un récord histórico de 412.400 millones de dólares en un solo mes. El motor "
            "de esta expansión es la manufactura de alta tecnología, que lidera el crecimiento "
            "exportador del país ante la debilidad del consumo interno."
        ),
        "fuente_label": "CGTN — Tech innovation unlocks new growth momentum for China's economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-16/Tech-innovation-unlocks-new-growth-momentum-for-China-s-economy-1OOMQp36DmM/share_amp.html",
    },
    {
        "emoji": "☀️",
        "titulo": "LONGi logra un nuevo récord mundial de eficiencia solar: 27,6%",
        "cuerpo": (
            "El gigante chino de la energía solar LONGi ha alcanzado una eficiencia certificada del "
            "27,6% en su nueva célula ACM (Advanced Crystal Module), junto con un módulo de 672 W de "
            "potencia, batiendo su propio récord mundial. La compañía planea integrar esta tecnología "
            "en su producción en masa a lo largo de varios centros manufactureros. En paralelo, China "
            "proyecta añadir entre 180 y 240 GW de nueva capacidad solar fotovoltaica en 2026, "
            "consolidando su posición como líder mundial en energía solar instalada."
        ),
        "fuente_label": "TaiyangNews — China Solar PV News Snippets - July 2026",
        "fuente_url": "https://taiyangnews.info/markets/china-solar-pv-news-snippets-july-13-2026",
    },
    {
        "emoji": "🛰️",
        "titulo": "China avanza en energía solar espacial: transmisión inalámbrica al 20,8% de eficiencia",
        "cuerpo": (
            "Investigadores de la Universidad de Xidian han logrado un avance clave en el proyecto "
            "'Zhuri' (Sol Cazador): un sistema de transmisión inalámbrica de energía que puede cargar "
            "múltiples objetivos en movimiento de forma simultánea, con una eficiencia del 20,8% a 100 "
            "metros de distancia. El proyecto prevé verificaciones en órbita terrestre baja hacia 2030 "
            "y una estación comercial de gigavatios en órbita geoestacionaria para 2050. China lanzó "
            "además dos nuevas alianzas industriales en SNEC 2026 para acelerar el sector de la "
            "energía solar espacial."
        ),
        "fuente_label": "CGTN — China advances space solar power breakthrough",
        "fuente_url": "https://news.cgtn.com/news/2026-05-19/China-advances-space-solar-power-breakthrough-1NgRg7RgnpC/p.html",
    },
    {
        "emoji": "🏭",
        "titulo": "Más del 30% de las grandes empresas industriales chinas ya usan inteligencia artificial",
        "cuerpo": (
            "Según datos del gobierno chino, más del 30% de las grandes empresas industriales del país "
            "han incorporado la inteligencia artificial a sus procesos productivos. La transformación "
            "tecnológica consolida la manufactura de alta tecnología como el motor principal de la "
            "resiliencia económica del país. El 15.º Plan Quinquenal (2026-2030) fija el objetivo de "
            "que el 90% de la economía productiva integre la IA para 2030. China suma ya más de "
            "600 millones de usuarios de IA generativa, más de la mitad del total mundial."
        ),
        "fuente_label": "Scio.gov.cn — As AI races ahead, China bets on a people-centered digital future",
        "fuente_url": "http://english.scio.gov.cn/m/in-depth/2026-07/06/content_118584284.html",
    },
    {
        "emoji": "💻",
        "titulo": "Conferencia Global de Economía Digital 2026: Pekín como referente del futuro digital",
        "cuerpo": (
            "Del 2 al 5 de julio, Pekín acogió la Conferencia Global de Economía Digital 2026, donde "
            "China se posicionó como principal motor de la economía digital mundial. El evento reunió "
            "a representantes de más de 80 países y abordó la integración de IA, big data y 5G/6G en "
            "los sectores productivos. China lidera la adopción de estas tecnologías a escala industrial "
            "gracias a su infraestructura de 5G (con 5G-A ya en 330 ciudades) y su base de usuarios "
            "de IA más grande del mundo."
        ),
        "fuente_label": "CRI Español — Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cri.cn/2026/07/02/ARTI1782972617748340",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, energia, IA y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 14-21 Julio 2026"
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
