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

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


NOTICIAS = [
    {
        "emoji": "🤝",
        "titulo": "Cumbre histórica Trump-Xi en Pekín: acuerdos fantásticos y apertura a empresas de EE.UU.",
        "cuerpo": (
            "Del 13 al 15 de mayo, Donald Trump visitó China en lo que Xi Jinping calificó de 'visita "
            "histórica' — el primer viaje de un mandatario estadounidense a Pekín desde 2017. Ambos "
            "líderes alcanzaron acuerdos en agricultura (200 aviones Boeing, petróleo, soja), energía "
            "e inteligencia artificial. Xi prometió que China 'se abrirá más ampliamente', ante la "
            "presencia de Elon Musk (Tesla/SpaceX), Tim Cook (Apple) y Jensen Huang (Nvidia). La "
            "cumbre abrió conversaciones sobre reducción gradual de aranceles y 'barreras de seguridad' "
            "conjuntas en IA. Xi definió el resultado como el inicio de 'una nueva relación bilateral "
            "de estabilidad estratégica constructiva'."
        ),
        "fuente_label": "Infobae — Trump y Xi cierran acuerdos fantásticos en Pekín",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/15/donald-trump-y-xi-jinping-se-preparan-para-un-segundo-dia-de-conversaciones-en-beijing/",
    },
    {
        "emoji": "🤖",
        "titulo": "China acelera la IA agéntica: de entrenar modelos a desplegarlos a escala masiva",
        "cuerpo": (
            "Alibaba, Tencent y ByteDance han pivotado en masa hacia la IA agéntica — sistemas que "
            "razonan y ejecutan tareas complejas de forma autónoma — . La carrera ya no es quién "
            "tiene el mejor modelo de lenguaje, sino quién despliega IA en productos reales a mayor "
            "escala. Alibaba lanzó un servicio 3D de restaurantes con su modelo generativo Tongyi "
            "Wanxiang. Los ingresos de la industria digital china crecieron un 12,9% en Q1 2026 "
            "impulsados por la inferencia masiva. China ya tiene 602 millones de usuarios de IA "
            "generativa — más de la mitad del total mundial — y el sector central de IA superó "
            "el billón de yuanes en valor en 2025."
        ),
        "fuente_label": "SCMP — China takes confident strides in AI innovation 2026",
        "fuente_url": "https://www.scmp.com/tech/tech-war/article/3338528/tech-war-china-takes-confident-strides-develop-more-ai-innovation-2026",
    },
    {
        "emoji": "💾",
        "titulo": "EE.UU. aprueba chips H200 de Nvidia para 10 firmas chinas; China acelera sus propios semiconductores",
        "cuerpo": (
            "En el marco de la cumbre Trump-Xi, EE.UU. autorizó a Alibaba, Tencent, ByteDance y "
            "JD.com la compra de chips H200 de Nvidia — aunque de momento sin entregas completadas. "
            "China mantiene cautela estratégica: teme que las importaciones frenen el impulso de "
            "sus propios semiconductores. Huawei (Ascend 910C), Moore Threads y MetaX aceleran su "
            "hoja de ruta. Jensen Huang admitió que Nvidia tiene 'cero por ciento de cuota de mercado' "
            "en China y que la política de exportación 'ya ha salido en gran medida por la culata'. "
            "China avanza hacia una infraestructura de IA de 'uso exclusivamente doméstico'."
        ),
        "fuente_label": "CNBC — U.S. clears H200 chip sales to 10 China firms",
        "fuente_url": "https://www.cnbc.com/2026/05/14/us-clears-h200-chip-sales-to-10-china-firms-as-nvidia-ceo-looks-for-breakthrough.html",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD bate el récord histórico de exportaciones: +71% en abril y 56% de cuota mundial",
        "cuerpo": (
            "BYD vendió 321.123 unidades en abril de 2026, con más de 130.000 exportadas — el "
            "primer mes en que sus ventas internacionales superan esa barrera, con un crecimiento "
            "del 71% interanual. El motor principal: el encarecimiento del petróleo por las "
            "tensiones en el Estrecho de Ormuz disparó la demanda de eléctricos en Asia-Pacífico, "
            "Europa y América Latina. China ya controla el 56% de la cuota global de vehículos "
            "eléctricos puros. BYD proyecta 1,6 millones de exportaciones en todo 2026, superando "
            "su objetivo previo de 1,5 millones."
        ),
        "fuente_label": "Bloomberg — BYD Exports Jump as Soaring Fuel Prices Spur EV Demand",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-05-01/byd-exports-jump-as-soaring-fuel-prices-spur-global-ev-demand",
    },
    {
        "emoji": "⚡",
        "titulo": "Hito sin precedentes: más del 60% de los coches vendidos en China en abril fueron eléctricos",
        "cuerpo": (
            "En abril de 2026, más del 60% de todos los vehículos vendidos en China fueron "
            "eléctricos o híbridos enchufables — la primera vez que una gran economía supera "
            "este umbral en un mes completo. El auge del precio del petróleo ha adelantado el "
            "punto de inflexión que los analistas preveían para finales de año. Las marcas "
            "domésticas — BYD, Li Auto, AITO (Huawei) y Xiaomi Auto — dominan el segmento, "
            "mientras los fabricantes tradicionales de combustión luchan por adaptarse. China "
            "avanza hacia la electrificación total de su parque automovilístico antes de 2035."
        ),
        "fuente_label": "CiberCuba — China rompe otro techo: 60% de coches eléctricos en abril",
        "fuente_url": "https://www.cibercuba.com/noticias/2026-04-27-u1-e13-s54124-nid327318-china-rompe-otro-techo-60-carros-vendidos-abril-serian",
    },
    {
        "emoji": "🦾",
        "titulo": "China despliega 8.500 robots IA para gestionar su red eléctrica: inversión de 1.000 millones de dólares",
        "cuerpo": (
            "La State Grid Corporation of China ha destinado 6.800 millones de yuanes (≈1.000 "
            "millones de dólares) para adquirir 8.500 robots con inteligencia artificial en 2026, "
            "en el 'Año Uno del Despliegue' de la robótica en infraestructura crítica. La flota "
            "incluye 500 robots humanoides para trabajos de ultra-alto voltaje, 5.000 robot dogs "
            "cuadrúpedos para patrullaje e inspección, y 3.000 robots de doble brazo con ruedas "
            "para mantenimiento. Los fabricantes Unitree Robotics, Deep Robotics, AgiBot, UBTech "
            "y Fourier Intelligence suministran la flota. El sector eléctrico total invertirá más "
            "de 10.000 millones de yuanes en robótica durante 2026."
        ),
        "fuente_label": "SCMP — China plans to invest billions on a robot army to run its power grid",
        "fuente_url": "https://www.scmp.com/economy/china-economy/article/3351323/china-plans-invest-billions-robot-army-run-its-power-grid",
    },
    {
        "emoji": "🚀",
        "titulo": "Tianzhou-10 se acopla con éxito a la Estación Espacial Tiangong",
        "cuerpo": (
            "El 11 de mayo de 2026, el cohete Larga Marcha CZ-7 Y11 despegó desde el Centro "
            "Espacial de Wenchang con la nave carguera Tianzhou-10. El acoplamiento con el "
            "módulo Tianhe de la estación Tiangong se completó con éxito pocas horas después, "
            "supervisado por la tripulación de la Shenzhou-21. La misión transporta suministros, "
            "equipamiento científico y combustible. China mantiene su programa de misiones "
            "espaciales intensivas en 2026: el lanzamiento de la Chang'e-7 al polo sur lunar "
            "está previsto para agosto y la misión tripulada Shenzhou-23 figura en el calendario anual."
        ),
        "fuente_label": "Eureka / Daniel Marín — Lanzamiento y acoplamiento del Tianzhou-10",
        "fuente_url": "https://danielmarin.naukas.com/2026/05/11/lanzamiento-y-acoplamiento-del-tianzhou-10-con-la-estacion-espacial-china/",
    },
    {
        "emoji": "📊",
        "titulo": "China fija meta: la economía digital alcanzará el 12,5% del PIB en 2030",
        "cuerpo": (
            "El XV Plan Quinquenal (2026-2030) introduce por primera vez el concepto de 'economía "
            "inteligente' como evolución de la economía digital, basada en la integración profunda "
            "de la IA en todos los sectores productivos. Las metas son concretas: el valor añadido "
            "de las industrias digitales clave representará el 12,5% del PIB para 2030; las seis "
            "grandes industrias emergentes (robótica inteligente, semiconductores, drones, "
            "biotecnología, nueva energía y espacio) superarán los 10 billones de yuanes en "
            "producción combinada. La IA, el 6G y la robótica son los tres pilares que China "
            "define como motores activos del crecimiento presente y futuro."
        ),
        "fuente_label": "The Conversation — China 2026-2030: cinco años de salto tecnológico estratégico",
        "fuente_url": "https://theconversation.com/2026-2030-cinco-anos-en-los-que-china-busca-consolidar-su-poder-global-mediante-la-tecnologia-la-autosuficiencia-y-la-proyeccion-exterior-278464",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio, robotica e inteligencia artificial.", bold=False),
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
    title = "China Al Dia — Semana 10-16 Mayo 2026"
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
