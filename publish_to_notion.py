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
        "emoji": "💾",
        "titulo": "Huawei anuncia la 'Ley Tau': el breakthrough que podría revolucionar los semiconductores chinos",
        "cuerpo": (
            "Esta semana, Huawei sacudió al mundo tecnológico al anunciar un avance en diseño de chips "
            "basado en la llamada Ley Tau (o 'Her's Law'), un paradigma alternativo a la Ley de Moore "
            "que permitiría fabricar chips de vanguardia sin depender de litografías avanzadas. El "
            "hashtag correspondiente acumuló más de 40 millones de visualizaciones en Weibo. La empresa "
            "afirma que este modelo podría permitirle producir semiconductores de última generación en "
            "un plazo de cinco años, representando un paso decisivo en la carrera por la autosuficiencia "
            "tecnológica de China."
        ),
        "fuente_label": "NBC News — Huawei touts chip design breakthrough",
        "fuente_url": "https://www.nbcnews.com/world/asia/chinas-huawei-touts-chip-design-breakthrough-bid-defy-us-sanctions-rcna346783",
    },
    {
        "emoji": "🤝",
        "titulo": "Trump y Xi firman 'acuerdos fantásticos': nueva etapa en el comercio global",
        "cuerpo": (
            "El 14 y 15 de mayo, Donald Trump y Xi Jinping celebraron una cumbre bilateral en la que "
            "anunciaron haber alcanzado acuerdos comerciales históricos. Entre los puntos acordados: "
            "la ampliación del comercio agrícola bilateral con reducciones arancelarias, la compra de "
            "aeronaves estadounidenses por parte de China con garantías de suministro de motores, y el "
            "uso del Consejo de Comercio como foro permanente de negociación. Trump calificó los "
            "resultados de 'fantásticos', mientras China subrayó el carácter equilibrado y positivo "
            "de los consensos alcanzados."
        ),
        "fuente_label": "El Informador — China y EU acuerdo sobre aranceles",
        "fuente_url": "https://www.informador.mx/economia/china-y-eu-sorprenden-con-acuerdo-sobre-aranceles-buscan-impulsar-comercio-bilateral-20260516-0072.html",
    },
    {
        "emoji": "🎮",
        "titulo": "EE.UU. autoriza la venta de chips Nvidia H200 a Alibaba, Tencent, ByteDance y JD.com",
        "cuerpo": (
            "En el contexto del deshielo comercial, Washington aprobó la venta de chips Nvidia H200 "
            "—la generación más avanzada de aceleradores de IA— a los principales gigantes tecnológicos "
            "chinos: Alibaba, Tencent, ByteDance y JD.com. La medida fue recibida como un soplo de "
            "aire fresco para el sector tecnológico chino, que llevaba meses acumulando demanda "
            "contenida. Los analistas señalan que este movimiento podría acelerar significativamente "
            "el desarrollo de modelos de IA en China y reforzar la apuesta de Pekín por convertirse "
            "en potencia global de IA."
        ),
        "fuente_label": "CNBC — Trump-Xi summit revives China tech rally, Nvidia H200 sales cleared",
        "fuente_url": "https://www.cnbc.com/2026/05/14/trump-xi-meeting-china-stocks-ai-rally.html",
    },
    {
        "emoji": "🧠",
        "titulo": "El plan de IA de Xi: transformar toda la economía china con inteligencia artificial",
        "cuerpo": (
            "Un análisis publicado esta semana revela los detalles del ambicioso plan de Xi Jinping "
            "para convertir la IA en infraestructura transversal de la economía china. El objetivo: "
            "el 70% de la economía productiva integrada con IA para 2027 y el 90% para 2030. El sector "
            "ya cuenta con más de 6.200 empresas de IA, una industria central valorada en 1,2 billones "
            "de yuanes y 602 millones de usuarios de IA generativa —más de la mitad de todos los "
            "usuarios del mundo—. Las patentes de IA crecieron un 31,2% interanual en el Q1 2026."
        ),
        "fuente_label": "Le Grand Continent — El plan de IA de Xi para transformar China",
        "fuente_url": "https://legrandcontinent.eu/es/2026/05/13/bastidores-del-plan-ia-de-xi-para-transformar-china/",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree Robotics sale a bolsa: $610 millones para el fabricante de robots más viral del mundo",
        "cuerpo": (
            "Unitree Robotics, conocida por sus robots que hacen artes marciales y dan volteretas con "
            "millones de visualizaciones en redes sociales, presentó una solicitud de OPV en el "
            "Shanghai Stock Exchange por 4.200 millones de yuanes (~610 millones de dólares). Sus "
            "inversores incluyen a Tencent, Alibaba, Xiaomi, ByteDance, BYD y Geely. La compañía "
            "despliega robots actualmente en fábricas de BYD y universidades. Su valoración ya supera "
            "los 7.000 millones de dólares, consolidando a China como el epicentro global de la "
            "robótica humanoide."
        ),
        "fuente_label": "Rest of World — Unitree files for $610M Shanghai IPO",
        "fuente_url": "https://restofworld.org/2026/unitree-china-humanoid-robot-shanghai-ipo/",
    },
    {
        "emoji": "☀️",
        "titulo": "China realiza los primeros experimentos de centrales solares espaciales",
        "cuerpo": (
            "El equipo del proyecto Sun Chasing de la Universidad Xidian completó esta semana los "
            "primeros experimentos a gran escala de transmisión de energía solar desde el espacio. "
            "Las pruebas demostraron transmisión inalámbrica de energía a más de 100 metros y "
            "transmisión eficiente por microondas a objetivos en movimiento, con hasta 1.180 W "
            "entregados. El objetivo a largo plazo: construir una planta solar en órbita geoestacionaria "
            "a 36.000 km de la Tierra que supere en eficiencia a los paneles solares terrestres "
            "en un factor de 10 veces."
        ),
        "fuente_label": "PV Magazine — China realiza primeros experimentos solares espaciales",
        "fuente_url": "https://www.pv-magazine-mexico.com/2026/05/20/china-realiza-los-primeros-experimentos-para-centrales-solares-espaciales/",
    },
    {
        "emoji": "🚗",
        "titulo": "La ONU elogia el liderazgo climático de China: 21,5M puntos de recarga y 60% del mercado mundial EV",
        "cuerpo": (
            "El enviado de la ONU para el clima destacó esta semana que los vehículos eléctricos chinos "
            "ahorrarán a la economía global más de 28.000 millones de dólares en importaciones de "
            "petróleo solo en 2026. China cerró marzo con 21,48 millones de puntos de recarga para "
            "vehículos eléctricos (4,9 millones públicos, 16 millones privados) y controla cerca del "
            "60% de las ventas mundiales de coches eléctricos. El plan de convertir 40 millones de "
            "coches eléctricos en una gigantesca red de baterías descentralizada para hogares avanza "
            "con fuerza."
        ),
        "fuente_label": "ONU Noticias — China liderazgo climático transición energética",
        "fuente_url": "https://news.un.org/es/story/2026/05/1541448",
    },
    {
        "emoji": "🗺️",
        "titulo": "El XV Plan Quinquenal (2026-2030): 6G, computación cuántica e interfaces cerebro-computadora",
        "cuerpo": (
            "El XV Plan Quinquenal de China sitúa al país en una carrera tecnológica sin precedentes. "
            "Entre sus objetivos más ambiciosos: el despliegue del 6G, la computación cuántica y las "
            "interfaces cerebro-computadora como tecnologías estratégicas de estado. El presupuesto en "
            "Ciencia y Tecnología asciende a 1,3 billones de yuanes (+7,1%). El plan subraya la "
            "ambición de consolidar a China como potencia financiera global y lograr avances decisivos "
            "en autosuficiencia tecnológica en los próximos cinco años."
        ),
        "fuente_label": "The Conversation ES — China 2026-2030 poder global tecnología",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
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
    title = "China Al Dia — Semana 20-27 Mayo 2026"
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
