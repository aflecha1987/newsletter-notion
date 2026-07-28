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
    # ── SEMANA 21-28 JULIO 2026 ──────────────────────────────────────────────
    {
        "emoji": "🚀",
        "titulo": "China recupera por primera vez una etapa de cohete con aterrizaje controlado en plataforma flotante",
        "cuerpo": (
            "El 10 de julio, el cohete Larga Marcha 10B fue lanzado desde la isla de Hainan y, "
            "aproximadamente seis minutos después de la separación del primer tramo, el propulsor "
            "regresó a una plataforma flotante utilizando una red tensada, convirtiéndose en la primera "
            "recuperación exitosa de una etapa de cohete mediante red en la historia. La CASC calificó "
            "el hito como un 'avance histórico' para la cohetería reutilizable china. El componente "
            "recuperado está previsto que vuelva a volar este mismo año, marcando un hito clave en la "
            "carrera espacial del siglo XXI."
        ),
        "fuente_label": "CNN Español — China prueba cohete reutilizable",
        "fuente_url": "https://cnnespanol.cnn.com/2026/07/10/mundo/video/china-prueba-cohete-reutilizable-trax",
    },
    {
        "emoji": "🤖",
        "titulo": "WAIC 2026 en Shanghái: China propone una nueva gobernanza global de la IA y crea la WAICO",
        "cuerpo": (
            "Del 17 al 20 de julio, Shanghái acogió la Conferencia Mundial de Inteligencia Artificial "
            "(WAIC 2026), con más de 1.100 empresas expositoras, 140 foros y 1.400 invitados "
            "internacionales bajo el lema 'La Alianza en la IA para un futuro más brillante'. El "
            "presidente Xi Jinping pronunció el discurso inaugural y anunció la creación de la "
            "Organización Mundial de Cooperación en Inteligencia Artificial (WAICO) con sede permanente "
            "en Shanghái, consolidando el posicionamiento de China como centro global de gobernanza de la IA."
        ),
        "fuente_label": "CGTN Español — WAIC 2026 innovaciones",
        "fuente_url": "https://espanol.cgtn.com/2026/07/19/ARTI1784426596140231",
    },
    {
        "emoji": "🧠",
        "titulo": "Alibaba y Moonshot AI presentan modelos de IA de código abierto que presionan a Silicon Valley",
        "cuerpo": (
            "El 20 de julio, China presentó dos modelos de IA de código abierto de primer nivel mundial: "
            "Kimi K3 (Moonshot AI) con 2,8 billones de parámetros, ventana de contexto de 1 millón de "
            "tokens y capacidades multimodales nativas; y Qwen3.8-Max (Alibaba) con 2,4 billones de "
            "parámetros y rendimiento superior en codificación y razonamiento. Ambos modelos superan o "
            "igualan a los mejores modelos occidentales en múltiples benchmarks, consolidando a China en "
            "la primera línea de la IA global de código abierto."
        ),
        "fuente_label": "La República — China avanza en IA con Alibaba y Moonshot",
        "fuente_url": "https://larepublica.es/2026/07/22/china-avanza-en-la-carrera-de-la-inteligencia-artificial-con-nuevos-modelos-de-alibaba-y-moonshot-ai/",
    },
    {
        "emoji": "📱",
        "titulo": "Apple Intelligence aprobada en China: funcionará con el modelo Qwen de Alibaba",
        "cuerpo": (
            "El 15 de julio, la Administración del Ciberespacio de China aprobó oficialmente Apple "
            "Intelligence para su lanzamiento, casi 22 meses después de que Apple señalara la brecha. "
            "Las funciones de IA de iOS, iPadOS, macOS y visionOS para usuarios chinos funcionarán con "
            "el modelo Qwen de Alibaba, en cumplimiento de la normativa local. En el segundo trimestre, "
            "las ventas de Apple en Gran China crecieron un 28% hasta 20.500 millones de dólares, "
            "demostrando el enorme potencial del mercado tecnológico chino."
        ),
        "fuente_label": "TechCrunch — Apple Intelligence aprobada en China con Qwen",
        "fuente_url": "https://techcrunch.com/2026/07/15/apple-intelligence-approved-for-launch-in-china-with-alibabas-qwen-ai/",
    },
    {
        "emoji": "🎯",
        "titulo": "China aprueba su Plan Maestro de IA 2026: inversión récord dentro del XV Plan Quinquenal",
        "cuerpo": (
            "El Consejo de Estado aprobó el Plan Maestro de IA 2026, que sitúa la inteligencia artificial "
            "como prioridad nacional absoluta. La inversión será la más elevada en la historia del país "
            "para esta tecnología, con el objetivo de liderar globalmente en capacidades de IA para 2030 "
            "y autosuficiencia plena para 2035. El 15.º Plan Quinquenal integra IA, 6G, robótica, "
            "biotecnología y energía limpia como los cinco pilares del desarrollo chino hasta 2030."
        ),
        "fuente_label": "Moncloa — China plan maestro IA 2026",
        "fuente_url": "https://www.moncloa.com/2026/07/12/china-plan-maestro-ia-2026-3398625/",
    },
    {
        "emoji": "🔬",
        "titulo": "Xi Jinping: China ha pasado de participante a líder global en ciencia y tecnología",
        "cuerpo": (
            "El 8 de julio, durante la Conferencia Nacional de Premios de Ciencia y Tecnología, el "
            "presidente Xi Jinping instó a acelerar la autosuficiencia científica. Destacó que China ha "
            "transitado de ser un participante a convertirse en líder en ciencia y tecnología global, "
            "y fijó 2035 como horizonte para consolidar al país como potencia tecnológica de primer "
            "rango. El presupuesto en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones de yuanes "
            "en el XV Plan Quinquenal."
        ),
        "fuente_label": "Xinhua — Xi insta a impulsar innovación en ciencia y tecnología",
        "fuente_url": "http://spanish.xinhuanet.com/20260708/351fa1e6395b401dace4f81c1f581872/c.html",
    },
    {
        "emoji": "☀️",
        "titulo": "China supera al carbón en capacidad solar instalada: un hito histórico en la energía verde",
        "cuerpo": (
            "En 2026, China alcanza un hito histórico: la capacidad instalada de energía solar supera "
            "por primera vez a la del carbón. El país concentra aproximadamente la mitad de la capacidad "
            "eólica y solar instalada del mundo, con 641 GW eólicos y más de 1.200 GW solares. El XV "
            "Plan Quinquenal fija objetivos para 2030: reducir las emisiones por unidad de PIB en un 17% "
            "y elevar la cuota de energías no fósiles al 25% del consumo total, integrando clima y "
            "energía en un mismo capítulo estratégico por primera vez."
        ),
        "fuente_label": "Ecoticias — China lidera energía solar superando al carbón",
        "fuente_url": "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez",
    },
    {
        "emoji": "🌏",
        "titulo": "China preside APEC 2026: libre comercio, digitalización y multilateralismo en Asia-Pacífico",
        "cuerpo": (
            "China asume la presidencia de la APEC 2026, con la cumbre prevista para noviembre en "
            "Shenzhen. Las prioridades son la reactivación del Área de Libre Comercio del Asia-Pacífico "
            "(FTAAP), la liberalización de los servicios digitales y la economía verde. El comercio de "
            "China con los miembros del RCEP alcanzó 13,85 billones de yuanes en 2025 (+5,3%), "
            "consolidando el liderazgo regional de Pekín en un momento en que el multilateralismo cobra "
            "renovada importancia frente al proteccionismo global."
        ),
        "fuente_label": "Empresa Exterior — China preside APEC 2026",
        "fuente_url": "https://empresaexterior.com/art/101322/china-asume-la-presidencia-de-apec-2026-con-el-objetivo-de-impulsar-el-area-de-libre-comercio-de-asia-pacifico-ftaap",
    },
    {
        "emoji": "📊",
        "titulo": "PIB de China: crecimiento del 4,3% en Q2 2026; las exportaciones se mantienen sólidas",
        "cuerpo": (
            "La economía china creció un 4,3% interanual en el segundo trimestre de 2026, por debajo "
            "del objetivo oficial del 4,5-5%, con un avance trimestral del 0,9%. Las exportaciones "
            "mantuvieron un desempeño sólido como motor principal, mientras el consumo interno mostró "
            "cierta debilidad por la corrección del sector inmobiliario. El primer trimestre registró un "
            "sólido 5%, y el gobierno mantiene herramientas de política fiscal y monetaria para apoyar "
            "la demanda doméstica en la segunda mitad del año."
        ),
        "fuente_label": "Agencia Nova — Economía china Q2 2026",
        "fuente_url": "https://agencianova.com/nota.asp?id=169892&id_tiponota=101&n=2026_7_16",
    },
    {
        "emoji": "🛣️",
        "titulo": "Belt and Road 2026: hacia proyectos de alta calidad con 66.200 millones movilizados",
        "cuerpo": (
            "La Iniciativa Belt and Road avanza en 2026 con un nuevo enfoque centrado en la sostenibilidad "
            "y la eficiencia. Las principales tendencias son el financiamiento flexible (equity frente a "
            "deuda) y la priorización de proyectos de energías renovables y tecnología. En el primer "
            "semestre de 2025 se movilizaron 66.200 millones de dólares en proyectos de construcción, "
            "cifra récord. La conectividad entre Asia, Europa, África y América Latina continúa "
            "fortaleciéndose a través de corredores estratégicos modernizados."
        ),
        "fuente_label": "El Mundo MX — China impulsa Belt and Road 2026",
        "fuente_url": "https://elmundomx.com/internacional/china-impulsa-la-iniciativa-belt-and-road-en-2026-con-nuevos-enfoques-estrategicos/",
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
    title = "China Al Dia — Semana 21-28 Julio 2026"
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
