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
        "titulo": "Shenzhou-23: China lanza a un astronauta a un año en órbita, camino a la Luna",
        "cuerpo": (
            "El 24 de mayo, China puso en órbita la misión Shenzhou-23 desde Jiuquan. Por primera vez, "
            "uno de los tres astronautas permanecerá en la Estación Espacial Tiangong durante un año "
            "completo. La misión incluye a Lai Ka-ying, primera astronauta de Hong Kong, un hito "
            "histórico para el programa espacial chino. El lanzamiento forma parte de la hoja de ruta "
            "de la CNSA para llevar humanos a la Luna antes de 2030, utilizando la nave Mengzhou y el "
            "módulo de aterrizaje Lanyue. China sigue acelerando su programa espacial con misiones "
            "cada vez más ambiciosas y complejas."
        ),
        "fuente_label": "La Jornada — China envía astronautas con vista puesta en alunizaje 2030",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/05/24/ciencia-y-tecnologia/china-envia-a-astronauta-a-mision-espacial-de-un-ano-con-vista-puesta-en-alunizaje-en-2030",
    },
    {
        "emoji": "🔬",
        "titulo": "Huawei desafía la Ley de Moore con la 'Ley Tau': chips de 1,4 nm para 2031",
        "cuerpo": (
            "El 25 de mayo, en el ISCAS de Shanghái, Huawei presentó la 'Ley Tau', un nuevo paradigma "
            "de escalado de chips basado en optimizar el tiempo de propagación de señales —en lugar de "
            "la reducción geométrica tradicional—, mediante la tecnología LogicFolding. La empresa se "
            "comprometió a chips equivalentes a 1,4 nm para 2031. Los procesadores Kirin de otoño de "
            "2026 serán los primeros en incorporar esta arquitectura. El anuncio refuerza la apuesta de "
            "China por la soberanía tecnológica frente a las restricciones de exportación de Occidente."
        ),
        "fuente_label": "WwwHatsNew — Huawei semiconductores 1,4nm 2031 Ley Tau LogicFolding",
        "fuente_url": "https://wwwhatsnew.com/2026/05/26/huawei-semiconductores-1-4nm-2031-ley-tau-logicfolding/",
    },
    {
        "emoji": "🧠",
        "titulo": "DeepSeek V4: el modelo open-source más avanzado, 27 veces más barato que sus rivales",
        "cuerpo": (
            "DeepSeek lanzó V4-Pro con 1,6 billones de parámetros y un contexto de un millón de tokens, "
            "superando a todos los modelos open-source en razonamiento, código y conocimiento del mundo. "
            "Solo es superado por el modelo cerrado Gemini Pro 3.1 de Google. Su versión Flash es "
            "27 veces más barata para inferencia que sus equivalentes occidentales. DeepSeek sigue siendo "
            "open-source y gratuito, desafiando el modelo de negocio de OpenAI y Anthropic. China ya "
            "cuenta con 602 millones de usuarios de IA generativa, liderando el mundo en adopción."
        ),
        "fuente_label": "Think.es — Nuevo LLM de DeepSeek subraya el avance tecnológico de China",
        "fuente_url": "https://www.think.es/nuevo-llm-de-deepseek-subraya-el-avance-tecnologico-en-china-pese-a-restricciones-de-ee-uu/",
    },
    {
        "emoji": "⚡",
        "titulo": "China activa la turbina eólica marina más grande del mundo: 20 MW, 96.000 hogares",
        "cuerpo": (
            "El 16 de mayo, Mingyang Smart Energy activó en el Mar de China Meridional, frente a Hainan, "
            "la turbina eólica marina más grande del mundo con una potencia de 20 megavatios. Una sola "
            "turbina puede abastecer a 96.000 hogares durante un año completo. En enero-mayo de 2026, "
            "la capacidad solar de China creció un 57% y la eólica un 21% respecto al mismo período de "
            "2025. China construye actualmente 448 gigavatios de capacidad renovable —la mitad del total "
            "global en construcción—, con más de 1,6 teravatios ya en funcionamiento."
        ),
        "fuente_label": "Canal26 — China activa la turbina eólica marina más grande del mundo",
        "fuente_url": "https://www.canal26.com/internacionales/2026/05/16/energia-renovable-a-gran-escala-china-activa-la-turbina-eolica-marina-mas-grande-del-mundo-capaz-de-abastecer-a-96000-hogares/",
    },
    {
        "emoji": "☀️",
        "titulo": "Hito histórico: la energía solar china supera al carbón por primera vez",
        "cuerpo": (
            "En 2026, China alcanzó un hito sin precedentes en la transición energética global: la "
            "capacidad instalada de energía solar superó por primera vez a la del carbón. El país "
            "también duplicará su producción de energía limpia para 2035 con una inversión de 1 billón "
            "de yuanes anuales en la red eléctrica durante el período 2026-2030. China instaló más "
            "energía eólica en un solo año que Estados Unidos en toda su historia, consolidándose como "
            "el líder global indiscutible de las energías renovables y la transición verde."
        ),
        "fuente_label": "Ecoticias — China lidera la energía solar superando al carbón por primera vez",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🤝",
        "titulo": "China y EE.UU. firman tregua comercial: reducción de aranceles y nueva Junta de Comercio",
        "cuerpo": (
            "El 16 de mayo, China y Estados Unidos confirmaron un principio de acuerdo para reducir "
            "aranceles mutuamente, ampliar el comercio agrícola y crear una 'Junta de Comercio' "
            "permanente. El acuerdo podría derivar en recortes arancelarios sobre más de 30.000 millones "
            "de dólares en productos, y supone el primer avance sustancial en las relaciones comerciales "
            "bilaterales desde la guerra arancelaria de 2025. La medida apunta a descomprimir la tensión "
            "y facilitar el intercambio en sectores estratégicos como tecnología, agricultura y vehículos "
            "eléctricos."
        ),
        "fuente_label": "Ambito — China anuncia principio de acuerdo con EEUU para reducir aranceles",
        "fuente_url": "https://www.ambito.com/mundo/china-anuncio-un-principio-acuerdo-eeuu-reducir-aranceles-n6278385",
    },
    {
        "emoji": "🚗",
        "titulo": "Vehículos eléctricos chinos: 1,5 millones de exportaciones en 2026, récord histórico",
        "cuerpo": (
            "China exportó más de 1,5 millones de vehículos eléctricos e híbridos en la primera mitad "
            "de 2026, con un crecimiento del 88% interanual en enero-febrero y récords mensuales "
            "consecutivos en marzo y abril. BYD lidera las exportaciones y opera plantas en Hungría, "
            "Brasil y Tailandia, con el objetivo de fabricar todos sus vehículos europeos localmente "
            "para 2028. La industria automotriz eléctrica china consolida su dominio global con "
            "presencia creciente en Asia-Pacífico, Europa, América Latina y el Sudeste Asiático."
        ),
        "fuente_label": "16 Válvulas — China logra récord de exportación de vehículos electrificados en 2026",
        "fuente_url": "https://www.16valvulas.com.ar/crecimiento-imparable-china-logro-otro-record-de-exportacion-de-vehiculos-electrificados-con-mas-de-15-millones-de-unidades-enviadas-a-nivel-global-en-2026/",
    },
    {
        "emoji": "🤖",
        "titulo": "El auge de los robots con IA en China: producción crece un 94% en 2026",
        "cuerpo": (
            "La Academia Damo de Alibaba señala que 2026 es el punto de inflexión para los robots "
            "humanoides en China, con envíos globales esperados de 35.000 unidades, un aumento del 94%. "
            "El Ministerio de Industria y Tecnología declaró los robots humanoides 'industria estratégica "
            "emergente', con Shenzhen y Guangzhou como centros de fabricación. Las empresas chinas ya "
            "tienen contratos reales con fábricas y centros logísticos, mientras sus competidoras "
            "occidentales siguen en fase de desarrollo. China apunta a que el 90% de su economía integre "
            "IA en sus procesos productivos para 2030."
        ),
        "fuente_label": "La Jornada — China apuesta a robots con IA para todo tipo de labores",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/05/10/economia/china-apuesta-a-robots-con-inteligencia-artificial-para-todo-tipo-de-labores",
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
    title = "China Al Dia — Semana 26 Mayo – 1 Junio 2026"
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
