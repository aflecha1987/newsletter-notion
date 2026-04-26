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
        "titulo": "DeepSeek lanza V4: 1,6 billones de parámetros y sin chips Nvidia",
        "cuerpo": (
            "El 24 de abril, DeepSeek presentó la vista previa de su modelo V4, el lanzamiento más "
            "esperado del año en IA. DeepSeek-V4-Pro cuenta con 1,6 billones de parámetros y una "
            "ventana de contexto de 1 millón de tokens —ocho veces más que la versión anterior—, "
            "reduciendo los costos de inferencia hasta 7 veces respecto a ChatGPT. El aspecto más "
            "estratégico: el modelo fue construido íntegramente sobre los chips Ascend 950 de Huawei, "
            "prescindiendo completamente de Nvidia. El lanzamiento ocurrió el mismo día en que la "
            "Casa Blanca acusó a empresas chinas de robo de modelos de IA, con DeepSeek en el foco "
            "de las acusaciones. Una demostración directa de la autosuficiencia tecnológica china."
        ),
        "fuente_label": "CNBC — DeepSeek V4 preview open-source AI competition",
        "fuente_url": "https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html",
    },
    {
        "emoji": "🚗",
        "titulo": "Auto China 2026: Pekín se convierte en la capital mundial de la inteligencia automotriz",
        "cuerpo": (
            "El salón Auto China 2026, inaugurado el 24 de abril en Pekín, ha establecido un nuevo "
            "estándar global. Con 380.000 m² de exposición, 1.451 vehículos y 181 premieres mundiales, "
            "el evento exhibe la convergencia definitiva entre movilidad eléctrica, inteligencia "
            "artificial y diseño de nueva generación. Las marcas chinas dominan la escena: BYD, BAIC, "
            "Chery y EXEED presentaron sus propuestas más avanzadas, mientras Volkswagen y Porsche "
            "aprovechan el salón para sus mayores ofensivas eléctricas. El concepto central del evento, "
            "'El Futuro de la Inteligencia', sintetiza la posición de China como laboratorio de "
            "innovación automotriz más activo del mundo."
        ),
        "fuente_label": "V12 Magazine — AUTO CHINA 2026: China redefine el futuro del auto",
        "fuente_url": "https://v12magazine.com/actualidad/mundo/auto-china-2026-innovaciones/",
    },
    {
        "emoji": "🏃",
        "titulo": "Robot humanoide bate el récord mundial de la media maratón en Pekín",
        "cuerpo": (
            "El 19 de abril, el robot humanoide Lightning, desarrollado por Honor (spin-off de Huawei), "
            "completó los 21 km de la media maratón de E-Town en Pekín en tan solo 50 minutos y 26 "
            "segundos, superando el récord mundial humano por más de 6 minutos. Honor copó los tres "
            "primeros puestos de la categoría robótica, con todos los finalistas corriendo de forma "
            "completamente autónoma, sin control remoto. Más de 100 equipos participaron este año, "
            "casi cinco veces más que en la edición inaugural de 2025, donde el ganador tardó 2 horas "
            "y 40 minutos. Un hito que marca el ritmo vertiginoso del desarrollo robótico chino."
        ),
        "fuente_label": "NPR — Humanoid robot wins Beijing half-marathon",
        "fuente_url": "https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon",
    },
    {
        "emoji": "🤖",
        "titulo": "China producirá un 94% más robots con IA en 2026: el sector vive su época dorada",
        "cuerpo": (
            "Decenas de fabricantes chinos de robótica anunciaron planes para aumentar su producción "
            "de robots con inteligencia artificial incorporada en un 94% durante 2026. El sector abarca "
            "desde robots para entornos de alto riesgo (instalaciones energéticas, tanques químicos, "
            "plataformas marinas) hasta robots de servicio para el cuidado de personas mayores. Las "
            "startups chinas de humanoides ya están enviando unidades a fábricas y centros comerciales "
            "con contratos reales, mientras sus competidoras estadounidenses siguen mayoritariamente "
            "en fase de desarrollo. TechCrunch calificó este momento como 'el madrugón del mercado "
            "robótico chino'."
        ),
        "fuente_label": "TechCrunch — Why China's humanoid robot industry is winning the early market",
        "fuente_url": "https://techcrunch.com/2026/02/28/why-chinas-humanoid-robot-industry-is-winning-the-early-market/",
    },
    {
        "emoji": "📈",
        "titulo": "La bolsa tecnológica china alcanza máximos de 11 años: el índice ChiNext se dispara",
        "cuerpo": (
            "Las acciones tecnológicas chinas cotizadas en el mercado continental están superando "
            "significativamente a sus equivalentes de Hong Kong, impulsadas por el entusiasmo inversor "
            "en torno al hardware de IA y la visibilidad de beneficios empresariales reales. El índice "
            "ChiNext casi ha duplicado su valor en el último año, alcanzando esta semana un máximo de "
            "11 años. Los analistas apuntan a que son los resultados empresariales concretos —y no solo "
            "las expectativas— los que sustentan las valoraciones, diferenciando este rally de los "
            "anteriores ciclos especulativos."
        ),
        "fuente_label": "Bloomberg — China Tech Split Emerges as ChiNext Rally Beats Hong Kong",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-23/china-tech-split-emerges-as-chinext-rally-beats-hong-kong-peer",
    },
    {
        "emoji": "💹",
        "titulo": "PIB de China crece un 5% en Q1 2026, superando expectativas",
        "cuerpo": (
            "La economía china arrancó 2026 con fuerza: el PIB creció un 5% interanual en el primer "
            "trimestre, por encima de las previsiones de los analistas. El motor principal fue la "
            "manufactura de alta tecnología, que creció un 12,5%, con robots industriales y circuitos "
            "integrados disparándose un 33% y un 24% respectivamente. El comercio exterior aumentó "
            "un 15% en el mismo período, con exportaciones de bienes creciendo un 18,3% entre enero "
            "y febrero —el primer crecimiento de doble dígito desde marzo de 2023—, reflejando la "
            "resistencia de la segunda economía del mundo pese a las turbulencias geopolíticas."
        ),
        "fuente_label": "CGTN Español — Buen desempeño económico de China en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-25/2047876215277211649/index.html",
    },
    {
        "emoji": "🛣️",
        "titulo": "La Ruta de la Seda se reinventa: los aranceles occidentales aceleran la transformación de la BRI",
        "cuerpo": (
            "Según un análisis de Foreign Policy de abril, los aranceles impuestos por Occidente están "
            "acelerando paradójicamente la transformación de la Iniciativa de la Franja y la Ruta (BRI). "
            "Lo que comenzó como un programa de infraestructuras físicas —puertos, ferrocarriles, "
            "carreteras— evoluciona hacia una extensión sofisticada de la política industrial china, "
            "con énfasis en cadenas de suministro alternativas, plataformas digitales y comercio en "
            "yuanes. Los países del Sur Global están encontrando en la BRI una palanca frente a la "
            "volatilidad de las cadenas de suministro occidentales."
        ),
        "fuente_label": "Foreign Policy — China's BRI Reinvention Accelerated By Western Tariffs",
        "fuente_url": "https://foreignpolicy.com/2026/04/03/china-belt-and-road-initiative-reinvention-trade/",
    },
    {
        "emoji": "🤝",
        "titulo": "Sánchez visita China: «el mayor nivel de interlocución política en 53 años»",
        "cuerpo": (
            "El presidente del Gobierno español Pedro Sánchez completó una visita de Estado a China "
            "que, según sus propias palabras, supone 'elevar la interlocución política con China al "
            "mayor nivel de los últimos cincuenta y tres años'. La visita incluyó reuniones con el "
            "presidente Xi Jinping y acuerdos de cooperación en energías renovables, tecnología e "
            "inversión. España se convierte en uno de los países europeos con la relación bilateral "
            "más activa con Pekín en el actual contexto geopolítico internacional."
        ),
        "fuente_label": "La Moncloa — Sánchez: máximo nivel de interlocución política con China",
        "fuente_url": "https://www.lamoncloa.gob.es/presidente/actividades/Paginas/2026/140426-sanchez-viaje-china-segunda-jornada.aspx",
    },
    {
        "emoji": "⚡",
        "titulo": "China planea doblar su energía limpia para 2035 con una inversión billonaria",
        "cuerpo": (
            "El 17 de abril, la Comisión Nacional de Desarrollo y Reforma anunció un plan para "
            "duplicar el suministro de energía no fósil de China para 2035 respecto a los niveles "
            "de 2025. El ambicioso programa incluye nuevos parques eólicos marinos, grandes plantas "
            "solares en el desierto y un macroproyecto hidroeléctrico en el Tíbet. Las dos grandes "
            "empresas estatales de la red eléctrica invertirán 1 billón de yuanes anuales "
            "(aproximadamente 146.000 millones de dólares) durante todo el 15.º Plan Quinquenal "
            "(2026-2030). State Grid ya aumentó un 50% su gasto en conexión de nuevas energías."
        ),
        "fuente_label": "Bloomberg — China Lifts Green Push With Plan to Double Clean Energy by 2035",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-17/china-lifts-green-push-with-plan-to-double-clean-energy-by-2035",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 llega a la base de lanzamiento: China apunta al polo sur lunar",
        "cuerpo": (
            "El 10 de abril todos los módulos de la misión Chang'e-7 llegaron a la Base Espacial de "
            "Wenchang para iniciar las pruebas previas al lanzamiento, previsto para agosto de 2026. "
            "La misión incluye un orbitador, un módulo de aterrizaje, un rover y una sonda mini-"
            "saltadora diseñada para explorar cráteres en sombra permanente del polo sur lunar, "
            "donde se sospecha la existencia de agua en forma de hielo. La CNSA confirmó también "
            "para este año las misiones tripuladas Shenzhou-23 y los primeros ensayos del cohete "
            "reutilizable Larga Marcha 10, pieza clave del programa lunar tripulado antes de 2030."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "💾",
        "titulo": "Semiconductores chinos baten récord histórico de ingresos impulsados por la IA",
        "cuerpo": (
            "Las empresas chinas de chips reportaron ingresos récord en el primer trimestre de 2026, "
            "impulsadas por el boom de la IA y la aceleración de la autosuficiencia tecnológica. SMIC, "
            "el mayor fabricante chino, registró 9.300 millones de dólares en ingresos en 2025 (+16%) "
            "y proyecta superar los 11.000 millones en 2026. CXMT (memoria) disparó sus ingresos un "
            "130% interanual hasta 55.000 millones de yuanes. China alcanzará el 42% de la capacidad "
            "global de producción de chips en nodos maduros (22-40nm) para 2028, frente al 37% actual."
        ),
        "fuente_label": "CNBC — Chinese chip firms hit record revenue driven by AI boom",
        "fuente_url": "https://www.cnbc.com/2026/04/03/chinese-chip-firms-record-revenue-ai-boom-us-curbs.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "El 15.º Plan Quinquenal (2026-2030): IA, 6G, robots y biotech como pilares del futuro",
        "cuerpo": (
            "El nuevo plan quinquenal chino sitúa las 'Nuevas Fuerzas Productivas de Calidad' en el "
            "centro de su estrategia de desarrollo. Los ejes son claros: IA Plus (aplicar la IA como "
            "infraestructura transversal a toda la economía), 6G, robótica, biotecnología y economía "
            "de baja altitud (drones). Las industrias emergentes suman ya casi 6 billones de yuanes "
            "y aspiran a 10 billones para 2030. El presupuesto en Ciencia y Tecnología creció un 7,1% "
            "hasta 1,3 billones de yuanes. China no solo quiere liderar estas tecnologías: quiere "
            "que sean el motor de su desarrollo económico de las próximas dos décadas."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de abril de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, diplomacia y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 20-26 Abril 2026"
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
