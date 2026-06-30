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
        "titulo": "Summer Davos 2026 en Dalian: Li Qiang presenta la \"Oportunidad China 2.0\" ante el mundo",
        "cuerpo": (
            "Del 23 al 25 de junio, Dalian acogió la XVII edición del Foro Económico Mundial de los Nuevos "
            "Campeones —el llamado 'Summer Davos'—, bajo el lema 'Innovar a escala'. Más de 1.700 participantes "
            "de más de 90 países debatieron cómo la IA está rediseñando el crecimiento global. El Premier Li "
            "Qiang acuñó el concepto de 'Oportunidad China 2.0': mientras la primera oleada abrió China como "
            "fábrica global, la nueva oleada ofrece acceso a tecnologías avanzadas —EVs, paneles solares, chips, "
            "baterías, IA y robótica— asequibles para todos los mercados. El foro cerró con un llamamiento a "
            "convertir la innovación en empleos, crecimiento y competitividad a escala global."
        ),
        "fuente_label": "World Economic Forum — Special address by Li Qiang at Summer Davos 2026",
        "fuente_url": "https://www.weforum.org/stories/2026/06/summer-davos-2026-special-address-by-li-qiang-premier-of-the-peoples-republic-of-china/",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones chinas marcan récord histórico: USD 376.780 millones en mayo (+19,4%)",
        "cuerpo": (
            "Las exportaciones chinas de mayo de 2026 alcanzaron USD 376.780 millones, el nivel más alto jamás "
            "registrado, con un crecimiento del 19,4% interanual (frente al 14,1% de abril). Los motores "
            "principales fueron la demanda de semiconductores y hardware para IA, y el efecto de anticipación "
            "de compras ante la escalada de precios de la energía por el conflicto en Oriente Medio. Las "
            "exportaciones hacia EE.UU. crecieron un 35,4% interanual en mayo. Los analistas señalan "
            "una aceleración general en junio, con la manufactura repuntando y el consumo interno recuperándose. "
            "BBVA Research mantiene su previsión de PIB 2026 en 4,5%, en línea con el objetivo oficial del gobierno."
        ),
        "fuente_label": "CNBC — China's economy picks up in June on rebounding U.S. exports",
        "fuente_url": "https://www.cnbc.com/2026/06/29/china-economy-june-trade-exports-manufacturing-tariffs-iran-war-consumption-ai-technology-.html",
    },
    {
        "emoji": "🏗️",
        "titulo": "He Lifeng en Sichuan: acelerar modernización de las industrias clave (29 junio)",
        "cuerpo": (
            "El viceprimer ministro He Lifeng visitó el 29 de junio las ciudades de Chengdu, Deyang y Mianyang "
            "(Sichuan) para inspeccionar fabricantes de equipos de alta tecnología. He instó a lograr avances en "
            "tecnologías fundamentales, acelerar la modernización digital e inteligente, y fomentar nuevas fuerzas "
            "productivas de calidad. Abogó por estrechar la colaboración entre universidades, institutos de "
            "investigación, empresas privadas y estatales. Los sectores estratégicos prioritarios del XV Plan "
            "Quinquenal incluyen circuitos integrados, máquinas herramienta de alta gama, software básico, "
            "materiales avanzados y biomanufactura."
        ),
        "fuente_label": "La Jornada — China insta a acelerar la modernización de sus industrias claves",
        "fuente_url": "https://www.jornada.com.mx/2026/06/29/economia/021n1eco",
    },
    {
        "emoji": "🤖",
        "titulo": "China lanza plan trienal para integrar IA en telecomunicaciones (2026-2028)",
        "cuerpo": (
            "El 10 de junio, el Ministerio de Industria y Tecnología de la Información publicó un plan trienal "
            "(2026-2028) para acelerar la integración de la inteligencia artificial en el sector de las "
            "telecomunicaciones. Los objetivos incluyen redes más autónomas, mayor cobertura de computación "
            "de baja latencia y expansión masiva de aplicaciones de IA. El plan forma parte de la estrategia "
            "nacional 'IA Plus', que busca que el 70% de la economía productiva integre IA para 2027 y el "
            "90% para 2030. Las industrias de IA del país apuntan a superar los 10 billones de yuanes "
            "en valor para 2030."
        ),
        "fuente_label": "Gobierno de China — China issues three-year plan to boost AI integration",
        "fuente_url": "https://english.www.gov.cn/news/202606/10/content_WS6a296017c6d00ca5f9a0b876.html",
    },
    {
        "emoji": "💡",
        "titulo": "Modelos chinos de IA compiten globalmente: Kimi K2.5 cuesta 4 veces menos que GPT-5",
        "cuerpo": (
            "Los laboratorios de IA chinos continúan estrechando la brecha de rendimiento con sus rivales "
            "estadounidenses, al tiempo que ofrecen precios radicalmente más competitivos. Kimi K2.5, de "
            "Moonshot AI, se posiciona con un coste cuatro veces inferior a GPT-5 con prestaciones comparables. "
            "Tras el impacto global de DeepSeek R1 —premiado como una de las 'Mejores Invenciones de 2025' "
            "por Time Magazine—, China acumula nuevos lanzamientos de modelos frontera. El concepto de "
            "'Oportunidad China 2.0' en IA significa mayor acceso global a modelos avanzados a precios "
            "asequibles, democratizando la inteligencia artificial."
        ),
        "fuente_label": "WEF — Why China's AI breakthroughs should come as no surprise",
        "fuente_url": "https://www.weforum.org/stories/2025/06/china-ai-breakthroughs-no-surprise/",
    },
    {
        "emoji": "🚀",
        "titulo": "Tianwen-2 alcanza el asteroide Kamoʻoalewa: primer retorno de muestra asteroidal de China",
        "cuerpo": (
            "La sonda Tianwen-2, lanzada en mayo de 2025, alcanzó en junio de 2026 el punto de encuentro con "
            "el asteroide 469219 Kamoʻoalewa, un cuerpo próximo a la Tierra que podría ser un fragmento "
            "desprendido de la Luna. La misión es la primera en la historia de China diseñada para retornar "
            "muestras de un asteroide a la Tierra, previsto para 2027. Tras concluir esta fase, Tianwen-2 "
            "pondrá rumbo al cometa 311P/PanSTARRS, al que estudiará desde la órbita a partir de 2035. "
            "China avanza así en la exploración del Sistema Solar con una misión de doble objetivo histórico, "
            "complementando el programa lunar Chang'e."
        ),
        "fuente_label": "Wikipedia — Programa espacial chino (Tianwen-2)",
        "fuente_url": "https://en.wikipedia.org/wiki/Chinese_space_program",
    },
    {
        "emoji": "☀️",
        "titulo": "Energía solar espacial: China logra transmitir potencia kilowatt sin cables desde el espacio",
        "cuerpo": (
            "Un equipo del proyecto Sun Chasing de la Universidad Xidian ha completado los primeros experimentos "
            "de transmisión inalámbrica de energía solar espacial a escala kilowatt. El sistema alcanzó una "
            "eficiencia de transmisión de corriente continua a corriente continua del 20,8% a 100 metros, "
            "entregando 1.180 vatios de potencia. En paralelo, otro experimento alimentó con éxito un dron "
            "a 30 km/h con 143 vatios estables desde 30 metros. En SNEC 2026, China lanzó dos alianzas "
            "industriales para avanzar en energía solar espacial y tecnologías de perovskita. La hoja de "
            "ruta incluye pruebas en órbita baja y una demostración a escala de megavatio en torno a 2030."
        ),
        "fuente_label": "PV Magazine — China conducts first experiments for space-based solar power plants",
        "fuente_url": "https://www.pv-magazine.com/2026/05/20/china-conducts-first-experiments-for-space-based-solar-power-plants/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD exportaciones récord: 160.644 unidades en mayo 2026 (+80% interanual)",
        "cuerpo": (
            "BYD alcanzó en mayo de 2026 un nuevo récord de ventas en el exterior: 160.644 unidades exportadas, "
            "un crecimiento del 80% interanual. Las exportaciones supusieron el 42% de las ventas totales del "
            "fabricante durante el mes. El 9 de junio, BYD proyectó que el 80% de las ventas de automóviles "
            "en China serán eléctricas en el corto plazo, acelerando la transición del mercado interno. "
            "La compañía consolida su posición como el mayor fabricante de vehículos de nueva energía del "
            "mundo, con fuerte presencia en Asia-Pacífico, Europa y América Latina. El sector chino de "
            "vehículos eléctricos se convierte en uno de los principales motores de las exportaciones totales."
        ),
        "fuente_label": "CNBC — BYD predicts 80% of China car sales will soon be electric",
        "fuente_url": "https://www.cnbc.com/2026/06/09/electric-vehicle-giant-byd-predicts-80percent-of-china-car-sales-will-soon-be-electric.html",
    },
]


def build_blocks():
    today = "30 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio y energia.", bold=False),
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
    title = "China Al Dia — Semana 23-30 Junio 2026"
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
