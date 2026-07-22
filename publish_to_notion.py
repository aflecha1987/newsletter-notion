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
        "titulo": "Conferencia Mundial de IA en Shanghai: Xi Jinping lidera el llamado a la cooperación global",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghai acogió la Conferencia Mundial de Inteligencia Artificial (WAIC 2026) "
            "con más de 1.100 empresas participantes y 3.000 productos en exposición, la mayor edición de su historia. "
            "El presidente Xi Jinping instó a la cooperación internacional y advirtió que la IA no debe estar "
            "dominada por ningún país. China anunció la creación de una nueva organización global de IA con sede "
            "en Shanghai, firmada por 29 países (Rusia, Indonesia, Pakistán, Kazajistán, Laos, entre otros), "
            "y aportará 5.000 plazas en programas de intercambio en los próximos 5 años, con centros de cooperación "
            "en la ASEAN, la Liga Árabe, la Unión Africana, CELAC, los BRICS y la OCS."
        ),
        "fuente_label": "El Imparcial — China presenta plan global de IA en Shanghai",
        "fuente_url": "https://www.elimparcial.com/mundo/2026/07/17/china-presenta-plan-global-de-inteligencia-artificial-para-reducir-la-brecha-digital-y-crea-con-29-paises-una-organizacion-con-sede-en-shanghai/",
    },
    {
        "emoji": "🦾",
        "titulo": "China lidera el desarrollo mundial de robots humanoides: 70% de las ventas globales",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de China confirmó el 20 de julio que el país cuenta con más de "
            "400 modelos completos de robots humanoides y cuadrúpedos, representando el 70% de las ventas mundiales "
            "en el primer semestre de 2026. En julio abrió en Shanghai el primer centro de entrenamiento heterogéneo "
            "de robots humanoides del mundo: 5.000 m², más de 100 tipos de robots de más de una docena de empresas "
            "generando 50.000 datos diarios. Robots AgiBot Genie G2 trabajaron 6 días consecutivos en una línea de "
            "producción real realizando 64.828 tareas con una tasa de éxito del 99,99%. Xpeng planea producir más "
            "de 1.000 robots al mes a finales de 2026 y comenzar entregas comerciales de su robot Iron en 2027."
        ),
        "fuente_label": "Xinhua Español — China lidera desarrollo global de robots humanoides",
        "fuente_url": "http://spanish.xinhuanet.com/20260720/edcafb7f97f24238b185c57fc34de8fe/c.html",
    },
    {
        "emoji": "💾",
        "titulo": "Huawei dobla chips Ascend y China exporta semiconductores por valor récord de 177.000 M$",
        "cuerpo": (
            "China exportó 179.440 millones de circuitos integrados por un valor superior a los 177.000 millones "
            "de dólares en el primer semestre de 2026, con un incremento del 96% interanual. Huawei planea producir "
            "unas 600.000 unidades de su chip Ascend 910C en 2026, duplicando el nivel anterior, con producción "
            "total de la línea Ascend de hasta 1,6 millones de dies. Las exportaciones de servidores y equipos de "
            "memoria crecieron un 41,3% hasta más de 138.000 millones de dólares. Las sanciones de EE.UU. están "
            "acelerando la autosuficiencia tecnológica china, con un grupo de empresas lideradas por Huawei "
            "apuntando a fabricar chips HBM para IA de forma completamente doméstica."
        ),
        "fuente_label": "Gulf News — Huawei to double output of AI chip as Nvidia wavers in China",
        "fuente_url": "https://gulfnews.com/technology/huawei-to-double-output-of-top-ai-chip-as-nvidia-wavers-in-china-1.500287469",
    },
    {
        "emoji": "🚗",
        "titulo": "China exporta más coches en un mes que en todo 2019: primer millón mensual de vehículos",
        "cuerpo": (
            "Las exportaciones de automóviles de China superaron por primera vez el millón de unidades en junio de 2026, "
            "frente a los menos de 700.000 coches que exportó en todo el año 2019. BYD lideró el crecimiento con un "
            "aumento del 94,7% interanual, con las ventas internacionales representando ya el 43,5% de su volumen "
            "mensual total. En el primer semestre, las exportaciones de automóviles chinos superaron los 4,4 millones "
            "de unidades. La CAAM proyecta superar los 10 millones de vehículos exportados en el total de 2026, "
            "consolidando a China como el mayor exportador de coches del mundo. La escasez de buques ro-ro ha "
            "llevado a la industria a innovar apilando vehículos en barcos convencionales con éxito."
        ),
        "fuente_label": "Motor16 — Exportaciones de coches chinos en 2026 baten récords",
        "fuente_url": "https://www.motor16.com/las-ultimas-noticias/exportaciones-coches-chinos-2026-record/",
    },
    {
        "emoji": "⚡",
        "titulo": "Hito histórico: la energía solar supera al carbón en China por primera vez",
        "cuerpo": (
            "En 2026, China alcanza un hito energético sin precedentes: la capacidad instalada de energía solar "
            "supera por primera vez a la del carbón. La nueva capacidad instalada de energías renovables superará "
            "los 300 GW este año, y la eólica y la solar representarán conjuntamente la mitad de la capacidad "
            "total de generación eléctrica del país. La capacidad eléctrica total de China ya superó los "
            "4.000 millones de kilovatios en el segundo trimestre. Este avance se alinea con el objetivo de "
            "doble carbono: emisiones máximas antes de 2030 y neutralidad climática antes de 2060, y sitúa "
            "a China como el mayor inversor y productor de energías renovables del planeta."
        ),
        "fuente_label": "CGTN Español — La capacidad de energía solar de China superará al carbón",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-29/2049332090556919810/index.html",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 lista para el polo sur lunar: el cohete Larga Marcha-5 llega a Wenchang",
        "cuerpo": (
            "El cohete Larga Marcha-5 Y14 llegó al Centro Espacial de Wenchang para iniciar el ensamblaje final "
            "y las pruebas previas al lanzamiento de la misión Chang'e-7, previsto para la segunda mitad de 2026. "
            "La misión incluirá un orbitador, un satélite repetidor, un módulo de aterrizaje, un rover y una "
            "mini sonda saltadora diseñada para explorar cráteres en sombra permanente del polo sur lunar, donde "
            "se sospecha la presencia de hielo de agua. Chang'e-7 es un paso clave en el programa chino de "
            "exploración lunar no tripulada, preparando el terreno para una misión tripulada antes de 2030."
        ),
        "fuente_label": "OKDiario — China en la Luna 2026: misiones, logros y objetivos espaciales",
        "fuente_url": "https://okdiario.com/ciencia/china-luna-2026-misiones-logros-objetivos-16568199",
    },
    {
        "emoji": "📈",
        "titulo": "PIB China Q2 2026: crecimiento del 4,3% en un entorno global complejo",
        "cuerpo": (
            "La economía china creció un 4,3% interanual en el segundo trimestre de 2026, por debajo del 5% "
            "del primer trimestre y del objetivo oficial de 4,5%-5%, condicionado por la guerra en Irán, "
            "la debilidad de la demanda interna y menores niveles de inversión, aunque el dinamismo exportador "
            "compensó parte del impacto. El Banco Mundial subraya la necesidad de un reequilibrio hacia el "
            "consumo interno como motor de crecimiento sostenible. El consenso de analistas de Morgan Stanley, "
            "Goldman Sachs y ANZ sitúa el crecimiento anual de China en 2026 en torno al 4,5-4,6%."
        ),
        "fuente_label": "Bloomberg — Economía de China queda bajo el objetivo de crecimiento",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-07-15/economia-de-china-queda-bajo-el-objetivo-de-crecimiento",
    },
    {
        "emoji": "🔒",
        "titulo": "China estudia nuevos controles a la exportación de IA y chips para proteger su ventaja tecnológica",
        "cuerpo": (
            "Según el Financial Times, China estudia reforzar las restricciones a la exportación de tecnologías "
            "de inteligencia artificial y chips avanzados, en una medida destinada a proteger el desarrollo local "
            "de sectores estratégicos y evitar que sus avances sean utilizados en su contra. La medida sería la "
            "respuesta espejo a las restricciones de exportación que EE.UU. aplica sobre China, y supondría un "
            "nuevo capítulo en la reconfiguración del orden tecnológico global. China ya aprobó durante la semana "
            "el plan maestro de IA 2026 con inversión récord y control tecnológico total como eje central."
        ),
        "fuente_label": "Infoarenales — China evalúa endurecer controles a exportación de IA y chips",
        "fuente_url": "https://infoarenales.com/2026/07/21/china-evalua-endurecer-los-controles-a-la-exportacion-de-modelos-de-ia-y-chips-segun-el-financial-times/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: inteligencia artificial, robotica, energia, espacio y economia.", bold=False),
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
    title = "China Al Dia — Semana 14-22 Julio 2026"
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
