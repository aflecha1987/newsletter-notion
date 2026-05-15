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
        "emoji": "🤝",
        "titulo": "Cumbre histórica Trump-Xi en Pekín: acuerdos comerciales y estabilidad estratégica",
        "cuerpo": (
            "Del 13 al 15 de mayo, Pekín acogió la cumbre bilateral más esperada del año entre Donald Trump "
            "y Xi Jinping. Ambos líderes acordaron construir una 'relación estratégica constructiva y estable' "
            "como marco para los próximos años. En el plano comercial, China se comprometió a comprar "
            "200 aviones Boeing, incrementar las compras de productos agrícolas estadounidenses por decenas "
            "de miles de millones de dólares anuales, y se acordó crear un 'Consejo de Comercio' bilateral. "
            "Pekín también manifestó interés en adquirir petróleo de EE.UU. y ambas partes acordaron que el "
            "Estrecho de Ormuz 'debe permanecer abierto'. Los analistas describen el resultado como una "
            "estabilización de las relaciones, con una tregua comercial que se prorroga al menos un año más."
        ),
        "fuente_label": "CNBC — Trump-Xi Beijing Summit: trade, Taiwan, Iran",
        "fuente_url": "https://www.cnbc.com/2026/05/14/trump-xi-beijing-summit-trade-taiwan-ai-iran-rare-earths-tariffs.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree presenta el primer robot mecha tripulado del mundo listo para producción en masa",
        "cuerpo": (
            "El 12 de mayo, Unitree Robotics (Hangzhou) presentó el GD01, el primer mecha tripulado del "
            "mundo disponible para producción en masa. El robot de 2,7 metros de altura y 500 kg puede "
            "transportar a un piloto en su cabina integrada y transitar entre dos modos: bípedo humanoide "
            "y cuadrúpedo. Su precio de salida es de 3,9 millones de yuanes (aproximadamente 573.000 dólares). "
            "Una demo viral muestra al GD01 derribando un muro de ladrillos mientras lleva al piloto. "
            "Unitree ya envió más de 5.500 robots humanoides en 2025 y las empresas chinas acaparan "
            "el 90% de las ventas globales de humanoides."
        ),
        "fuente_label": "Euronews — China's Unitree unveils transformable humanoid mecha robot",
        "fuente_url": "https://www.euronews.com/video/2026/05/13/chinas-unitree-unveils-transformable-humanoid-mecha-robot-with-cockpit",
    },
    {
        "emoji": "🏭",
        "titulo": "China domina el 85% del mercado nacional de robots industriales",
        "cuerpo": (
            "La innovación está impulsando la manufactura china como nunca antes. Los proveedores chinos "
            "de robots industriales han alcanzado una cuota del 85% del mercado doméstico en el sector "
            "metalúrgico y de maquinaria. Las fábricas 'oscuras' —sin trabajadores humanos, operadas "
            "íntegramente por robots coordinados con IA— están pasando de ser experimentos a convertirse "
            "en el modelo de producción del futuro. Robots de logística, inspección, atención sanitaria y "
            "servicios ya operan comercialmente en hospitales, aeropuertos, hoteles y centros comerciales."
        ),
        "fuente_label": "Prensa Latina — Innovación impulsa la manufactura en China",
        "fuente_url": "https://www.prensa-latina.cu/2026/05/15/innovacion-impulsa-la-fuerza-de-la-manufactura-en-china/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4 baja precios un 75% y supera en benchmarks a GPT-5.2 y Gemini 3.0",
        "cuerpo": (
            "El 8 de mayo, DeepSeek anunció un descuento del 75% en su modelo V4-Pro, válido hasta el "
            "31 de mayo. Los modelos V4-Pro (1,6 billones de parámetros) y V4-Flash (284.000 millones) "
            "fueron entrenados exclusivamente con chips Ascend de Huawei, sin Nvidia. Según sus benchmarks, "
            "V4-Pro supera a GPT-5.2 de OpenAI y a Gemini 3.0-Pro de Google en razonamiento. DeepSeek "
            "está siendo valorada en cerca de 45.000 millones de dólares en una ronda liderada por el "
            "principal fondo estatal chino de semiconductores. En mayo, el uso global de modelos chinos "
            "de IA creció un 960%."
        ),
        "fuente_label": "Al Jazeera — DeepSeek unveils latest models",
        "fuente_url": "https://www.aljazeera.com/economy/2026/4/24/chinas-deepseek-unveils-latest-model-a-year-after-upending-global-tech",
    },
    {
        "emoji": "🗺️",
        "titulo": "El plan de Xi para convertir la IA en la columna vertebral de China",
        "cuerpo": (
            "Un análisis del Grand Continent (13 de mayo) revela los bastidores del plan de IA del "
            "presidente Xi Jinping: convertir la inteligencia artificial en infraestructura transversal "
            "para toda la economía, no solo en un sector puntual. La estrategia 'IA Plus' apunta a que "
            "el 70% de la economía productiva integre IA para 2027 y el 90% para 2030. En mayo, los "
            "modelos chinos ya representan más de la mitad de los usuarios globales de IA generativa "
            "(602 millones), y las patentes de IA en China crecieron un 31,2% en el Q1 2026."
        ),
        "fuente_label": "El Grand Continent — Bastidores del plan IA de Xi para transformar China",
        "fuente_url": "https://legrandcontinent.eu/es/2026/05/13/bastidores-del-plan-ia-de-xi-para-transformar-china/",
    },
    {
        "emoji": "📦",
        "titulo": "Exportaciones de China en abril: 359.000 M$ impulsadas por el boom de la IA",
        "cuerpo": (
            "China cerró abril de 2026 con exportaciones totales por 359.000 millones de dólares, un "
            "incremento del 14% interanual. El motor fue la IA: las exportaciones de chips se duplicaron "
            "(+100%), y los equipos de cómputo ligados a IA crecieron un 47%. Los productos relacionados "
            "con IA representaron aproximadamente la mitad del crecimiento exportador total del mes. "
            "En los dos primeros meses del año, las exportaciones totales ya habían crecido un 21,8%, "
            "batiendo todas las previsiones de los analistas."
        ),
        "fuente_label": "Ámbito — China cierra abril con exportaciones de US$359.000 millones",
        "fuente_url": "https://www.ambito.com/tecnologia/china-cierra-abril-exportaciones-us359000-millones-impulsadas-el-auge-la-inteligencia-artificial-n6277559",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar supera al carbón en capacidad instalada en China",
        "cuerpo": (
            "En 2026, China alcanza por primera vez en su historia un cambio estructural definitivo: "
            "la energía solar supera al carbón en capacidad instalada. La eólica y la solar representan "
            "ya el 47,3% de la capacidad eléctrica total del país, superando a la energía térmica. "
            "El año pasado, China instaló tres veces más capacidad eólica que el resto del mundo junto. "
            "Se prevé agregar más de 400 millones de kilovatios de nueva capacidad eléctrica en 2026, "
            "de los que más de 300 millones corresponderán a energías renovables. China también construye "
            "embalses de almacenamiento hidroeléctrico a gran escala para complementar la generación "
            "solar y eólica."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🚗",
        "titulo": "NEV chinos: 1,3 millones de unidades exportadas en los primeros 4 meses de 2026",
        "cuerpo": (
            "En los cuatro primeros meses de 2026, China exportó más de 1,3 millones de unidades de "
            "vehículos de nueva energía (NEV), marcando un crecimiento significativo frente a 2025. "
            "La puntuación media de satisfacción de compradores de NEV en China alcanzó 829 sobre 1.000 "
            "(+23 puntos frente a 2025), con marcas domésticas liderando con 834 puntos. La cuota de "
            "vehículos eléctricos puros (BEV) subió al 66,9% del mercado NEV (frente al 58,5% en 2025). "
            "CNN Business calificó a los fabricantes chinos de eléctricos como listos para 'dominar "
            "el siglo XXI'."
        ),
        "fuente_label": "CleanTechnica — Chinese Automakers Are Going To Take Over The World",
        "fuente_url": "https://cleantechnica.com/2026/05/14/chinese-automakers-are-going-to-take-over-the-world/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, robotica, energia y geopolitica.", bold=False),
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
    title = "China Al Dia — Semana 8-15 Mayo 2026"
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
