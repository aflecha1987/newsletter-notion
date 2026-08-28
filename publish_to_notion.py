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
        "emoji": "📊",
        "titulo": "China mantiene PIB del 4,7 % y lidera con 'nuevas fuerzas productivas'",
        "cuerpo": (
            "En el primer semestre de 2026, la economia china crecio un 4,7 % interanual, dentro del "
            "objetivo oficial de 4,5-5 %. Las nuevas fuerzas productivas —semiconductores, vehiculos "
            "electricos, energias limpias e inteligencia artificial— aportaron mas del 40 % del "
            "crecimiento total. La produccion de baterias de litio aumento un 39,3 % y la penetracion "
            "acumulada de vehiculos de nueva energia en ventas minoristas alcanzo el 54,1 %."
        ),
        "fuente_label": "Prensa Latina — Economia china estable con PIB de 4,7 % y nuevas fuerzas productivas",
        "fuente_url": "https://www.prensa-latina.cu/2026/08/24/economia-china-estable-con-pib-de-47-y-nuevas-fuerzas-productivas/",
    },
    {
        "emoji": "🤖",
        "titulo": "Nuevo 'momento DeepSeek': China lanza el modelo de IA mas importante del año",
        "cuerpo": (
            "China ha protagonizado lo que analistas califican como el 'lanzamiento de IA mas importante "
            "de 2026'. La industria central de IA de China ya supera 1,2 billones de yuanes, con mas "
            "de 6.200 empresas activas en el sector y adopcion de IA en mas del 30 % de las empresas "
            "manufactureras. El nuevo modelo redefine la carrera global de la inteligencia artificial "
            "y demuestra la capacidad china de iterar a velocidades sin precedentes."
        ),
        "fuente_label": "Educatronica — Industria de la IA en China: que esta cambiando en 2026",
        "fuente_url": "https://educatronica.org/2026/04/12/industria-inteligencia-artificial-china-2026/",
    },
    {
        "emoji": "🌐",
        "titulo": "Conferencia Mundial de IA 2026: mas de 1.100 empresas y China como hub global",
        "cuerpo": (
            "La Conferencia Mundial de IA 2026 reunio a mas de 1.100 empresas participantes de todo "
            "el mundo y se consolido como la plataforma estrategica de referencia para que las "
            "multinacionales desplieguen sus proyectos en China. Ejecutivos internacionales destacaron "
            "el ecosistema de IA chino como el mas completo del planeta en cuanto a integracion de "
            "hardware, software e infraestructura de datos."
        ),
        "fuente_label": "CRI en espanol — Altos ejecutivos destacan el ecosistema de IA de China",
        "fuente_url": "https://espanol.cri.cn/2026/07/21/ARTI1784601918680690",
    },
    {
        "emoji": "📈",
        "titulo": "Superavit comercial record: mas de 100.000 millones de dolares por tres meses consecutivos",
        "cuerpo": (
            "China ha registrado un superavit comercial superior a los 100.000 millones de dolares "
            "durante tres meses consecutivos, impulsado principalmente por exportaciones de alta "
            "tecnologia: semiconductores, sistemas fotovoltaicos y vehiculos electricos. Solo en "
            "mayo, BYD incremento sus exportaciones de vehiculos de nueva energia un 80,7 % "
            "respecto al mismo mes de 2025."
        ),
        "fuente_label": "Sputnik Mundo — La alta tecnologia impulsa el superavit comercial de China",
        "fuente_url": "https://noticiaslatam.lat/20260820/la-modernizacion-industrial-y-la-alta-tecnologia-impulsan-el-superavit-comercial-de-china-dice-1174735241.html",
    },
    {
        "emoji": "⚡",
        "titulo": "China produce tanta energia renovable que su red no puede absorberla toda",
        "cuerpo": (
            "El exito de la transicion energetica china plantea un reto inedito: el pais ha tenido "
            "que curtailar unos 360 TWh de energia solar y eolica en el primer semestre de 2026. "
            "China se ha convertido en el primer pais del mundo donde el problema ya no es producir "
            "energia limpia suficiente, sino construir la red capaz de aprovecharla toda. Invierte "
            "masivamente en baterias de gran escala y modernizacion de la red electrica."
        ),
        "fuente_label": "Somos Electricos — China desperdicia 360 TWh de solar y eolica en seis meses",
        "fuente_url": "https://www.somoselectricos.com/curiosidades/china-tiene-tanta-energia-solar-eolica-que-empieza-desperdiciarla-360-twh-solo-seis-meses/20260820093543062406.html",
    },
    {
        "emoji": "🚗",
        "titulo": "China: el 70 % de los VE del planeta y normas de eficiencia mas exigentes del mundo",
        "cuerpo": (
            "Desde enero de 2026, China aplica una norma obligatoria de consumo energetico para VE, "
            "la mas exigente del mundo. El objetivo es que en 2030 los vehiculos de nueva energia "
            "representen el 30 % de todos los automoviles registrados. China ya fabrica mas del "
            "70 % de los vehiculos electricos del planeta y cerca del 85 % de las celdas de bateria "
            "a nivel mundial."
        ),
        "fuente_label": "ECOticias — China y el futuro electrico de sus carreteras",
        "fuente_url": "https://www.ecoticias.com/movilidad-electrica/china-pone-fecha-al-gran-cambio-de-sus-carreteras-tres-de-cada-diez-vehiculos-deberan-ser-electricos-o-hibridos-en-2030",
    },
    {
        "emoji": "🚄",
        "titulo": "China supera los 50.000 km de alta velocidad y desarrolla el tren mas rapido del mundo",
        "cuerpo": (
            "China ha cruzado la barrera de los 50.000 kilometros de red de alta velocidad ferroviaria, "
            "la mas extensa del planeta. A mediados de 2026 se inauguro la linea Xi'an-Shiyan (257 km, "
            "hasta 350 km/h). En paralelo, ingenieros chinos trabajan en un prototipo capaz de alcanzar "
            "450 km/h en pruebas y 400 km/h en operacion comercial, lo que lo convertiria en el tren "
            "de pasajeros mas veloz del mundo."
        ),
        "fuente_label": "Excelsior — China supera los 50.000 km de trenes de alta velocidad",
        "fuente_url": "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico",
    },
    {
        "emoji": "🚉",
        "titulo": "Primera linea ferroviaria privada de alta velocidad: 100 millones de pasajeros",
        "cuerpo": (
            "La primera linea ferroviaria de alta velocidad de China operada con capital privado, en "
            "la provincia de Zhejiang, ha transportado a mas de 100 millones de pasajeros desde su "
            "inauguracion, a menos de cuatro anos y medio de operacion. El exito abre la puerta a la "
            "participacion privada en nuevas lineas y demuestra la viabilidad economica del modelo "
            "sin subsidio estatal directo."
        ),
        "fuente_label": "Xinhua en espanol — Primera linea privada de alta velocidad supera 100 millones de pasajeros",
        "fuente_url": "https://spanish.news.cn/20260628/05e1abf0363347dd8a8d829c5211f64c/c.html",
    },
    {
        "emoji": "🏥",
        "titulo": "China lidera los ensayos clinicos globales y digitaliza la salud con IA",
        "cuerpo": (
            "El XV Plan Quinquenal de China (2026-2030) reconoce la biomedicina como industria pilar "
            "emergente, con la IA como catalizador para acortar plazos y reducir costos de I+D "
            "farmaceutica. China ya concentra el liderazgo global en ensayos clinicos de nuevas "
            "terapias oncologicas y edicion genetica. El gobierno impulsa un sistema digital de "
            "salud publica con IA para mejorar el acceso medico en todo el territorio."
        ),
        "fuente_label": "Gizmodo ES — El gran salto de China en medicina y terapias contra el cancer",
        "fuente_url": "https://es.gizmodo.com/el-gran-salto-de-china-en-medicina-domina-los-ensayos-y-gana-terreno-en-terapias-contra-el-cancer-2000250266",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · Semana 22-28 agosto 2026", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, energia e infraestructura.", bold=False),
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
    title = "China Al Dia — Semana 22-28 Ago 2026"
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
