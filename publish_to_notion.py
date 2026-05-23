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
        "emoji": "🚀",
        "titulo": "China lanza el primer programa para enviar un robot humanoide al espacio",
        "cuerpo": (
            "La empresa Engine AI, con sede en Shenzhen, anunció una alianza con Beijing Interstellar "
            "Human Spaceflight Technology para desplegar el robot PM01 en el espacio, convirtiéndolo en "
            "el primer robot astronauta humanoide de la historia. Con 1,38 metros de altura y 40 kg, el "
            "PM01 está equipado con sensores de alta precisión, respuesta ultrarrápida y toma de "
            "decisiones autónoma. El objetivo: superar los límites fisiológicos humanos en el espacio, "
            "asumiendo el mantenimiento externo de estaciones espaciales y la exploración de zonas de "
            "alto riesgo. En paralelo, un laboratorio chino ya demostró el primer control de un humanoide "
            "a través de un satélite en órbita baja, en lo que se considera un hito histórico en robótica espacial."
        ),
        "fuente_label": "Interesting Engineering — World's first robot astronaut, China's Engine AI",
        "fuente_url": "https://interestingengineering.com/ai-robotics/worlds-first-humanoid-robot-astronaut-china",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree Robotics sale a bolsa en Shanghái: 610 millones de dólares para dominar el mercado humanoide",
        "cuerpo": (
            "Unitree Robotics, el mayor fabricante de robots humanoides del mundo, presentó una solicitud "
            "de OPV en el Star Market de Shanghái para recaudar 4.200 millones de yuanes (610 millones "
            "de dólares). La compañía registró ingresos de 1.708 millones de yuanes en 2025 (+335% "
            "interanual) y un beneficio neto que se disparó un 674%. Los humanoides pasaron del 27,6% "
            "al 51,5% de sus ingresos en apenas un año. Unitree envió más de 5.500 unidades en 2025, "
            "conquistando el 32,4% del mercado global. Casi la mitad de los fondos captados en la OPV "
            "se destinarán a entrenar modelos de IA durante los próximos tres años, consolidando a "
            "la empresa como el gran referente mundial de la robótica humanoide."
        ),
        "fuente_label": "Rest of World — Unitree China humanoid robot Shanghai IPO",
        "fuente_url": "https://restofworld.org/2026/unitree-china-humanoid-robot-shanghai-ipo/",
    },
    {
        "emoji": "🧠",
        "titulo": "China convierte los robots con IA en eje central de su estrategia nacional",
        "cuerpo": (
            "Según el informe de la Federación Internacional de Robótica (IFR) del 6 de mayo, China ha "
            "elevado la robótica y la 'inteligencia incorporada' al tejido conectivo de toda su "
            "modernización económica. El 15.º Plan Quinquenal (2026-2030) integra los robots humanoides "
            "junto al 6G, las interfaces cerebro-máquina y la fusión nuclear como fronteras tecnológicas "
            "prioritarias. El plan prevé que el 70% de la economía productiva incorpore IA antes de 2027 "
            "y el 90% antes de 2030, con un valor objetivo del sector de 10 billones de yuanes para 2030. "
            "El presupuesto en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones de yuanes."
        ),
        "fuente_label": "RoboticsTomorrow — China makes AI-powered robots core of national strategy",
        "fuente_url": "https://www.roboticstomorrow.com/news/2026/05/06/china-makes-ai-powered-robots-core-of-national-strategy-%E2%80%93-ifr-reports/26521/",
    },
    {
        "emoji": "🔬",
        "titulo": "Bastidores del plan de IA de Xi: apertura, costes bajos y despliegue masivo como ventaja global",
        "cuerpo": (
            "Un análisis publicado en Le Grand Continent el 13 de mayo revela los pilares de la "
            "estrategia de IA de Xi Jinping: mientras EE.UU. apuesta por controlar la frontera "
            "tecnológica, China opta por apertura, costes más bajos, política industrial y despliegue "
            "masivo. El resultado: 602 millones de usuarios de IA generativa —más de la mitad del "
            "total mundial— y patentes de IA creciendo un 31,2% interanual en Q1 2026. Como señal del "
            "reconocimiento internacional de este liderazgo, Xi y Trump acordaron en la cumbre de "
            "Pekín lanzar un diálogo intergubernamental sobre gobernanza de la IA, el primero entre "
            "las dos superpotencias."
        ),
        "fuente_label": "Le Grand Continent — Bastidores del plan de IA de Xi para transformar China",
        "fuente_url": "https://legrandcontinent.eu/es/2026/05/13/bastidores-del-plan-ia-de-xi-para-transformar-china/",
    },
    {
        "emoji": "🌍",
        "titulo": "La ONU elogia a China: 'La transición energética ha sido sobrecogedora'",
        "cuerpo": (
            "El secretario ejecutivo de ONU Cambio Climático, Simon Stiell, intervino en la Universidad "
            "Tsinghua de Pekín con un mensaje contundente: la transición energética china ha sido "
            "'sobrecogedora'. China no solo ha cumplido sus objetivos climáticos: los ha superado. "
            "Sus metas de capacidad eólica y solar para 2030 se alcanzaron seis años antes de lo "
            "previsto. El objetivo del 20% de ventas de coches eléctricos en 2025 fue triplicado: la "
            "cifra real fue del 50%. Los vehículos eléctricos chinos ahorrarán más de 28.000 millones "
            "de dólares en importaciones de petróleo solo en 2026. La inversión en energías limpias "
            "superó los 625.000 millones de dólares en 2024."
        ),
        "fuente_label": "ONU Noticias — Liderazgo climático de China: la transición ha sido sobrecogedora",
        "fuente_url": "https://news.un.org/es/story/2026/05/1541448",
    },
    {
        "emoji": "💨",
        "titulo": "China activa la turbina eólica marina más grande del mundo: 20 MW, 96.000 hogares",
        "cuerpo": (
            "El 16 de mayo, Mingyang Smart Energy puso en marcha una turbina eólica marina de 20 "
            "megavatios en aguas cercanas a Hainan, en el Mar de China Meridional. Con 242 metros de "
            "altura y palas de 128 metros —área equivalente a más de dos campos de fútbol—, es la "
            "turbina marina más potente jamás construida. Puede abastecer de electricidad a unas 96.000 "
            "viviendas al año y resistir ráfagas de hasta 79,8 m/s. Este hito se enmarca en el impulso "
            "chino para que las energías no fósiles representen el 63% de la capacidad instalada a "
            "finales de 2026, superando al carbón por primera vez en la historia."
        ),
        "fuente_label": "Canal 26 — China activa la turbina eólica marina más grande del mundo",
        "fuente_url": "https://www.canal26.com/internacionales/2026/05/16/energia-renovable-a-gran-escala-china-activa-la-turbina-eolica-marina-mas-grande-del-mundo-capaz-de-abastecer-a-96000-hogares/",
    },
    {
        "emoji": "🔌",
        "titulo": "21,5 millones de puntos de recarga eléctrica: China construye la red de movilidad del futuro",
        "cuerpo": (
            "China cerró marzo de 2026 con 21,48 millones de puntos de recarga para vehículos eléctricos "
            "e híbridos enchufables, un 46,9% más que hace un año. Esta infraestructura, la mayor del "
            "mundo por un margen abrumador, refleja la apuesta de Pekín por la electromovilidad como "
            "pilar de su seguridad energética y reducción de la dependencia del petróleo. El país cerró "
            "2025 con el 50% de las ventas de coches nuevos siendo eléctricos, consolidando la mayor "
            "transición de movilidad de la historia en tiempo récord."
        ),
        "fuente_label": "The Clinic — La guerra silenciosa del enchufe: China lidera la recarga eléctrica",
        "fuente_url": "https://www.theclinic.cl/2026/05/22/puntos-de-recarga-para-autos-electricos/",
    },
    {
        "emoji": "📈",
        "titulo": "Goldman Sachs eleva previsión para China al 4,8% en 2026 pese a las tensiones globales",
        "cuerpo": (
            "Goldman Sachs revisó al alza su estimación de crecimiento para China en 2026 hasta el 4,8% "
            "del PIB, impulsado por el fuerte desempeño exportador en los primeros meses del año. China "
            "fijó su objetivo en 4,5-5,0%, reflejando el giro hacia un desarrollo de 'calidad primero'. "
            "El motor es la manufactura de alta tecnología: el comercio de equipos electromecánicos y "
            "electrónica creció a doble dígito, y las exportaciones a Asia-Pacífico y países en "
            "desarrollo compensaron la caída de los envíos a EE.UU. Los semiconductores importados "
            "alcanzaron 135.000 millones de dólares en el último trimestre, impulsados por la "
            "demanda de computación para IA."
        ),
        "fuente_label": "Goldman Sachs — China's economy expected to grow 4.8% in 2026",
        "fuente_url": "https://www.goldmansachs.com/insights/articles/chinas-economy-expected-to-grow-in-2026-amid-surging-exports",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, energia y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 18-23 Mayo 2026"
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
