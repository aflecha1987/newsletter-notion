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
        "emoji": "🏗️",
        "titulo": "China prepara una inversión de $295.000 millones en centros de datos de IA",
        "cuerpo": (
            "Pekín está ultimando un plan para construir una red nacional interconectada de centros de datos "
            "de inteligencia artificial con una inversión de 2 billones de yuanes (~295.000 millones de dólares) "
            "a lo largo de cinco años. El plan, elaborado por la Comisión Nacional de Desarrollo y Reforma, "
            "establece que al menos el 80% de la tecnología —chips de IA incluidos— provenga de fabricantes "
            "nacionales como Huawei, reduciendo drásticamente la dependencia de Nvidia. El objetivo es conectar "
            "todas las instalaciones en una red cohesionada antes de 2028. Si se suman las mejoras en la red "
            "eléctrica necesarias, el capital total requerido podría superar los 5 billones de yuanes."
        ),
        "fuente_label": "Bloomberg — China Prepares $295 Billion Plan to Fund Nationwide AI Buildout",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-09/china-prepares-295-billion-plan-to-fund-nationwide-ai-buildout",
    },
    {
        "emoji": "🚀",
        "titulo": "Larga Marcha 12B: vuelo inaugural sorpresa con satélites Qianfan a bordo",
        "cuerpo": (
            "El 1 de junio, China lanzó sin previo aviso el cohete Larga Marcha 12B desde el desierto de Gobi. "
            "El vehículo —con 72 metros de altura, capacidad de 20 toneladas a órbita baja y nueve motores "
            "YF-102R en la primera etapa— puso en órbita dos nuevos satélites de la megaconstelación Qianfan "
            "(Mil Velas) en su vuelo de debut. El cohete incorpora 'doble inteligencia' de toma de decisiones "
            "en vuelo y mejoras estructurales para reducir peso. El recorrido desde el concepto hasta el primer "
            "vuelo tomó apenas 21 meses. El cohete está diseñado para ser reutilizable, aunque la recuperación "
            "del propulsor se realizará en misiones posteriores."
        ),
        "fuente_label": "SpaceNews — China conducts surprise launch of Long March 12B",
        "fuente_url": "https://spacenews.com/china-conducts-surprise-launch-of-long-march-12b-delivers-qianfan-satellites-on-debut-flight/",
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e-7 confirmada para agosto: rumbo al polo sur lunar en busca de agua",
        "cuerpo": (
            "La misión Chang'e-7 está en recta final de preparativos en la Base Espacial de Wenchang, con "
            "lanzamiento confirmado para agosto de 2026. La misión incluye un orbitador, un módulo de "
            "aterrizaje, un rover y una revolucionaria mini-sonda saltadora diseñada para explorar cráteres "
            "en sombra permanente del polo sur lunar, donde se sospecha la existencia de hielo de agua. "
            "China tiene previsto evaluar el sitio como candidato para una futura base de investigación lunar "
            "permanente. El programa espacial chino encadena un año de récord: Tianwen-2 rumbo a su asteroide, "
            "Shenzhou-23 y Shenzhou-24 tripuladas, y los primeros ensayos del cohete reutilizable Larga "
            "Marcha 10."
        ),
        "fuente_label": "Xinhua — Update: China to launch Chang'e-7 lunar probe in second half of 2026",
        "fuente_url": "https://english.news.cn/20260410/259404a56762458fb68126d26a2b2672/c.html",
    },
    {
        "emoji": "🤖",
        "titulo": "China abre la primera 'escuela para robots humanoides' del mundo en Shanghái",
        "cuerpo": (
            "El National and Local Co-built Humanoid Robotics Innovation Center de Shanghái inauguró en julio "
            "el primer centro de entrenamiento heterogéneo de robots humanoides del mundo, en el distrito de "
            "alta tecnología de Zhangjiang. El espacio de más de 5.000 m² acoge simultáneamente a más de "
            "100 modelos distintos de robots de más de una docena de empresas. El programa inicial los entrena "
            "en 10 tareas clave: desde doblar ropa y ordenar estantes hasta limpiar equipos industriales y "
            "atender en entornos de turismo. El centro generará alrededor de 50.000 datos al día —10 millones "
            "al año— para acelerar el aprendizaje colectivo de los humanoides chinos."
        ),
        "fuente_label": "New Atlas — China opens first robot training school for humanoids",
        "fuente_url": "https://newatlas.com/ai-humanoids/first-humanoid-training-academy/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD se lanza a la robótica humanoide: el fabricante de VE más grande del mundo da el salto",
        "cuerpo": (
            "BYD, el mayor fabricante de vehículos eléctricos del mundo, anunció oficialmente en junio que "
            "desarrolla sus propios robots humanoides. El vicepresidente ejecutivo Li Ke confirmó que la "
            "iniciativa aprovechará tecnologías que la compañía ya domina en sus automóviles: motores "
            "eléctricos de alta eficiencia, baterías, sensórica y sistemas de control. BYD colabora "
            "simultáneamente con AgiBot y UBTech, dos de las empresas de robótica china más avanzadas. "
            "Al igual que Tesla con Optimus, BYD ve los humanoides como clave para revolucionar la "
            "eficiencia de su fabricación a escala masiva."
        ),
        "fuente_label": "Emol — BYD desafía a Tesla: trabaja para desarrollar robots humanoides",
        "fuente_url": "https://www.emol.com/noticias/Autos/2026/06/09/1202308/byd-desarrollo-robots-humanoides.html",
    },
    {
        "emoji": "📡",
        "titulo": "Plan trienal de IA: integrar la inteligencia artificial en toda la red de comunicaciones para 2028",
        "cuerpo": (
            "El Ministerio de Industria y Tecnología de la Información publicó en junio un plan trienal para "
            "acelerar la integración de la IA en el sector de las telecomunicaciones y comunicaciones de China. "
            "El plan establece objetivos concretos: redes más autónomas, mayor cobertura de computación de "
            "baja latencia en el borde de la red y expansión masiva de aplicaciones de IA para 2028. Es parte "
            "de la estrategia IA Plus del 15.º Plan Quinquenal, que busca convertir la IA en infraestructura "
            "transversal de toda la economía nacional."
        ),
        "fuente_label": "Gov.cn — China issues three-year plan to boost AI integration with ICT sector",
        "fuente_url": "https://english.www.gov.cn/news/202606/10/content_WS6a296017c6d00ca5f9a0b876.html",
    },
    {
        "emoji": "⚡",
        "titulo": "China publica su plan de energía limpia 2026-2030: energía no fósil al 25% para 2030",
        "cuerpo": (
            "El 25 de junio, la Comisión Nacional de Desarrollo y Reforma y la Administración Nacional de "
            "Energía publicaron el Plan del Sistema de Nueva Energía del 15.º Plan Quinquenal. Las metas "
            "para 2030 son ambiciosas: la energía no fósil representará el 25% del consumo energético total "
            "y la eólica y solar sumarán más del 50% de la capacidad instalada de generación eléctrica. "
            "Para esa fecha, la energía no fósil debe contribuir el 50% de la electricidad generada, "
            "convirtiéndose en la principal fuente de electricidad del país. China también establece como "
            "objetivo que las tecnologías y equipos clave de la cadena energética sean en gran medida "
            "autosuficientes y estén bajo control nacional."
        ),
        "fuente_label": "Gov.cn / Xinhua — China targets clean, low-carbon new energy system by 2030",
        "fuente_url": "https://english.www.gov.cn/news/202606/25/content_WS6a3d2904c6d00ca5f9a0bcde.html",
    },
    {
        "emoji": "☀️",
        "titulo": "Energía solar espacial: China transmite 1.180 W de forma inalámbrica a 100 metros",
        "cuerpo": (
            "El proyecto Sun Chasing de China alcanzó un nuevo hito: el sistema de transmisión inalámbrica "
            "de energía desarrollado por investigadores chinos logró enviar 1.180 vatios de potencia a más "
            "de 100 metros de distancia, con una eficiencia de corriente continua a corriente continua del "
            "20,8%. En una demostración adicional, un dron volando a 30 km/h recibió 143 vatios de energía "
            "estable desde 30 metros de altitud. Una alianza de 13 empresas y centros de investigación "
            "—incluyendo GCL Technology y Trina Solar— fue lanzada para impulsar la energía solar espacial "
            "como nuevo motor de crecimiento del sector fotovoltaico chino."
        ),
        "fuente_label": "PV Magazine — China conducts first experiments for space-based solar power plants",
        "fuente_url": "https://www.pv-magazine.com/2026/05/20/china-conducts-first-experiments-for-space-based-solar-power-plants/",
    },
    {
        "emoji": "📈",
        "titulo": "La economía china mantiene el rumbo: crecimiento del 4,5-5% en 2026",
        "cuerpo": (
            "El último informe de BBVA Research de junio mantiene la previsión de crecimiento del PIB chino "
            "en 4,5% para 2026, alineada con el objetivo gubernamental de 4,5-5%. El motor principal sigue "
            "siendo la manufactura de alta tecnología —robots industriales, semiconductores y vehículos "
            "eléctricos—, mientras el consumo interno muestra señales de recuperación gradual. El viceprimer "
            "ministro He Lifeng instó a acelerar la modernización de sectores clave equilibrando desarrollo "
            "y seguridad. China trabaja en nuevas políticas de estímulo al consumo doméstico dentro del "
            "marco del 15.º Plan Quinquenal, que busca reequilibrar su economía hacia un modelo más "
            "orientado a la demanda interna."
        ),
        "fuente_label": "BBVA Research — China Economic Outlook June 2026",
        "fuente_url": "https://www.bbvaresearch.com/en/publicaciones/china-economic-outlook-june-2026/",
    },
]


def build_blocks():
    today = "1 de julio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, espacio, economia y energia.", bold=False),
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
    title = "China Al Dia — Semana 24 Jun - 1 Jul 2026"
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
