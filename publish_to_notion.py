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
        "titulo": "DeepSeek lanza V4: el modelo de IA chino que supera a GPT-5.4 en programacion",
        "cuerpo": (
            "El 24 de abril, DeepSeek publico la version preliminar de su modelo V4, un año despues de "
            "revolucionar el mundo de la IA con DeepSeek-R1. El nuevo modelo llega en dos versiones MoE: "
            "V4-Pro (1,6 billones de parametros, 49B activos) y V4-Flash (284B), ambos con contexto de "
            "1 millon de tokens. V4-Pro obtuvo 3.206 puntos en Codeforces, superando a GPT-5.4 (3.168) "
            "y convirtiendose en el modelo con mayor puntuacion en programacion competitiva jamas publicado. "
            "Para entrenar V4, DeepSeek se asocio con Huawei y su tecnologia Supernode basada en chips "
            "Ascend 950. El modelo es de codigo abierto y gratuito para descarga."
        ),
        "fuente_label": "CNBC — DeepSeek releases preview of long-awaited V4 model",
        "fuente_url": "https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html",
    },
    {
        "emoji": "🔬",
        "titulo": "China supera a EE.UU. en gasto en I+D por primera vez en la historia",
        "cuerpo": (
            "Segun datos de la OCDE publicados esta semana, el gasto de China en I+D alcanzo 1,03 billones "
            "de dolares en 2024, superando por primera vez al de EE.UU. (1,01 billones). Es la primera vez "
            "desde la Segunda Guerra Mundial que cualquier pais desplaza a EE.UU. del primer puesto. Desde "
            "2004, China ha aumentado su gasto en I+D al 14% anual, el doble que EE.UU. En 2024, China "
            "tambien supero a EE.UU. en publicaciones cientificas totales y registro 1,8 millones de "
            "solicitudes de patente frente a las 603.191 de EE.UU. El 15.o Plan Quinquenal fija un "
            "crecimiento del gasto en I+D de al menos el 7% anual."
        ),
        "fuente_label": "The Conversation — China surpasses US in research spending",
        "fuente_url": "https://theconversation.com/china-surpasses-us-in-research-spending-the-consequences-extend-far-beyond-scientific-ranking-and-clout-280543",
    },
    {
        "emoji": "⚛️",
        "titulo": "QBoson recauda 145 M$ para la primera fabrica china de chips cuanticos fototonicos",
        "cuerpo": (
            "La startup QBoson ha cerrado una ronda de 1.000 millones de yuanes (~145 M$) para construir "
            "la primera fabrica de chips cuanticos fotonicos de China, convirtiendo la computacion cuantica "
            "en industria manufacturera real. En paralelo, investigadores de las universidades Sun Yat-sen "
            "y Tianjin lograron la primera realizacion experimental de skyrmiones cuanticos opticos en "
            "semiconductores, un avance clave para la computacion cuantica tolerante a fallos. El 15.o "
            "Plan Quinquenal incluye la tecnologia cuantica como uno de los siete motores de crecimiento "
            "economico del pais para la proxima decada."
        ),
        "fuente_label": "Quantum Zeitgeist — China Quantum Computing Companies 2026",
        "fuente_url": "https://quantumzeitgeist.com/china-quantum-computing-companies-2026/",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23: primer año continuo en el espacio y Pakistan llega a Tiangong",
        "cuerpo": (
            "La mision Shenzhou-23 establece el primer año completo de tripulacion china en la estacion "
            "espacial Tiangong. Ademas, el plan de vuelos incluye la visita del primer astronauta "
            "pakistani a Tiangong, consolidando el caracter internacional de la estacion y la estrategia "
            "de China de construir un programa espacial abierto a socios globales. En 2026, China tiene "
            "previsto superar las 25 misiones espaciales, el calendario mas ambicioso de su historia, "
            "con el acercamiento de Tianwen-2 a su asteroide y ensayos del cohete reutilizable Larga "
            "Marcha 10, pieza clave del programa lunar tripulado antes de 2030."
        ),
        "fuente_label": "Universe Today — China's space programme prepares for its busiest year yet",
        "fuente_url": "https://www.universetoday.com/articles/chinas-space-programme-prepares-for-its-busiest-year-yet",
    },
    {
        "emoji": "🚗",
        "titulo": "Salon del Automovil de Pekin 2026: la mayor exposicion de vehiculos electricos del mundo",
        "cuerpo": (
            "El 19.o Salon Internacional del Automovil de Pekin abrio el 27 de abril con 380.000 m2, "
            "1.451 vehiculos de 21 paises, 181 estrenos mundiales y 71 coches concepto. Un solo pabellon "
            "contenia mas modelos electricos que todos los disponibles en EE.UU. Destacaron: el XPeng GX "
            "(750 km, hardware L4 por 58.000$), el BYD Denza Z (hypercar 1.000 CV descapotable rumbo a "
            "Europa), el Xiaomi Aero GT y el Robotaxi autonomo de Geely. Volkswagen anuncio una ofensiva "
            "de mas de 20 modelos electrificados en China solo en 2026, en lo que llamo su mayor ofensiva "
            "de producto en el pais."
        ),
        "fuente_label": "Electrek — Beijing Auto Show 2026: a glimpse at the future of the auto industry",
        "fuente_url": "https://electrek.co/2026/04/26/beijing-auto-show-2026-insane-glimpse-future-auto-industry/",
    },
    {
        "emoji": "💧",
        "titulo": "China dispara pedidos de vehiculos de hidrogeno: 2.131 unidades en solo dos meses",
        "cuerpo": (
            "En marzo y abril de 2026, China registro 10 grandes anuncios de pedidos de vehiculos de "
            "hidrogeno por un total de 2.131 unidades, incluyendo 1.500 camiones pesados y comerciales. "
            "El mercado chino de electrolizadores se dobla cada año, con tecnologia que ya compite en "
            "madurez con la europea. El objetivo nacional: 100.000 vehiculos de hidrogeno en circulacion "
            "para 2030, con el precio del hidrogeno verde por debajo de 3,6 dolares/kg. China lidera la "
            "transicion global al hidrogeno junto con India, mientras Occidente recorta incentivos al sector."
        ),
        "fuente_label": "Fuel Cells Works — China sees 10 hydrogen vehicle announcements",
        "fuente_url": "https://fuelcellsworks.com/2026/04/22/clean-energy/china-sees-10-hydrogen-vehicle-announcements-covering-over-2-131-units-in-march-and-april",
    },
    {
        "emoji": "🛡️",
        "titulo": "China bloquea la compra de Manus por Meta: soberania tecnologica en plena guerra del chip",
        "cuerpo": (
            "El 27 de abril, la Comision Nacional de Desarrollo y Reforma ordeno deshacer la adquisicion "
            "de la startup de IA Manus por Meta, valorada en 2.000 millones de dolares. La NDRC invoco "
            "leyes de control de exportaciones tecnologicas y normas sobre inversion extranjera para "
            "bloquear la operacion. Manus, aunque con sede en Singapur, tiene raices chinas y ha "
            "desarrollado un agente de IA autonomo reconocido mundialmente. Para Pekin, ceder esta "
            "tecnologia habria supuesto perder un activo estrategico en plena guerra tecnologica. La "
            "decision llega semanas antes de la esperada cumbre Trump-Xi en Pekin."
        ),
        "fuente_label": "CNBC — China blocks Meta's $2 billion acquisition of AI startup Manus",
        "fuente_url": "https://www.cnbc.com/2026/04/27/meta-manus-china-blocks-acquisition-ai-startup.html",
    },
    {
        "emoji": "📈",
        "titulo": "Economia china: comercio exterior +18%, manufactura de alta tecnologia +12,5% en Q1 2026",
        "cuerpo": (
            "Los datos del primer trimestre de 2026 confirman la fortaleza de la economia china: comercio "
            "exterior total +18% hasta 1,69 billones de dolares, exportaciones +14,7%, importaciones "
            "+22,7%. Los principales exportados fueron semiconductores, ordenadores y vehiculos electricos. "
            "La manufactura de alta tecnologia crecio un 12,5%, con robots industriales (+33%) y circuitos "
            "integrados (+24%) liderando. China fijo su objetivo de PIB para 2026 en 4,5-5%, con el "
            "primer trimestre ya en el 5%, el ritmo mas rapido en tres trimestres. El presupuesto en "
            "Ciencia y Tecnologia sube un 7,1% hasta 1,3 billones de yuanes."
        ),
        "fuente_label": "China Briefing — China's Q1 2026 GDP",
        "fuente_url": "https://www.china-briefing.com/news/chinas-q1-2026-gdp/",
    },
    {
        "emoji": "🌐",
        "titulo": "La Jornada: ¿Estamos preparados para 'China 2.0'?",
        "cuerpo": (
            "La publicacion mexicana La Jornada analizo esta semana el nuevo modelo de desarrollo chino "
            "bajo el concepto de 'China 2.0': un pais que ha completado su transicion de la manufactura "
            "barata a la innovacion de frontera, y que ahora exporta no solo productos sino estandares "
            "tecnologicos, modelos de gobernanza e infraestructura digital al Sur Global. La pregunta ya "
            "no es si China puede competir con Occidente en tecnologia, sino si el resto del mundo "
            "—incluyendo America Latina— tiene capacidad institucional para aprovechar o responder a "
            "este nuevo actor global. Una lectura imprescindible para entender la China de hoy."
        ),
        "fuente_label": "La Jornada — ¿Estamos preparados para China 2.0?",
        "fuente_url": "https://www.jornada.com.mx/2026/04/22/economia/017a1eco",
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
    title = "China Al Dia — Semana 21-28 Abril 2026"
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
