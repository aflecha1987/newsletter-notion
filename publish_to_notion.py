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

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}


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
        "emoji": "🦄",
        "titulo": "China crea 67 nuevos unicornios en medio año: uno cada tres días, impulsados por la IA",
        "cuerpo": (
            "En la primera mitad de 2026, China registró 67 nuevas empresas unicornio —startups valoradas "
            "en más de 1.000 millones de dólares—, lo que equivale a una nueva cada tres días. La "
            "inteligencia artificial y la robótica son los sectores protagonistas de este boom. Como "
            "símbolo de esta madurez, el 3 de julio la Comisión Reguladora de Valores aprobó la solicitud "
            "de Unitree Robotics para cotizar en el Mercado STAR de Shanghái, marcando un hito para la "
            "industria robótica china y consolidando el camino de estas empresas hacia los mercados de "
            "capitales globales."
        ),
        "fuente_label": "DiarioBitcoin — China: un unicornio cada 3 días en la primera mitad de 2026",
        "fuente_url": "https://www.diariobitcoin.com/startups-verticales/china-creo-un-nuevo-unicornio-cada-3-dias-durante-la-primera-mitad-de-2026-y-la-ia-domina/",
    },
    {
        "emoji": "🧠",
        "titulo": "China lidera el mundo con 1.509 modelos de lenguaje y se prepara para la WAIC 2026",
        "cuerpo": (
            "China encabeza el ranking global de modelos de lenguaje de gran escala (LLMs) con 1.509 "
            "modelos desarrollados en el país. El primer gran aldabonazo lo dio DeepSeek-R1 a principios "
            "de 2025, cuando el laboratorio de Hangzhou demostró que era posible entrenar modelos de IA "
            "de primer nivel con una fracción del coste de sus competidores. La Conferencia Mundial de IA "
            "2026 (WAIC) se celebrará en Shanghái del 17 al 20 de julio, mostrando agentes de IA, "
            "ecosistemas de código abierto y aplicaciones industriales. Más del 30% de las grandes "
            "empresas industriales chinas ya han adoptado la IA en sus procesos, según el Ministerio "
            "de Industria y Tecnología de la Información."
        ),
        "fuente_label": "CGTN — AI expert: China provides a unique environment for AI innovation",
        "fuente_url": "https://news.cgtn.com/news/2026-07-04/AI-expert-China-provides-a-unique-environment-for-AI-innovation-1OvhxTG8WJO/p.html",
    },
    {
        "emoji": "🏥",
        "titulo": "Diagnóstico inteligente en el metro: IA y Medicina Tradicional China se fusionan",
        "cuerpo": (
            "China despliega quioscos de diagnóstico asistido por IA en estaciones de metro y puntos "
            "urbanos estratégicos. Los dispositivos realizan escaneos faciales y oculares para generar "
            "informes de salud personalizados en minutos, midiendo presión arterial, saturación de oxígeno "
            "y temperatura. Un sistema de IA aplica criterios milenarios —análisis facial, observación "
            "de la lengua, lectura digital del pulso mediante sensores multicapa— en tiempo real. La "
            "empresa Guanwei Intelligent Technology digitaliza y moderniza el diagnóstico de la medicina "
            "tradicional china con inteligencia artificial de última generación."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional China",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
    {
        "emoji": "🤖",
        "titulo": "Morgan Stanley dobla sus previsiones: 50.000 robots humanoides en China en 2026",
        "cuerpo": (
            "Morgan Stanley revisó casi al doble su previsión de envíos de robots humanoides en China "
            "para 2026: de 28.000 a 50.000 unidades. Los fabricantes chinos han dejado atrás la fase "
            "de demostraciones y comenzado a desplegar humanoides en entornos productivos reales, con "
            "contratos en sectores industriales tradicionales. Las autoridades chinas anunciaron además "
            "la creación de un sistema nacional de identificación digital para robots humanoides, "
            "convirtiendo a China en el primer país en regular de forma sistemática esta nueva categoría "
            "de máquinas. La IA impulsa la robotización de sectores como la hostelería, la logística "
            "y la manufactura tradicional."
        ),
        "fuente_label": "Política Exterior — Los robots de China alcanzan la madurez",
        "fuente_url": "https://www.politicaexterior.com/los-robots-de-china-estan-alcanzando-la-madurez/",
    },
    {
        "emoji": "🚢",
        "titulo": "China gestiona un tercio del comercio marítimo mundial con 8 de los 10 mayores puertos",
        "cuerpo": (
            "China concentra cerca de un tercio del transporte marítimo internacional, con 8 de los 10 "
            "mayores puertos del mundo por volumen de carga. El país opera 60 terminales portuarias "
            "automatizadas —30 de contenedores—, representando el 27% del total mundial. En paralelo, "
            "el comercio de servicios creció un 6% interanual en los primeros cinco meses de 2026, con "
            "exportaciones de servicios disparándose un 15,9% hasta 1,23 billones de yuanes. China "
            "recibe además más inversión extranjera de la que envía al exterior, según el Ministerio "
            "de Comercio, con una composición de inversión que mejora trimestre a trimestre."
        ),
        "fuente_label": "Aporrea — China concentra un tercio del comercio global",
        "fuente_url": "https://www.aporrea.org/internacionales/n420589.html",
    },
    {
        "emoji": "🌐",
        "titulo": "China abre su economía: reduce de 63 a 48 los sectores vedados a inversión extranjera",
        "cuerpo": (
            "China anunció una nueva reducción de su lista negativa de inversiones extranjeras, pasando "
            "de 63 a 48 sectores con restricciones. Se eliminan limitaciones de propiedad en seguros, "
            "automóviles, finanzas y agricultura. Las nuevas normas entran en vigor el 28 de julio. "
            "China promete además un comercio más equilibrado y mayor apertura económica tras registrar "
            "un superávit comercial récord. Los inversores globales están comprando esta narrativa: "
            "según un análisis de US News, el mercado de acciones chino está marcando su propio ritmo "
            "al separarse de las tendencias de los mercados globales, atrayendo capital internacional."
        ),
        "fuente_label": "El Cronista — Reducirán las trabas para invertir en China",
        "fuente_url": "https://www.cronista.com/internacionales/reduciran-las-trabas-para-invertir-en-china/",
    },
    {
        "emoji": "⚡",
        "titulo": "China sumará 400 millones de kW renovables en 2026: la energía limpia superará el 63% del mix",
        "cuerpo": (
            "En 2026, China incorporará más de 400 millones de kilovatios de nueva capacidad de generación, "
            "de los cuales más de 300 millones provendrán de fuentes eólicas y solares. Para finales de "
            "año, la energía no fósil representará el 63% del mix energético nacional —un récord "
            "histórico—. La capacidad total instalada alcanzó los 3.650 millones de kW en junio. Un "
            "proyecto emblema del período es la línea de corriente continua Tibet–Gran Área de la Bahía, "
            "que una vez operativa enviará más de 43.000 millones de kWh de electricidad limpia al sur "
            "de China. El consumo total de electricidad en julio superó el billón de kWh."
        ),
        "fuente_label": "Ambientum — Estrategia Energética de China: Liderazgo y Renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
    },
    {
        "emoji": "🟢",
        "titulo": "China exige energía verde obligatoria para los centros de datos de inteligencia artificial",
        "cuerpo": (
            "A partir de agosto de 2026, nuevas reglas de consumo renovable distribuirán la responsabilidad "
            "no solo entre generadoras eléctricas, sino también entre provincias e industrias intensivas "
            "como el acero, el cemento, el aluminio y los centros de datos de IA. China busca "
            "convertirse en el primer gran 'electroestado' del mundo: un país donde no basta con producir "
            "energía renovable, sino que empresas y territorios están obligados a consumirla. La medida "
            "refuerza el liderazgo verde chino y pone la sostenibilidad en el centro de su estrategia "
            "tecnológica, especialmente relevante dado el exponencial consumo energético de la IA."
        ),
        "fuente_label": "El Ecosistema Startup — China exige energía verde a centros de datos IA",
        "fuente_url": "https://ecosistemastartup.com/china-exige-energia-verde-a-centros-de-datos-ia-desafios-2026/",
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e-7 lista para agosto: China explorará el polo sur de la Luna en busca de agua",
        "cuerpo": (
            "La misión Chang'e-7 completó la llegada de todos sus módulos a la Base Espacial de Wenchang "
            "y avanza en las pruebas previas al lanzamiento, previsto para agosto de 2026. La misión "
            "incluye un orbitador, un módulo de aterrizaje, un rover y una sonda saltadora diseñada "
            "para explorar los cráteres en sombra permanente del polo sur lunar, donde se sospecha la "
            "existencia de hielo de agua. Paralelamente, el satélite SMILE —misión conjunta China-ESA— "
            "marca un nuevo capítulo en el estudio de la magnetosfera terrestre, consolidando la "
            "cooperación espacial internacional de China."
        ),
        "fuente_label": "Prensa Latina — SMILE marca nuevo capítulo en ciencia espacial china",
        "fuente_url": "https://www.prensa-latina.cu/2026/06/25/smile-marca-nuevo-capitulo-en-desarrollo-de-ciencia-espacial-china/",
    },
    {
        "emoji": "☄️",
        "titulo": "China planea desviar un asteroide y construye una red de vigilancia espacial 360°",
        "cuerpo": (
            "La Administración Nacional del Espacio de China (CNSA) anunció la construcción de un sistema "
            "coordinado de vigilancia terrestre y espacial sin puntos ciegos para asteroides cercanos a "
            "la Tierra, junto con una misión de impacto cinético contra el asteroide 2016 WP8 prevista "
            "para diciembre de 2027. El objetivo: demostrar la capacidad de China para desviar objetos "
            "potencialmente peligrosos antes de que representen una amenaza real. El proyecto sitúa a "
            "China como uno de los actores globales en defensa planetaria, junto a la NASA y la ESA."
        ),
        "fuente_label": "Gizmodo ES — China lanzará nave para golpear un asteroide en 2027",
        "fuente_url": "https://es.gizmodo.com/china-lanzara-en-diciembre-de-2027-una-nave-para-golpear-un-asteroide-y-desviar-su-orbita-tambien-construira-una-red-de-vigilancia-360-sin-puntos-ciegos-2000244439",
    },
    {
        "emoji": "💊",
        "titulo": "CMEF 2026 en Shanghái: 300.000 visitantes debaten el futuro de la IA médica",
        "cuerpo": (
            "La Feria China de Equipamiento Médico (CMEF 2026), celebrada en Shanghái, congregó a más "
            "de 300.000 participantes de 150 países bajo el lema 'Fusión de la innovación, evolución "
            "sin límites'. Las sesiones centrales abordaron la IA en atención médica, interfaces "
            "cerebro-computadora, economía plateada y regulación farmacéutica. La industria biomédica "
            "china acelera su transformación hacia la innovación tecnológica: en 2024, cerca del 28% "
            "de los acuerdos globales de licencia entre grandes farmacéuticas provinieron de biotechs "
            "chinas, con más de 41.000 millones de dólares en valor total de transacciones."
        ),
        "fuente_label": "PR Newswire — CMEF 2026 concluye en Shanghai",
        "fuente_url": "https://www.prnewswire.com/news-releases/cmef-2026-concluye-en-shanghai-un-escenario-global-para-los-avances-medicos-y-las-tendencias-futuras-302759219.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "El 15.º Plan Quinquenal (2026-2030): autosuficiencia tecnológica y liderazgo digital",
        "cuerpo": (
            "El nuevo plan quinquenal chino aprobado en 2026 sitúa la autosuficiencia tecnológica y "
            "las 'Nuevas Fuerzas Productivas de Calidad' en el centro de su estrategia. Los ejes son "
            "IA Plus, 6G, robótica, biotecnología y economía de baja altitud (drones). La Conferencia "
            "Global de Economía Digital 2026, celebrada en Beijing, presentó el plan como la hoja de "
            "ruta para que China lidere la economía digital global. Las industrias de IA apuntan a "
            "superar los 10 billones de yuanes en valor para 2030, con el 90% de la economía productiva "
            "integrada con IA en ese horizonte."
        ),
        "fuente_label": "CRI Español — La Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cri.cn/2026/07/02/ARTI1782972617748340",
    },
]


def build_blocks():
    today = date.today()
    fecha_es = f"{today.day} de {MESES_ES[today.month]} de {today.year}"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {fecha_es}", "🇨🇳"),
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
    title = "China Al Dia — Semana 3-9 Julio 2026"
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
