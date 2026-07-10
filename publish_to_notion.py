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
    # ── SEMANA 4-10 JULIO 2026 ──────────────────────────────────────────────
    {
        "emoji": "🧠",
        "titulo": "DeepSeek desarrolla su propio chip de IA para dejar de depender de NVIDIA",
        "cuerpo": (
            "La empresa china de inteligencia artificial DeepSeek, que ya sacudió a Silicon Valley a "
            "principios de 2025, está diseñando su propio chip de inferencia de IA para reducir su "
            "dependencia tanto de NVIDIA como de Huawei. El chip está orientado a la inferencia —la "
            "etapa en la que un modelo ya entrenado genera respuestas para millones de usuarios— y "
            "no al entrenamiento de nuevos modelos. Esta es una señal clara de que China avanza hacia "
            "la autosuficiencia plena en toda la cadena de valor de la inteligencia artificial. "
            "Paralelamente, las autoridades chinas estudian blindar sus modelos más avanzados ante "
            "el acceso extranjero, marcando un nuevo frente en la carrera tecnológica global."
        ),
        "fuente_label": "China en las Américas — DeepSeek desarrolla su propio chip de IA",
        "fuente_url": "https://chinalasamericas.com/2026/07/07/china-deepseek-desarrolla-su-propio-chip-de-ia-segun-fuentes/",
    },
    {
        "emoji": "🏭",
        "titulo": "Más del 30% de las grandes empresas industriales chinas ya usan IA",
        "cuerpo": (
            "Según datos del Ministerio de Industria y Tecnología de la Información de China, más del "
            "30% de las grandes empresas industriales del país han adoptado ya la inteligencia artificial "
            "en sus procesos. La cifra refleja el éxito del programa 'IA Plus' del gobierno, que tiene "
            "como meta que el 70% de la economía productiva esté integrada con IA para 2027. El XV "
            "Plan Quinquenal (2026-2030) profundiza esta apuesta, convirtiendo la transformación digital "
            "en el pilar central del desarrollo económico de la próxima década."
        ),
        "fuente_label": "teleSUR — China apuesta por un futuro digital centrado en la gente",
        "fuente_url": "https://www.telesurtv.net/ruta-a-china/ia-avanza-china-futuro-digital/",
    },
    {
        "emoji": "🤖",
        "titulo": "China exporta 10,4 millones de robots en solo 5 meses de 2026",
        "cuerpo": (
            "En los primeros cinco meses de 2026, China exportó 10,4 millones de robots por un valor "
            "de 19.990 millones de yuanes, liderados por robots de limpieza (14.000 millones de yuanes), "
            "robots industriales y robots bionómicos. Morgan Stanley elevó su previsión de envíos de "
            "robots humanoides a 50.000 unidades para este año, casi el doble de su estimación anterior, "
            "valorando el mercado chino de humanoides en 2.000 millones de dólares en 2026. Un brazo "
            "robótico que antes costaba 20.000 euros ahora puede ensamblarse por menos de 5.000 usando "
            "componentes estándar chinos, gracias a la cadena de suministro de vehículos eléctricos."
        ),
        "fuente_label": "IndexBox — China's Robot Exports Surge in First Five Months of 2026",
        "fuente_url": "https://www.indexbox.io/blog/chinas-robot-exports-surge-in-first-five-months-of-2026/",
    },
    {
        "emoji": "🏥",
        "titulo": "Conferencia Global de Economía Digital: la medicina tradicional china entra en la era de la IA",
        "cuerpo": (
            "Durante la Conferencia Global de Economía Digital 2026 celebrada en Pekín, uno de los "
            "momentos más llamativos fue la presentación de un dispositivo de diagnóstico inteligente "
            "que digitaliza la Medicina Tradicional China: analiza el rostro, la lengua y el pulso con "
            "sensores de IA multicapa, ya disponible en más de una docena de idiomas —incluyendo inglés, "
            "coreano, ruso y tailandés— y en proceso de expansión internacional. La conferencia reunió "
            "soluciones de economía digital de todo el país, reflejando cómo China combina herencia "
            "milenaria con tecnología de vanguardia."
        ),
        "fuente_label": "CRI Español — Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cri.cn/2026/07/02/ARTI1782972617748340",
    },
    {
        "emoji": "🚁",
        "titulo": "Nuevas normas para drones en vigor: China regula la economía de baja altitud",
        "cuerpo": (
            "Las normas de aviación revisadas entraron en vigor en julio de 2026, exigiendo que el "
            "diseño, la fabricación y las operaciones de drones obtengan certificación de la CAAC "
            "(Administración de Aviación Civil de China), con identificación electrónica obligatoria. "
            "El marco regulatorio formaliza el acceso al mercado de la 'economía de baja altitud' —uno "
            "de los sectores prioritarios del 15.º Plan Quinquenal—, mejorando la seguridad y preparando "
            "el terreno para la masificación de drones comerciales, logísticos y de transporte de personas."
        ),
        "fuente_label": "Observatorio de Política China — Política Exterior Jul 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-65/",
    },
    {
        "emoji": "📈",
        "titulo": "Banco Mundial: China mantiene resiliencia con crecimiento del 4,4% proyectado",
        "cuerpo": (
            "El Banco Mundial confirmó en su China Economic Update de julio de 2026 que la economía "
            "del país se mantuvo resiliente en la primera mitad del año, impulsada por la inversión "
            "en alta tecnología y las exportaciones. Se proyecta un crecimiento del 4,4% para 2026 "
            "y del 4,3% para 2027, con la manufactura de alta tecnología —robots industriales, "
            "circuitos integrados, vehículos eléctricos— como principal motor. Los sectores de "
            "semiconductores y equipos electrónicos registran crecimientos de doble dígito."
        ),
        "fuente_label": "Banco Mundial — China Economic Update, July 2026",
        "fuente_url": "https://www.worldbank.org/en/news/press-release/2026/07/07/rebalancing-growth-china-economic-update",
    },
    {
        "emoji": "💰",
        "titulo": "Superávit comercial histórico: 1,2 billones de dólares y expansión global de la Franja y la Ruta",
        "cuerpo": (
            "China cerró 2025 con un superávit comercial de mercancías de 1,2 billones de dólares, "
            "el mayor de su historia, con un comercio exterior total de 6,5 billones de dólares. "
            "En 2026, las empresas chinas continúan su expansión internacional mediante adquisiciones "
            "y proyectos de infraestructura vinculados a la Franja y la Ruta. El Ferrocarril "
            "China-Kirguistán-Uzbekistán (4.700 millones de dólares), aprobado como proyecto emblema "
            "de la BRI, conectará Asia Central con Europa en una ruta más corta y económica que las "
            "actuales, consolidando la proyección global de China."
        ),
        "fuente_label": "Mas Container — China transforma su superávit en capital privado global",
        "fuente_url": "https://mascontainer.com/china-transforma-su-superavit-record-en-capital-privado-hacia-los-mercados-globales/",
    },
    {
        "emoji": "🤝",
        "titulo": "China y la UE reactivan su mecanismo de consultas comerciales para el otoño",
        "cuerpo": (
            "El Ministerio de Comercio de China anunció esta semana que China y la Unión Europea "
            "celebrarán la segunda reunión de su mecanismo permanente de consultas sobre comercio "
            "e inversión durante el otoño de 2026. Este canal de diálogo, creado en 2025 para "
            "gestionar las fricciones comerciales bilaterales, cobra mayor relevancia en un contexto "
            "en que el comercio Chino-UE superó los 850.000 millones de euros en 2025. Camboya "
            "también expresó su interés en ampliar la cooperación con China en comercio, inversión "
            "e infraestructura."
        ),
        "fuente_label": "Observatorio de Política China — Resumen Política Exterior",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-65/",
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e-7 en cuenta atrás: China apunta al polo sur de la Luna en agosto",
        "cuerpo": (
            "La misión lunar Chang'e-7 tiene previsto su lanzamiento para agosto de 2026 desde la "
            "Base Espacial de Wenchang. La misión incluye un orbitador, un módulo de aterrizaje, "
            "un rover y una mini-sonda saltadora diseñada para explorar cráteres en sombra permanente "
            "del polo sur lunar, donde se sospecha la existencia de agua en forma de hielo. En "
            "paralelo, la sonda Tianwen-2 se acerca a su objetivo en el cinturón de asteroides y los "
            "astronautas de Shenzhou-23 continúan sus experimentos a bordo de la estación Tiangong, "
            "incluyendo un 'hospital espacial' con chips neuroinspired desarrollados íntegramente en China."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "🌟",
        "titulo": "Astrónomos chinos detectan pulsos de radio de una estrella de neutrones dormida",
        "cuerpo": (
            "Astrónomos chinos han detectado pulsos de radio inesperados provenientes de una estrella "
            "de neutrones que llevaba años sin actividad, un hallazgo que abre nuevas ventanas para "
            "entender la física de los objetos más densos del universo. Además, China lanzó un nuevo "
            "satélite marino para el monitoreo oceánico y ambiental, y científicos chinos publicaron "
            "resultados que adelantan el origen conocido de las células sanguíneas humanas, con "
            "potenciales aplicaciones en medicina regenerativa y tratamiento de enfermedades hematológicas."
        ),
        "fuente_label": "South China Morning Post — China Science",
        "fuente_url": "https://www.scmp.com/topics/china-science",
    },
    {
        "emoji": "⚡",
        "titulo": "China lidera la transición energética global: perovskita, baterías y 1 billón de yuanes al año",
        "cuerpo": (
            "China se consolida como líder mundial en energías renovables en 2026. Las claves de su "
            "ventaja competitiva son las células solares de perovskita —con eficiencias que ya superan "
            "el 30%— y los avances en almacenamiento energético mediante baterías de estado sólido y "
            "bombeo hidráulico. El XV Plan Quinquenal destina 1 billón de yuanes anuales para conectar "
            "nuevas fuentes renovables a la red eléctrica, y State Grid aumentó un 50% su gasto en "
            "este rubro solo en el primer trimestre. China instala cada semana más energía solar que "
            "muchos países en todo un año."
        ),
        "fuente_label": "Ambientum — Estrategia Energética de China: Liderazgo y Renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
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
    title = "China Al Dia — Semana 4-10 Julio 2026"
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
