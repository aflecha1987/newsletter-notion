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


# -----------------------------------------------------------------------
# EDICION: Semana del 4 al 10 de agosto de 2026
# -----------------------------------------------------------------------
NOTICIAS = [
    {
        "seccion": "PORTADA",
        "emoji": "📦",
        "titulo": "Las exportaciones chinas de julio suben un 23,9 % y lideran la demanda tecnológica global",
        "cuerpo": (
            "En julio de 2026, China registró exportaciones por 397.852 millones de dólares, con un "
            "crecimiento del 23,9 % respecto al mismo mes del año anterior. El superávit comercial del "
            "mes alcanzó 112.500 millones de dólares, y el acumulado enero–julio se situó en 687.370 "
            "millones de dólares. Los motores del crecimiento fueron los semiconductores, vehículos "
            "eléctricos (+57 % en el mes) y equipos de IA, que en conjunto representaron más del 40 % "
            "de los ingresos de exportación. Tanto el motor tecnológico como la diversificación geográfica "
            "hacia el Sur Global siguen siendo las claves del dinamismo exportador chino."
        ),
        "fuentes": [
            ("CNBC", "https://www.cnbc.com/2026/08/07/china-july-trade-exports-imports-surplus-imbalance-tariffs-.html"),
            ("Diario en Positivo", "https://www.diarioenpositivo.com/economia/economia-macro-exportaciones-chinas-crecieron-239-julio-aupadas-ventas-tecnologicas/20260807111310088278.html"),
            ("Revista EYN", "https://www.revistaeyn.com/centroamericaymundo/exportaciones-chinas-crecieron-178-en-julio-gracias-a-chips-o-vehiculos-electricos-BA31641451"),
        ],
    },
    {
        "seccion": "TECNOLOGÍA E IA",
        "emoji": "🤖",
        "titulo": "Kimi K3 y DeepSeek V4: China consolida su liderazgo en IA frontier",
        "cuerpo": (
            "El modelo Kimi K3 de Moonshot AI supera esta semana benchmarks de razonamiento matemático "
            "y código de los modelos líderes occidentales. Simultáneamente, DeepSeek V4 ha migrado toda "
            "su inferencia a hardware doméstico, eliminando la dependencia de chips Nvidia y reduciendo "
            "el coste de contexto largo en más del 50 %. La IA ya es el mayor motor del crecimiento "
            "económico chino: la electrónica e informática aportó más del 50 % de la expansión del PIB "
            "en el segundo trimestre, y las exportaciones relacionadas con IA representaron 1,1 puntos "
            "porcentuales del PIB nominal en los primeros cuatro meses del año, casi el triple de su "
            "peso en todo 2025."
        ),
        "fuentes": [
            ("CNBC — U.S. lead over China in AI is all but gone", "https://www.cnbc.com/2026/08/02/ai-model-competition-us-china.html"),
            ("Moncloa — Plan Maestro IA China 2026", "https://www.moncloa.com/2026/07/12/china-plan-maestro-ia-2026-3398625/"),
            ("Somos Innovación — China ventaja IA 2026", "https://somosinnovacion.global/llms-robots-y-autos-inteligentes-china-tendra-una-ventaja-en-ia-en-2026/"),
        ],
    },
    {
        "seccion": "TECNOLOGÍA E IA",
        "emoji": "🏆",
        "titulo": "Forbes China AI TOP 50: las empresas que lideran la revolución de productividad",
        "cuerpo": (
            "Forbes China publicó esta semana la lista de las 50 empresas más influyentes en IA de "
            "China en 2026, que van desde gigantes como Alibaba, Tencent y Baidu hasta startups como "
            "Moonshot AI, Zhipu AI y MiniMax. La selección destaca las compañías que aplican IA para "
            "multiplicar la productividad en industria, salud, finanzas y logística. China supera ya "
            "las 6.200 empresas de IA con una industria central valorada en más de 1,2 billones de yuanes."
        ),
        "fuentes": [
            ("NewsFile Corp — Forbes China AI TOP 50", "https://www.newsfilecorp.com/release/298372/Forbes-China-Unveils-the-2026-AI-TOP-50-These-Companies-Powering-a-Productivity-Revolution"),
            ("Educatrónica — IA en China 2026", "https://educatronica.org/2026/04/12/industria-inteligencia-artificial-china-2026/"),
        ],
    },
    {
        "seccion": "SEMICONDUCTORES",
        "emoji": "💾",
        "titulo": "CXMT debuta en bolsa con +472 %: el mayor IPO tecnológico del año en Asia",
        "cuerpo": (
            "ChangXin Memory Technologies (CXMT) completó su salida a bolsa en el mercado de Shanghai "
            "con una valorización de más del 472 % en su primer día de cotización, convirtiéndose en "
            "la empresa más valiosa listada en bolsas continentales chinas. El IPO captó 8.600 millones "
            "de dólares —el mayor listado de semiconductores jamás registrado en China—. Los ingresos "
            "de la empresa se dispararon un 700 % interanual en los primeros tres meses de 2026, "
            "impulsados por la demanda de IA y la sustitución de proveedores extranjeros. De inmediato "
            "anunció la construcción de una segunda planta en Pekín y espera llegar al 15 % del mercado "
            "global de DRAM para 2028."
        ),
        "fuentes": [
            ("Euronews — CXMT shares soar in blockbuster listing", "https://www.euronews.com/business/2026/07/27/china-memory-chipmaker-cxmts-shares-soar-in-blockbuster-listing"),
            ("Yahoo Finanzas ES — CXMT valorización 500%", "https://es-us.finanzas.yahoo.com/noticias/fabricante-chino-chips-cxmt-valoriz%C3%B3-150156777.html"),
            ("Bloomberg — CXMT IPO to challenge Samsung, SK Hynix, Micron", "https://www.bloomberg.com/news/features/2026-07-09/china-s-cxmt-chipmaker-eyes-ipo-to-challenge-samsung-sk-hynix-micron"),
        ],
    },
    {
        "seccion": "ENERGÍA",
        "emoji": "⚛️",
        "titulo": "China aprueba 8 nuevos reactores nucleares por 25.000 millones de dólares",
        "cuerpo": (
            "El Consejo de Estado aprobó el 31 de julio cuatro nuevos proyectos nucleares, que suman "
            "ocho reactores adicionales con una inversión total de más de 170.000 millones de yuanes "
            "(25.000 millones de dólares). Los proyectos incluyen la planta Jinqimen (Zhejiang), "
            "Taipingling (Guangdong), Zhuanghe (Liaoning) y Laiyang (Shandong). Utilizarán los diseños "
            "domésticos Hualong One (HPR1000) y Guohe One (CAP1400), ambos considerados reactores de "
            "tercera generación. El objetivo es alcanzar 110 GW de capacidad nuclear instalada para "
            "2030 —un salto del 80 % desde los 62,5 GW actuales—."
        ),
        "fuentes": [
            ("Bloomberg — China Approves $25 Billion Nuclear Expansion", "https://www.bloomberg.com/news/articles/2026-07-31/china-approves-25-billion-nuclear-expansion-as-energy-demand-soars"),
            ("El Día DO — China aprueba ocho nuevos reactores", "https://eldia.com.do/china-aprueba-ocho-nuevos-reactores-nucleares-por-23-700-millones-de-dolares/"),
            ("Caixin Global — Beijing Clears Eight New Reactors", "https://www.caixinglobal.com/2026-08-01/beijing-clears-eight-new-reactors-as-china-accelerates-nuclear-buildout-102470294.html"),
        ],
    },
    {
        "seccion": "TRANSPORTE",
        "emoji": "🚗",
        "titulo": "BYD supera un hito histórico: por primera vez vende más coches fuera que dentro de China",
        "cuerpo": (
            "BYD entregó en marzo de 2026 más vehículos en mercados internacionales que en su propio "
            "país por primera vez en su historia. Con una cuota de mercado global del 4,8 %, la marca "
            "china se sitúa ya en el sexto lugar del ranking mundial de fabricantes, por delante de "
            "Mercedes-Benz y BMW. BYD mantiene su objetivo de vender entre 1,5 y 1,6 millones de "
            "unidades en el exterior en 2026. En julio, las exportaciones de vehículos eléctricos "
            "chinos en conjunto crecieron un 57 %, y China en su totalidad exportó 905.000 turismos "
            "en un solo mes —más de todo lo exportado en 2019—."
        ),
        "fuentes": [
            ("Electrive — BYD sells more cars overseas than in China", "https://www.electrive.com/2026/03/02/byd-sells-more-cars-overseas-than-in-china-for-the-first-time/"),
            ("Híbridos y Eléctricos — 3 marcas chinas en top 10 mundial", "https://www.hibridosyelectricos.com/coches/por-encima-tesla-mercedes-bmw-china-coloca-3-sus-marcas-en-top-10-mundial-por-venta-coches_88549_102.html"),
            ("Motor16 — Exportaciones coches chinos 2026 récord", "https://www.motor16.com/las-ultimas-noticias/exportaciones-coches-chinos-2026-record/"),
        ],
    },
    {
        "seccion": "ESPACIO",
        "emoji": "🌕",
        "titulo": "China lidera la nueva carrera espacial al polo sur lunar",
        "cuerpo": (
            "Con misiones robóticas programadas para finales de 2026, China se posiciona como el actor "
            "más avanzado en la carrera para establecer presencia en el polo sur de la Luna. A diferencia "
            "de EE.UU., que afronta retrasos en su programa Artemis, China mantiene su cronograma con "
            "la misión Chang'e-7 y avanza en la construcción de la Estación Internacional de Investigación "
            "Lunar (ILRS), en colaboración con Rusia, Pakistán y más de 20 países del Sur Global. El "
            "polo sur lunar concentra hielo de agua, recurso clave para futuras colonias permanentes."
        ),
        "fuentes": [
            ("CNN Español — Carrera espacial polo sur lunar", "https://cnnespanol.cnn.com/2026/08/07/ciencia/carrera-espacial-luna-china-eeuu-trax"),
            ("Astro Aventura — China hacia la Luna 2030", "https://astroaventura.net/aeroespacial/objetivo-2030-los-grandes-avances-de-china-para-llevar-astronautas-a-caminar-sobre-la-superficie-de-la-luna/"),
        ],
    },
    {
        "seccion": "ESPACIO",
        "emoji": "🐕",
        "titulo": "Científicos chinos proponen robots tipo perro para custodiar la futura base lunar",
        "cuerpo": (
            "Investigadores de la Agencia Espacial China han publicado una propuesta en la que "
            "cuadrúpedos robóticos —similares a los fabricados por Unitree Robotics— protegerían y "
            "operarían en los exteriores de la Estación de Investigación Lunar durante las noches lunares, "
            "que duran 14 días terrestres. Los perros robot rastrearían la superficie en busca de hielo, "
            "inspeccionarían la infraestructura en busca de microfisuras y servirían como primera "
            "respuesta ante emergencias. Es la primera propuesta de su tipo: usar robots cuadrúpedos "
            "de IA para misiones de exploración lunar autónoma a larga duración."
        ),
        "fuentes": [
            ("La República PE — Científicos proponen perros robot para la Luna", "https://larepublica.pe/ciencia/2026/08/08/cientificos-espaciales-proponen-usar-perros-robots-para-proteger-la-estacion-de-investigacion-lunar-de-china-515584"),
        ],
    },
]

EDITION_TITLE = "China Al Dia — Semana 4-10 Ago 2026"
EDITION_DATE = "4 al 10 de agosto de 2026"


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p(f"Recopilacion de las noticias mas relevantes de China durante la semana del {EDITION_DATE}: tecnologia, economia, espacio y sociedad."),
        divider(),
    ]

    seccion_actual = None
    for n in NOTICIAS:
        if n["seccion"] != seccion_actual:
            seccion_actual = n["seccion"]
            blocks.append(h1(seccion_actual))

        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        for label, url in n["fuentes"]:
            blocks.append(p_link(label, url))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🇨🇳"},
        "cover": {"type": "external", "external": {
            "url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
        }},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": EDITION_TITLE}}]}
        },
        "children": build_blocks(),
    }

    print(f"Creando pagina en Notion: '{EDITION_TITLE}'")
    print(f"Noticias incluidas: {len(NOTICIAS)}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "").replace("-", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id}")
    print(f"\nListo!")
    print(f"URL: {page_url}")
    return page_url


if __name__ == "__main__":
    create_notion_page()
