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
        "emoji": "⚡",
        "titulo": "China supera por primera vez el 40 % de generación eléctrica renovable — un hito histórico",
        "cuerpo": (
            "En el primer semestre de 2026, las energías renovables representaron el 41,2 % de la "
            "generación eléctrica de China, superando por primera vez en la historia la barrera del "
            "40 %. La participación del carbón cayó al 49,7 %, también por primera vez por debajo del "
            "50 % en un semestre completo. Durante ese período, el país incorporó 117 GW de nueva "
            "potencia renovable, equivalente al 73,9 % de toda la nueva capacidad eléctrica instalada. "
            "La capacidad renovable total alcanzó 2.455 GW, más del 60 % del parque nacional de generación."
        ),
        "fuente_label": "Energías Renovables — China supera el 40% de generación renovable",
        "fuente_url": "https://www.energias-renovables.com/panorama/china-supera-por-primera-vez-el-40-20260803",
    },
    {
        "emoji": "🤖",
        "titulo": "Conferencia Mundial de IA en Shanghai: más de 400 modelos de robots humanoides en exhibición",
        "cuerpo": (
            "Las principales empresas tecnológicas chinas exhibieron cientos de productos de vanguardia "
            "en la Conferencia Mundial de IA celebrada en Shanghai del 17 al 20 de julio, en medio de "
            "la intensa rivalidad tecnológica entre EE.UU. y China. Las empresas chinas han desarrollado "
            "más de 400 modelos de robots humanoides, más de la mitad del total mundial. El foro reunió "
            "a delegados de más de 80 países y marcó el inicio de la que puede ser la mayor ofensiva "
            "exportadora de tecnología china de la historia."
        ),
        "fuente_label": "ABC News — Shanghai science forum shows China's AI and robotics advances",
        "fuente_url": "https://abcnews.com/International/wireStory/shanghai-science-forum-photos-show-chinas-ai-robotics-134935594",
    },
    {
        "emoji": "💾",
        "titulo": "China construye su segunda fábrica de chips de memoria tras su salida a bolsa de 8.600 millones",
        "cuerpo": (
            "ChangXin Memory Technologies (CXMT) anunció la construcción de su segunda fábrica de chips "
            "de memoria, apenas días después de completar su salida a bolsa por 8.600 millones de dólares "
            "—una de las mayores IPO tecnológicas del año en Asia—. La nueva planta refuerza la apuesta "
            "de China por la autosuficiencia en semiconductores. CXMT ya fabrica chips DRAM comparables "
            "a los de Samsung y SK Hynix de hace dos generaciones, a un precio significativamente menor."
        ),
        "fuente_label": "El Nacional Cat — Fábrica de chips para la era de la robótica",
        "fuente_url": "https://www.elnacional.cat/es/tecnologia/futuro-ia-sera-made-in-china-preparan-fabrica-chips-era-robotica_1677494_102.html",
    },
    {
        "emoji": "🦾",
        "titulo": "Revolución robótica en APEC: delegados visitan la mayor exposición de robots de China",
        "cuerpo": (
            "El 26 de julio, delegados de la APEC Digital Week visitaron en Chengdu una empresa china "
            "de robótica con más de 70 modelos de robots industriales y colaborativos con IA incorporada. "
            "La demostración incluyó robots de precisión submilimétrica para cirugía remota y cuadrúpedos "
            "para inspección en entornos peligrosos. China aspira a que el sector robótico aporte "
            "10 billones de yuanes a la economía para 2030."
        ),
        "fuente_label": "CGTN — China's robot revolution on show for APEC delegates in Chengdu",
        "fuente_url": "https://news.cgtn.com/news/2026-07-26/China-s-robot-revolution-on-show-for-APEC-delegates-in-Chengdu-1P66b1P7rdm/p.html",
    },
    {
        "emoji": "🌐",
        "titulo": "México y China estrechan lazos científicos en IA, robótica y semiconductores",
        "cuerpo": (
            "El 23 de julio, la Secihti de México sostuvo una reunión con el embajador de China para "
            "impulsar proyectos conjuntos de inteligencia artificial, robótica, electromovilidad y "
            "semiconductores. El acuerdo incluye programas de movilidad para jóvenes investigadores, "
            "laboratorios compartidos y desarrollo conjunto de patentes. Es parte de una tendencia más "
            "amplia: en 2026, más de 40 países de Latinoamérica, África y Asia han firmado acuerdos "
            "de cooperación tecnológica con China."
        ),
        "fuente_label": "La Jornada — México y China impulsan alianza en IA, robótica y electromovilidad",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/07/23/ciencias/mexico-y-china-impulsan-alianza-en-inteligencia-artificial-robotica-y-electromovilidad",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones de energía limpia se disparan: aerogeneradores +35,6 %, baterías +37,6 %, vehículos +65,3 %",
        "cuerpo": (
            "Los datos del primer semestre de 2026 revelan un crecimiento explosivo en las exportaciones "
            "chinas de tecnología verde. Las ventas al exterior de aerogeneradores aumentaron un 35,6 % "
            "interanual, las de baterías de litio un 37,6 %, y las de automóviles alcanzaron 5,096 "
            "millones de unidades, un alza del 65,3 %. Además, los astilleros chinos captaron 1.131 de "
            "los 1.481 buques encargados en todo el mundo, aproximadamente el 72 % del mercado global "
            "de construcción naval. China consolida su dominio en las industrias del futuro."
        ),
        "fuente_label": "Tricontinental — Noticias de China No. 32",
        "fuente_url": "https://thetricontinental.org/es/asia/noticias-de-china-no-32/",
    },
    {
        "emoji": "💼",
        "titulo": "El comercio de servicios de China crece un 8,3 % en el primer semestre",
        "cuerpo": (
            "Según datos del Ministerio de Comercio publicados el 5 de agosto, el comercio de servicios "
            "de China se expandió un 8,3 % interanual en el primer semestre de 2026. Las exportaciones "
            "de servicios de viajes lideraron el crecimiento con un +31,1 %, reflejo de la recuperación "
            "del turismo internacional. Los servicios tecnológicos —consultoría digital, software y "
            "propiedad intelectual— crecieron un 14,2 %, convirtiéndose en el segundo motor de ingresos."
        ),
        "fuente_label": "China.org.cn — Comercio de servicios crece 8,3% en el primer semestre",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-08/05/content_118634357.htm",
    },
    {
        "emoji": "🗺️",
        "titulo": "La Iniciativa Cinturón y Ruta marca récord: 126.400 millones en el primer semestre",
        "cuerpo": (
            "Un análisis cifra la participación de China en la Iniciativa Cinturón y Ruta (BRI) en el "
            "primer semestre de 2026 en 49.800 millones en inversiones y 76.500 millones en contratos "
            "de construcción, totalizando 126.400 millones de dólares en 186 proyectos. Los sectores "
            "con mayor crecimiento son energía limpia, minería crítica y nuevas tecnologías (5G, centros "
            "de datos, inteligencia artificial). Las empresas más activas fueron PowerChina, State "
            "Construction Engineering y China Communications Construction Corporation."
        ),
        "fuente_label": "Green Finance & Development Center — BRI 2026 H1",
        "fuente_url": "https://greenfdc.org/chinas-investment-and-construction-engagement-in-the-belt-and-road-initiative-bri-2026-h1/",
    },
    {
        "emoji": "🧊",
        "titulo": "La estación antártica Qinling alcanza el 50 % de energía renovable en plena noche polar",
        "cuerpo": (
            "La estación Qinling, el puesto antártico más moderno de China, logró esta semana un hito "
            "en eficiencia energética: las energías renovables representan ya el 50 % de su suministro "
            "eléctrico incluso durante los meses de oscuridad polar. El sistema combina paneles "
            "fotovoltaicos de alta eficiencia, almacenamiento en baterías y aerogeneradores de pequeña "
            "potencia diseñados para resistir temperaturas de -50 °C. El logro sirve de banco de pruebas "
            "para tecnologías de energía verde en condiciones extremas."
        ),
        "fuente_label": "People's Daily — Estación Qinling logra avance en energía verde",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0805/c92121-20485504.html",
    },
    {
        "emoji": "🛰️",
        "titulo": "El proyecto solar espacial chino: una central de 100.000 GWh al año en órbita geoestacionaria",
        "cuerpo": (
            "China avanza en el proyecto 'Tres Gargantas en el espacio', una central solar en órbita "
            "geoestacionaria a 36.000 km de altitud que podría generar hasta 100.000 millones de kWh "
            "anuales —similar al consumo total de países como los Países Bajos—. A diferencia de los "
            "paneles terrestres, los satélites reciben luz solar las 24 horas del día, sin nubes ni "
            "ciclos noche-día. El plan prevé lanzar el primer satélite de pruebas en 2028 y tener "
            "una planta comercial plenamente operativa hacia 2050."
        ),
        "fuente_label": "El Español — China construye paneles solares en el espacio a 36.000 km",
        "fuente_url": "https://www.elespanol.com/ciencia/20260413/china-cambia-estrategia-construye-paneles-solares-espacio-kilometros-trabajan-horas-dia/1003744201225_0.html",
    },
    {
        "emoji": "💊",
        "titulo": "China firma acuerdos de licencias biotecnológicas por 60.000 millones en el primer trimestre",
        "cuerpo": (
            "Mientras el mundo miraba a DeepSeek y los robots humanoides, China construía en silencio "
            "una potencia farmacéutica global. Las empresas biotech chinas firmaron acuerdos de licencia "
            "transfronteriza por un valor récord de 60.000 millones de dólares solo en el primer "
            "trimestre de 2026. China ya no quiere fabricar medicamentos baratos: quiere cobrar por "
            "las moléculas, las patentes y la investigación. El país ha captado el 39 % de los ensayos "
            "clínicos globales, más que EE.UU. y la UE combinados."
        ),
        "fuente_label": "Gizmodo ES — China y su silenciosa exportación biotecnológica",
        "fuente_url": "https://es.gizmodo.com/todos-miraban-a-deepseek-y-a-los-robots-humanoides-pero-china-estaba-preparando-una-exportacion-mucho-mas-silenciosa-ahora-sus-medicamentos-empiezan-a-llenar-las-carteras-de-las-farmaceuticas-occide-2000249516",
    },
    {
        "emoji": "🏥",
        "titulo": "IA y medicina tradicional china: los quioscos de diagnóstico inteligente llegan al metro",
        "cuerpo": (
            "China ha comenzado a desplegar quioscos de diagnóstico asistido por inteligencia artificial "
            "en estaciones de metro y puntos urbanos, combinando biomedicina avanzada con la Medicina "
            "Tradicional China (MTC). Los dispositivos miden presión arterial, frecuencia cardíaca, "
            "saturación de oxígeno y temperatura; la IA aplica simultáneamente criterios de la MTC: "
            "análisis facial, observación de lengua e interpretación digital del pulso. El objetivo "
            "es detectar enfermedades crónicas de forma precoz, descargando presión de los centros "
            "de salud primaria."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
    {
        "emoji": "🌏",
        "titulo": "China anuncia contramedidas frente a las restricciones tecnológicas de EE.UU.",
        "cuerpo": (
            "El 5 de agosto, el gobierno chino anunció 'contramedidas necesarias' en respuesta a las "
            "últimas restricciones tecnológicas impuestas por Washington, que incluyeron robots "
            "humanoides y cuadrúpedos chinos en su lista de importaciones prohibidas por 'seguridad "
            "nacional'. Pekín respondió con controles a la exportación de drones de doble uso hacia "
            "EE.UU. e inició una investigación de seguridad nacional sobre equipos de imagen de "
            "oficina importados. Analistas señalan que China mantiene ventajas estructurales en "
            "fabricación que limitan la eficacia de estas sanciones."
        ),
        "fuente_label": "Cubadebate — China anuncia contramedidas ante restricciones tecnológicas de EE.UU.",
        "fuente_url": "http://www.cubadebate.cu/noticias/2026/08/05/china-anuncia-contramedidas-necesarias-ante-restricciones-tecnologicas-de-estados-unidos/",
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
    title = "China Al Dia — Semana 28 Jul - 6 Ago 2026"
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
