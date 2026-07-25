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
        "emoji": "🌏",
        "titulo": "APEC 2026 en Chengdu: China lidera la agenda digital e IA de Asia-Pacífico",
        "cuerpo": (
            "El 23 de julio, la Reunión Ministerial de APEC sobre Tecnologías Digitales e IA concluyó en "
            "Chengdu con la adopción de la Declaración de Chengdu, un acuerdo entre las 21 economías del "
            "foro para impulsar conjuntamente la IA y las tecnologías digitales. Bajo el lema 'Tecnologías "
            "Digitales e IA para el Empoderamiento de una Comunidad de Asia-Pacífico', más de 1.000 delegados "
            "acordaron acelerar la transformación digital de industrias tradicionales y desarrollar "
            "infraestructuras de comunicación de nueva generación. El sector de IA de Chengdu alcanza ya "
            "los 22.100 millones de dólares, consolidando la ciudad como gran polo tecnológico mundial."
        ),
        "fuente_label": "People's Daily Español — Reunión Ministerial APEC adopta Declaración de Chengdu",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0724/c31621-20481321.html",
    },
    {
        "emoji": "🤖",
        "titulo": "DeepSeek-R1: el nuevo 'momento Sputnik' de la inteligencia artificial china",
        "cuerpo": (
            "El 21 de julio, DeepSeek lanzó su modelo DeepSeek-R1, comparado por los medios con el "
            "histórico lanzamiento del Sputnik soviético de 1957 por el impacto que supone para el "
            "equilibrio tecnológico global. El modelo supera en varias métricas clave a los modelos "
            "occidentales más avanzados. Paralelamente, fuentes del sector confirman que DeepSeek está "
            "desarrollando sus propios chips de IA para reducir dependencias externas, y que la startup "
            "estudia una posible salida a bolsa en China en 2027. La dirección priorizará la investigación "
            "de vanguardia por encima de la comercialización a corto plazo."
        ),
        "fuente_label": "La República ES — DeepSeek-R1 marca un nuevo hito en la IA",
        "fuente_url": "https://larepublica.es/2026/07/21/china-desafia-a-occidente-el-lanzamiento-de-deepseek-r1-marca-un-nuevo-hito-en-la-inteligencia-artificial/",
    },
    {
        "emoji": "🏫",
        "titulo": "China abre en Shanghái la primera 'escuela mundial para robots humanoides'",
        "cuerpo": (
            "Shanghái inauguró en julio el primer centro de entrenamiento heterogéneo de robots humanoides "
            "del mundo: más de 5.000 m2 donde más de 100 tipos distintos de robots de más de una docena "
            "de fabricantes entrenan simultáneamente y comparten datos entre sí. La producción china de "
            "robots humanoides superará las 100.000 unidades en 2026. El robot AgiBot Genie G2 ya "
            "demostró en junio una jornada continua de 64 horas en una fábrica de tabletas con una tasa "
            "de éxito del 99,99%. El Gobierno tiene como objetivo instalar 10.000 humanoides avanzados "
            "en fábricas antes de que acabe el año."
        ),
        "fuente_label": "WWWhatsnew — Centro entrenamiento robots humanoides Shanghái",
        "fuente_url": "https://wwwhatsnew.com/2026/05/27/centro-entrenamiento-robots-humanoides-shanghai-china-2026/",
    },
    {
        "emoji": "🦾",
        "titulo": "China concentra el 70% de robots cuadrúpedos y la mitad de humanoides del mundo",
        "cuerpo": (
            "Un informe publicado esta semana confirma que China concentra aproximadamente el 70% de las "
            "ventas mundiales de robots cuadrúpedos y cuenta con más de 400 modelos distintos de robots "
            "humanoides, cifra que supera la mitad de todos los modelos disponibles en el mercado global. "
            "Según el Ministerio de Industria y Tecnología de la Información (MIIT), más del 30% de las "
            "grandes empresas industriales chinas ya han incorporado la inteligencia artificial en sus "
            "procesos productivos."
        ),
        "fuente_label": "Prensa Latina — China con liderazgo en robótica inteligente e IA",
        "fuente_url": "https://www.prensa-latina.cu/2026/07/20/china-con-liderazgo-en-robotica-inteligente-ia-y-otras-industrias/",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior de China sube un 16,9% en el primer semestre de 2026",
        "cuerpo": (
            "El comercio exterior de China alcanzó los 25,47 billones de yuanes (unos 3,75 billones de "
            "dólares) entre enero y junio de 2026, superando por primera vez la barrera de los 25 billones "
            "en un semestre, con un crecimiento interanual del 16,9%. Las exportaciones ascendieron a "
            "14,73 billones de yuanes (+13,4%), acumulando 11 trimestres consecutivos de crecimiento. "
            "Las importaciones sumaron 10,74 billones de yuanes (+22,1%). El PIB del segundo trimestre "
            "creció un 4,3% interanual, impulsado especialmente por el sector exportador de alta tecnología, "
            "con las exportaciones vinculadas a IA y electrónica creciendo un 27%."
        ),
        "fuente_label": "People's Daily Español — Comercio exterior de China crece 16,9%",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0715/c31620-20477940.html",
    },
    {
        "emoji": "⚡",
        "titulo": "China construye 339 GW de nueva capacidad renovable: líder mundial en energía limpia",
        "cuerpo": (
            "Según el Global Energy Monitor, China tiene en construcción 180 GW de energía solar y "
            "159 GW de energía eólica, totalizando 339 GW de nueva capacidad renovable, casi nueve "
            "veces lo que construye EE.UU. en el mismo período. China ya tiene instalada más del doble "
            "de capacidad eólica y solar que cualquier otro país del mundo, y está en camino de alcanzar "
            "1.200 GW de capacidad instalada antes de 2027, seis años antes de lo proyectado. La "
            "iniciativa Ruta de la Seda Verde amplía además la inversión renovable a los países socios "
            "de la Franja y la Ruta."
        ),
        "fuente_label": "Ambientum — Estrategia energética de China: liderazgo y renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 y Shenzhou-23: China acelera hacia la Luna y consolida su estación espacial",
        "cuerpo": (
            "La misión tripulada Shenzhou-23, lanzada el 24 de mayo, sigue en órbita consolidando la "
            "capacidad china para misiones de larga duración. La misión Chang'e-7 completa sus "
            "preparativos finales con lanzamiento previsto para agosto de 2026: explorará el polo sur "
            "lunar en busca de agua en forma de hielo en cráteres en sombra permanente. China y Rusia "
            "avanzan en el proyecto ILRS (Estación Internacional de Investigación Lunar) con planes de "
            "construir una central eléctrica en la Luna para alimentar una base permanente antes de 2030. "
            "La NASA reconoció públicamente la competencia real con China por regresar a la Luna."
        ),
        "fuente_label": "Okdiario — China en la Luna 2026: misiones y objetivos",
        "fuente_url": "https://okdiario.com/ciencia/china-luna-2026-misiones-logros-objetivos-16568199",
    },
    {
        "emoji": "🗺️",
        "titulo": "BRI 2026: China pivota hacia la Ruta de la Seda Digital y Verde",
        "cuerpo": (
            "Analistas del Observatorio Global de la UDLAP señalan que China ha reorientado la Iniciativa "
            "Franja y Ruta hacia un modelo de cooperación de alta calidad: proyectos más pequeños, más "
            "sostenibles y con mayor contenido tecnológico. Los nuevos ejes son la Ruta de la Seda Digital "
            "(despliegue de redes 5G, e-commerce y ciudades inteligentes en países socios) y la Ruta de "
            "la Seda Verde (energías renovables y transporte limpio). La inversión en infraestructura "
            "digital y verde ya supera en volumen a la inversión tradicional en infraestructura física, "
            "marcando una nueva etapa de la cooperación internacional china."
        ),
        "fuente_label": "Observatorio Global UDLAP — BRI 2026: de la expansión a la cooperación estratégica",
        "fuente_url": "https://observatorioglobal.udlap.mx/the-belt-and-road-initiative-in-2026-from-expansion-to-strategic-high-quality-cooperation/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de julio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today} · Semana 19-25 julio 2026", "🇨🇳"),
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
    title = "China Al Dia — Semana 19-25 Julio 2026"
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
