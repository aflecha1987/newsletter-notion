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
        "titulo": "Conferencia Mundial de IA 2026: Shanghai, capital global de la inteligencia artificial",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghai acoge la Conferencia Mundial de Inteligencia Artificial 2026 "
            "(WAIC 2026), con el presidente Xi Jinping como orador principal en la ceremonia de apertura. "
            "Más de 1.400 invitados internacionales de 60 países, más de 1.100 empresas y 300 debuts mundiales "
            "de productos. Bajo el lema 'Socios inteligentes, co-creando el futuro', el evento reúne los dos "
            "grandes ejes de la conferencia: computación inteligente e inteligencia encarnada (embodied AI). "
            "China lidera el mundo con 1.509 modelos de IA de gran tamaño operativos."
        ),
        "fuente_label": "CGTN — Shanghai to host record-breaking World AI Conference",
        "fuente_url": "https://news.cgtn.com/news/2026-07-07/Shanghai-to-host-record-breaking-World-AI-Conference-July-17-to-20-1OAHU3xSEog/p.html",
    },
    {
        "emoji": "🏭",
        "titulo": "Más del 30% de las grandes empresas industriales chinas ya han adoptado la IA",
        "cuerpo": (
            "Según el Ministerio de Industria y Tecnología de la Información (MIIT), más del 30% de las "
            "grandes empresas industriales de China han integrado la inteligencia artificial en sus procesos. "
            "Las patentes vinculadas a IA crecieron un 34,8% interanual en el primer semestre de 2026, y "
            "las relativas a industrias estratégicas emergentes aumentaron un 15,6%. China ha invertido "
            "3,93 billones de yuanes en I+D durante 2025 (2,8% del PIB), e instalado 295.000 robots "
            "industriales en fábricas, el 54% de la producción mundial."
        ),
        "fuente_label": "Prensa Latina — China reporta alza en indicadores de consumo e innovación",
        "fuente_url": "https://www.prensa-latina.cu/2026/07/13/china-reporta-alza-en-indicadores-de-consumo-e-innovacion-tecnologica/",
    },
    {
        "emoji": "🌐",
        "titulo": "China defiende ante la ONU la IA de código abierto para todos los países",
        "cuerpo": (
            "En el primer Diálogo Global sobre Gobernanza de la IA de la ONU (6-7 de julio, Ginebra), "
            "China reafirmó su apoyo a la inteligencia artificial de código abierto como mecanismo para "
            "que los países del Sur Global desarrollen sus propias capacidades. La delegación china propuso "
            "un marco multilateral de gobernanza que evite monopolios tecnológicos y garantice el acceso "
            "equitativo a los beneficios de la IA, posicionando a China como defensora del multilateralismo "
            "tecnológico frente a enfoques más restrictivos."
        ),
        "fuente_label": "DiarioBitcoin — China respalda la IA de código abierto ante la ONU",
        "fuente_url": "https://www.diariobitcoin.com/regulacion/china-respalda-la-ia-de-codigo-abierto-ante-la-onu-y-pone-en-duda-rumores-de-controles/",
    },
    {
        "emoji": "🦾",
        "titulo": "El duopolio robótico chino: Unitree y AgiBot producen el 80% de los humanoides del mundo",
        "cuerpo": (
            "China aumentará un 94% su producción de robots humanoides en 2026. Unitree Robotics y AgiBot "
            "controlan casi el 80% del mercado global. AgiBot alcanzó los 10.000 robots Expedition A3 "
            "producidos, triplicando su capacidad en tres meses. Unitree recibió aprobación para cotizar "
            "en el STAR Market de Shanghai —primera empresa de 'IA encarnada' en bolsa A-share china—, "
            "con una capacidad anual objetivo de 75.000 robots humanoides y 115.000 cuadrúpedos. "
            "Las empresas chinas enviaron el 80% de los humanoides del mundo en 2025."
        ),
        "fuente_label": "TrendForce — China Humanoid Robot Output to Surge 94% in 2026",
        "fuente_url": "https://www.trendforce.com/presscenter/news/20260409-13007.html",
    },
    {
        "emoji": "🚀",
        "titulo": "El cohete de Chang'e-7 llega a Wenchang: China se lanza al polo sur lunar en agosto",
        "cuerpo": (
            "El 14 de julio, el cohete Larga Marcha 5 (Y14) para la misión Chang'e-7 llegó al Centro "
            "Espacial de Wenchang. El lanzamiento está previsto para agosto de 2026. La misión aterrizará "
            "en el borde del cráter Shackleton (polo sur lunar) con un orbitador, un rover, un módulo de "
            "aterrizaje y una innovadora sonda mini-saltadora que explorará cráteres en sombra permanente "
            "en busca de agua en forma de hielo. La misión lleva 21 cargas científicas, incluyendo "
            "6 experimentos internacionales de países como Francia, Suiza e Italia."
        ),
        "fuente_label": "Guangming Online — Carrier rocket for Chang'e-7 arrives at launch site",
        "fuente_url": "https://en.gmw.cn/2026-07/14/content_38885156.htm",
    },
    {
        "emoji": "☀️",
        "titulo": "Zhuri: China capta energía solar en el espacio y la envía a la Tierra",
        "cuerpo": (
            "El proyecto Zhuri de energía solar espacial de la Academia de Tecnología Espacial de China "
            "(CAST) alcanzó en 2026 la generación de 1.180 vatios en órbita baja (LEO). Esta tecnología "
            "captura energía solar sin interrupciones climáticas y la transmite a la Tierra mediante "
            "microondas. El roadmap prevé un prototipo de 0,5 MW en órbita geoestacionaria para 2030 "
            "y una estación piloto de 20 MW con antena de 100 metros para 2035. China es el único país "
            "con un roadmap escalonado y público para esta tecnología transformadora."
        ),
        "fuente_label": "El Ecosistema Startup — Zhuri: China logra 1.180W de energía solar espacial",
        "fuente_url": "https://ecosistemastartup.com/zhuri-china-logra-1-180w-de-energia-solar-espacial-en-2026/",
    },
    {
        "emoji": "🚗",
        "titulo": "Hito histórico: China exporta más de un millón de vehículos en un mes, con eléctricos como protagonistas",
        "cuerpo": (
            "En junio de 2026, China superó por primera vez la barrera del millón de vehículos exportados "
            "en un solo mes, con los vehículos de nuevas energías (NEV) representando más del 50% del total. "
            "BYD batió su propio récord con 175.349 unidades exportadas (+94,73% interanual). Las "
            "exportaciones de NEV alcanzaron 523.000 unidades en junio, multiplicando por 1,6 la cifra "
            "del año anterior. BYD proyecta 1,5 millones de ventas en el exterior en todo 2026, "
            "consolidándose como el mayor fabricante de vehículos eléctricos del mundo."
        ),
        "fuente_label": "CarNewsChina — China's monthly vehicle exports exceed 1 million for first time",
        "fuente_url": "https://carnewschina.com/2026/07/10/chinas-monthly-vehicle-exports-exceed-1-million-for-the-first-time-with-nevs-claiming-over-half/",
    },
    {
        "emoji": "📈",
        "titulo": "El Banco Mundial confirma: China crece al 5% y lidera el comercio con ASEAN y la UE",
        "cuerpo": (
            "La actualización económica del Banco Mundial de julio de 2026 confirma que China creció un "
            "5% interanual en el primer trimestre, en línea con el objetivo del gobierno (4,5%-5%). "
            "El comercio con la ASEAN —mayor socio de China— creció un 20,3% interanual, y el comercio "
            "con la UE subió un 19,9% en los primeros meses del año. La fortaleza exportadora industrial "
            "sigue siendo el principal motor del crecimiento, con el comercio exterior registrando "
            "crecimiento de doble dígito desde inicio de 2026."
        ),
        "fuente_label": "Banco Mundial — China Economic Update July 2026",
        "fuente_url": "https://thedocs.worldbank.org/en/doc/1ef2e7b9c02124a80292f5d43cce0961-0070012026/china-economic-update-july-2026",
    },
    {
        "emoji": "🔬",
        "titulo": "Xi Jinping: China pasa de seguidor a líder mundial en ciencia y tecnología",
        "cuerpo": (
            "En la Conferencia Nacional de Premios de Ciencia y Tecnología, el presidente Xi Jinping "
            "afirmó que China ha pasado de ser seguidor a convertirse en líder en ciencia y tecnología, "
            "e instó a acelerar la autosuficiencia científica para consolidar al país como potencia "
            "tecnológica global para 2035. El período 2026-2030 será decisivo. El presupuesto nacional "
            "en C+T aumentó un 7,1% hasta 1,3 billones de yuanes, y las autorizaciones de patentes "
            "en industrias emergentes crecieron un 15,6% interanual."
        ),
        "fuente_label": "Xinhua en Español — Xi insta a impulsar modernización mediante innovación",
        "fuente_url": "http://spanish.xinhuanet.com/20260708/351fa1e6395b401dace4f81c1f581872/c.html",
    },
    {
        "emoji": "🌍",
        "titulo": "China y el Sur Global: nueva era de cooperación en tecnología, industria y bienestar",
        "cuerpo": (
            "China está construyendo con los países del Sur Global 'ecosistemas de desarrollo completos' "
            "que abarcan capacidad industrial, innovación tecnológica, transformación digital, desarrollo "
            "verde y seguridad alimentaria. En África, Asia y América Latina, los proyectos chinos van "
            "desde infraestructura hasta programas de nutrición infantil, como el lanzado en Liberia "
            "el 3 de julio. En el plano multilateral, China y el Sur Global coordinan posiciones en "
            "la ONU, el G20 y los BRICS+ para impulsar una gobernanza global más justa y multipolar."
        ),
        "fuente_label": "Mundo Global — China y su hoja de ruta diplomática 2026",
        "fuente_url": "https://mundoglobal.org/china-marca-su-hoja-de-ruta-para-2026-en-las-dos-sesiones-crecimiento-diplomacia-y-mayor-presencia-en-el-sur-global/",
    },
    {
        "emoji": "🏥",
        "titulo": "Conferencia de Economía Digital 2026: diagnóstico médico con IA en minutos, para todos",
        "cuerpo": (
            "La Conferencia Global de Economía Digital 2026 (2-5 julio, Beijing) exhibió quioscos de "
            "diagnóstico médico impulsados por IA que combinan biomedicina moderna con medicina tradicional "
            "china: análisis facial, observación de la lengua y lectura digital del pulso generan informes "
            "de salud personalizados en minutos. El evento, bajo el lema 'Inteligencia inclusiva, "
            "conectividad sin fronteras', también presentó soldadura inteligente de última generación "
            "y guías turísticas por avatar digital. La Comisión Nacional de Salud de China promueve "
            "la integración de IA en servicios médicos como estrategia nacional."
        ),
        "fuente_label": "CRI Español — Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cri.cn/2026/07/02/ARTI1782972617748340",
    },
    {
        "emoji": "⚡",
        "titulo": "China, líder mundial en transición energética: renovables, almacenamiento y eficiencia",
        "cuerpo": (
            "China se ha consolidado como líder mundial en la transición hacia energías renovables, "
            "con la energía solar y eólica como pilares. Las innovaciones en perovskitas (solar de "
            "nueva generación) y en sistemas de almacenamiento (baterías y bombeo hidráulico) afrontan "
            "el reto de la intermitencia. Durante el 15.º Plan Quinquenal (2026-2030), las dos grandes "
            "empresas estatales de la red eléctrica invertirán 1 billón de yuanes anuales (~146.000 M$) "
            "en la conexión de nuevas energías a la red. State Grid ya aumentó un 50% su gasto en "
            "conexión verde en el primer trimestre de 2026."
        ),
        "fuente_label": "Ambientum — Estrategia Energética de China: Liderazgo y Renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
    },
]


def build_blocks():
    today = "14 de julio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · Semana del 7 al {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, diplomacia y sociedad.", bold=False),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        blocks.append(p_link(n["fuente_label"], n["fuente_url"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas · Proxima edicion: 21 de julio de 2026", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 7-14 Julio 2026"
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
