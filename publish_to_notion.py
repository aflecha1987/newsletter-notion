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
        "titulo": "China inaugura la primera 'escuela para robots humanoides' del mundo en Shanghái",
        "cuerpo": (
            "En julio de 2026, Shanghái abre el primer gran centro de entrenamiento para robots humanoides "
            "del planeta, en el distrito de Zhangjiang. El complejo de más de 5.000 m² alberga más de 100 "
            "modelos distintos de robots —de más de una docena de fabricantes— entrenando simultáneamente. "
            "El centro generará 50.000 entradas de datos diarias en pleno funcionamiento, con una meta de "
            "10 millones de entradas reales para fin de año. El objetivo: acelerar el aprendizaje por "
            "imitación entre modelos y convertir a China en el epicentro global de la robótica avanzada."
        ),
        "fuente_label": "WWWhatsnew — Centro entrenamiento robots humanoides Shanghái",
        "fuente_url": "https://wwwhatsnew.com/2026/05/27/centro-entrenamiento-robots-humanoides-shanghai-china-2026/",
    },
    {
        "emoji": "🧠",
        "titulo": "Zhipu AI lanza GLM-5.2: supera a GPT-5.5 a un séptimo del coste",
        "cuerpo": (
            "La empresa china Zhipu AI publicó su modelo de código abierto GLM-5.2 bajo licencia MIT, "
            "que supera a GPT-5.5 en el benchmark SWE-bench Pro con apenas una séptima parte del coste "
            "por token de salida. El lanzamiento confirma la tendencia: los modelos chinos de código "
            "abierto compiten directamente con los sistemas propietarios de OpenAI y Google, pero a un "
            "coste muy inferior para las empresas. La caída de la cuota de mercado global de ChatGPT por "
            "debajo del 50% por primera vez refleja este cambio de paradigma en la industria global de IA."
        ),
        "fuente_label": "Kersai — AI Breakthroughs June 2026",
        "fuente_url": "https://kersai.com/ai-breakthroughs-june-2026-mid-year-update/",
    },
    {
        "emoji": "💡",
        "titulo": "China anuncia el mayor plan de infraestructura IA del mundo: 295.000 millones de dólares",
        "cuerpo": (
            "El 9 de junio, el gobierno chino anunció un plan quinquenal de 295.000 millones de dólares "
            "para infraestructura de inteligencia artificial, con el objetivo de que más del 80% de la "
            "tecnología provenga de chips domésticos, reduciendo la dependencia exterior. El plan incluye "
            "centros de datos de nueva generación, redes de computación en la nube para IA y proyectos "
            "de investigación en IA aplicada a industria, salud y educación. China ya cuenta con más de "
            "602 millones de usuarios de IA generativa, más de la mitad del total mundial."
        ),
        "fuente_label": "The Quantum Insider — China Five-Year Plan AI & Quantum",
        "fuente_url": "https://thequantuminsider.com/2026/03/05/chinas-new-five-year-plan-specifically-targets-quantum-leadership-and-ai-expansion/",
    },
    {
        "emoji": "🔬",
        "titulo": "DeepSeek V4 Pro: 1,6 billones de parámetros, entrenado a un 27% del coste anterior",
        "cuerpo": (
            "DeepSeek lanzó su serie V4, incluyendo el DeepSeek-V4-Pro (1,6 billones de parámetros) y el "
            "V4-Flash (284.000 millones), ambos con ventana de contexto de 1 millón de tokens. El modelo "
            "supera a todos los sistemas de código abierto y se sitúa muy cerca de los modelos propietarios "
            "de Google y OpenAI en conocimiento del mundo y capacidades agente. El coste de entrenamiento "
            "fue un 27% del de su versión anterior, demostrando la eficiencia creciente del ecosistema "
            "chino de IA pese a las restricciones de exportación de chips occidentales."
        ),
        "fuente_label": "La Nacion PY — DeepSeek lanza nuevo modelo IA",
        "fuente_url": "https://www.lanacion.com.py/mundo/2026/04/24/china-deepseek-lanza-su-esperado-nuevo-modelo-de-ia/",
    },
    {
        "emoji": "📈",
        "titulo": "Conferencia Global de Economía Digital 2026 arranca en Pekín",
        "cuerpo": (
            "El 2 de julio, Pekín acogió el inicio de la Conferencia Global de Economía Digital 2026, "
            "con la participación de directivos de grandes corporaciones, académicos internacionales y "
            "funcionarios ministeriales de más de 20 países. El foro analiza cómo la IA, el 5G y la "
            "manufactura inteligente están redefiniendo la economía global, con China posicionándose "
            "como arquitecta del nuevo modelo económico digital. El PIB de China creció un 5% interanual "
            "en Q1 2026, superando las expectativas de los analistas, con la manufactura de alta "
            "tecnología creciendo un 12,5%."
        ),
        "fuente_label": "CGTN Español — Conferencia Economía Digital 2026",
        "fuente_url": "https://espanol.cgtn.com/",
    },
    {
        "emoji": "🌏",
        "titulo": "Premier Li Qiang: 'Los avances tecnológicos de China son una oportunidad, no una amenaza'",
        "cuerpo": (
            "El 24 de junio, el Primer Ministro Li Qiang intervino ante foros económicos internacionales "
            "para presentar el concepto de 'Oportunidad China 2.0', en contraposición a la narrativa del "
            "'China Shock'. Li subrayó que los avances en IA, robótica y vehículos eléctricos chinos "
            "benefician al mundo entero al reducir costes y acelerar la descarbonización global. Las "
            "exportaciones de circuitos integrados crecieron un 83,4% anual durante los cinco primeros "
            "meses del año, un indicador del peso creciente de China en la cadena de valor tecnológica global."
        ),
        "fuente_label": "La Jornada — Avances tecnológicos de China son una oportunidad",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/06/24/economia/avances-tecnologicos-de-china-son-una-oportunidad-no-una-amenaza-dice-el-premier-li-quiang",
    },
    {
        "emoji": "🚄",
        "titulo": "China supera los 50.000 km de trenes de alta velocidad: la red más grande del mundo",
        "cuerpo": (
            "La red ferroviaria de alta velocidad de China superó oficialmente los 50.000 kilómetros en "
            "operación, consolidándose como la mayor del planeta. Esta semana se anunció además una nueva "
            "línea que conectará 7 estaciones clave en menos de 60 minutos a velocidades de 350 km/h. "
            "Los proyectos incluyen la conexión Chengdu-Chongqing (finalización de puentes completada) y "
            "el avance del túnel submarino Shenzhen-Jiangmen, que ya supera los 113 metros de profundidad, "
            "el proyecto ferroviario submarino más ambicioso de su tipo en el mundo."
        ),
        "fuente_label": "Excélsior — China 50 mil km trenes alta velocidad",
        "fuente_url": "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico",
    },
    {
        "emoji": "⚡",
        "titulo": "8.500 robots con IA para gestionar la mayor red eléctrica del mundo",
        "cuerpo": (
            "La red eléctrica nacional china, la más grande del mundo, desplegará 8.500 robots dotados "
            "de IA durante 2026 para realizar tareas de mantenimiento en torres de alta tensión que hoy "
            "realizan trabajadores humanos. La inversión en robótica del sector eléctrico superará los "
            "10.000 millones de yuanes este año. Ant Group también anunció esta semana una inversión de "
            "73 millones de dólares en Zeroth, startup china líder en robótica humanoide, reforzando el "
            "ecosistema de inversión privada en el sector y la apuesta por la automatización inteligente."
        ),
        "fuente_label": "Voz Pópuli — China 8.500 robots IA red eléctrica",
        "fuente_url": "https://www.vozpopuli.com/indux/china-encarga-8-500-robots-con-inteligencia-artificial-para-gestionar-la-red-electrica-mas-grande-del-mundo-y-se-gastara-1-000-millones-de-dolares-solo-en-2026/2984/",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 en la base de lanzamiento: China apunta al polo sur lunar en agosto",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 —orbitador, módulo de aterrizaje, rover y sonda "
            "mini-saltadora— completaron su traslado a la Base Espacial de Wenchang para las pruebas "
            "previas al lanzamiento, previsto para agosto de 2026. La sonda mini-saltadora está diseñada "
            "para adentrarse en cráteres del polo sur lunar en sombra permanente donde se sospecha la "
            "existencia de agua en forma de hielo, un recurso clave para las futuras bases lunares. "
            "Además, la misión Tianwen-2 ya está en ruta hacia su encuentro con un asteroide y un cometa."
        ),
        "fuente_label": "Global Times — China 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🌐",
        "titulo": "Wang Yi en gira nórdica y China como sede de la APEC 2026",
        "cuerpo": (
            "El Ministro de Exteriores Wang Yi inició el 2 de julio una gira por los países nórdicos "
            "(Dinamarca, Suecia, Noruega y Finlandia) para reforzar los lazos con Europa, en un contexto "
            "de creciente interés europeo en la cooperación económica con Pekín. Air China también "
            "inauguró esta semana una nueva ruta directa Pekín-Venecia, la 40ª conexión aérea directa "
            "entre China e Italia. Como sede de la APEC 2026, China lidera el impulso a la integración "
            "económica Asia-Pacífico y la construcción de una comunidad regional de prosperidad compartida."
        ),
        "fuente_label": "Embajada China CR — Conferencia de Prensa 1 julio 2026",
        "fuente_url": "https://cr.china-embassy.gov.cn/esp/fyrth/202607/t20260702_11974023.htm",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
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
    title = "China Al Dia — Semana 28 Jun – 4 Jul 2026"
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
