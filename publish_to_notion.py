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
        "emoji": "🤝",
        "titulo": "Cumbre histórica Trump-Xi en Pekín: hacia una nueva era sino-estadounidense",
        "cuerpo": (
            "El presidente Donald Trump aterrizó el 13 de mayo en Pekín para una cumbre de dos días con "
            "Xi Jinping, la primera visita de un mandatario estadounidense a China desde 2017. Ambos líderes "
            "abrieron el encuentro con promesas de un 'futuro fantástico' para la relación bilateral. En la "
            "agenda: extensión de la tregua arancelaria, creación de una junta comercial bilateral, acuerdos "
            "en sectores aeroespacial, agrícola y energético, y negociaciones sobre IA. Xi Jinping reiteró: "
            "'Una y otra vez se ha demostrado que en una guerra comercial no hay vencedores.'"
        ),
        "fuente_label": "El Financiero — Trump y Xi abren cumbre con promesas de un 'futuro fantástico'",
        "fuente_url": "https://www.elfinanciero.com.mx/mundo/2026/05/13/trump-y-xi-jinping-abren-cumbre-en-pekin-con-promesas-de-un-futuro-fantastico-entre-eu-y-china/",
    },
    {
        "emoji": "💻",
        "titulo": "Hanyuan-2: China presenta la primera computadora cuántica de doble núcleo del mundo",
        "cuerpo": (
            "La empresa CAS Cold Atom Technology presentó oficialmente la Hanyuan-2, la primera computadora "
            "cuántica de átomos neutros con arquitectura de doble núcleo del planeta. La innovación consiste "
            "en dos núcleos independientes que, al dividir el procesamiento, minimizan las interferencias "
            "entre cúbits adyacentes y mejoran la escalabilidad futura del sistema. Un hito que consolida "
            "el liderazgo chino en computación cuántica y abre el camino a sistemas de mayor potencia."
        ),
        "fuente_label": "Canal 26 — China presenta la primera computadora cuántica de doble núcleo",
        "fuente_url": "https://www.canal26.com/tecnologia/2026/05/12/china-lidera-la-carrera-digital-presentaron-la-primera-computadora-cuantica-de-doble-nucleo-del-mundo/",
    },
    {
        "emoji": "🤖",
        "titulo": "KAI: el robot con piel háptica que dobla ropa, pone el lavavajillas y enhebra agujas",
        "cuerpo": (
            "La firma Kinetix AI presentó a KAI, un robot humanoide con piel háptica diseñado para el hogar. "
            "Puede ensamblar productos, poner el lavavajillas, doblar ropa o enhebrar una aguja. Su piel "
            "sensorial multicapa le permite percibir texturas y adaptar la presión de sus movimientos a cada "
            "tarea. Con movilidad avanzada y sistema de aprendizaje continuo, KAI representa la nueva frontera "
            "de la robótica doméstica china, sector que apunta a 100 millones de hogares para 2030."
        ),
        "fuente_label": "Cubadebate — China presenta a KAI, el robot con piel humana para el hogar",
        "fuente_url": "http://www.cubadebate.cu/noticias/2026/05/13/china-presenta-a-kai-el-nuevo-robot-con-piel-humana-que-ayuda-en-las-tareas-hogar/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4 se valora en 45.000 millones de dólares y escala con chips Huawei",
        "cuerpo": (
            "El mayor fondo estatal chino de semiconductores (el 'Big Fund') negoció liderar una ronda de "
            "financiación que valoraría DeepSeek en cerca de 45.000 millones de dólares, con Tencent como "
            "coinversor. Al mismo tiempo, DeepSeek V4 ya es totalmente compatible con los chips Huawei "
            "Ascend 950PR, acelerando el ecosistema tecnológico autónomo chino. Las ventas de chips de IA "
            "de Huawei se dispararon este año, superando a Nvidia en el mercado doméstico por primera vez."
        ),
        "fuente_label": "Diario Financiero — DeepSeek se acerca a una valoración de 45.000 millones",
        "fuente_url": "https://www.df.cl/internacional/ft/la-startup-china-de-ia-deepseek-se-acerca-a-una-valorizacion-de-us-45-000",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones chinas: +21,8% interanual, el mayor salto en cuatro años",
        "cuerpo": (
            "El comercio exterior de China arrancó 2026 con el mayor crecimiento en cuatro años: +21,8% "
            "interanual en los primeros dos meses, frente al 5,5% de 2025. Las exportaciones de alta "
            "tecnología se dispararon un 26,9%, con semiconductores, automóviles y buques liderando el "
            "repunte. China diversificó destinos con fuerza hacia Asia-Pacífico, América Latina y África, "
            "consolidando su papel como motor del comercio global en un entorno geopolítico desafiante."
        ),
        "fuente_label": "ING Think — China's trade growth starts 2026 strong with biggest gain in four years",
        "fuente_url": "https://think.ing.com/snaps/chinas-trade-growth-starts-2026-strong-with-biggest-gain-in-four-years-a/",
    },
    {
        "emoji": "🚗",
        "titulo": "Auto China 2026: el mayor salón automovilístico del mundo con 181 estrenos mundiales",
        "cuerpo": (
            "El Salón de Beijing 2026 (Auto China) se celebró del 24 de abril al 3 de mayo bajo el lema "
            "'El futuro de la inteligencia'. Con 380.000 m², 1.451 vehículos y 181 estrenos mundiales, fue "
            "el evento de automoción más importante del planeta este año. Los vehículos eléctricos e "
            "inteligentes dominaron la exposición, con BYD, NIO, Huawei y Xiaomi entre los protagonistas. "
            "China consolida su posición como el mayor mercado y exportador de vehículos eléctricos."
        ),
        "fuente_label": "V12 Magazine — Auto China 2026: China redefine el futuro del automóvil",
        "fuente_url": "https://v12magazine.com/actualidad/mundo/auto-china-2026-innovaciones/",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar supera al carbón en capacidad instalada en China",
        "cuerpo": (
            "En 2026, por primera vez en la historia, la capacidad instalada solar en China superará a la "
            "del carbón. El Consejo de Electricidad proyecta que las fuentes no fósiles alcanzarán el 63% "
            "de la capacidad instalada total antes de fin de año. China añadirá más de 400 millones de kW "
            "de nueva capacidad en 2026, más de 300 de fuentes renovables. El país fabrica más del 80% de "
            "los paneles solares del mundo y el 60% de las turbinas eólicas."
        ),
        "fuente_label": "EcoTicias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "⚡",
        "titulo": "China gestiona 1.840 GW renovables con almacenamiento hidroeléctrico a gran escala",
        "cuerpo": (
            "El crecimiento desbordado de renovables obligó a China a acelerar la construcción de embalses "
            "para gestionar excedentes de su red de 1.840 GW eólicos y solares. La nueva línea de ±800 kV "
            "Tíbet-Gran Bahía enviará más de 43.000 millones de kWh de electricidad limpia al sur del país. "
            "China ya no compite solo con fábricas: compite con un sistema energético completo e integrado "
            "que convierte la energía verde en una ventaja competitiva industrial sin precedentes."
        ),
        "fuente_label": "Ategi — China ya no compite solo con fábricas, compite con un sistema energético completo",
        "fuente_url": "https://ategi.com/2026/05/09/china-ya-no-compite-solo-con-fabricas-compite-con-un-sistema-energetico-completo/",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 en rampa de lanzamiento: exploración del polo sur lunar prevista en agosto",
        "cuerpo": (
            "Los módulos de la misión Chang'e-7 llegaron a la Base Espacial de Wenchang e iniciaron pruebas "
            "pre-lanzamiento con fecha prevista para agosto de 2026. La misión incluye orbitador, módulo de "
            "aterrizaje, rover y una sonda mini-saltadora diseñada para explorar cráteres en sombra permanente "
            "del polo sur lunar en busca de hielo. La CNSA confirmó además 19 misiones espaciales en 2026, "
            "incluyendo Tianwen-2, Shenzhou-23 y el cohete reutilizable Larga Marcha 10."
        ),
        "fuente_label": "Milenio — China Chang'e-7: misión al polo sur de la Luna en busca de hielo",
        "fuente_url": "https://www.milenio.com/ciencia-y-salud/china-change-7-mision-polo-sur-luna-busqueda-hielo",
    },
    {
        "emoji": "🌐",
        "titulo": "China y la ASEAN avanzan hacia el Código de Conducta en el Mar del Sur",
        "cuerpo": (
            "China y los países de la ASEAN aceleraron esta semana las negociaciones para cerrar el Código "
            "de Conducta en el Mar del Sur de China, un acuerdo clave para la estabilidad regional. Pekín "
            "reafirmó su voluntad de cooperar con los países vecinos en la gestión de diferencias. El "
            "portavoz del Ministerio de Exteriores subrayó que el mar puede ser 'pacífico y estable' con "
            "diálogo y normas claras, semana marcada también por la histórica cumbre bilateral con EE.UU."
        ),
        "fuente_label": "FMPRC — Conferencia de Prensa del Portavoz del Ministerio de Exteriores",
        "fuente_url": "https://www.fmprc.gov.cn/esp/xwfw/lxjzzdh/202605/t20260510_11907959.html",
    },
    {
        "emoji": "🏭",
        "titulo": "China lidera la IA global: tres empresas en el TOP 10 de TIME 2026",
        "cuerpo": (
            "TIME publicó su lista de las 10 empresas de IA más influyentes de 2026 y tres son chinas. "
            "DeepSeek V4 ya es compatible con los procesadores Ascend de Huawei. Las patentes de IA "
            "crecen un 31,2% interanual y China cuenta con 602 millones de usuarios de IA generativa, "
            "más de la mitad del total mundial. La industria central de IA del país superó el billón "
            "de yuanes en valor en 2025 y apunta a los 10 billones para 2030."
        ),
        "fuente_label": "People's Daily ES — La innovación impulsa la fuerza de la manufactura en China",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0513/c31616-20455780.html",
    },
    {
        "emoji": "📋",
        "titulo": "El XV Plan Quinquenal 2026-2030: China aprueba su primera Ley especial de Desarrollo",
        "cuerpo": (
            "China aprobó esta semana la primera Ley especial sobre el Plan de Desarrollo Estatal, un hito "
            "institucional sin precedentes. El XV Plan Quinquenal sitúa las 'Nuevas Fuerzas Productivas de "
            "Calidad' —IA, 6G, robótica, biotecnología y drones— como ejes del crecimiento nacional. Las "
            "industrias emergentes aspiran a pasar de 6 a 10 billones de yuanes antes de 2030, con un "
            "presupuesto en Ciencia y Tecnología que crece un 7,1% hasta 1,3 billones de yuanes."
        ),
        "fuente_label": "Pravda ES — China aprueba la primera Ley especial sobre el Plan de Desarrollo",
        "fuente_url": "https://spanish.news-pravda.com/world/2026/05/11/921110.html",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, espacio y diplomacia.", bold=False),
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
    title = "China Al Dia — Semana 8-14 Mayo 2026"
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
