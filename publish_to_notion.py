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
        "emoji": "💾",
        "titulo": "Alibaba lanza el chip de IA Zhenwu M890: tres veces más potente que el H20 de NVIDIA",
        "cuerpo": (
            "El 19 de mayo, Alibaba presentó el Zhenwu M890, su acelerador de IA de última generación "
            "desarrollado por su subsidiaria T-Head. El chip ofrece tres veces el rendimiento del modelo "
            "anterior (810E) y supera al H20 de NVIDIA —el chip que EE.UU. permite exportar a China—. "
            "Con 144 GB de memoria HBM3 y 800 GB/s de ancho de banda, está optimizado para entrenamiento "
            "e inferencia de agentes IA. Alibaba ya ha entregado más de 560.000 unidades Zhenwu a más de "
            "400 clientes en 20 industrias. La hoja de ruta incluye el V900 en 2027 (216 GB, 1.200 GB/s) "
            "y el J900 en 2028, consolidando la apuesta china por la soberanía en hardware de IA."
        ),
        "fuente_label": "CNBC — Alibaba reveals more powerful Zhenwu AI chip, new LLM",
        "fuente_url": "https://www.cnbc.com/2026/05/19/alibaba-reveals-more-powerful-zhenwu-ai-chip-new-llm.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Alibaba lanza Qwen3.7-Max: el LLM de agentes que trabaja 35 horas sin degradarse",
        "cuerpo": (
            "El 20 de mayo, Alibaba presentó Qwen3.7-Max, su nuevo modelo de lenguaje diseñado para la "
            "era de los agentes IA. Puede ejecutar tareas complejas de forma autónoma durante hasta 35 "
            "horas sin degradación de rendimiento, automatizando flujos de trabajo, depurando código y "
            "resolviendo problemas de múltiples etapas. Los modelos Qwen superan ya el billón de descargas "
            "acumuladas en plataformas abiertas. Qwen3.7-Max-Preview figura entre los 15 primeros modelos "
            "del mundo en el ranking global Chatbot Arena, señalando que la brecha con los LLMs "
            "occidentales se estrecha a gran velocidad."
        ),
        "fuente_label": "TechNode — Alibaba introduces Qwen3.7-Max as next-gen AI agent model",
        "fuente_url": "https://technode.com/2026/05/21/alibaba-introduces-qwen3-7-max-as-next-gen-ai-agent-model/",
    },
    {
        "emoji": "🛡️",
        "titulo": "China bloquea la compra de la startup de IA Manus por Meta: la IA agéntica es seguridad nacional",
        "cuerpo": (
            "La Oficina del Mecanismo de Revisión de Seguridad de China ordenó cancelar la adquisición "
            "de Manus —startup china de IA agéntica— por parte de Meta, bloqueando una transacción "
            "valorada en unos 2.000 millones de dólares. El gobierno chino declaró la IA agéntica como "
            "activo estratégico de seguridad nacional, trazando una línea clara sobre qué tecnologías "
            "no están disponibles para adquisición extranjera. Manus, conocida por sus capacidades de "
            "agentes autónomos, se convirtió en símbolo de la nueva política china de soberanía "
            "tecnológica en el campo de la inteligencia artificial."
        ),
        "fuente_label": "SCMP — China takes confident strides in AI innovation in 2026",
        "fuente_url": "https://www.scmp.com/tech/tech-war/article/3338528/tech-war-china-takes-confident-strides-develop-more-ai-innovation-2026",
    },
    {
        "emoji": "🤝",
        "titulo": "Cumbre Xi-Trump: acuerdos comerciales históricos y nueva era de estabilidad estratégica",
        "cuerpo": (
            "Los días 14 y 15 de mayo, Xi Jinping recibió a Donald Trump en Pekín en la primera visita "
            "de Estado desde 2017. La cumbre produjo resultados concretos: China comprará productos "
            "agrícolas estadounidenses por mínimo 17.000 millones de dólares al año entre 2026-2028; "
            "adquirirá 200 aviones Boeing; y se crearon el Consejo de Comercio EE.UU.-China y el Consejo "
            "de Inversión EE.UU.-China. Ambos países acordaron asegurar el tránsito por el Estrecho de "
            "Ormuz. Xi declaró ante los CEOs de Tesla, Apple y Boeing que China 'abrirá más' al "
            "capital extranjero, señalando una nueva fase en las relaciones bilaterales."
        ),
        "fuente_label": "CNBC — Xi tells Musk, Tim Cook and other CEOs: China will open wider",
        "fuente_url": "https://www.cnbc.com/2026/05/14/xi-china-open-us-business-ai-chips.html",
    },
    {
        "emoji": "🚗",
        "titulo": "Casi uno de cada tres autos vendidos en el mundo en 2026 será eléctrico: China lidera",
        "cuerpo": (
            "Según previsiones publicadas esta semana, cerca del 30% de todos los automóviles vendidos "
            "globalmente en 2026 serán vehículos eléctricos, con China como principal impulsor. BYD "
            "espera superar 1,5 millones de unidades exportadas este año, un 15% por encima de su "
            "objetivo previo. Las exportaciones chinas de eléctricos e híbridos marcaron récord histórico "
            "en el Q1 2026, con un crecimiento superior al 120% interanual. En mercados como México, el "
            "90% de los vehículos eléctricos vendidos provienen de China, reflejando la consolidación "
            "de las marcas chinas en el mercado automotriz global."
        ),
        "fuente_label": "BioBioChile — Con China liderando: casi uno de cada tres autos será eléctrico",
        "fuente_url": "https://www.biobiochile.cl/noticias/economia/mercado-automotriz/2026/05/20/con-china-liderando-preven-que-casi-uno-de-cada-tres-autos-vendidos-a-nivel-global-seran-electricos.shtml",
    },
    {
        "emoji": "🚀",
        "titulo": "China confirma misiones tripuladas a la Luna en 2027: el jefe de la NASA advierte del avance chino",
        "cuerpo": (
            "El administrador de la NASA, Jared Isaacman, declaró el 19 de mayo en la conferencia ASCEND "
            "que China lanzará misiones tripuladas a la Luna en 2027, advirtiendo que el escenario "
            "geopolítico fuera de la órbita terrestre 'se está ajustando a favor de China'. China, que ya "
            "completó su 19.ª misión espacial de 2026 esta semana, avanza con Chang'e-7 (lanzamiento en "
            "agosto) para explorar el polo sur lunar en busca de agua helada, y con el cohete reutilizable "
            "Larga Marcha 10. El país tiene el objetivo firme de enviar taikonautas a la Luna antes de 2030."
        ),
        "fuente_label": "EspacioTech — Isaacman: China lanzará misiones tripuladas a la Luna en 2027",
        "fuente_url": "https://www.espaciotech.net/2026/05/21/jared-isaacman-asegura-que-china-lanzara-misiones-tripuladas-a-la-luna-en-2027/",
    },
    {
        "emoji": "⚡",
        "titulo": "China presenta el condensador sincrónico más avanzado del mundo para estabilizar renovables",
        "cuerpo": (
            "Dongfang Electric Motor presentó un condensador sincrónico de 35 kV que se conecta "
            "directamente a la red eléctrica, eliminando el transformador elevador intermedio. Diseñado "
            "para estabilizar la energía solar y eólica, convierte la electricidad intermitente en "
            "corriente estable apta para la red. China también opera la mayor batería de almacenamiento "
            "de aire líquido del mundo: 60 MW de potencia y 600 MWh de capacidad —10 horas de "
            "suministro continuo—. El plan quinquenal destina 1 billón de yuanes anuales a infraestructura "
            "energética limpia hasta 2030, con el objetivo de duplicar la energía no fósil para 2035."
        ),
        "fuente_label": "Ecoticias — China presenta un condensador nunca visto para energías renovables",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-se-pasa-el-juego-y-presenta-al-mundo-un-condensador-nunca-visto-capaz-de-estabilizar-la-energia-y-convertirla-en-renovable",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China: +5% en Q1 2026 y exportaciones al alza pese a tensiones geopolíticas",
        "cuerpo": (
            "La economía china cerró el primer trimestre de 2026 con un crecimiento del 5% interanual, "
            "por encima de las previsiones. El motor principal fue la manufactura de alta tecnología "
            "(+12,5%), con robots industriales (+33%) y circuitos integrados (+24%) como líderes. "
            "Las exportaciones totales crecieron un 14,5% hasta abril, aunque las ventas a EE.UU. "
            "cayeron un 10% por los aranceles. China diversifica activamente sus mercados: Asia-Pacífico, "
            "Latinoamérica y África absorben el crecimiento. El objetivo para 2026 es un crecimiento "
            "del 4,5-5%, el más prudente en décadas, apostando por calidad antes que velocidad."
        ),
        "fuente_label": "CGTN Español — Comercio exterior de China aumenta 15% en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-15/2044294393639481345/index.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "El XV Plan Quinquenal (2026-2030): IA, 6G, robots y biotech como pilares del futuro",
        "cuerpo": (
            "El XV Plan Quinquenal sitúa las Nuevas Fuerzas Productivas de Calidad en el centro de la "
            "estrategia nacional. Los ejes: IA Plus como infraestructura transversal (70% de la economía "
            "integrada con IA para 2027; 90% para 2030); despliegue de 6G; producción de robots IA "
            "+94% en 2026; biotecnología y drones como sectores estratégicos. El presupuesto en Ciencia "
            "y Tecnología sube un 7,1% hasta 1,3 billones de yuanes. Las industrias emergentes —chips, "
            "robots inteligentes y economía de baja altitud— suman ya 6 billones de yuanes y aspiran "
            "a 10 billones en 2030. China no solo quiere liderar: quiere que sea el motor de su "
            "economía durante las próximas dos décadas."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
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
    title = "China Al Dia — Semana 15-22 Mayo 2026"
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
