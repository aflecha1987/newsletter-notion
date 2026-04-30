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
        "titulo": "DeepSeek V4: la IA china que corre en chips propios y destroza precios globales",
        "cuerpo": (
            "El 24 de abril, DeepSeek lanzó su esperado modelo V4 en dos versiones: DeepSeek-V4-Pro "
            "—con rendimiento comparable a los mejores modelos cerrados del mundo— y DeepSeek-V4-Flash, "
            "una variante más pequeña y económica. Lo que hace histórico este lanzamiento es que es la "
            "primera vez que un modelo de IA de frontera chino se construye para correr nativamente en "
            "los chips Huawei Ascend 950, sin depender de hardware Nvidia. El precio del V4-Pro es de "
            "apenas $3,48 por millón de tokens, y el V4-Flash cuesta solo $0,28 —más de 10 veces más "
            "barato que sus equivalentes de OpenAI. ByteDance, Tencent y Alibaba se lanzaron en días a "
            "asegurar nuevos pedidos de chips Ascend 950, cuya producción masiva arrancó en abril."
        ),
        "fuente_label": "Fortune — DeepSeek V4: price, performance and Huawei chips",
        "fuente_url": "https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/",
    },
    {
        "emoji": "🏆",
        "titulo": "China lidera las patentes de IA con el 60% del total mundial",
        "cuerpo": (
            "El 29 de abril, el 9.º Summit de la China Digital en Fujian presentó el Informe de "
            "Desarrollo de China Digital (2025): China acumula ya el 60% de todas las patentes de IA "
            "del mundo. El valor añadido de la economía digital representa más del 10,5% del PIB del "
            "país, y la industria central de IA ha superado los 1,2 billones de yuanes (≈ 174.900 "
            "millones de dólares). El Índice de Desarrollo de la China Digital llegó a 170,1 en 2025, "
            "un salto del 12,99% interanual. La IA ha pasado de ser una promesa a ser infraestructura "
            "productiva real en todos los sectores de la economía."
        ),
        "fuente_label": "Xinhua — China leads in AI patents, digital economy booms",
        "fuente_url": "https://english.news.cn/20260429/926b297fc87846bb96166d24f5968d75/c.html",
    },
    {
        "emoji": "🧠",
        "titulo": "La IA se hace física: robots, coches y electrodomésticos con cerebro propio",
        "cuerpo": (
            "CNBC describió el 27 de abril la gran tendencia del momento: la IA china abandona la "
            "pantalla para instalarse en el mundo físico. El 38,2% del capital riesgo de IA en China "
            "en 2025 fue a robótica, no a aplicaciones de consumo. En Suzhou, la startup JoyIn anunció "
            "que su humanoide Zeroth M1 será el primero en usar funciones OpenClaw, con pedidos previos "
            "para julio. Fabricantes extranjeros (Volkswagen, GM, BMW) anunciaron modelos para China "
            "integrando IA de ByteDance y otras compañías locales —no de Silicon Valley—, marcando un "
            "punto de inflexión en quién define la inteligencia de los vehículos del futuro."
        ),
        "fuente_label": "CNBC China Connection — AI is moving into the physical world fast",
        "fuente_url": "https://www.cnbc.com/2026/04/27/china-ai-hardware-shipping-einclaw-style3d-vw-alibaba.html",
    },
    {
        "emoji": "🚗",
        "titulo": "Auto China 2026: el mayor salón del automóvil del mundo, dominado por la innovación china",
        "cuerpo": (
            "El 24 de abril abrió el Salón del Automóvil de Pekín 2026: 380.000 m² de superficie "
            "(récord mundial), 1.451 vehículos y 181 premieres mundiales. BYD presentó su batería de "
            "estado sólido de sulfuro con 480 Wh/kg en un vehículo real —la primera vez que esto ocurre "
            "en producción—, con instalación en pequeña serie en 2027 y paridad de precio con baterías "
            "de litio en 2030. La conducción autónoma L3 comenzó a escalar masivamente, y la carga "
            "ultra rápida entra en la era del megavatio. Xiaomi presentó el Aero GT, mientras Chery "
            "mostró el iCar RoBox, consolidando la imagen de China como epicentro de la innovación "
            "en movilidad eléctrica global."
        ),
        "fuente_label": "The Electric Viking — Beijing Auto Show 2026 highlights",
        "fuente_url": "https://theelectricviking.com/beijing-auto-show-2026-opens-with-record-scale-new-ev-brands-and-a-showdown-in-smart-driving-tech/",
    },
    {
        "emoji": "🚀",
        "titulo": "11.º Día del Espacio de China: 70 años de exploración y 92 misiones en 2025",
        "cuerpo": (
            "El 24 de abril, China celebró su 11.º Día del Espacio en Chengdu, con el lema 'Siete "
            "décadas explorando el cielo, alcanzando las estrellas juntos'. La fecha conmemora el "
            "lanzamiento del primer satélite chino Dongfanghong-1 en 1970 y el 70.º aniversario del "
            "programa espacial. Balance de 2025: 92 misiones de lanzamiento (+35% vs 2024). Para 2026: "
            "misión tripulada Shenzhou-23, pruebas del cohete reutilizable Larga Marcha 10 y "
            "acercamiento de Tianwen-2 a su asteroide objetivo —la primera misión china de retorno de "
            "muestras de un asteroide—. La Conferencia Espacial de China 2026 (23-25 de abril) reunió "
            "más de 20 sesiones académicas en Chengdu."
        ),
        "fuente_label": "Xinhua Español — China llevará a cabo misiones espaciales intensivas en 2026",
        "fuente_url": "https://spanish.news.cn/20260418/dcdfd28416bd4044867e2f84cf6e9842/c.html",
    },
    {
        "emoji": "✈️",
        "titulo": "El turismo interno chino: 6.500 millones de viajes y 6,3 billones de yuanes en 2025",
        "cuerpo": (
            "El turismo interno se ha convertido en uno de los grandes motores de la demanda doméstica "
            "china. En 2025, los ciudadanos chinos realizaron más de 6.500 millones de viajes internos, "
            "generando 6,3 billones de yuanes —el equivalente al 12,6% de las ventas minoristas totales "
            "del país—. El valor añadido del turismo y sectores relacionados representó entre el 4,7% y "
            "el 4,9% del PIB, incluyendo el gasto de turistas internacionales. El sector se digitaliza "
            "rápidamente, con reservas por IA y experiencias de realidad aumentada en destinos "
            "históricos, convirtiéndose en un laboratorio viviente de la economía inteligente china."
        ),
        "fuente_label": "La Jornada — Turismo interno fortalece a China",
        "fuente_url": "https://www.jornada.com.mx/2026/04/27/economia/024n1eco",
    },
    {
        "emoji": "💾",
        "titulo": "China acapara los datos: la materia prima del siglo XXI",
        "cuerpo": (
            "Un análisis publicado el 23 de abril apunta a un hecho con implicaciones profundas: China "
            "no solo lidera en IA, sino en la infraestructura de datos que la alimenta. El país ha "
            "construido la mayor red de centros de datos del mundo, con inversión récord en cables "
            "submarinos propios y un ecosistema de aplicaciones (WeChat, TikTok, Alipay, Didi) que "
            "genera volúmenes de datos sin equivalente en Occidente. La regulación nacional sobre datos "
            "—orientada al uso estratégico más que a la restricción— permite a las empresas chinas "
            "entrenar modelos con datasets de un tamaño y diversidad difíciles de replicar fuera del "
            "país, consolidando una ventaja competitiva estructural en la era de la IA."
        ),
        "fuente_label": "Sercolombiano — China acapara los datos, la materia prima del futuro",
        "fuente_url": "https://www.sercolombiano.com/2026/04/23/china-acapara-los-datos-la-materia-prima-del-futuro/",
    },
    {
        "emoji": "🗺️",
        "titulo": "XV Plan Quinquenal: autosuficiencia tecnológica, IA transversal y estándares propios",
        "cuerpo": (
            "Los análisis de la semana profundizan en el XV Plan Quinquenal (2026-2030). Tres ejes "
            "destacan: primero, la autosuficiencia tecnológica —DeepSeek V4 y Huawei Ascend son el "
            "ejemplo práctico de la semana—; segundo, la iniciativa 'IA Plus', que busca que todos los "
            "sectores productivos incorporen IA de forma nativa, desde la sanidad a la agricultura; "
            "tercero, China no quiere exportar solo bienes, sino también estándares tecnológicos: 6G, "
            "IA, vehículo eléctrico y modelos de gobernanza digital. El presupuesto en Ciencia y "
            "Tecnología creció un 7,1% hasta 1,3 billones de yuanes, marcando la apuesta estructural "
            "del país por liderar la próxima fase de la economía global."
        ),
        "fuente_label": "La Mar de Onuba — China Plan Quinquenal 2026-2030",
        "fuente_url": "https://revista.lamardeonuba.es/china-plan-quinquenal-2026-2030-tecnologia-autosuficiencia/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de abril de %Y")
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
    title = "China Al Dia — Semana 23-30 Abril 2026"
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
