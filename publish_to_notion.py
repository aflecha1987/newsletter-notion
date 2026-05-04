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
        "emoji": "🧠",
        "titulo": "DeepSeek V4: China lanza el modelo de IA más potente del mundo con chips Huawei",
        "cuerpo": (
            "El 24 de abril, DeepSeek publicó bajo licencia MIT (código abierto) su nuevo modelo V4, "
            "entrenado íntegramente sobre chips Ascend de Huawei sin ningún componente de Nvidia. "
            "El V4-Pro cuenta con 1,6 billones de parámetros totales (49.000 millones activos por token), "
            "una ventana de contexto de un millón de tokens y ha sido entrenado sobre 33 billones de tokens. "
            "Supera a GPT-4o y Claude 3.5 Sonnet en benchmarks de razonamiento matemático y codificación. "
            "La ausencia total de Nvidia en la documentación técnica confirma que China ha logrado construir "
            "una pila de IA soberana de primer nivel global. Además, la valoración de DeepSeek se duplicó "
            "en horas hasta 20.000 millones de dólares, con Tencent y Alibaba negociando su entrada como inversores."
        ),
        "fuente_label": "Euronews — DeepSeek V4: everything to know as the AI race speeds up",
        "fuente_url": "https://www.euronews.com/next/2026/04/24/chinas-deepseek-releases-new-ai-model-v4-heres-everything-to-know-as-the-ai-race-speeds-up",
    },
    {
        "emoji": "📊",
        "titulo": "China procesa 140 billones de tokens de IA al día: el boom de las IPOs tecnológicas",
        "cuerpo": (
            "China procesa ya 140 billones de tokens de IA cada día, frente a los apenas 100.000 millones "
            "de enero de 2024, un crecimiento de más de 1.400 veces en poco más de dos años. El país ha "
            "construido lo que Fortune denomina una «economía de tokens»: modelos de código abierto, "
            "infraestructura barata y millones de aplicaciones reales. En enero, Zhipu AI y MiniMax debutaron "
            "en la Bolsa de Hong Kong con capitalizaciones de 56.000 millones y 37.000 millones de dólares "
            "respectivamente, las mayores IPOs tecnológicas de la ciudad en cinco años. Biren, el diseñador "
            "de chips de IA, cotizará próximamente."
        ),
        "fuente_label": "Fortune — China's token economy, AI boom and blazing IPOs",
        "fuente_url": "https://fortune.com/2026/04/12/china-token-economy-ai-boom-big-tech-startups/",
    },
    {
        "emoji": "📦",
        "titulo": "China embarca IA en hardware real: los dispositivos inteligentes ya llegan a clientes",
        "cuerpo": (
            "Mientras muchas empresas occidentales siguen en fase de prototipado, las compañías chinas de IA "
            "ya entregan hardware real. EinClaw lanzó un clip de micrófono de 43 dólares que conecta al usuario "
            "con un agente de IA mediante voz. OpenPie fabrica cajas de 14.600 dólares que ejecutan modelos "
            "de IA localmente con chips chinos de bajo coste, con objetivo de entregar 10.000 unidades antes "
            "de fin de año. Style3D, con respaldo de Alibaba, muestra su plataforma de moda digital con IA "
            "en ferias del sector. Esta oleada de hardware confirma que China ha pasado de la investigación "
            "a la comercialización a gran escala."
        ),
        "fuente_label": "CNBC — In China, companies are shipping AI hardware",
        "fuente_url": "https://www.cnbc.com/2026/04/27/china-ai-hardware-shipping-einclaw-style3d-vw-alibaba.html",
    },
    {
        "emoji": "🔬",
        "titulo": "Xi Jinping en Shanghái: «La investigación básica es el interruptor maestro de la tecnología»",
        "cuerpo": (
            "El 30 de abril, el presidente Xi Jinping presidió en Shanghái un simposio de alto nivel sobre "
            "investigación básica. Xi subrayó que 'la investigación básica es el origen de todo el sistema "
            "científico y el interruptor maestro de todas las cuestiones tecnológicas', instando a aumentar "
            "los recursos, diversificar la financiación y acelerar la integración entre industria, academia e "
            "investigación. El discurso llega en un momento en que la competencia global en ciencia y tecnología "
            "se concentra en las fronteras de la investigación básica, y refleja la determinación de Pekín de "
            "que China no solo aplique la tecnología de otros, sino que lidere su creación."
        ),
        "fuente_label": "Xinhua ES — Xi destaca importancia de impulsar investigación básica",
        "fuente_url": "http://spanish.xinhuanet.com/20260430/c30236f026f94202aba86f0d64535756/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Unitree Robotics presenta solicitud de salida a bolsa: 610 millones de dólares en el STAR Market",
        "cuerpo": (
            "Unitree Robotics, la startup de robots humanoides más reconocida de China, ha presentado "
            "formalmente su solicitud de OPV en el STAR Market de Shanghái por valor de 4.200 millones "
            "de yuanes (aproximadamente 610 millones de dólares). La compañía se ha hecho famosa globalmente "
            "por sus robots cuadrúpedos y humanoides de bajo coste, disponibles para particulares y empresas, "
            "y acumula pedidos de fábricas, centros logísticos y universidades de todo el mundo. La salida "
            "a bolsa impulsaría su capacidad de producción e I+D en el momento de máxima ebullición del "
            "sector robótico chino."
        ),
        "fuente_label": "36Kr — Why Is Unitree Robotics Preparing for IPO",
        "fuente_url": "https://eu.36kr.com/en/p/3414050818248068",
    },
    {
        "emoji": "🚕",
        "titulo": "Pony AI lanza el primer servicio comercial de robotaxi en Europa, con Uber, en Zagreb",
        "cuerpo": (
            "La empresa china de conducción autónoma Pony AI inauguró el primer servicio comercial de "
            "robotaxi en Europa en Zagreb (Croacia), en asociación con Uber y el operador local Verne. "
            "Los vehículos circulan sin conductor de seguridad a bordo en rutas preestablecidas de la ciudad. "
            "Pony AI —que ya opera en Guangzhou, Pekín y Shanghái, y cotiza en el Nasdaq— amplía así su "
            "presencia internacional en un mercado históricamente dominado por actores occidentales. "
            "El lanzamiento demuestra que la tecnología china de conducción autónoma está lista para mercados "
            "regulados exigentes como el europeo."
        ),
        "fuente_label": "Futunn — Behind the Record-Breaking IPO: Pony AI",
        "fuente_url": "https://news.futunn.com/en/post/64478832/behind-the-record-breaking-ipo-pony-ai-02026-hk-ponyus",
    },
    {
        "emoji": "🌍",
        "titulo": "China aplica arancel cero a todos los países africanos desde el 1 de mayo",
        "cuerpo": (
            "Desde el 1 de mayo de 2026, China aplica arancel cero al 100% de los productos procedentes "
            "de los 53 países africanos con los que mantiene relaciones diplomáticas. El primer cargamento "
            "bajo la nueva política fue un lote de 24 toneladas de manzanas sudafricanas que cruzó la aduana "
            "china libre de impuestos. En el primer trimestre de 2026, el comercio bilateral China-África "
            "creció un 26,8% interanual hasta los 92.160 millones de dólares, muy por encima del promedio "
            "del comercio exterior chino. La medida consolida la posición de China como principal socio "
            "comercial del continente africano y refuerza la cooperación Sur-Sur."
        ),
        "fuente_label": "Xinhua ES — China autoriza primer lote bajo política de arancel cero para África",
        "fuente_url": "http://spanish.xinhuanet.com/20260501/f20605fdb3a54b20a4a203426b5257d5/c.html",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar supera al carbón en capacidad instalada en China",
        "cuerpo": (
            "A 30 de abril de 2026, la capacidad solar instalada en China ha superado por primera vez "
            "en la historia la capacidad del carbón. El Consejo de Electricidad de China prevé que en 2026 "
            "se añadan más de 300 millones de kilovatios de nueva energía renovable, el 68,2% de toda la "
            "nueva capacidad nacional. La solar y la eólica juntas representarán el 50% de la capacidad "
            "eléctrica total del país antes de fin de año, y las fuentes no fósiles llegarán al 63% de "
            "la capacidad instalada. La participación del carbón caerá al 31%, desde más del 50% de hace "
            "apenas una década. China lidera la transición energética global con una velocidad sin precedentes."
        ),
        "fuente_label": "Ecoticias — China: energía solar supera al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🗓️",
        "titulo": "APEC Shanghái y Suzhou: China define apertura e innovación como ejes de mayo",
        "cuerpo": (
            "China acogerá en mayo dos citas clave de la agenda APEC 2026: la Segunda Reunión de Altos "
            "Funcionarios se celebrará del 11 al 19 de mayo en Shanghái, junto con el Foro de Mujeres "
            "y Economía, y del 20 al 23 de mayo tendrá lugar en Suzhou la reunión de ministros de "
            "Comercio, centrada en reforzar el sistema económico multilateral y reducir barreras a la "
            "economía digital. China ha definido como objetivos prioritarios para su presidencia de APEC "
            "la apertura económica, la innovación tecnológica y la integración regional."
        ),
        "fuente_label": "Prensa Latina — China define apertura e innovación entre objetivos para APEC 2026",
        "fuente_url": "https://www.prensa-latina.cu/2026/04/27/china-define-apertura-e-innovacion-entre-objetivos-para-apec-2026/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, energia y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 27 Abril - 4 Mayo 2026"
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
