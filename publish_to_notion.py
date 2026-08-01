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
        "titulo": "China supera los 100.000 robots humanoides producidos en 2026",
        "cuerpo": (
            "La producción de robots humanoides en China superará las 100.000 unidades en 2026, según "
            "cifras presentadas en la Conferencia Mundial de Inteligencia Artificial (WAIC 2026) celebrada "
            "en Shanghái del 17 al 20 de julio. Con más de 400 modelos de robots humanoides y cuadrúpedos, "
            "China representa ya aproximadamente el 70% de las ventas globales del sector. El Ministerio "
            "de Industria y Tecnología de la Información prevé instalar 10.000 robots en fábricas antes de "
            "que acabe el año. Las startups chinas de robótica ya firman contratos reales con fábricas y "
            "centros comerciales, mientras sus rivales globales siguen mayoritariamente en fase de prototipo."
        ),
        "fuente_label": "CGTN — China's output of humanoid robots set to exceed 100,000 in 2026",
        "fuente_url": "https://news.cgtn.com/news/2026-07-08/China-s-output-of-humanoid-robots-set-to-exceed-100-000-in-2026-1OBFKOQ9WUg/p.html",
    },
    {
        "emoji": "🧠",
        "titulo": "WAIC 2026: robot centauro y primeras licencias de IA generativa para humanoides",
        "cuerpo": (
            "La Conferencia Mundial de IA 2026 (WAIC) reunió del 17 al 20 de julio en Shanghái a líderes "
            "globales del sector. El Centro de Innovación de Robots Humanoides de Pekín obtuvo las primeras "
            "licencias de IA generativa del mundo específicamente diseñadas para robots humanoides, tras "
            "superar con éxito los controles regulatorios chinos. Además, Run Robotics presentó un robot "
            "centauro que combina un chasis todoterreno de cuatro ruedas con un cuerpo humanoide completo "
            "en la parte superior, abriendo nuevas aplicaciones en logística industrial y entornos hostiles."
        ),
        "fuente_label": "CGTN — Tech innovation unlocks new growth momentum for China's economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-16/Tech-innovation-unlocks-new-growth-momentum-for-China-s-economy-1OOMQp36DmM/share_amp.html",
    },
    {
        "emoji": "🌐",
        "titulo": "China propone ante la ONU un marco global de gobernanza de la IA",
        "cuerpo": (
            "China presentó ante las Naciones Unidas un documento de posición sobre gobernanza global "
            "de la inteligencia artificial en el que defiende la igualdad soberana de los países, el "
            "multilateralismo y el desarrollo inclusivo de la IA. La propuesta incluye el establecimiento "
            "de normas internacionales para garantizar el uso seguro y equitativo de la tecnología, "
            "rechazando que un pequeño número de potencias controle el acceso global a la IA. La postura "
            "china reafirma su visión de un orden tecnológico multipolar frente a los enfoques restrictivos del G7."
        ),
        "fuente_label": "Observatorio de Política China — Cronología OPCh julio 2026",
        "fuente_url": "https://www.politica-china.org/cronologia-opch-122/",
    },
    {
        "emoji": "📈",
        "titulo": "Politburó fija prioridades económicas para el segundo semestre: IA, infraestructura y consumo",
        "cuerpo": (
            "El Buró Político del PCCh celebró el 30 de julio su reunión semestral de análisis económico. "
            "Las decisiones más relevantes: aceleración del consumo interno con campañas nacionales en "
            "turismo y ocio; profundización de la iniciativa IA Plus para integrar la IA en toda la "
            "economía productiva; construcción de seis redes nacionales de infraestructura; combate a la "
            "competencia 'involutiva' (guerras de precios destructivas); y política fiscal más activa "
            "con posibles nuevas bajadas de tipos. La reunión también priorizó la protección de los "
            "derechos laborales de los trabajadores de plataformas digitales."
        ),
        "fuente_label": "Caixin Global — China's Politburo signals additional policy measures to bolster economy",
        "fuente_url": "https://www.caixinglobal.com/2026-07-31/chinas-politburo-signals-additional-policy-measures-to-bolster-economy-102469709.html",
    },
    {
        "emoji": "💹",
        "titulo": "PIB crece un 4,7% en el primer semestre de 2026; manufactura avanzada lidera con +13,3%",
        "cuerpo": (
            "El PIB chino creció un 4,7% interanual en el primer semestre de 2026. El motor más potente "
            "fue la manufactura de alta tecnología, que se expandió un 13,3%, con sectores como robots "
            "industriales y circuitos integrados en cabeza. La producción industrial mantuvo una expansión "
            "estable y el sector exportador continuó su impulso récord. La tecnología de la información "
            "y la IA siguen siendo los grandes catalizadores del crecimiento, según el Ministerio de "
            "Industria y Tecnología de la Información."
        ),
        "fuente_label": "CGTN — How China sees its economic priorities for second half of 2026",
        "fuente_url": "https://news.cgtn.com/news/2026-07-31/How-China-sees-its-economic-priorities-for-second-half-of-2026-1PdUTeRi0PC/p.html",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de vehículos eléctricos suben un 68,7% en H1 2026; China supera 1 millón de coches exportados en un mes",
        "cuerpo": (
            "Las exportaciones chinas de vehículos de nueva energía crecieron un 68,7% interanual en los "
            "primeros seis meses de 2026. En junio se alcanzó un hito histórico: China exportó más de "
            "1 millón de vehículos en un solo mes por primera vez (1,037 millones), de los cuales 523.000 "
            "fueron eléctricos, superando por primera vez el 50% del total exportado en un mes. Las "
            "exportaciones de coches de pasajeros subieron un 80% interanual en junio. BYD superó a "
            "Tesla en ventas de coches 100% eléctricos durante el segundo trimestre, consolidando su "
            "liderazgo global."
        ),
        "fuente_label": "TechNode — China's electric vehicle exports rise 68.7% in H1 2026",
        "fuente_url": "https://technode.com/2026/07/14/chinas-electric-vehicle-exports-rise-68-7-in-h1-2026/",
    },
    {
        "emoji": "⚡",
        "titulo": "BYD alcanza 17 millones de vehículos eléctricos y despliega 7.000 estaciones de carga ultrarrápida",
        "cuerpo": (
            "El 8 de julio salió de la fábrica de Xi'an el vehículo de nueva energía número 17 millones "
            "de BYD: un Seal 08 con batería Blade de segunda generación y tecnología Flash Charging "
            "(carga completa en 9 minutos). Más de 7.000 estaciones Flash Charging operan ya en China, "
            "con planes de llegar a 20.000 estaciones nacionales y 6.000 internacionales antes de 2027 "
            "(3.000 solo en Europa). BYD Semiconductor también comenzó a suministrar módulos de gestión "
            "de baterías a otros fabricantes chinos, expandiendo su negocio más allá de los vehículos propios."
        ),
        "fuente_label": "Car News China — China's monthly vehicle exports exceed 1 million for the first time",
        "fuente_url": "https://carnewschina.com/2026/07/10/chinas-monthly-vehicle-exports-exceed-1-million-for-the-first-time-with-nevs-claiming-over-half/",
    },
    {
        "emoji": "🌞",
        "titulo": "Energías renovables: China lidera con aerogeneradores, baterías de litio y plantas termosolares",
        "cuerpo": (
            "Las exportaciones chinas de aerogeneradores y baterías de litio crecieron un 35,6% y un "
            "37,6% respectivamente en el primer semestre de 2026. China opera ya 24 plantas termosolares "
            "de concentración (almacenan calor solar y generan electricidad estable), con otras 26 en "
            "construcción (3,2 GW adicionales), a un coste de solo 15.000 yuanes por kilovatio con más "
            "del 95% de equipos de fabricación nacional. Los astilleros chinos captaron el 72% del "
            "mercado mundial de nuevos buques encargados: 1.131 de los 1.481 contratos globales del período."
        ),
        "fuente_label": "Tricontinental Institute — Noticias de China No. 32",
        "fuente_url": "https://thetricontinental.org/es/asia/noticias-de-china-no-32/",
    },
    {
        "emoji": "🚀",
        "titulo": "China intensifica su programa espacial: Long March 10, Shenzhou-23 y Chang'e-7 al polo sur lunar",
        "cuerpo": (
            "La CNSA confirmó un calendario espacial sin precedentes para 2026: Shenzhou-23, nueva "
            "misión tripulada a la estación espacial con un taikonauta en estancia de un año completo; "
            "Tianwen-2, acercamiento al asteroide objetivo para toma de muestras; primer lanzamiento del "
            "cohete Long March 10 (clave para el alunizaje tripulado antes de 2030); y Chang'e-7, "
            "con todos sus módulos ya en la base de lanzamiento de Wenchang, rumbo al polo sur lunar "
            "donde se sospecha la presencia de agua helada en cráteres en sombra permanente."
        ),
        "fuente_label": "SpaceNews — China targets 2026 for first Long March 10 launch",
        "fuente_url": "https://spacenews.com/china-targets-2026-for-first-long-march-10-launch-new-lunar-crew-spacecraft-flight/",
    },
    {
        "emoji": "🏥",
        "titulo": "China fusiona IA y Medicina Tradicional en quioscos de diagnóstico en el metro",
        "cuerpo": (
            "China ha comenzado a desplegar en estaciones de metro y espacios públicos quioscos de "
            "diagnóstico médico asistido por IA que integran tecnología biomédica con principios de "
            "la Medicina Tradicional China (MTC). Estos dispositivos miden constantes vitales mientras "
            "la IA analiza el rostro del usuario, observa la lengua e interpreta el pulso mediante "
            "sensores multicapa —tres técnicas clásicas de diagnóstico en la MTC—. El resultado es un "
            "diagnóstico preventivo inmediato y gratuito para cualquier ciudadano. La Comisión Nacional "
            "de Salud ha promovido activamente esta integración como parte de la estrategia nacional "
            "de salud digital."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional China",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
    {
        "emoji": "🌏",
        "titulo": "Shenzhen se prepara para la Cumbre APEC 2026 en noviembre",
        "cuerpo": (
            "China acogerá la 33.ª Cumbre de Líderes de la APEC en Shenzhen los días 18 y 19 de "
            "noviembre de 2026, bajo el lema 'Construyendo una comunidad de Asia-Pacífico para "
            "prosperar juntos'. Los ministros de Comercio ya iniciaron reuniones preparatorias en "
            "las que China pidió rechazar las barreras comerciales y defender el multilateralismo "
            "y el sistema de la OMC. La cumbre se perfila como la gran plataforma diplomática del año "
            "para el liderazgo chino, con posible bilateral Xi Jinping-Trump en un contexto de tregua "
            "táctica tras la reunión de Pekín de mayo."
        ),
        "fuente_label": "Bloomberg Línea — China acogerá la Cumbre de la APEC en 2026",
        "fuente_url": "https://www.bloomberglinea.com/mundo/china-acogera-la-cumbre-de-la-apec-en-2026-anuncia-xi-jinping/",
    },
]


def build_blocks():
    today = "1 de agosto de 2026"
    semana = "28 de julio al 1 de agosto de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p(f"Recopilacion de las noticias mas relevantes de China esta semana ({semana}): tecnologia, economia, espacio y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 28 Julio - 1 Agosto 2026"
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
