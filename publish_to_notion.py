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
        "titulo": "China lidera la carrera de IA con modelos abiertos y precios mínimos",
        "cuerpo": (
            "China ha adoptado una estrategia diferenciada para ganar la carrera de la inteligencia artificial: "
            "modelos de código abierto, costes mínimos y rápida implantación comercial. DeepSeek V4 Pro, con "
            "1,6 billones de parámetros, se ha convertido en el mayor modelo de pesos abiertos del mundo, "
            "funcionando sobre chips Huawei Ascend 950 en lugar de GPU de Nvidia. En junio, DeepSeek ocupó "
            "el primer lugar en la clasificación de nuevos proveedores empresariales de Ramp, ganando terreno "
            "entre empresas estadounidenses. Zhipu AI lanzó GLM-5.2 de acceso libre y MiniMax M3 —con contexto "
            "de un millón de tokens y código abierto— amplían un ecosistema en el que China genera un "
            "unicornio de IA cada cinco días."
        ),
        "fuente_label": "ABC Color — China acelera con modelos abiertos y bajos precios",
        "fuente_url": "https://www.abc.com.py/ciencia/2026/07/02/china-acelera-con-modelos-abiertos-y-bajos-precios-en-su-carrera-de-ia-con-estados-unidos/",
    },
    {
        "emoji": "💰",
        "titulo": "DeepSeek cierra una ronda histórica de 7.400 millones de dólares",
        "cuerpo": (
            "DeepSeek cerró su primera ronda de financiación externa captando más de 50.000 millones de yuanes "
            "(aproximadamente 7.400 millones de dólares) a una valoración superior a los 50.000 millones de dólares. "
            "El objetivo declarado de la compañía no es ganar la carrera de modelos de IA, sino construir una "
            "industria china de hardware que no dependa de Nvidia ni de TSMC. China genera ya un unicornio de IA "
            "cada cinco días, según datos publicados esta semana, consolidando su ecosistema tecnológico con "
            "independencia de las restricciones de exportación estadounidenses."
        ),
        "fuente_label": "Wwwhatsnew — DeepSeek ronda 7.400 millones, unicornios IA China",
        "fuente_url": "https://wwwhatsnew.com/2026/06/30/deepseek-ronda-7400-millones-china-unicornios-ia-2026/",
    },
    {
        "emoji": "🧑‍🤝‍🧑",
        "titulo": "UBTech lanza el U1: el robot confidente que combate la soledad",
        "cuerpo": (
            "La empresa china UBTech presentó el U1, un robot humanoide de apariencia hiperrealista para ofrecer "
            "compañía emocional a los 120 millones de personas solteras y los 320 millones de mayores de 60 años en China. "
            "Con autonomía de cuatro horas, el U1 conversa, detecta fatiga o estrés y aprende de cada interacción. "
            "Disponible en versiones de 1,68 m y 1,83 m, su precio parte de 119.800 yuanes (≈ 16.500 dólares). "
            "El contexto es revelador: 140 empresas chinas lanzaron 330 modelos de robots humanoides en el último año, "
            "China concentra el 85 % de los humanoides instalados en el mundo, y el mercado podría alcanzar "
            "los 15.000 millones de dólares en 2030."
        ),
        "fuente_label": "El Universal Colombia — China apuesta por androides sociales",
        "fuente_url": "https://www.eluniversal.com.co/tecnologia/2026/07/02/un-robot-como-confidente-china-apuesta-por-androides-sociales/",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar de China supera al carbón por primera vez",
        "cuerpo": (
            "En 2026, China alcanza un cambio estructural sin precedentes: la capacidad instalada de energía solar "
            "supera por primera vez a la del carbón. La solar y la eólica juntas alcanzan la mitad de la potencia "
            "instalada total del país. China añadirá más de 300 millones de kilovatios de capacidad renovable este año, "
            "dentro de un total de 400 GW de nueva instalación eléctrica. A finales de 2026, las energías no fósiles "
            "representarán el 63 % de la capacidad instalada, mientras el carbón caerá al 31 %. La potencia de parques "
            "eólicos y solares ya en funcionamiento supera 1,6 teravatios —más que cualquier otro país del mundo."
        ),
        "fuente_label": "Ecoticias — China supera al carbón con energía solar por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🛸",
        "titulo": "China experimenta con paneles solares en órbita para transmitir energía a la Tierra",
        "cuerpo": (
            "China avanza en su proyecto Sun Chasing: paneles solares en el espacio que recolectan energía y la "
            "transmiten inalámbricamente a la Tierra o a naves espaciales. En las pruebas más recientes, el sistema "
            "alcanzó una eficiencia de transmisión del 20,8 % en 100 metros, entregando 1.180 vatios. El equipo "
            "también desarrolló un sistema de carga inalámbrica para drones que, en pruebas a 30 km/h, recibió "
            "143 vatios estables desde 30 metros. El primer prototipo de 500 kW en órbita está previsto para 2030, "
            "y una central plenamente operativa de 20 MW para 2035, con la planta definitiva de 2 GW para 2050."
        ),
        "fuente_label": "PV Magazine — China realiza primeros experimentos de energía solar espacial",
        "fuente_url": "https://www.pv-magazine.com/2026/05/20/china-conducts-first-experiments-for-space-based-solar-power-plants/",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 y Shenzhou-23: China mantiene el ritmo espacial mientras la NASA recorta",
        "cuerpo": (
            "Mientras la NASA cancela 41 misiones por recortes presupuestarios, China mantiene su ritmo espacial. "
            "Chang'e-7 está en preparación final para su lanzamiento a finales de 2026, con destino al polo sur lunar, "
            "donde podría haber agua en forma de hielo. Shenzhou-23, lanzada en mayo, lleva a un astronauta que "
            "permanecerá un año en la estación Tiangong —un hito en resistencia humana en el espacio—. Las misiones "
            "Chang'e-7 y 8 sentarán las bases de la futura Estación Internacional de Investigación Lunar (ILRS), "
            "proyecto conjunto con Rusia, con misiones tripuladas a la Luna previstas antes de 2030."
        ),
        "fuente_label": "Xataka — China hace virguerías en el espacio mientras la NASA recorta",
        "fuente_url": "https://www.xataka.com/espacio/nasa-se-enfrenta-a-cancelacion-41-misiones-china-esta-haciendo-autenticas-virguerias-espacio",
    },
    {
        "emoji": "🏭",
        "titulo": "China moderniza industrias y refuerza corredores comerciales estratégicos",
        "cuerpo": (
            "Las autoridades chinas han intensificado su llamado a modernizar industrias clave, aprovechando el servicio "
            "de trenes de carga China-Europa y el Nuevo Corredor Internacional de Comercio Terrestre-Marítimo para "
            "convertir las regiones interiores en centros de exportación de alta calidad. En paralelo, la robótica "
            "transforma la propia cadena de suministro: en proyectos de energía como los de la cuenca del Tarim, "
            "sistemas automatizados instalan paneles solares cuatro o cinco veces más rápido que el trabajo manual, "
            "con mayor precisión y menores costes operativos, demostrando cómo la tecnología y la industria se "
            "retroalimentan en el modelo de desarrollo chino."
        ),
        "fuente_label": "La Jornada — China insta a modernizar sus industrias clave",
        "fuente_url": "https://www.jornada.com.mx/2026/06/29/economia/021n1eco",
    },
    {
        "emoji": "🧠",
        "titulo": "La 'inteligencia encarnada': el motor oculto del plan quinquenal chino",
        "cuerpo": (
            "Más allá de la IA generativa, la inteligencia encarnada —robots con IA que interactúan físicamente con "
            "el mundo— se ha convertido en uno de los seis motores de crecimiento designados del XV Plan Quinquenal, "
            "junto a computación cuántica, biofabricación, hidrógeno, fusión nuclear e interfaz cerebro-computadora. "
            "Este reconocimiento desbloquea el acceso al Fondo Nacional de Inversión en IA de 60.000 millones de "
            "yuanes (≈ 8.200 millones de dólares). El plan no trata la robótica como un subsidio sectorial, sino "
            "como el tejido conectivo de toda la modernización económica china, con más de 140 empresas activas "
            "y 330 modelos de robots humanoides lanzados en el último año."
        ),
        "fuente_label": "Merics — Inteligencia encarnada: la apuesta de China por la robótica",
        "fuente_url": "https://merics.org/en/report/embodied-ai-chinas-ambitious-path-transform-its-robotics-industry",
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
    title = "China Al Dia — Semana 27 Junio - 3 Julio 2026"
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
