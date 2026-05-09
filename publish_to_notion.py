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
        "titulo": "DeepSeek V4: la IA china que no necesita a Nvidia y vale 50.000 millones",
        "cuerpo": (
            "El 24 de abril DeepSeek lanzó su nuevo modelo insignia V4, y esta semana el impacto en la "
            "industria china de chips se ha hecho notar. DeepSeek V4 fue diseñado de forma nativa sobre "
            "los chips Ascend 950 de Huawei, sin depender de hardware occidental. El modelo supera a todos "
            "los rivales de código abierto en matemáticas y programación, y solo queda por detrás de "
            "Gemini 3.1-Pro de Google en conocimiento general. La startup china ya se valora en "
            "50.000 millones de dólares. ByteDance, Tencent y Alibaba aceleraron sus pedidos de chips "
            "Huawei tras el lanzamiento, mientras Cambricon registró en Q1 2026 ingresos de 423 millones "
            "de dólares (+160% interanual) y Huawei prevé acercarse a 12.000 millones en chips de IA en 2026."
        ),
        "fuente_label": "Xataka — DeepSeek V4 impulsa la industria china de chips",
        "fuente_url": "https://www.xataka.com/empresas-y-economia/deepseek-v4-ha-dado-a-china-impulso-que-necesita-frente-a-eeuu-cuatro-fabricantes-chips-grandes-ganadores",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD domina el Salón del Automóvil de Pekín 2026 con carga en 5 minutos",
        "cuerpo": (
            "El Salón del Automóvil de Pekín 2026, celebrado en un recinto de 220.000 m², convirtió a BYD "
            "en su protagonista absoluta. La compañía ocupó íntegramente el pabellón E3 con 1.451 vehículos "
            "expuestos a través de sus divisiones BYD, Denza, Fangchengbao y Yangwang. La estrella técnica "
            "fue el sistema Flash Charging, capaz de cargar una batería del 10% al 70% en tan solo 5 minutos, "
            "igualando la experiencia de repostar un coche de combustión. El nuevo SEAL 08 y el SEALION 08 "
            "incorporan también la segunda generación de la batería Blade y suspensión neumática Disus-A."
        ),
        "fuente_label": "Cadena 3 — Salón del Automóvil de Beijing 2026: BYD lidera con 1.451 autos",
        "fuente_url": "https://www.cadena3.com/noticia/cadena-3-en-china/salon-del-automovil-de-beijing-2026-byd-lidera-la-mega-muestra-con-1451-autos_544903",
    },
    {
        "emoji": "🧠",
        "titulo": "IA en el volante: la guerra de precios de EVs chinos se convierte en carrera de inteligencia artificial",
        "cuerpo": (
            "Las marcas de coches eléctricos en China han transformado su rivalidad comercial: ya no se "
            "trata solo de bajar precios, sino de ofrecer la IA más avanzada a bordo. El modelo Doubao "
            "de ByteDance está presente en 145 modelos de vehículos de más de 50 marcas, con una "
            "penetración de más de 7 millones de coches en circulación. Baidu, Alibaba y Volcano Engine "
            "compiten en el mismo espacio, convirtiendo el habitáculo del coche en el próximo gran campo "
            "de batalla de la inteligencia artificial china."
        ),
        "fuente_label": "CNBC — China EV price war turns into AI arms race",
        "fuente_url": "https://www.cnbc.com/2026/05/01/china-ev-ai-features-price-war-bytedance-alibaba-doubao-volcano-engine.html",
    },
    {
        "emoji": "🚛",
        "titulo": "Camiones autónomos chinos: 700 millones de kilómetros recorridos en carreteras reales",
        "cuerpo": (
            "Los camiones de conducción autónoma de Inceptio han acumulado ya 700 millones de kilómetros "
            "en carreteras reales de China, y la compañía apunta a superar los 1.000 millones antes de "
            "que termine 2026. Los directivos del sector advierten que, pese a los avances en IA, la "
            "expansión del despliegue comercial seguirá siendo gradual por razones regulatorias y de "
            "infraestructura, no tecnológicas. China cuenta ya con la mayor flota de vehículos de "
            "transporte autónomo operativa del mundo."
        ),
        "fuente_label": "CNBC — China's self-driving truck leaders: AI breakthroughs won't accelerate rollout",
        "fuente_url": "https://www.cnbc.com/2026/05/01/chinas-self-driving-truck-leaders-say-ai-breakthroughs-wont-accelerate-rollout-heres-why.html",
    },
    {
        "emoji": "⚡",
        "titulo": "Pekín acoge la XVI Exposición de Energía Limpia: China ya compite con un ecosistema energético completo",
        "cuerpo": (
            "Esta semana Pekín fue sede de la XVI Exposición Internacional de Energía Limpia, con cerca "
            "de 800 expositores en el Centro Nacional de Convenciones. El evento refleja la posición de "
            "China como líder mundial en la transición verde. Según análisis publicados esta semana, China "
            "ya no compite solo con fábricas de paneles solares o turbinas eólicas: ha construido un "
            "ecosistema energético completo, que abarca generación, almacenamiento, red de distribución "
            "y exportación de tecnología. La capacidad instalada de renovables en China alcanza "
            "2.650 gigavatios en 2026, frente a los 2.360 de 2025."
        ),
        "fuente_label": "Ategi — China ya compite con un sistema energético completo",
        "fuente_url": "https://ategi.com/2026/05/09/china-ya-no-compite-solo-con-fabricas-compite-con-un-sistema-energetico-completo/",
    },
    {
        "emoji": "🏭",
        "titulo": "China instala el 54% de todos los robots industriales del planeta",
        "cuerpo": (
            "La Federación Internacional de Robótica (IFR) confirmó esta semana que China concentra el "
            "54% de los robots industriales instalados anualmente en todo el planeta, y ha situado la "
            "robótica como pieza central de su estrategia industrial en el 15.º Plan Quinquenal (2026-2030). "
            "Las prioridades incluyen robots con IA incorporada ('embodied AI'), humanoides y robots de "
            "servicio para el sector sanitario y el cuidado de personas mayores. Las startups chinas de "
            "robótica reportan contratos reales en fábricas, hospitales y centros comerciales, mientras "
            "sus competidoras occidentales siguen mayoritariamente en fase de desarrollo."
        ),
        "fuente_label": "IFR — China makes AI-powered robots core of national strategy",
        "fuente_url": "https://ifr.org/ifr-press-releases/news/china-makes-ai-powered-robots-core-of-national-strategy",
    },
    {
        "emoji": "📊",
        "titulo": "China cierra la brecha de la IA: de 2 años de retraso a menos de 6 meses",
        "cuerpo": (
            "Según el análisis del South China Morning Post publicado esta semana, mientras hace un año "
            "se estimaba que China llevaba entre 1 y 2 años de retraso en IA respecto a Estados Unidos, "
            "los últimos datos apuntan a que esa brecha se ha reducido a menos de 6 meses. El ecosistema "
            "de startups de IA chinas —liderado por DeepSeek, Zhipu AI, Moonshot AI y Baidu— está "
            "cerrando distancias en modelos de razonamiento, agentes autónomos y aplicaciones industriales. "
            "Eric Schmidt, ex-CEO de Google, también confirmó esta semana que China está muy cerca de "
            "igualar las capacidades de IA de Estados Unidos."
        ),
        "fuente_label": "SCMP — China takes confident strides in AI innovation in 2026",
        "fuente_url": "https://www.scmp.com/tech/tech-war/article/3338528/tech-war-china-takes-confident-strides-develop-more-ai-innovation-2026",
    },
    {
        "emoji": "🛡️",
        "titulo": "China bloquea la compra de Manus por Meta: la IA estratégica se queda en casa",
        "cuerpo": (
            "El Gobierno chino activó su Ley de Antibloqueo para impedir que Meta adquiriera Manus, "
            "la startup china de agentes de IA autónomos que se viralizó globalmente a principios de 2026. "
            "La medida señala una nueva etapa en la geopolítica tecnológica: Pekín no solo protege su "
            "industria, sino que utiliza el marco regulatorio como herramienta estratégica para retener "
            "las innovaciones en IA dentro del ecosistema nacional. Es la primera vez que China activa "
            "explícitamente esta ley en el sector tecnológico contra una adquisición de Silicon Valley."
        ),
        "fuente_label": "Al Jazeera — China blocks Meta from acquiring AI startup Manus",
        "fuente_url": "https://www.aljazeera.com/news/2026/4/27/china-blocks-us-tech-giant-meta-from-acquiring-ai-startup-manus",
    },
    {
        "emoji": "🗺️",
        "titulo": "La inversión china en América Latina sigue creciendo: infraestructura, energía y tecnología",
        "cuerpo": (
            "Según un análisis publicado esta semana por La Jornada, China ha consolidado su posición "
            "como uno de los principales inversores en América Latina y el Caribe, con proyectos en "
            "infraestructura, energía, minería y tecnología. La estrategia combina préstamos soberanos "
            "con inversión directa de empresas como COSCO (logística), State Grid (electricidad), "
            "Huawei (telecomunicaciones) y BYD (movilidad eléctrica), posicionando a la región como "
            "un socio estratégico para la expansión global del modelo productivo chino."
        ),
        "fuente_label": "La Jornada — Inversión de China en América Latina y el Caribe",
        "fuente_url": "https://www.jornada.com.mx/2026/05/06/economia/016a1eco",
    },
    {
        "emoji": "🏖️",
        "titulo": "18 millones de turistas visitan Pekín en el Primero de Mayo: el consumo interior se dispara",
        "cuerpo": (
            "Las vacaciones del Primero de Mayo (1-5 de mayo) movilizaron a un volumen récord de "
            "turistas por toda China. Solo Pekín recibió más de 18 millones de visitas, reflejando la "
            "vitalidad del consumo interior y la recuperación del sector servicios chino. El turismo "
            "doméstico sigue siendo uno de los principales motores del crecimiento económico en 2026, "
            "compensando la moderación de las exportaciones en algunos segmentos y demostrando la "
            "solidez de la demanda interna china."
        ),
        "fuente_label": "Xinhua Español — Turismo en China durante vacaciones del Primero de Mayo",
        "fuente_url": "https://spanish.xinhuanet.com/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, automovil, energia y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 5-9 Mayo 2026"
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
