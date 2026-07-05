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
        "titulo": "China domina el 90% del mercado mundial de robots humanoides",
        "cuerpo": (
            "China controla ya el 90% del mercado global de robots humanoides, con un valor de mercado de "
            "14.200 millones de dólares en 2026 y un crecimiento del 47% interanual. Los grandes fabricantes "
            "de vehículos eléctricos —BYD, NIO, Xiaomi, GAC y Chery— han entrado en masa en el sector robótico, "
            "aprovechando la misma cadena de suministro de actuadores, motores y engranajes de precisión que hizo "
            "de China el mayor fabricante de automóviles del mundo. Xiaomi ya utiliza robots humanoides para "
            "instalar piezas en la línea de producción de su fábrica de EVs en Pekín, describiendo a los robots "
            "como 'becarios' con potencial ilimitado."
        ),
        "fuente_label": "Rest of World — China is running the EV playbook on humanoid robots",
        "fuente_url": "https://restofworld.org/2026/china-humanoid-robots-unitree-agibot-tesla-optimus/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4 impulsa la independencia tecnológica china: Huawei Ascend 950 agotado",
        "cuerpo": (
            "El lanzamiento de DeepSeek V4, diseñado de forma nativa para funcionar sobre chips Huawei Ascend 950, "
            "ha desencadenado una carrera de pedidos entre las grandes tecnológicas chinas. ByteDance, Tencent y "
            "Alibaba aceleraron compras masivas del chip de Huawei tras comprobar que el modelo V4 supera a sus "
            "competidores occidentales en muchas tareas al tiempo que cuesta cuatro veces menos que GPT de OpenAI. "
            "DeepSeek, fundada hace menos de tres años, ya está valorada en 50.000 millones de dólares. Su fundador "
            "fue recibido personalmente por Xi Jinping junto a los CEOs de Huawei, BYD, Alibaba, Tencent, Meituan "
            "y CATL, en una señal inequívoca del respaldo gubernamental al ecosistema tecnológico chino."
        ),
        "fuente_label": "Xataka — DeepSeek V4 y los cuatro grandes ganadores de los chips chinos",
        "fuente_url": "https://www.xataka.com/empresas-y-economia/deepseek-v4-ha-dado-a-china-impulso-que-necesita-frente-a-eeuu-cuatro-fabricantes-chips-grandes-ganadores",
    },
    {
        "emoji": "💾",
        "titulo": "Metax: el primer GPU chino de altas prestaciones fabricado 100% con tecnología doméstica",
        "cuerpo": (
            "La empresa china Metax presentó su GPU de nueva generación construida íntegramente sobre tecnología "
            "de proceso doméstica, cerrando el último eslabón que faltaba en la cadena de fabricación de chips de "
            "entrenamiento de alta gama en China. El chip logró compatibilidad completa con los modelos Tongyi "
            "Qianwen de Alibaba y DeepSeek, lo que le permitió obtener un contrato de clúster de computación "
            "inteligente por 660 millones de yuanes. En paralelo, Biren Technology debutó en la Bolsa de Hong Kong "
            "con una subida del 120% en su primer día, señal de la confianza del capital global en la capacidad "
            "china de competir en el segmento más avanzado de los chips de IA."
        ),
        "fuente_label": "SIC Components — China's AI Chip Landscape 2026",
        "fuente_url": "https://www.sic-components.com/extension/d_blog_module/post?post_id=391",
    },
    {
        "emoji": "🌐",
        "titulo": "Premier Li Qiang en Summer Davos: 'La tecnología china es una oportunidad, no una amenaza'",
        "cuerpo": (
            "El Premier chino Li Qiang intervino en el Foro Económico Mundial de Verano (Summer Davos) celebrado "
            "en Dalian para afirmar que los avances tecnológicos de China representan 'una oportunidad para el "
            "mundo, no una amenaza'. Subrayó que 'China ha forjado un camino en el que la innovación tecnológica "
            "lidera la modernización industrial, que a su vez impulsa nuevas iteraciones tecnológicas.' El Foro "
            "puso el foco en el modelo de crecimiento liderado por la innovación del país, que el 15.º Plan "
            "Quinquenal proyecta como motor de las próximas dos décadas."
        ),
        "fuente_label": "AP / WSLS — Premier says China's tech advancements an opportunity for the world",
        "fuente_url": "https://www.wsls.com/business/2026/06/24/premier-says-chinas-tech-advancements-an-opportunity-for-the-world-not-a-threat/",
    },
    {
        "emoji": "💻",
        "titulo": "China inaugura la Conferencia Global de Economía Digital 2026 en Pekín",
        "cuerpo": (
            "El 2 de julio arrancó en Pekín la Conferencia Global de Economía Digital 2026, reuniendo a "
            "ejecutivos de empresas, representantes de consejos empresariales, académicos internacionales y "
            "ministros de Kazajistán, Colombia y Chad. La conferencia refuerza el posicionamiento de China como "
            "epicentro de la transformación digital global. La economía digital 'núcleo' del país ya representa "
            "el 8,9% del PIB y se proyecta que alcance el 12,5% para 2030, con la tecnología móvil y la "
            "transformación digital sumando 2 billones de dólares adicionales a la economía."
        ),
        "fuente_label": "CGTN Español — Conferencia Global de Economía Digital 2026",
        "fuente_url": "https://espanol.cgtn.com/",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones de semiconductores chinos se disparan un 83,4% en los primeros cinco meses",
        "cuerpo": (
            "Las exportaciones chinas de circuitos integrados crecieron un 83,4% interanual en los primeros "
            "cinco meses de 2026, consolidando a China como el gran proveedor global de chips. El crecimiento "
            "económico del primer trimestre se situó en el 5% interanual, atribuido a la aceleración de las "
            "'nuevas fuerzas productivas de calidad'. Deutsche Bank califica el plan económico chino para 2026 "
            "como un camino de estabilidad y crecimiento estratégico, con el objetivo oficial de crecer entre "
            "un 4,5% y un 5%."
        ),
        "fuente_label": "Xinhua — Innovación tecnológica gana impulso en China en 2026",
        "fuente_url": "https://spanish.news.cn/20260312/609871a2816b42efaf0f7d9ac3b5ff7a/c.html",
    },
    {
        "emoji": "🏆",
        "titulo": "Hong Kong, segunda economía más competitiva del mundo según el IMD",
        "cuerpo": (
            "Hong Kong ascendió al segundo puesto en el ranking de competitividad económica global del IMD "
            "(Instituto Internacional para el Desarrollo de la Gestión, con sede en Suiza), consolidándose "
            "como la plataforma de pruebas preferida por las empresas que buscan lanzar nuevos modelos de "
            "negocio y aplicaciones industriales de tecnología de vanguardia. Su pertenencia a la Gran Bahía "
            "Guangdong-Hong Kong-Macao potencia su competitividad como puente entre China continental y los "
            "mercados globales."
        ),
        "fuente_label": "Xinhua — Hong Kong's emerging testing ground function",
        "fuente_url": "https://english.news.cn/20260703/0c7d655b08454650b64167725d610c67/c.html",
    },
    {
        "emoji": "🤝",
        "titulo": "China abre la puerta a mayor cooperación con EE.UU. en comercio agrícola",
        "cuerpo": (
            "El 2 de julio, el portavoz del Ministerio de Comercio chino, He Yadong, declaró que China está "
            "dispuesta a colaborar con Estados Unidos para crear condiciones favorables para el comercio "
            "agrícola bilateral, en un momento de normalización gradual de las relaciones comerciales entre "
            "las dos grandes potencias. La señal fue interpretada por los mercados como un paso constructivo "
            "hacia la estabilidad del comercio global."
        ),
        "fuente_label": "Al Poniente — Resumen Económico semana del 29 de junio al 3 de julio",
        "fuente_url": "https://alponiente.com/resumen-economico-de-la-semana-del-29-de-junio-al-03-de-julio-de-2026/",
    },
    {
        "emoji": "✈️",
        "titulo": "Air China inaugura la ruta directa Pekín-Venecia en el 40.º aniversario del vuelo China-Italia",
        "cuerpo": (
            "Air China abrió esta semana una nueva ruta directa entre Pekín y Venecia, añadiendo un nuevo "
            "enlace de alto valor entre China e Italia. La inauguración coincide con el 40.º aniversario del "
            "establecimiento de los servicios aéreos directos entre ambos países, que han transformado las "
            "relaciones turísticas y comerciales italo-chinas a lo largo de cuatro décadas. China suma así "
            "otra conexión directa a Europa en el marco de su estrategia de expansión de la conectividad aérea global."
        ),
        "fuente_label": "Observatorio de Política China — Resumen Política Exterior 26 junio - 2 julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-65/",
    },
    {
        "emoji": "🗺️",
        "titulo": "15.º Plan Quinquenal 2026-2030: cuántica, 6G, fusión nuclear e IA encarnada como pilares",
        "cuerpo": (
            "El nuevo plan quinquenal chino identifica como motores de crecimiento para 2026-2030: tecnología "
            "cuántica, biofabricación, hidrógeno, fusión nuclear, interfaces cerebro-computadora, IA encarnada "
            "(embodied AI) y comunicaciones 6G. La estrategia 'IA Plus' busca extender la inteligencia artificial "
            "a la totalidad de los sectores productivos: manufactura avanzada, salud, educación y defensa. El plan "
            "marca el inicio del ciclo de autosuficiencia tecnológica plena, con el objetivo declarado de que el "
            "70% de la economía integre IA en sus procesos para 2027 y el 90% para 2030. Las industrias de IA "
            "apuntan a superar los 10 billones de yuanes en valor para 2030."
        ),
        "fuente_label": "World Economic Forum — China's innovation systems driving the next growth cycle",
        "fuente_url": "https://www.weforum.org/stories/2026/06/china-innovation-systems-driving-the-next-growth-cycle/",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de julio de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, robotica, chips y diplomacia.", bold=False),
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
    title = "China Al Dia — Semana 29 Junio - 5 Julio 2026"
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
