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
        "emoji": "🌊",
        "titulo": "China inaugura el primer centro de datos submarino del mundo, alimentado por energía eólica marina",
        "cuerpo": (
            "El proyecto más futurista del año cobra vida: HiCloud Technology, en colaboración con agencias del gobierno chino, "
            "ha puesto en plena operación el primer centro de datos submarino del mundo alimentado exclusivamente con energía "
            "eólica marina. La instalación se encuentra a unos 10 km de la costa del Área Especial de Lin-gang (Shanghái), a "
            "unos 9 metros de profundidad, rodeada de un parque eólico de más de 50 turbinas. Alberga 2.000 servidores con una "
            "capacidad de 24 megavatios y usa el agua del océano para refrigeración pasiva. El coste de construcción fue de "
            "aproximadamente 226 millones de dólares. China ya planifica un clúster de centros de datos submarinos con una "
            "capacidad total de 500 MW, marcando el inicio de una nueva era para la infraestructura digital global."
        ),
        "fuente_label": "Gizmodo — China Turns on the World's First Underwater Data Center",
        "fuente_url": "https://gizmodo.com/china-turns-on-the-worlds-first-underwater-data-center-2000769502",
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23 en órbita: un astronauta vivirá un año en el espacio",
        "cuerpo": (
            "La misión Shenzhou-23, lanzada el 24 de mayo, sigue su curso con tres astronautas a bordo de la estación espacial "
            "Tiangong. El hito más notable: uno de los tripulantes completará 365 días continuos en órbita, un récord absoluto "
            "para China que permitirá estudiar los efectos de la microgravedad en el cuerpo humano. La misión la comandan Zhu "
            "Yangzhu (veterano de la Shenzhou-16), Zhang Zhiyuan (ex piloto de combate) y Lai Ka-ying, primera astronauta "
            "procedente de Hong Kong y doctora en informática forense. Esta expedición forma parte de la hoja de ruta que busca "
            "llevar a astronautas chinos a la superficie lunar antes de 2030."
        ),
        "fuente_label": "Infobae — Un año en órbita: China da un paso decisivo en su programa lunar",
        "fuente_url": "https://www.infobae.com/america/mundo/2026/05/24/un-ano-en-orbita-china-da-un-paso-decisivo-en-su-programa-lunar-con-el-lanzamiento-de-la-mision-shenzhou-23/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek lanza V4: 1,6 billones de parámetros entrenados con el 73% menos de coste",
        "cuerpo": (
            "La empresa china DeepSeek presentó su nuevo modelo de inteligencia artificial DeepSeek V4 Pro Max, con 1,6 billones "
            "de parámetros totales y un contexto máximo de un millón de tokens. Lo más llamativo es su eficiencia: el coste de "
            "entrenamiento equivalió al 27% del coste de la versión anterior, una demostración de que China avanza hacia modelos "
            "cada vez más potentes y económicos. El modelo supera a los mejores sistemas de código abierto disponibles en pruebas "
            "de razonamiento y conocimiento del mundo, y solo es superado ligeramente por Gemini Pro 3.1 de Google. Disponible "
            "bajo licencia MIT, accesible vía web, app móvil y API para desarrolladores."
        ),
        "fuente_label": "France 24 Español — DeepSeek lanza su esperado nuevo modelo de IA",
        "fuente_url": "https://www.france24.com/es/minuto-a-minuto/20260424-la-empresa-china-deepseek-lanza-su-esperado-nuevo-modelo-de-ia",
    },
    {
        "emoji": "⚡",
        "titulo": "8.500 robots con IA para gestionar la red eléctrica más grande del mundo",
        "cuerpo": (
            "La State Grid Corporation of China ha reservado cerca de 1.000 millones de dólares (6.800 millones de yuanes) para "
            "adquirir 8.500 robots con inteligencia artificial en 2026. Las unidades sustituirán a trabajadores humanos en las "
            "tareas de mayor riesgo: mantenimiento de torres de alta tensión, inspección de subestaciones en zonas remotas y "
            "reparación de líneas en condiciones extremas. A lo largo del XV Plan Quinquenal (2026-2030), la inversión total de "
            "las dos grandes eléctricas estatales en modernización de red alcanzará los 4 billones de yuanes (≈ 574.000 millones "
            "de dólares). Un proyecto sin precedentes que combina robótica, IA y energía limpia a escala nacional."
        ),
        "fuente_label": "Vozpópuli — China encarga 8.500 robots con IA para gestionar su red eléctrica",
        "fuente_url": "https://www.vozpopuli.com/indux/china-encarga-8-500-robots-con-inteligencia-artificial-para-gestionar-la-red-electrica-mas-grande-del-mundo-y-se-gastara-1-000-millones-de-dolares-solo-en-2026/2984/",
    },
    {
        "emoji": "☀️",
        "titulo": "Robots instalando paneles solares a 4.300 metros de altitud en el Tíbet",
        "cuerpo": (
            "Un proyecto solar de 300 MW en Chamdo (Región Autónoma del Tíbet / Xizang) ha desplegado robots de instalación "
            "adaptados a la alta montaña para afrontar condiciones extremas: escasez de oxígeno, clima severo y una ventana de "
            "construcción de menos de cinco meses al año. Los robots realizan navegación autónoma, posicionamiento preciso e "
            "instalación integrada de paneles, respaldados por una red 5G para supervisión en tiempo real. Una vez en "
            "funcionamiento pleno, el proyecto generará unos 530 millones de kWh anuales, suficientes para cubrir las necesidades "
            "de 1,38 millones de personas, además de haber generado casi 15 millones de yuanes en ingresos para comunidades locales."
        ),
        "fuente_label": "China Daily — Robots install solar panels at Xizang's 4,300-meter altitude project",
        "fuente_url": "https://www.chinadaily.com.cn/a/202605/05/WS69f9a840a310d6866eb46ee3.html",
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior de China crece un 15,3% en los primeros cinco meses de 2026",
        "cuerpo": (
            "El valor total de las importaciones y exportaciones de China alcanzó los 20,68 billones de yuanes (≈ 2,86 billones "
            "de dólares) entre enero y mayo de 2026, un aumento interanual del 15,3%. Las exportaciones crecieron un 11,8%, "
            "hasta los 11,91 billones de yuanes, mientras que las importaciones se dispararon un 20,5% hasta los 8,77 billones, "
            "lo que refleja una reactivación de la demanda interna. La producción industrial aumentó un 5,4% interanual en el "
            "mismo período, con los sectores de alta tecnología y fabricación avanzada como principales motores del crecimiento."
        ),
        "fuente_label": "Empresas Exterior — Exportaciones de China crecen 21,8% en 2026",
        "fuente_url": "https://empresaexterior.com/art/101805/las-exportaciones-de-china-se-disparan-un-218-al-inicio-de-2026-y-baten-todas-las-previsiones",
    },
    {
        "emoji": "🌏",
        "titulo": "China presidirá la APEC 2026 en Shenzhen con la IA y el libre comercio como ejes",
        "cuerpo": (
            "China acogerá por tercera vez la cumbre del Foro de Cooperación Económica Asia-Pacífico (APEC), con la reunión "
            "de líderes económicos prevista para el 18 y 19 de noviembre en Shenzhen. El lema elegido es 'Building an "
            "Asia-Pacific Community to Prosper Together'. La agenda gira en torno a tres ejes: gobernanza de la IA centrada "
            "en el bien común, resiliencia de las cadenas de suministro globales e infraestructura digital. En 2026 se han "
            "programado casi 300 reuniones ministeriales y técnicas en toda China para preparar el consenso político previo "
            "al encuentro cumbre de noviembre."
        ),
        "fuente_label": "Diario Financiero — China despliega su potencial tecnológico para la APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "🎬",
        "titulo": "28.ª edición del Festival Internacional de Cine de Shanghái",
        "cuerpo": (
            "Del 12 al 21 de junio, Shanghái acoge la 28ª edición de su Festival Internacional de Cine (SIFF), uno de los "
            "certámenes cinematográficos más importantes de Asia. El festival reúne a realizadores, productores y actores de "
            "decenas de países y consolida a la ciudad como un hub cultural global. En paralelo, el 15 de junio Shanghai "
            "Disneyland celebró su décimo aniversario, con celebraciones y nuevas atracciones que refuerzan la posición del "
            "parque como uno de los más visitados de Asia. La agenda cultural de Shanghái en junio refleja la apertura y "
            "dinamismo de la ciudad como capital cosmopolita de China."
        ),
        "fuente_label": "CGTN Español — Festival de Cine de Shanghái 2026",
        "fuente_url": "https://espanol.cgtn.com/",
    },
    {
        "emoji": "📜",
        "titulo": "China publica un libro blanco sobre una gobernanza global más justa",
        "cuerpo": (
            "El 17 de junio, la Oficina de Información del Consejo de Estado presentó el libro blanco 'Una gobernanza global "
            "más justa y equitativa: principios, propuestas y acciones de China'. El documento expone la visión china de "
            "reforma de las instituciones multilaterales y defiende un orden internacional más representativo para los países "
            "en desarrollo. La presentación coincide con un periodo de intensa actividad diplomática china y se enmarca en la "
            "estrategia de proyección global del XV Plan Quinquenal (2026-2030), que sitúa a China como promotora activa de "
            "un multilateralismo renovado."
        ),
        "fuente_label": "CGTN — China's White Paper on Global Governance",
        "fuente_url": "https://www.cgtn.com/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de junio de %Y")
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
    title = "China Al Dia — Semana 11-18 Junio 2026"
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
