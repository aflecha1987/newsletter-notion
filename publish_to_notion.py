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
        "titulo": "DeepSeek lanza V4 hoy: el modelo de IA más potente de China con 1,6 billones de parámetros",
        "cuerpo": (
            "Hoy 24 de abril, DeepSeek ha lanzado oficialmente DeepSeek-V4, su modelo de inteligencia "
            "artificial más avanzado, más de un año después de haber sacudido al mundo con R1. La versión "
            "Pro cuenta con 1,6 billones de parámetros y un contexto de un millón de palabras; la versión "
            "Flash ofrece 284.000 millones de parámetros para uso más ligero. En benchmarks de conocimiento "
            "mundial, V4-Pro lidera de forma significativa todos los modelos de código abierto y solo es "
            "ligeramente superado por Gemini-Pro-3.1 de Google. El modelo está optimizado para herramientas "
            "de programación como Claude Code y CodeBuddy. Huawei confirmó que sus chips Ascend AI soportan "
            "completamente el nuevo modelo, consolidando el ecosistema de hardware chino independiente."
        ),
        "fuente_label": "CNBC — DeepSeek V4 release: open-source AI competition China",
        "fuente_url": "https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Día del Espacio de China 2026: Chang'e-7, fábrica orbital y misiones intensivas",
        "cuerpo": (
            "El 24 de abril se celebra el 11.º Día del Espacio de China en Chengdu. La CNSA confirmó "
            "un calendario sin precedentes: Chang'e-7 ya está en la Base de Wenchang para el lanzamiento "
            "previsto en agosto (explorará el polo sur lunar buscando hielo); la misión tripulada "
            "Shenzhou-23; el acercamiento de Tianwen-2 a su asteroide; y ensayos del cohete reutilizable "
            "Larga Marcha 10. En paralelo, China diseña un módulo inflable para convertir la estación "
            "Tiangong en una fábrica orbital capaz de producir materiales imposibles de fabricar en la "
            "Tierra. En 2025 China realizó 92 lanzamientos espaciales, un 35% más que en 2024."
        ),
        "fuente_label": "Xinhua — China llevará a cabo misiones espaciales intensivas en 2026",
        "fuente_url": "https://spanish.news.cn/20260418/dcdfd28416bd4044867e2f84cf6e9842/c.html",
    },
    {
        "emoji": "⚡",
        "titulo": "Energía renovable china supera al carbón: récord de 1.840 GW de capacidad limpia",
        "cuerpo": (
            "A finales de 2025, la capacidad acumulada de energía eólica y solar en China superó los "
            "1.840 GW, siendo por primera vez mayor que la del carbón y el gas en el mix eléctrico chino. "
            "En el Q1 2026 la generación limpia alcanzó 0,7 billones de kWh (+2,8% interanual). Hay "
            "448 GW de nueva capacidad renovable en construcción —la mitad del total mundial en esa fase—. "
            "China ya planifica doblar su energía no fósil para 2035, con una inversión de 1 billón de "
            "yuanes anuales en la red eléctrica durante el 15.º Plan Quinquenal (2026-2030)."
        ),
        "fuente_label": "Spanish.china.org.cn — Sector energético chino en Q1 2026",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-04/22/content_118456847.htm",
    },
    {
        "emoji": "🌍",
        "titulo": "Modelos chinos de IA dominan los países en desarrollo: a una décima parte del costo",
        "cuerpo": (
            "Según un informe de Microsoft, los modelos de IA chinos —encabezados por DeepSeek— están "
            "ganando terreno acelerado en los países en desarrollo, donde ofrecen un rendimiento comparable "
            "a las alternativas de EE.UU. a una décima parte del costo. La industria central de IA de "
            "China superó el billón de yuanes en valor en 2025, con 602 millones de usuarios de IA "
            "generativa (más de la mitad de los usuarios globales). China presentó además avances en "
            "RISC-V con la plataforma Xiangshan y el sistema operativo Ruyi, primer OS nativo compatible "
            "con el estándar internacional RVA23 de alto desempeño."
        ),
        "fuente_label": "Cubadebate — Modelos gigantes chinos de IA logran uso global generalizado",
        "fuente_url": "http://www.cubadebate.cu/especiales/2026/04/22/modelos-gigantes-chinos-de-ia-logran-uso-global-generalizado/",
    },
    {
        "emoji": "🏃",
        "titulo": "Robot humanoide bate el récord mundial de la media maratón en Pekín",
        "cuerpo": (
            "El 19 de abril, el robot humanoide Lightning, desarrollado por Honor (spin-off de Huawei), "
            "completó los 21 km de la media maratón de E-Town en Pekín en 50 minutos y 26 segundos, "
            "superando el récord mundial humano por más de 6 minutos. Honor copó los tres primeros puestos "
            "de la categoría robótica; todos los finalistas corrieron de forma autónoma, sin control remoto. "
            "Más de 100 equipos participaron este año, casi cinco veces más que en la edición inaugural "
            "de 2025. China producirá un 94% más robots con IA en 2026, con startups de humanoides ya "
            "enviando unidades a fábricas y centros comerciales con contratos reales."
        ),
        "fuente_label": "NPR — Humanoid robot wins Beijing half-marathon",
        "fuente_url": "https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon",
    },
    {
        "emoji": "📈",
        "titulo": "PIB +5% en Q1 2026: manufactura de alta tecnología y chips lideran el crecimiento",
        "cuerpo": (
            "La economía china creció un 5% interanual en el primer trimestre de 2026, superando las "
            "previsiones. La manufactura de alta tecnología creció un 12,5%, con robots industriales "
            "+33% y circuitos integrados +24%. El comercio exterior aumentó un 15%, con exportaciones "
            "de bienes creciendo un 18,3% entre enero y febrero —primer doble dígito desde marzo 2023—. "
            "Las empresas de chips registraron ingresos récord: SMIC proyecta superar $11.000 millones "
            "en 2026 y CXMT creció un 130% interanual hasta 55.000 millones de yuanes. China alcanzará "
            "el 42% de la capacidad global de chips en nodos maduros para 2028."
        ),
        "fuente_label": "CGTN Español — Comercio exterior de China aumenta 15% en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-15/2044294393639481345/index.html",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de vehículos eléctricos chinos baten récord histórico: +140%",
        "cuerpo": (
            "Las exportaciones chinas de vehículos eléctricos e híbridos se dispararon un 140% interanual "
            "en marzo de 2026, alcanzando 349.000 unidades, el máximo histórico. El catalizador fue el "
            "shock del precio del petróleo por tensiones en el Estrecho de Ormuz, que aceleró el paso "
            "al eléctrico en Asia-Pacífico, Europa y América. BYD lidera las exportaciones, seguida de "
            "Geely y Chery. BYD apunta a 1,5 millones de ventas en el exterior en 2026, un 15% más "
            "de su objetivo anterior."
        ),
        "fuente_label": "Bloomberg — China's EV Exports Jump to Record",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-09/china-ev-exports-jump-to-record-as-iran-oil-shock-entices-buyers",
    },
    {
        "emoji": "🏗️",
        "titulo": "Puerto de Chancay (Perú): la Franja y la Ruta transforma el comercio latinoamericano",
        "cuerpo": (
            "El Puerto de Chancay en Perú, con una inversión china de entre 3.500 y 4.000 millones de "
            "dólares, avanza en su expansión y prevé una nueva etapa a partir de 2027. El proyecto "
            "reduce los tiempos de tránsito de América del Sur a Asia de 35 a 23 días, desbancando la "
            "ruta tradicional por el Canal de Panamá. Es el emblema de la Iniciativa de la Franja y "
            "la Ruta en América Latina, que en 10 años ha canalizado más de 1,5 billones de dólares "
            "en infraestructura en más de 150 países."
        ),
        "fuente_label": "Canal 26 — País sudamericano apuesta a China para transformar comercio del Pacífico",
        "fuente_url": "https://www.canal26.com/internacionales/2026/04/23/el-pais-sudamericano-que-apuesta-a-china-para-transformar-el-comercio-del-pacifico-desde-2027/",
    },
    {
        "emoji": "🏥",
        "titulo": "IA y medicina tradicional china: quioscos de diagnóstico inteligente en el metro",
        "cuerpo": (
            "China despliega quioscos de diagnóstico asistido por IA en estaciones de metro, combinando "
            "tecnología biomédica con la Medicina Tradicional China. Estos dispositivos miden presión "
            "arterial, frecuencia cardíaca, saturación de oxígeno y temperatura, mientras la IA aplica "
            "análisis facial, observación de la lengua e interpretación del pulso mediante sensores de "
            "presión multicapa. La Comisión Nacional de Salud promueve la integración de IA en los "
            "servicios médicos como parte de la estrategia de salud digital nacional."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional China",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
    {
        "emoji": "🗺️",
        "titulo": "15.º Plan Quinquenal (2026-2030): IA, 6G, robots y biotech como pilares del futuro",
        "cuerpo": (
            "El nuevo plan quinquenal sitúa las Nuevas Fuerzas Productivas de Calidad en el centro de "
            "la estrategia nacional. Los ejes: IA Plus (el 70% de la economía integrada con IA para "
            "2027; el 90% para 2030), 6G, robótica, biotecnología y drones. Las industrias emergentes "
            "suman casi 6 billones de yuanes y aspiran a 10 billones en 2030. El presupuesto en Ciencia "
            "y Tecnología creció un 7,1% hasta 1,3 billones de yuanes. El gasto en I+D se elevará "
            "al menos un 7% anual y la economía digital central alcanzará el 12,5% del PIB para 2030."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de abril de %Y")
    blocks = [
        callout(f"Newsletter diaria · China Al Dia · {today} · Dia del Espacio de China", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China hoy: DeepSeek V4, espacio, energia renovable, economia e IA.", bold=False),
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
    title = "China Al Dia — 24 Abril 2026 · DeepSeek V4 + Dia del Espacio"
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
