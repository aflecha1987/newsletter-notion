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
        "titulo": "China lidera la IA global: 20 de los 50 modelos más usados en el mundo son chinos",
        "cuerpo": (
            "En solo un año, China ha pasado de una presencia marginal a liderar el ranking de inteligencia "
            "artificial a escala global. El país ya concentra 20 de los 50 modelos de IA más utilizados en "
            "todo el mundo y encabeza la clasificación mundial con 1.509 grandes modelos de lenguaje "
            "registrados. Más del 30% de las grandes empresas industriales chinas ya han adoptado la IA en "
            "sus procesos productivos, con la manufactura como principal campo de aplicación. El Ministerio "
            "de Industria y Tecnología de la Información confirmó estos datos en una rueda de prensa "
            "celebrada en Shanghái durante la Conferencia Global de Economía Digital 2026."
        ),
        "fuente_label": "CriptoTendencia — China concentra 20 de los 50 modelos de IA más usados",
        "fuente_url": "https://criptotendencia.com/2026/07/12/china-ya-concentra-20-de-los-50-modelos-de-ia-mas-utilizados-a-nivel-mundial-2/",
    },
    {
        "emoji": "🌐",
        "titulo": "Conferencia Global de Economía Digital 2026: China presenta el futuro digital para las personas",
        "cuerpo": (
            "La Conferencia Global de Economía Digital 2026 se celebró en Pekín del 2 al 5 de julio, "
            "reuniendo a gobiernos, empresas y expertos internacionales. El evento mostró soluciones "
            "digitales e innovaciones de IA orientadas a mejorar el bienestar social: desde diagnósticos "
            "médicos asistidos hasta ciudades inteligentes y servicios públicos digitalizados. China "
            "aceleró durante 2025 el despliegue de tecnologías digitales e inteligentes en toda su "
            "economía, y el plan de gobierno contempla que el 70% de la economía incorpore IA para "
            "2027 y el 90% para 2030."
        ),
        "fuente_label": "CRI Español — Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cri.cn/2026/07/02/ARTI1782972617748340",
    },
    {
        "emoji": "🏙️",
        "titulo": "WAIC 2026 en Shanghái: la mayor cumbre mundial de inteligencia artificial, del 17 al 20 de julio",
        "cuerpo": (
            "China acogerá la Conferencia Mundial de IA 2026 (WAIC) en Shanghái del 17 al 20 de julio, "
            "junto con la Reunión de Alto Nivel sobre Gobernanza Global de la IA. La WAIC se consolida "
            "como la plataforma global más importante para presentar los avances más punteros en "
            "inteligencia artificial, debatir marcos de gobernanza y tender puentes entre innovación "
            "tecnológica y responsabilidad ética. La conferencia incluirá demostraciones en vivo de "
            "robótica, generación de contenidos con IA y aplicaciones industriales de vanguardia."
        ),
        "fuente_label": "Global Times — China anuncia la WAIC 2026 en Shanghái",
        "fuente_url": "https://x.com/globaltimesnews/status/2074498976116809858",
    },
    {
        "emoji": "✈️",
        "titulo": "China inaugura su primer avión de ala fija 100% nacional para vigilancia ambiental atmosférica",
        "cuerpo": (
            "La Corporación de la Industria de Aviación de China (AVIC) completó con éxito el vuelo "
            "inaugural del primer avión de ala fija desarrollado íntegramente en China para la detección "
            "del medio ambiente atmosférico. La aeronave permite recopilar datos atmosféricos de alta "
            "precisión y refuerza la capacidad nacional de monitoreo climático y medioambiental, clave "
            "para los compromisos de China con la transición verde. Un hito en la aviación científica "
            "que demuestra la capacidad de desarrollo tecnológico autónomo del país."
        ),
        "fuente_label": "Observatorio de Política China — Resumen semana 3-9 julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-66/",
    },
    {
        "emoji": "☀️",
        "titulo": "Avance histórico: China transmite energía solar desde el espacio a más de 100 metros",
        "cuerpo": (
            "China dio un paso decisivo hacia las estaciones solares espaciales al desarrollar un sistema "
            "de verificación en tierra capaz de transmitir energía de forma inalámbrica mediante microondas "
            "a distancias superiores a 100 metros. El sistema logró una potencia de salida de 1.180 vatios, "
            "una eficiencia de transmisión de corriente continua del 20,8% y una eficiencia de captación "
            "del haz del 88%. Esta tecnología es la base de las futuras centrales solares espaciales que "
            "podrían suministrar energía limpia de forma continua a la Tierra, sin depender de ciclos "
            "día-noche ni condiciones meteorológicas."
        ),
        "fuente_label": "CGTN — China advances space solar power breakthrough",
        "fuente_url": "https://news.cgtn.com/news/2026-05-19/China-advances-space-solar-power-breakthrough-1NgRg7RgnpC/p.html",
    },
    {
        "emoji": "📊",
        "titulo": "Banco Mundial: China mantiene resiliencia económica respaldada por tecnología y exportaciones",
        "cuerpo": (
            "La actualización económica de julio 2026 del Banco Mundial confirma que China mantuvo un "
            "desempeño sólido en el primer semestre de 2026, sustentado por una fuerte inversión en "
            "tecnología de alto nivel y un robusto crecimiento exportador. Las políticas de apoyo, los "
            "amortiguadores frente a disrupciones en el suministro energético global y la inversión en "
            "manufactura avanzada han compensado la moderación del consumo interno. El Banco Mundial "
            "proyecta un crecimiento del 4,4% para 2026, con el sector de alta tecnología como "
            "principal motor."
        ),
        "fuente_label": "Banco Mundial — China Economic Update julio 2026",
        "fuente_url": "https://www.worldbank.org/en/news/press-release/2026/07/07/rebalancing-growth-china-economic-update",
    },
    {
        "emoji": "🤝",
        "titulo": "China y la UE acuerdan impulsar el comercio bilateral, la IA y la transición ecológica",
        "cuerpo": (
            "En la primera reunión del mecanismo de consultas sobre comercio e inversión entre China y "
            "la Unión Europea, ambas partes acordaron fortalecer la cooperación en inteligencia artificial, "
            "transición ecológica y comercio de servicios, e impulsar un crecimiento más equilibrado del "
            "intercambio bilateral. El acuerdo refleja el interés mutuo de las dos mayores potencias "
            "económicas del mundo por estabilizar sus relaciones comerciales y colaborar en los sectores "
            "del futuro, más allá de las tensiones geopolíticas que han marcado los últimos años."
        ),
        "fuente_label": "Observatorio de Política China — Resumen semana 3-9 julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-66/",
    },
    {
        "emoji": "🗣️",
        "titulo": "Premier Li Qiang: los avances tecnológicos de China son una oportunidad, no una amenaza",
        "cuerpo": (
            "El premier chino Li Qiang reiteró en Copenhague que el liderazgo tecnológico de China "
            "debe interpretarse como una oportunidad de colaboración para el mundo, no como una amenaza. "
            "Durante su encuentro con el rey de Dinamarca Federico X y con líderes europeos, Li subrayó "
            "la voluntad de China de abrir su mercado y cooperar en economía verde, innovación tecnológica "
            "e inteligencia artificial. Ambas naciones confirmaron su disposición a estrechar lazos en "
            "sectores emergentes como la economía verde y la IA."
        ),
        "fuente_label": "La Jornada — Avances tecnológicos de China son oportunidad, no amenaza",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/06/24/economia/avances-tecnologicos-de-china-son-una-oportunidad-no-una-amenaza-dice-el-premier-li-quiang",
    },
    {
        "emoji": "⚡",
        "titulo": "Las renovables superan al carbón en China: eólica y solar alcanzan 1.840 GW y nueva ley desde agosto",
        "cuerpo": (
            "A cierre de 2025, la capacidad acumulada de energía eólica y solar en China superó los "
            "1.840 GW, representando el 47,3% de la capacidad eléctrica total del país. Es la primera "
            "vez en la historia que estas energías limpias superan en el mix eléctrico al carbón y al "
            "gas. China planea añadir aproximadamente 100 GW adicionales de almacenamiento hidroeléctrico "
            "por bombeo en los próximos cinco años. A partir de agosto de 2026 entran en vigor nuevas "
            "reglas de consumo renovable obligatorio para provincias e industrias, consolidando el "
            "liderazgo verde del país."
        ),
        "fuente_label": "Ambientum — Estrategia Energética de China: Liderazgo y Renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
    },
    {
        "emoji": "🏥",
        "titulo": "China, potencia sanitaria global: acuerdos con 160 países y 30.000 médicos en 77 naciones",
        "cuerpo": (
            "China ha firmado acuerdos de cooperación en salud con más de 160 países y organizaciones "
            "internacionales, y ha enviado más de 30.000 trabajadores médicos a 77 países, atendiendo "
            "a más de 300 millones de pacientes en todo el mundo. La biomedicina ha sido identificada "
            "en el Plan de Trabajo del Gobierno 2026 como una industria pilar emergente. Las reformas "
            "regulatorias han acelerado la aprobación de ensayos clínicos entre un 30 y un 40%, "
            "reduciendo costes y atrayendo inversión en innovación farmacéutica nacional e internacional."
        ),
        "fuente_label": "CGTN — How China's healthcare advances are opening new doors to the world",
        "fuente_url": "https://news.cgtn.com/news/2026-06-30/How-China-s-healthcare-advances-are-opening-new-doors-to-the-world-1OowIE6zvz2/p.html",
    },
    {
        "emoji": "🌍",
        "titulo": "2026: Año de Intercambios entre Pueblos China-África y nuevo impulso a la cooperación",
        "cuerpo": (
            "China y África profundizan su cooperación en 2026, declarado Año de los Intercambios entre "
            "Pueblos China-África. Dentro de la implementación del Plan de Acción FOCAC 2024-2027, China "
            "ha puesto en marcha diez proyectos de intercambio cultural y social, incluyendo programas "
            "de nutrición infantil en Liberia y formación de profesionales africanos en China. La "
            "relación bilateral se expande hacia energía limpia, infraestructura digital y salud, con "
            "el horizonte puesto en la cumbre FOCAC de 2027 en la República del Congo."
        ),
        "fuente_label": "Africa Center — What to Expect from Africa-China Relations in 2026",
        "fuente_url": "https://africacenter.org/spotlight/africa-china-relations-2026/",
    },
    {
        "emoji": "🌎",
        "titulo": "China publica su tercer Documento de Política hacia América Latina: nueva era de cooperación",
        "cuerpo": (
            "El Gobierno chino publicó su tercer Documento de Política hacia América Latina y el Caribe, "
            "que eleva las relaciones con la región a una nueva fase. El documento incluye propuestas en "
            "infraestructura, tecnología verde, ciudades inteligentes, educación y cooperación en IA. "
            "México y China amplían sus vínculos con proyectos de movilidad sostenible y transporte "
            "ferroviario urbano. La CEPAL destaca que esta cooperación es una oportunidad para reducir "
            "las asimetrías globales y apoyar una recuperación económica transformadora en la región."
        ),
        "fuente_label": "CEPAL — Cooperación China y América Latina: oportunidad para reducir asimetrías",
        "fuente_url": "https://www.cepal.org/en/news/cooperation-between-china-and-latin-america-and-caribbean-opportunity-reduce-global-asymmetries",
    },
    {
        "emoji": "🗺️",
        "titulo": "XV Plan Quinquenal (2026-2030): economía digital y tecnología emergente como ejes del futuro",
        "cuerpo": (
            "El XV Plan Quinquenal (2026-2030) sitúa la economía digital y las tecnologías emergentes "
            "en el núcleo del modelo de desarrollo chino. Los objetivos contemplan el fortalecimiento "
            "de industrias clave como la IA, los semiconductores, la robótica, el 6G y la biotecnología, "
            "así como el fomento de centros industriales digitales competitivos a escala internacional. "
            "China aspira a convertir su modelo de economía digital en referente para el mundo en "
            "desarrollo durante la próxima década, con la Conferencia de Economía Digital 2026 como "
            "primera gran vitrina pública de esta ambiciosa hoja de ruta."
        ),
        "fuente_label": "The Conversation — 2026-2030: China busca consolidar su poder global mediante la tecnología",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
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
    title = f"China Al Dia — Semana 7-12 Julio 2026"
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
