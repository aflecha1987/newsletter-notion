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
        "emoji": "🧠",
        "titulo": "GLM-5.2: China abre un nuevo «momento DeepSeek» en la IA mundial",
        "cuerpo": (
            "El 20 de junio, la startup china Zhipu AI lanzó GLM-5.2, un modelo de lenguaje de código abierto "
            "que está generando la misma conmoción en Silicon Valley que DeepSeek R1 a principios de 2025. "
            "El modelo supera a Claude Opus 4.8 en programación, arrebató el primer puesto a Fable 5 en "
            "Design Arena, y se sitúa justo por debajo de GPT-5.5 en benchmarks generales, siendo el modelo "
            "abierto con mayor rendimiento del mundo. Lo más llamativo: cuesta entre 5 y 7 veces menos que "
            "sus competidores occidentales (aprox. $1,50-$4,50 por millón de tokens). Las acciones de Zhipu "
            "en Hong Kong subieron un 42% en 48 horas, llevando la capitalización de la empresa por encima "
            "del billón de dólares de Hong Kong por primera vez."
        ),
        "fuente_label": "Le Grand Continent — GLM-5.2, un nuevo momento DeepSeek",
        "fuente_url": "https://legrandcontinent.eu/es/2026/06/23/con-glm-5-2-china-ha-abierto-un-nuevo-momento-deepseek/",
    },
    {
        "emoji": "💻",
        "titulo": "Kimi K2.6: el primer modelo open source que supera a GPT-5 en programación",
        "cuerpo": (
            "Moonshot AI publicó Kimi K2.6, primer modelo de código abierto que logró superar a GPT-5.4 en "
            "SWE-Bench Pro (58,6 puntos frente a 57,7), el benchmark de referencia para tareas de programación "
            "autónoma. El modelo soporta hasta 262.000 tokens de contexto y fue calificado por la revista "
            "Nature como 'otro momento DeepSeek'. La batalla china de la IA ya no es entre China y Occidente: "
            "ahora es también entre Moonshot AI, Zhipu AI, DeepSeek y Alibaba compitiendo entre sí, "
            "empujando los límites globales a una velocidad sin precedentes."
        ),
        "fuente_label": "Genbeta — Kimi K2 protagoniza otro momento DeepSeek",
        "fuente_url": "https://www.genbeta.com/inteligencia-artificial/kimi-k2-protagoniza-otro-momento-deepseek-este-modelo-razonador-libre-made-in-china-empata-casi-todo-gpt-5",
    },
    {
        "emoji": "👥",
        "titulo": "China ya tiene más usuarios de IA que ningún otro país: 602 millones",
        "cuerpo": (
            "China cuenta con 602 millones de usuarios de inteligencia artificial generativa, más de la mitad "
            "del total mundial. En el primer trimestre de 2026, las patentes relacionadas con IA crecieron un "
            "31,2% interanual. La iniciativa gubernamental 'IA Plus' apunta a que el 70% de los sectores "
            "productivos incorporen IA para 2027, y el 90% para 2030, con las industrias de IA superando "
            "los 10 billones de yuanes en valor para esa fecha."
        ),
        "fuente_label": "Somos Innovación — China ventaja en IA 2026",
        "fuente_url": "https://somosinnovacion.global/llms-robots-y-autos-inteligentes-china-tendra-una-ventaja-en-ia-en-2026/",
    },
    {
        "emoji": "📦",
        "titulo": "El comercio exterior chino explota en junio: acuerdo con EE.UU. dispara exportaciones",
        "cuerpo": (
            "El comercio exterior de China batió todas las previsiones en junio de 2026 gracias al acuerdo "
            "comercial alcanzado con Estados Unidos. Las exportaciones totales crecieron un 21,8% interanual, "
            "con las exportaciones de tierras raras repuntando un 32% entre mayo y junio. El acuerdo incluye "
            "compras agrícolas y de aviones comerciales por parte de China, rebajando la tensión arancelaria "
            "y abriendo el camino a negociaciones más amplias. El superávit comercial de China siguió en "
            "máximos históricos."
        ),
        "fuente_label": "EmpresaExterior — Exportaciones de China se disparan en junio",
        "fuente_url": "https://empresaexterior.com/art/98387/el-comercio-exterior-chino-se-dispara-en-junio-impulsado-por-el-nuevo-entendimiento-con-estados-unidos-superando-todas-las-expectativas",
    },
    {
        "emoji": "🌏",
        "titulo": "APEC 2026 en Shenzhen: los líderes del Pacífico acuerdan impulsar el libre comercio",
        "cuerpo": (
            "La cumbre APEC celebrada en Shenzhen concluyó con un amplio consenso para avanzar hacia un "
            "Área de Libre Comercio de Asia-Pacífico (FTAAP). China aprovechó la cita para exhibir el "
            "poder tecnológico de Shenzhen: transporte autónomo, drones de pasajeros en fase final de "
            "prueba y robots humanoides prestando servicios al público. El presidente Xi Jinping subrayó "
            "que China apuesta por el multilateralismo y el comercio abierto frente a las corrientes "
            "proteccionistas globales."
        ),
        "fuente_label": "Diario Financiero — China despliega potencial en APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "🤝",
        "titulo": "22 empresas chinas aterrizan en Argentina buscando negocios millonarios",
        "cuerpo": (
            "Una delegación de 22 empresas chinas de los sectores de tecnología, energía, minería y agro "
            "llegaron a Argentina en una misión comercial de alto nivel, la más amplia en años. Entre ellas "
            "destacan firmas de vehículos eléctricos, energías renovables y manufactura avanzada. Las "
            "exportaciones argentinas a China crecieron 9,7 puntos porcentuales en el primer trimestre "
            "de 2026. La misión busca cerrar acuerdos de inversión directa en litio, hidrógeno verde "
            "e infraestructura ferroviaria."
        ),
        "fuente_label": "La Nación Argentina — Desembarco chino en Argentina",
        "fuente_url": "https://www.lanacion.com.ar/economia/masivo-desembarco-chino-en-la-argentina-22-empresas-llegaron-en-busca-de-negocios-millonarios-nid19062026/",
    },
    {
        "emoji": "🌙",
        "titulo": "Chang'e-7 lista para agosto: China explora el polo sur de la Luna en busca de agua",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 han superado las pruebas previas al vuelo en la "
            "Base Espacial de Wenchang, confirmando el lanzamiento para agosto de 2026. La misión incluye "
            "un orbitador, módulo de aterrizaje, rover de superficie y una sonda mini-saltadora diseñada "
            "para acceder a cráteres en sombra permanente del polo sur lunar, donde se sospecha la "
            "existencia de agua en forma de hielo. El hallazgo de agua lunar sería un paso decisivo para "
            "la futura base habitada que China planea instalar antes de 2035."
        ),
        "fuente_label": "OKDiario — China en la Luna 2026: misiones y objetivos",
        "fuente_url": "https://okdiario.com/ciencia/china-luna-2026-misiones-logros-objetivos-16568199",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23 en órbita y Larga Marcha 10 supera segundo ensayo en junio",
        "cuerpo": (
            "La misión Shenzhou-23, lanzada el 24 de mayo, mantiene a tres taikonautas en la Estación "
            "Espacial Tiangong, el noveno vuelo tripulado consecutivo al módulo orbital chino, operativo "
            "de forma ininterrumpida desde 2021. Tiangong acogerá próximamente astronautas de países del "
            "Sur Global en misiones conjuntas. En paralelo, el cohete reutilizable Larga Marcha 10, pieza "
            "clave del programa lunar tripulado, completó con éxito su segundo ensayo en junio, acercando "
            "a China a su meta de alunizar astronautas antes de 2030."
        ),
        "fuente_label": "Infobae — Shenzhou-23, un año en órbita",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/24/un-ano-en-orbita-china-da-un-paso-decisivo-en-su-programa-lunar-con-el-lanzamiento-de-la-mision-shenzhou-23/",
    },
    {
        "emoji": "⚡",
        "titulo": "China supera el 40% de electricidad renovable: lidera la transición energética mundial",
        "cuerpo": (
            "En la primera mitad de 2026, la generación eléctrica de fuentes renovables superó el 40% "
            "del total en China, convirtiéndose en el pilar principal de su estructura energética. Con "
            "capacidad de fabricación solar que supera ampliamente la demanda global, BYD liderando el "
            "mercado mundial de vehículos eléctricos, y un plan de inversión de 1 billón de yuanes "
            "anuales en redes eléctricas limpias hasta 2030, China no solo cumple sus objetivos "
            "climáticos: los supera con años de antelación."
        ),
        "fuente_label": "Ambientum — Estrategia energética de China: renovables 2026",
        "fuente_url": "https://www.ambientum.com/ambientum/cambio-climatico/estrategia-energetica-china-guia-completa-de-energia-renovable.asp",
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
    title = f"China Al Dia — Semana 17-24 Junio 2026"
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
