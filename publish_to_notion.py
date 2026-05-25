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
        "emoji": "🚀",
        "titulo": "Shenzhou-23: China lanza tres taikonautas al espacio con una misión histórica de un año en órbita",
        "cuerpo": (
            "El 24 de mayo de 2026, a las 23:08 hora de Pekín, un cohete Larga Marcha 2F despegó desde "
            "el centro de Jiuquan con tres taikonautas a bordo rumbo a la estación espacial Tiangong. La "
            "tripulación la forman el comandante Zhu Yangzhu, Zhang Zhiyuan y Lai Ka-ying —también conocida "
            "como Li Jiaying—, la primera astronauta de Hong Kong en volar al espacio. El hito más "
            "destacado: uno de los tres astronautas permanecerá un año entero en órbita, la estancia "
            "individual más larga jamás planificada por el programa espacial chino. La misión busca explorar "
            "los límites de la adaptabilidad humana en microgravedad, un paso crucial en la carrera china "
            "hacia el alunizaje tripulado antes de 2030."
        ),
        "fuente_label": "Infobae — Un año en órbita: China da un paso decisivo con la Shenzhou-23",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/24/un-ano-en-orbita-china-da-un-paso-decisivo-en-su-programa-lunar-con-el-lanzamiento-de-la-mision-shenzhou-23/",
    },
    {
        "emoji": "🤝",
        "titulo": "Cumbre Trump-Xi en Pekín: 'acuerdos comerciales fantásticos' y un nuevo mecanismo bilateral",
        "cuerpo": (
            "Del 13 al 15 de mayo, Pekín acogió la primera visita de Donald Trump a China en su segundo "
            "mandato. El resultado principal fue la creación del 'Board of Trade', un mecanismo bilateral "
            "permanente para supervisar compromisos comerciales, gestionar disputas y evitar nuevas "
            "escaladas arancelarias. Xi acordó la compra de 200 aviones Boeing y se abrieron nuevas vías "
            "para empresas estadounidenses en el mercado chino. Aunque no hubo un gran acuerdo estructural, "
            "ambas potencias consolidaron un modelo de 'competencia gestionada' orientado a evitar que la "
            "rivalidad derive en confrontación. Trump calificó los resultados de 'fantásticos' al abandonar Pekín."
        ),
        "fuente_label": "La Nación — Acuerdos comerciales y las conclusiones de la cumbre Trump-Xi",
        "fuente_url": "https://www.lanacion.com.ar/el-mundo/acuerdos-comerciales-y-una-advertencia-sobre-taiwan-las-conclusiones-de-la-cumbre-en-pekin-entre-nid15052026/",
    },
    {
        "emoji": "🤖",
        "titulo": "8.500 robots con IA para gestionar la red eléctrica más grande del mundo",
        "cuerpo": (
            "La State Grid Corporation of China, gestora de la red eléctrica más grande del planeta, "
            "invertirá 6.800 millones de yuanes (~1.000 millones de dólares) en 2026 para desplegar una "
            "flota de 8.500 robots con inteligencia artificial. La flota incluye unos 5.000 robots "
            "cuadrúpedos tipo perro robot, 500 humanoides para tareas complejas en redes de ultra alta "
            "tensión, y 3.000 robots con brazos articulados dobles. Sus funciones: inspeccionar "
            "subestaciones remotas, monitorizar redes de transmisión y realizar mantenimiento en entornos "
            "peligrosos o inaccesibles. El gasto total del sector eléctrico en robótica superará los "
            "10.000 millones de yuanes en 2026."
        ),
        "fuente_label": "Interesting Engineering — China plans 8,500 AI robots for power grid",
        "fuente_url": "https://interestingengineering.com/ai-robotics/china-8500-robots-power-grid",
    },
    {
        "emoji": "💾",
        "titulo": "China bloquea los chips Nvidia H200 para impulsar sus semiconductores domésticos",
        "cuerpo": (
            "Pese a que Washington autorizó en diciembre de 2025 la venta de chips Nvidia H200 a diez "
            "grandes empresas tecnológicas chinas —entre ellas Alibaba, Tencent y ByteDance—, Pekín ha "
            "bloqueado las importaciones para dirigir la inversión hacia fabricantes nacionales como "
            "Huawei. Hasta la fecha, ni un solo chip H200 ha sido enviado a China. La estrategia es "
            "clara: acelerar la adopción del Huawei Ascend 910C, el chip chino más avanzado, capaz de "
            "ofrecer un rendimiento comparable al H100 de Nvidia en cargas de trabajo específicas. La IA "
            "fue el gran ausente de las conversaciones formales en la cumbre Trump-Xi, pero sigue siendo "
            "el campo de batalla tecnológico central entre ambas potencias."
        ),
        "fuente_label": "CNBC — Trump's China visit sparks questions over chip exports",
        "fuente_url": "https://www.cnbc.com/2026/05/15/the-tech-download-trump-xi-talks-chips-rare-earths.html",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar china supera al carbón por primera vez en capacidad instalada",
        "cuerpo": (
            "En 2026, China alcanza un punto de inflexión energético sin precedentes: la capacidad solar "
            "instalada supera por primera vez a la del carbón, el combustible que dominó su sistema "
            "eléctrico durante décadas. El país está añadiendo más de 300 GW de nueva capacidad renovable "
            "este año, a un ritmo de 100 paneles solares por segundo. La capacidad eléctrica total de "
            "China superará los 4.000 millones de kilovatios antes de que termine el segundo trimestre. "
            "A finales de 2026, las energías no fósiles representarán alrededor del 63% de la capacidad "
            "instalada, mientras el peso del carbón descenderá hasta el 31%."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD y los coches eléctricos chinos conquistan el mundo: 400.000 unidades exportadas en abril",
        "cuerpo": (
            "En abril de 2026, China batió otro récord: más de 400.000 vehículos eléctricos e híbridos "
            "exportados en un solo mes, cifra sin precedentes en la historia de la industria automovilística "
            "global. BYD, que encabeza las exportaciones, ha elevado su objetivo de ventas internacionales "
            "para 2026 hasta 1,5 millones de unidades. La marca ya es el cuarto fabricante de eléctricos "
            "más vendido en Europa, con una cuota del 6,8% entre enero y marzo de 2026, por detrás solo "
            "de Volkswagen, BMW y Tesla."
        ),
        "fuente_label": "Movilidad Eléctrica — BYD y exportaciones de vehículos eléctricos chinos",
        "fuente_url": "https://movilidadelectrica.com/exportaciones-vehiculos-electricos-byd-mg-otras-marcas-oxigeno-industria-china/",
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e-7: la misión que buscará agua en la Luna sale en agosto de 2026",
        "cuerpo": (
            "China se prepara para el lanzamiento de Chang'e-7 en agosto de 2026, con destino al polo "
            "sur lunar. La misión incluye un orbitador, un módulo de aterrizaje, un rover y una sonda "
            "mini-saltadora diseñada para explorar los cráteres en sombra permanente donde se sospecha "
            "la existencia de hielo de agua. Si se confirma, sería un recurso vital para las futuras "
            "bases lunares. La misión es un paso clave en el programa que busca llevar taikonautas a "
            "la Luna antes de 2030, consolidando a China como segunda potencia espacial mundial."
        ),
        "fuente_label": "The Planetary Society — Chang'e-7: China's water-hunting lunar mission",
        "fuente_url": "https://www.planetary.org/space-missions/change-7",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
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
    title = "China Al Dia — Semana 19-25 Mayo 2026"
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
