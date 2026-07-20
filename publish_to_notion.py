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
        "titulo": "Xi Jinping inaugura la Conferencia Mundial de IA en Shanghái: «La IA no puede estar dominada por un solo país»",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghái acogió la Conferencia Mundial de Inteligencia Artificial 2026, "
            "con una superficie expositiva de más de 100.000 m², la participación de más de 1.100 empresas "
            "y la presentación de 3.000 productos, de los cuales más de 300 son primeras mundiales. En la "
            "ceremonia inaugural, el presidente Xi Jinping subrayó que la inteligencia artificial no debe "
            "ser dominada por ninguna nación en particular e instó a una gobernanza global inclusiva. China "
            "aprovechó el escenario para liderar el debate sobre el futuro de la IA, consolidando Shanghái "
            "como capital tecnológica del siglo XXI."
        ),
        "fuente_label": "CGTN Español — Últimas innovaciones en la Conferencia Mundial de IA 2026",
        "fuente_url": "https://espanol.cgtn.com/2026/07/19/ARTI1784426596140231",
    },
    {
        "emoji": "🌐",
        "titulo": "China y 29 países fundan la Organización Mundial de Cooperación en IA, con sede en Shanghái",
        "cuerpo": (
            "En el marco de la Conferencia Mundial de IA, el canciller Wang Yi y representantes de 29 naciones "
            "firmaron el acuerdo de creación de la Organización Mundial de Cooperación en Inteligencia Artificial, "
            "con sede permanente en Shanghái. Su objetivo es garantizar un desarrollo de la IA 'saludable, "
            "ordenado e inclusivo', especialmente para reducir la brecha digital entre países desarrollados "
            "y en vías de desarrollo. Es el primer organismo intergubernamental del mundo centrado "
            "exclusivamente en la IA."
        ),
        "fuente_label": "El Imparcial — China presenta plan global de IA con 29 países",
        "fuente_url": "https://www.elimparcial.com/mundo/2026/07/17/china-presenta-plan-global-de-inteligencia-artificial-para-reducir-la-brecha-digital-y-crea-con-29-paises-una-organizacion-con-sede-en-shanghai/",
    },
    {
        "emoji": "🏆",
        "titulo": "China ya tiene 20 de los 50 modelos de IA más utilizados del mundo",
        "cuerpo": (
            "En apenas doce meses, China pasó de contar con una presencia mínima entre los modelos de IA "
            "más usados globalmente a representar 20 de los 50 más populares. Los modelos chinos atraen a "
            "usuarios internacionales gracias a costes significativamente inferiores a los de sus competidores "
            "estadounidenses, manteniendo una calidad comparable en muchos casos. Esta expansión refleja la "
            "madurez del ecosistema de IA chino: más del 30% de las grandes empresas industriales del país "
            "ya han adoptado la IA en sus procesos productivos."
        ),
        "fuente_label": "CriptoTendencia — China concentra 20 de los 50 modelos de IA más utilizados",
        "fuente_url": "https://criptotendencia.com/2026/07/12/china-ya-concentra-20-de-los-50-modelos-de-ia-mas-utilizados-a-nivel-mundial-2/",
    },
    {
        "emoji": "🛰️",
        "titulo": "MAZU-FengYun: China lanza una «caja de IA» satelital para usuarios internacionales",
        "cuerpo": (
            "El 17 de julio, la Administración Meteorológica China publicó oficialmente la Caja de IA para "
            "Satélites MAZU-FengYun, una plataforma que integra la totalidad de los datos de observación "
            "de los satélites meteorológicos Fengyun de China con tecnología de inteligencia artificial. "
            "La herramienta está pensada para usuarios internacionales y representa un paso adelante en la "
            "apertura de la infraestructura espacial china como servicio global, especialmente para la "
            "predicción climática y la respuesta ante desastres naturales."
        ),
        "fuente_label": "CGTN — Tech innovation unlocks new growth momentum for China's economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-16/Tech-innovation-unlocks-new-growth-momentum-for-China-s-economy-1OOMQp36DmM/share_amp.html",
    },
    {
        "emoji": "📦",
        "titulo": "Comercio exterior de China supera los 25 billones de yuanes en el primer semestre: +16,9%",
        "cuerpo": (
            "La Administración General de Aduanas confirmó que el comercio exterior chino alcanzó los "
            "25,47 billones de yuanes (≈ 3,75 billones de dólares) en el primer semestre de 2026, un "
            "incremento interanual del 16,9% y la primera vez que se supera la barrera de los 25 billones "
            "en dicho período. Las exportaciones crecieron un 13,4% hasta los 14,73 billones de yuanes, "
            "mientras las importaciones se dispararon un 22,1% hasta los 10,74 billones, señal de una "
            "demanda interna en recuperación."
        ),
        "fuente_label": "People's Daily Español — Comercio exterior de China crece 16,9% en primer semestre",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0715/c31620-20477940.html",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China: +4,7% en el primer semestre de 2026",
        "cuerpo": (
            "La economía china creció un 4,7% interanual en el primer semestre de 2026, con el sector "
            "servicios liderando la expansión (+5,2%), seguido de la industria (+3,9%) y el sector "
            "primario (+3,7%). La innovación tecnológica —especialmente en IA, manufactura de alta gama "
            "e industria aeroespacial— está emergiendo como el principal motor de resiliencia económica, "
            "compensando la desaceleración del consumo interno y las turbulencias del entorno geopolítico "
            "global."
        ),
        "fuente_label": "CGTN — Tech innovation unlocks new growth momentum for China's economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-16/Tech-innovation-unlocks-new-growth-momentum-for-China-s-economy-1OOMQp36DmM/share_amp.html",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate récords de exportación: +94,7% interanual y objetivo de 1,5 millones de unidades",
        "cuerpo": (
            "BYD fijó en junio un nuevo récord de exportaciones con 175.349 unidades vendidas fuera de China, "
            "un 94,7% más que en junio de 2025. La empresa confía en alcanzar 1,5 millones de exportaciones "
            "en 2026, un 15% por encima de su objetivo inicial. Las exportaciones de vehículos eléctricos "
            "e híbridos chinos en su conjunto crecieron un 150% interanual, con un récord histórico de "
            "905.000 unidades en un solo mes —más que todo lo exportado en el año 2019—. El alza del precio "
            "del petróleo y la mayor competitividad en precio están impulsando la transición eléctrica en "
            "mercados de Asia-Pacífico, Europa y América Latina."
        ),
        "fuente_label": "Motor16 — Exportaciones de coches chinos baten récords en 2026",
        "fuente_url": "https://www.motor16.com/las-ultimas-noticias/exportaciones-coches-chinos-2026-record/",
    },
    {
        "emoji": "🚀",
        "titulo": "La nave espacial reutilizable Shenlong libera un nuevo objeto misterioso en órbita",
        "cuerpo": (
            "El avión espacial reutilizable chino Shenlong ('Dragón Divino'), que lleva meses en órbita "
            "en misión secreta, liberó otro objeto cuya naturaleza y función permanecen sin confirmar. "
            "El episodio ha renovado el interés internacional por el programa orbital chino y sus "
            "capacidades tecnológicas en materia de satélites de servicio, reabastecimiento en órbita "
            "y tecnologías de doble uso civil-militar. China avanza en paralelo en el desarrollo del "
            "cohete reutilizable Larga Marcha 10, pieza clave del programa lunar tripulado previsto "
            "antes de 2030."
        ),
        "fuente_label": "Gizmodo ES — La nave reutilizable de China libera otro objeto en el espacio",
        "fuente_url": "https://es.gizmodo.com/la-enigmatica-nave-reutilizable-de-china-libera-otro-objeto-en-el-espacio-y-alimenta-las-sospechas-sobre-su-programa-orbital-2000243625",
    },
    {
        "emoji": "☀️",
        "titulo": "El proyecto espacial más ambicioso de China: una central solar en órbita geoestacionaria",
        "cuerpo": (
            "China avanza en su proyecto de construir una estación de energía solar en órbita geoestacionaria "
            "a 36.000 km de altitud, donde el Sol brilla de forma continua sin interrupciones nocturnas ni "
            "nubes. La hoja de ruta contempla pruebas de generación y transmisión de energía en órbita baja "
            "para 2028, con el despliegue de la estación definitiva para 2030. La potencia inicial estimada "
            "es de 1 megavatio, pero el objetivo a largo plazo es convertirla en una fuente de energía "
            "limpia a escala industrial. Se trata del proyecto de infraestructura espacial más ambicioso "
            "de la historia."
        ),
        "fuente_label": "Ecoticias — El proyecto más arriesgado de China: energía solar desde el espacio",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-espacio-estacion-solar",
    },
    {
        "emoji": "🤝",
        "titulo": "Xi Jinping y el presidente de Kazajistán firman acuerdos bilaterales en Shanghái",
        "cuerpo": (
            "El 16 de julio, el presidente Xi Jinping recibió en Shanghái al presidente kazajo "
            "Kassym-Jomart Tokayev. Ambos mandatarios firmaron múltiples acuerdos en materia de economía, "
            "comercio, transporte, finanzas públicas y comunicación, profundizando la cooperación entre "
            "las dos naciones en el marco de la Ruta de la Seda y de la integración euroasiática. La "
            "reunión se enmarca en la creciente agenda diplomática de China en Asia Central."
        ),
        "fuente_label": "Observatorio de Política China — Resumen política exterior 10-16 julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-67/",
    },
    {
        "emoji": "🌍",
        "titulo": "China presenta su modelo de gobernanza de IA ante la ONU",
        "cuerpo": (
            "El 6 de julio, China presentó su posición ante el Diálogo Global Inaugural de la ONU sobre "
            "la Gobernanza de la Inteligencia Artificial, abogando por un marco multilateral que evite la "
            "concentración del poder tecnológico y garantice el acceso equitativo a los beneficios de la "
            "IA para todos los países, especialmente los del Sur Global. La propuesta china contrasta con "
            "los modelos de gobernanza promovidos por Occidente y ha recibido respaldo de numerosas "
            "delegaciones del mundo en vías de desarrollo."
        ),
        "fuente_label": "La Jornada — China desafía a Washington con nuevo modelo para gestionar la IA",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/07/17/politica/china-desafia-a-occidente-con-nuevo-modelo-alternativo-para-gestionar-la-ia",
    },
    {
        "emoji": "🛸",
        "titulo": "Conferencia de Información Aeroespacial 2026: BeiDou, teledetección y computación espacial",
        "cuerpo": (
            "Los días 16 y 17 de julio, Pekín acogió la Conferencia de Información Aeroespacial 2026, donde "
            "se presentaron los últimos avances en teledetección satelital, el sistema integrado de "
            "navegación-comunicación-teledetección BeiDou y tecnologías de computación espacial. BeiDou, "
            "el GPS chino, ya cubre todo el planeta y se está convirtiendo en pieza clave de la economía "
            "digital tanto en China como en decenas de países socios de la Iniciativa de la Franja y la Ruta."
        ),
        "fuente_label": "CGTN — Tech innovation unlocks new growth momentum for China's economy",
        "fuente_url": "https://news.cgtn.com/news/2026-07-16/Tech-innovation-unlocks-new-growth-momentum-for-China-s-economy-1OOMQp36DmM/share_amp.html",
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
    title = "China Al Dia — Semana 14-20 Julio 2026"
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
