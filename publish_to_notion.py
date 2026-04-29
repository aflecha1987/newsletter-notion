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
        "titulo": "DeepSeek V4: la IA más potente del mundo, entrenada con chips Huawei sin Nvidia",
        "cuerpo": (
            "El 24 de abril, DeepSeek presentó su nuevo modelo de inteligencia artificial V4 con dos versiones: "
            "V4-Pro (1,6 billones de parámetros) y V4-Flash (284.000 millones). El hito más significativo: fue "
            "entrenado íntegramente con chips Ascend de Huawei, prescindiendo por completo de las GPU de Nvidia. "
            "Una declaración de independencia tecnológica frente a las restricciones de exportación de EE.UU. "
            "Con un contexto de un millón de tokens, rinde por encima de GPT-5.2 de OpenAI y Gemini 3.0-Pro de "
            "Google en pruebas estándar de razonamiento, posicionándose como el modelo de código abierto más "
            "capaz del mundo."
        ),
        "fuente_label": "Bloomberg — DeepSeek V4 desafía a OpenAI y Google",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-24/deepseek-v4-la-nueva-ia-que-desafia-a-openai-y-google",
    },
    {
        "emoji": "🚗",
        "titulo": "Auto China 2026: el salón del automóvil más avanzado del mundo aterriza en Pekín",
        "cuerpo": (
            "El mayor salón del automóvil del planeta abrió sus puertas en Pekín del 24 al 28 de abril. "
            "El protagonista indiscutible fue XPENG con su Land Aircraft Carrier: un auto volador modular con "
            "precio previsto por debajo de los 2 millones de yuanes (~292.000 USD), del que ya se han tomado "
            "más de 7.000 reservas y cuya producción masiva arranca en 2027. También presentó el GX, su nuevo "
            "SUV buque insignia con 750 km de autonomía y hardware L4 listo para conducción autónoma, por "
            "58.000 USD. El salón reunió a fabricantes de todo el mundo y puso de manifiesto el liderazgo "
            "chino en vehículos eléctricos, IA física y movilidad aérea urbana."
        ),
        "fuente_label": "CnEVPost — XPENG flying car orders top 90/day at Beijing Auto Show",
        "fuente_url": "https://cnevpost.com/2026/04/27/xpeng-flying-car-unit-daily-orders-90-drawing-crowds-beijing-auto-show/",
    },
    {
        "emoji": "🚀",
        "titulo": "China planea 140 lanzamientos espaciales en 2026: récord absoluto",
        "cuerpo": (
            "La Agencia Espacial Nacional China (CNSA) confirmó en la Conferencia Espacial China 2026 "
            "(Chengdu, 23-25 de abril) que el país realizará alrededor de 140 lanzamientos orbitales este año, "
            "el mayor número en su historia. El 11 de abril ya se realizó un lanzamiento marino exitoso del "
            "cohete Smart Dragon-3 desde Guangdong. La constelación satelital Guowang alcanzó 168 satélites en "
            "órbita, rumbo a 310 antes de fin de año. La conferencia también detalló los ensayos del cohete "
            "reutilizable Larga Marcha 10 y la misión Chang'e-7 al polo sur lunar, prevista para agosto."
        ),
        "fuente_label": "SpaceNews — China targets 140 launches in 2026",
        "fuente_url": "https://spacenews.com/china-targets-140-launches-in-2026-amid-commercial-space-surge/",
    },
    {
        "emoji": "⚡",
        "titulo": "8.500 robots IA para gestionar toda la red eléctrica china en 2030",
        "cuerpo": (
            "La Corporación Estatal de la Red Eléctrica de China, la mayor empresa de servicios públicos del "
            "mundo, asignó una inversión inicial de 6.800 millones de yuanes (aproximadamente 845 millones de "
            "euros) para adquirir robots con inteligencia artificial en 2026. El plan contempla desplegar 8.500 "
            "robots en subestaciones, tendidos de alta tensión y zonas de riesgo antes de 2030, reemplazando "
            "tareas peligrosas para los operarios humanos. Un ejemplo más de cómo China integra la robótica "
            "como infraestructura nacional estratégica."
        ),
        "fuente_label": "El Español — China crea ejército de 8.500 robots para la red eléctrica",
        "fuente_url": "https://www.elespanol.com/omicrono/tecnologia/20260427/china-cambia-normas-creando-ejercito-robots-gestionar-toda-red-electrica/1003744224041_0.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Las fábricas chinas de humanoides producen un robot nuevo cada 30 minutos",
        "cuerpo": (
            "Varias plantas de fabricación de robots humanoides en China ya operan con ciclos de producción de "
            "un robot cada 30 minutos. Empresas como Unitree, Agibot y UBTECH lideran esta aceleración "
            "industrial. El sector proyecta producir casi el doble de unidades en 2026 respecto al año anterior. "
            "China emplea estos robots tanto en líneas de montaje industrial como en atención en comercios y "
            "hospitales, adelantándose en años a sus competidores occidentales en despliegue comercial real."
        ),
        "fuente_label": "La Verdad Noticias — Fábrica de robots revoluciona producción",
        "fuente_url": "https://laverdadnoticias.com/futuro-ahora/gadgets-que-importan/fabrica-de-robots",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar de China supera al carbón en capacidad instalada",
        "cuerpo": (
            "Por primera vez en la historia, China tiene más capacidad instalada de energía solar que de carbón. "
            "En el primer trimestre de 2026, la nueva capacidad eólica y solar sumó 57,16 millones de kW, "
            "representando el 68,2% de toda la capacidad eléctrica añadida en el período. La energía solar y "
            "eólica juntas generan ya más del 25% de la electricidad del país. Con 448 GW en construcción, "
            "la mitad del total mundial, China consolida su papel como motor de la transición energética global."
        ),
        "fuente_label": "Ecoticias — China lidera energía solar superando al carbón",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🏃",
        "titulo": "Robot humanoide bate el récord mundial de la media maratón en Pekín",
        "cuerpo": (
            "El 19 de abril, el robot humanoide Lightning, desarrollado por Honor (spin-off de Huawei), "
            "completó los 21 km de la media maratón de E-Town en Pekín en tan solo 50 minutos y 26 segundos, "
            "superando el récord mundial humano por más de 6 minutos. Honor copó los tres primeros puestos "
            "de la categoría robótica, con todos los finalistas corriendo de forma completamente autónoma, "
            "sin control remoto. Más de 100 equipos participaron este año, casi cinco veces más que en la "
            "edición inaugural de 2025, donde el ganador tardó 2 horas y 40 minutos."
        ),
        "fuente_label": "NPR — Humanoid robot wins Beijing half-marathon",
        "fuente_url": "https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China crece un 5% en Q1 2026, superando expectativas",
        "cuerpo": (
            "La economía china arrancó 2026 con fuerza: el PIB creció un 5% interanual en el primer "
            "trimestre, por encima de las previsiones de los analistas y el ritmo más rápido en tres "
            "trimestres. El motor principal fue la manufactura de alta tecnología, que creció un 12,5%, "
            "con robots industriales y circuitos integrados disparándose un 33% y un 24% respectivamente. "
            "El comercio exterior aumentó un 15% en el mismo período, con exportaciones de bienes "
            "creciendo un 18,3% en enero-febrero, el primer crecimiento de doble dígito desde marzo "
            "de 2023, reflejando la resistencia de la segunda economía del mundo pese a las "
            "turbulencias geopolíticas."
        ),
        "fuente_label": "CGTN Español — PIB de China crece 5% en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-16/2044673673351409665/index.html",
    },
    {
        "emoji": "🔬",
        "titulo": "Foro Zhongguancun 2026: China impulsa un ecosistema global de ciencia abierta con RISC-V",
        "cuerpo": (
            "En el Foro Zhongguancun 2026 celebrado en Pekín, China presentó su propuesta para un ecosistema "
            "global de ciencia y tecnología abierto. La Academia China de Ciencias presentó avances en RISC-V, "
            "incluida la plataforma Xiangshan y el sistema operativo Ruyi, descrito como el primero nativo "
            "compatible con el estándar internacional RVA23 de alto desempeño. Los cinco ejes de la propuesta: "
            "cooperación internacional, datos compartidos, estándares comunes, acceso equitativo a la "
            "infraestructura y gobernanza multilateral. China refuerza así su apuesta por el código abierto "
            "como alternativa a las arquitecturas dominadas por EE.UU."
        ),
        "fuente_label": "ContraPlano — China impulsa ecosistema global de ciencia y tecnología",
        "fuente_url": "https://contraplano.cl/china-ecosistema-global-ciencia-tecnologia-2026/",
    },
    {
        "emoji": "🗺️",
        "titulo": "El XV Plan Quinquenal (2026-2030): IA, 6G, robots y biotech como pilares del futuro",
        "cuerpo": (
            "El nuevo plan quinquenal chino sitúa las llamadas 'Nuevas Fuerzas Productivas de Calidad' "
            "en el centro de su estrategia de desarrollo. Los ejes son claros: IA Plus (aplicar la IA "
            "como infraestructura transversal a toda la economía), 6G, robótica, biotecnología y economía "
            "de baja altitud (drones). Las industrias emergentes como circuitos integrados, robots inteligentes "
            "y drones suman ya casi 6 billones de yuanes y aspiran a 10 billones para 2030. El presupuesto "
            "en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones de yuanes. China no solo quiere "
            "liderar estas tecnologías: quiere que sean el motor de su desarrollo económico de las "
            "próximas dos décadas."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
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
    title = "China Al Dia — Semana 22-29 Abril 2026"
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
