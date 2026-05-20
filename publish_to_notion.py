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
        "titulo": "Cumbre Xi-Trump en Pekín: acuerdos históricos y apertura tecnológica",
        "cuerpo": (
            "Del 13 al 15 de mayo, Donald Trump visitó China por primera vez desde 2017 en una cumbre "
            "que ambas partes calificaron de histórica. Xi Jinping recibió al presidente estadounidense "
            "junto a los principales CEO tecnológicos de EE.UU. —Elon Musk, Tim Cook— a quienes prometió "
            "que China 'abrirá más su puerta' a los negocios extranjeros. Los acuerdos incluyen: compras "
            "chinas de productos agrícolas por 17.000 millones de dólares anuales hasta 2028, pedido de "
            "200 aviones Boeing, acceso americano a minerales críticos y tierras raras chinas, y la "
            "creación de consejos bilaterales de comercio e inversión. El punto más destacado en "
            "tecnología: Washington autorizó la venta de chips Nvidia H200 a varias grandes empresas "
            "tecnológicas chinas. Xi Jinping aceptó además la invitación de Trump para visitar EE.UU. "
            "antes de que acabe el año."
        ),
        "fuente_label": "CNBC — Xi tells Musk, Tim Cook and other CEOs: China will 'open wider'",
        "fuente_url": "https://www.cnbc.com/2026/05/14/xi-china-open-us-business-ai-chips.html",
    },
    {
        "emoji": "💨",
        "titulo": "China enciende la turbina eólica marina más grande del mundo: 20 MW y 96.000 hogares",
        "cuerpo": (
            "El 16 de mayo, Mingyang Smart Energy activó en el mar de China Meridional la turbina eólica "
            "marina más potente jamás construida: 20 megavatios, con una altura de 242 metros y palas de "
            "128 metros —cada una equivale a más de dos campos de fútbol—. Diseñada para resistir tifones "
            "de máxima categoría, puede generar electricidad suficiente para abastecer a 96.000 hogares "
            "al año. La misma semana, la Corporación Three Gorges instaló la mayor turbina eólica flotante "
            "de un solo rotor del mundo (16 MW), a 70 km frente a la costa de Guangdong. China ya produce "
            "más del 60% de todos los aerogeneradores del planeta."
        ),
        "fuente_label": "Canal 26 — China activa la turbina eólica marina más grande del mundo",
        "fuente_url": "https://www.canal26.com/internacionales/2026/05/16/energia-renovable-a-gran-escala-china-activa-la-turbina-eolica-marina-mas-grande-del-mundo-capaz-de-abastecer-a-96000-hogares/",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree Robotics sale a bolsa: 610 millones de dólares para dominar el mercado de humanoides",
        "cuerpo": (
            "Unitree Robotics, la empresa china que se convirtió en 2025 en el mayor vendedor de robots "
            "humanoides del mundo, confirmó esta semana el avance de su OPV en el Shanghai Stock Exchange, "
            "buscando recaudar 4.200 millones de yuanes (~610 millones de dólares). En 2025 registró un "
            "beneficio neto ajustado de 600 millones de yuanes —un aumento del 674% respecto a 2024, su "
            "primer año en beneficios— y envió más de 5.500 unidades, con una cuota del 32,4% del mercado "
            "mundial de humanoides. La notoriedad de Unitree explotó a principios de 2025 cuando sus "
            "robots bailaron en el programa de televisión más visto de China."
        ),
        "fuente_label": "Bloomberg — China's Unitree Robotics Files for $610 Million Shanghai IPO",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-03-20/chinese-robot-maker-unitree-seeks-610-million-in-shanghai-ipo",
    },
    {
        "emoji": "🧠",
        "titulo": "El plan de IA de Xi: transformar cada sector de la economía china",
        "cuerpo": (
            "Un análisis publicado esta semana por Le Grand Continent revela los bastidores de la "
            "estrategia de Xi Jinping para convertir la inteligencia artificial en la columna vertebral "
            "del desarrollo económico chino. El plan apunta a que la IA deje de ser un sector en sí mismo "
            "para convertirse en infraestructura transversal: fábricas, agricultura, salud, finanzas, "
            "logística. China ya cuenta con 602 millones de usuarios de IA generativa —más de la mitad "
            "del total mundial— y la industria central de IA del país superó los 1,2 billones de yuanes "
            "en valor en 2025, con más de 6.200 empresas activas en el sector."
        ),
        "fuente_label": "El Grand Continent — Bastidores del plan de IA de Xi para transformar China",
        "fuente_url": "https://legrandcontinent.eu/es/2026/05/13/bastidores-del-plan-ia-de-xi-para-transformar-china/",
    },
    {
        "emoji": "🛡️",
        "titulo": "China bloquea la compra de Manus por Meta: la soberanía de la IA no está en venta",
        "cuerpo": (
            "El 27 de abril, la Comisión Nacional de Desarrollo y Reforma de China bloqueó la adquisición "
            "de Manus —la popular startup china de agentes de IA— por parte de Meta, ordenando a ambas "
            "partes cancelar la transacción. La decisión marca una línea clara: los activos estratégicos "
            "de inteligencia artificial desarrollados en China no están disponibles para adquisición "
            "extranjera. Manus se había viralizado globalmente a principios de 2026 como uno de los "
            "agentes de IA más capaces del mercado, compitiendo directamente con los sistemas de "
            "OpenAI y Google."
        ),
        "fuente_label": "USCC — China Bulletin May 5, 2026",
        "fuente_url": "https://www.uscc.gov/trade-bulletins/china-bulletin-may-5-2026",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-21 regresa a la Tierra y Chang'e-7 se prepara para agosto",
        "cuerpo": (
            "Esta semana regresó a la Tierra la tripulación de la Shenzhou-21, la décima misión tripulada "
            "a la Estación Espacial China Tiangong, tras seis meses de experimentos científicos en órbita. "
            "En paralelo, la Agencia Espacial Nacional China confirmó que todos los módulos de Chang'e-7 "
            "están en la base de lanzamiento de Wenchang para pruebas finales previas al lanzamiento "
            "previsto en agosto de 2026, con destino al polo sur lunar en busca de depósitos de hielo de "
            "agua en cráteres en sombra permanente. El objetivo: preparar el primer alunizaje tripulado "
            "chino antes de 2030."
        ),
        "fuente_label": "OkDiario Ciencia — China en la Luna 2026: misiones, logros y objetivos",
        "fuente_url": "https://okdiario.com/ciencia/china-luna-2026-misiones-logros-objetivos-16568199",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate su récord de exportaciones: 135.000 vehículos internacionales en abril",
        "cuerpo": (
            "BYD estableció en abril de 2026 un nuevo récord de entregas internacionales con 135.000 "
            "vehículos en un solo mes. La empresa produce hasta 4.400 coches al día en su mayor fábrica "
            "—en Xi'an— a un ritmo de un vehículo cada 20 segundos. Su división de semiconductores "
            "ha escalado de 5.000 obleas/mes en 2021 a casi 60.000 obleas/mes en 2026, consolidando "
            "la integración vertical total como ventaja competitiva global. BYD también anunció el "
            "despliegue de 20.000 estaciones de recarga ultrarrápida (800V) en China antes de "
            "finales de año."
        ),
        "fuente_label": "TechInsights — China Analysis: BYD Semiconductor's Revenue Growth",
        "fuente_url": "https://www.techinsights.com/blog/china-analysis-byd-semiconductors-revenue-growth-and-capacity-ramp-outlook-0",
    },
    {
        "emoji": "🌍",
        "titulo": "España y China firman tres acuerdos para fomentar inversiones sostenibles",
        "cuerpo": (
            "El Ministerio de Economía de España firmó con las autoridades chinas tres Memorandos de "
            "Entendimiento destinados a fortalecer la cooperación económica bilateral, promover "
            "inversiones sostenibles y facilitar el acceso de productos y servicios españoles al mercado "
            "chino. Los acuerdos destacan especialmente la aceleración de iniciativas vinculadas a la "
            "descarbonización, apoyando inversiones y tecnologías que reduzcan emisiones, en lo que "
            "supone un refuerzo de los lazos bilaterales en el ámbito de la transición energética verde."
        ),
        "fuente_label": "Energías Renovables — España y China firman tres acuerdos para inversiones sostenibles",
        "fuente_url": "https://www.energias-renovables.com/panorama/espa-a-y-china-firman-tres-acuerdos-20260415",
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
    title = "China Al Dia — Semana 14-20 Mayo 2026"
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
