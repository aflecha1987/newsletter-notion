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
        "emoji": "🤖",
        "titulo": "La WAIC 2026 convierte Shanghai en la capital global de la inteligencia artificial",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghai acogió la Conferencia Mundial de Inteligencia Artificial (WAIC 2026) "
            "bajo el lema 'Alianza en la IA para un futuro más brillante'. Con más de 1.100 empresas expositoras, "
            "3.000 productos en exhibición y 300 debuts mundiales, el evento superó todos los récords anteriores. "
            "Los temas centrales fueron los agentes de IA autónomos, la inteligencia encarnada (robótica), la "
            "computación científica y la gobernanza global de la IA. Shanghai se consolida como el epicentro "
            "mundial del desarrollo de la inteligencia artificial."
        ),
        "fuente_label": "People's Daily — 2026 WAIC set for July 17 with over 300 global product debuts",
        "fuente_url": "https://en.people.cn/n3/2026/0708/c90000-20475542.html",
    },
    {
        "emoji": "🧠",
        "titulo": "Moonshot AI presenta Kimi K3: el modelo chino que rivaliza con OpenAI y Anthropic",
        "cuerpo": (
            "El 16 de julio, Moonshot AI presentó Kimi K3, el modelo que sacudió al sector global de IA. "
            "Según la empresa, Kimi K3 supera a Claude Opus 4.8 y GPT-5.5 en benchmarks de código y agentes "
            "generales, acercándose a los modelos de gama alta de EE.UU. El precio de $15 por millón de tokens "
            "de salida es significativamente menor que los $50 de modelos equivalentes estadounidenses. La empresa "
            "anunció además una OPV en Hong Kong en los próximos seis meses. Moonshot levantó 2.000 millones de "
            "dólares en mayo con una valoración de más de 20.000 millones, consolidando el auge de la IA china."
        ),
        "fuente_label": "CNBC — China's Moonshot AI unveils Kimi K3 that rivals OpenAI, Anthropic",
        "fuente_url": "https://www.cnbc.com/2026/07/17/moonshot-ai-kimi-k3-model-openai-anthropic-china.html",
    },
    {
        "emoji": "🏭",
        "titulo": "El 30% de las grandes empresas industriales chinas ya integran la IA en sus procesos",
        "cuerpo": (
            "Según el Ministerio de Industria y Tecnología de la Información, más del 30% de las grandes "
            "empresas industriales del país han adoptado la inteligencia artificial en sus procesos productivos. "
            "La innovación tecnológica se ha convertido en el principal motor del crecimiento económico chino en "
            "2026, con la manufactura de alta tecnología liderando la expansión. En el primer semestre, el valor "
            "de exportaciones de circuitos integrados creció un 88,7% interanual, reflejando la aceleración del "
            "ecosistema tecnológico nacional."
        ),
        "fuente_label": "CGTN — Tech innovation unlocks new growth momentum for China's economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-16/Tech-innovation-unlocks-new-growth-momentum-for-China-s-economy-1OOMQp36DmM/share_amp.html",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China: +4,3% en Q2 2026, con exportaciones IA disparadas un 27%",
        "cuerpo": (
            "La economía china creció un 4,3% interanual en el segundo trimestre de 2026. Aunque por debajo "
            "del objetivo oficial (4,5-5%), los datos sectoriales son sólidos: la producción industrial avanzó "
            "un 5,3% en junio (superando previsiones del 4,6%), y las ventas minoristas crecieron un 1,0% en "
            "junio, por encima del -0,1% esperado. Las exportaciones se dispararon un 27% impulsadas por la "
            "demanda de productos IA, y la primera mitad del año acumuló un crecimiento del 4,7% interanual."
        ),
        "fuente_label": "Mundo Ejecutivo — Economía de China crece 4.3% en segundo trimestre",
        "fuente_url": "https://mundoejecutivocdmx.com/mundo-economico/economia-china-crece-4-3-segundo-trimestre-2026/",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de vehículos eléctricos +68,7% y robots industriales +18,6% en H1 2026",
        "cuerpo": (
            "China escala sin parar en la cadena de valor global. En el primer semestre de 2026: los vehículos "
            "eléctricos crecieron un 68,7% interanual en exportaciones; los robots industriales exportaron por "
            "valor de 6.290 millones de yuanes (+18,6%); los robots quirúrgicos triplicaron sus exportaciones; "
            "y los robots cuadrúpedos chinos controlan ya el 70% del mercado mundial. China ha desarrollado más "
            "de 400 modelos de robots humanoides, representando más de la mitad del total global. La manufactura "
            "de equipos contribuyó cerca del 50% al crecimiento de las exportaciones industriales."
        ),
        "fuente_label": "TechNode — China's electric vehicle exports rise 68.7% in H1 2026",
        "fuente_url": "https://technode.com/2026/07/14/chinas-electric-vehicle-exports-rise-68-7-in-h1-2026/",
    },
    {
        "emoji": "💾",
        "titulo": "Exportaciones de chips chinos casi se duplican en valor: +96% en el primer semestre",
        "cuerpo": (
            "China exportó circuitos integrados por valor de 177.280 millones de dólares en el primer semestre "
            "de 2026, un 96% más que un año antes. El salto refleja tanto la mayor integración de chips chinos "
            "en cadenas de suministro globales como el aumento de los precios medios, impulsado por la demanda "
            "de chips para IA. Las turbinas eólicas y las baterías de litio también registraron exportaciones "
            "récord: +35,6% y +37,6% respectivamente, consolidando el liderazgo chino en la economía verde."
        ),
        "fuente_label": "Revista Cloud — China casi duplica el valor de sus chips exportados",
        "fuente_url": "https://revistacloud.com/china-casi-duplica-el-valor-de-sus-chips-exportados-pero-no-su-volumen",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar supera al carbón en capacidad instalada en China",
        "cuerpo": (
            "En 2026, China ha alcanzado un punto de inflexión sin precedentes: la capacidad instalada de "
            "energía solar supera por primera vez a la del carbón. China concentra ya la mitad de toda la "
            "capacidad eólica y solar del mundo, con más de 1.200 GW solares y 641 GW eólicos instalados. "
            "Ember confirma que China lideró la expansión renovable global, concentrando más de la mitad del "
            "aumento mundial tanto en capacidad como en generación. Un hito que marca un cambio estructural "
            "irreversible en el sistema energético más grande del mundo."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez en 2026",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🛰️",
        "titulo": "Energía solar desde el espacio: China avanza en transmisión inalámbrica de electricidad orbital",
        "cuerpo": (
            "China ha logrado una eficiencia del 20,8% en transmisión inalámbrica de energía a 100 metros, "
            "cargando simultáneamente múltiples objetivos en movimiento. En la feria solar SNEC 2026 de Shanghai, "
            "se constituyeron dos nuevas alianzas industriales para el desarrollo de energía solar espacial, con "
            "13 miembros fundadores incluyendo GCL Technology y Trina Solar. El objetivo a largo plazo: colocar "
            "enormes paneles solares en órbita que transmitan energía de vuelta a la Tierra mediante microondas "
            "o láseres, revolucionando el suministro eléctrico global."
        ),
        "fuente_label": "CGTN — China advances space solar power breakthrough",
        "fuente_url": "https://news.cgtn.com/news/2026-05-19/China-advances-space-solar-power-breakthrough-1NgRg7RgnpC/p.html",
    },
    {
        "emoji": "🛸",
        "titulo": "Nuevo satélite BeiDou en órbita y próxima generación del GPS chino para 2027",
        "cuerpo": (
            "El 10 de julio China lanzó un nuevo satélite del sistema de navegación BeiDou a bordo de un cohete "
            "Larga Marcha-3A desde el centro de Xichang (Sichuan). La Oficina de Navegación por Satélite anunció "
            "además una actualización en órbita del sistema para optimizar el rendimiento de varios satélites. "
            "De cara a 2027, China planea lanzar los primeros satélites de prueba de la próxima generación "
            "BeiDou, que operará en múltiples órbitas y ofrecerá precisión de navegación a nivel de decímetro, "
            "superando las capacidades del GPS americano actual."
        ),
        "fuente_label": "CNSA — China launches new Beidou navigation satellite",
        "fuente_url": "https://www.cnsa.gov.cn/english/n6465652/n6465653/c6802255/content.html",
    },
    {
        "emoji": "🌐",
        "titulo": "China y la Conferencia Global de Economía Digital 2026: construyendo el futuro digital",
        "cuerpo": (
            "Del 2 al 5 de julio, Beijing acogió la Conferencia Global de Economía Digital 2026, que reunió "
            "a líderes tecnológicos, responsables políticos y expertos internacionales para debatir el futuro "
            "de la economía digital. En paralelo, la Conferencia de Información Aeroespacial 2026 (16-17 julio, "
            "Wuxi) mostró los últimos avances en teledetección satelital, sistemas integrados de navegación "
            "BeiDou y tecnologías de computación espacial. China tiene ya más de 400 empresas privadas del "
            "sector espacial, una cifra que el mundo occidental apenas ha comenzado a notar."
        ),
        "fuente_label": "CRI Español — Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cri.cn/2026/07/02/ARTI1782972617748340",
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
    title = "China Al Dia — Semana 14-23 Julio 2026"
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
