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
        "emoji": "🚗",
        "titulo": "Auto China 2026: el mayor salón del automóvil del mundo es chino — y eléctrico",
        "cuerpo": (
            "El Beijing Auto Show 2026 cerró el 3 de mayo con cifras sin precedentes: 1,28 millones de "
            "visitantes, 1.451 vehículos expuestos, 181 debuts mundiales y 71 concept cars. La edición "
            "de este año marcó un punto de inflexión: la competición ya no es solo de coches, sino de "
            "sistemas de conducción autónoma con IA y cockpits inteligentes. BYD presentó el Formula X "
            "(superdeportivo eléctrico) y el Denza Z, un hypercar de 1.000+ CV que llegará a Europa. "
            "XPeng desveló el GX SUV flagship con 750 km de autonomía y hardware L4 por 58.000 dólares. "
            "Huawei ADS 5.0 se convirtió en el primer sistema en ofrecer conducción autónoma de Nivel 3 "
            "lista para circular en carretera, ya integrada en modelos AITO y Arcfox. CNN Business lo "
            "resumió: '¿Qué crisis del petróleo? Los vehículos eléctricos de China están listos para "
            "dominar el siglo XXI'."
        ),
        "fuente_label": "CGTN — Major takeaways from Auto China 2026",
        "fuente_url": "https://news.cgtn.com/news/2026-05-03/Explainer-Major-takeaways-from-Auto-China-2026-1MQ7KdeiJfW/p.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Kimi K2: el nuevo 'momento DeepSeek' que sacude la IA global",
        "cuerpo": (
            "La revista Nature lo ha bautizado como 'otro momento DeepSeek': Kimi K2, el último modelo "
            "de la startup china Moonshot AI, supera a GPT-5 y Gemini Pro 3 en benchmarks de código y "
            "vídeo, con APIs entre 4 y 17 veces más baratas que las de OpenAI. El modelo es de código "
            "abierto, soporta hasta 2 millones de caracteres de contexto y es compatible con el estándar "
            "de API de OpenAI. La valoración de Moonshot AI refleja el impacto: de 4.300 millones de "
            "dólares en diciembre de 2025 a 18.000 millones en marzo de 2026. En menos de 20 días tras "
            "el lanzamiento, los ingresos acumulados de Kimi superaron todo lo facturado durante 2025."
        ),
        "fuente_label": "La Tercera — Kimi K2, el modelo que marca otro momento DeepSeek",
        "fuente_url": "https://www.latercera.com/tendencias/noticia/como-es-kimi-k2-el-nuevo-modelo-de-ia-de-china-que-marca-otro-momento-deepseek-segun-la-revista-nature/",
    },
    {
        "emoji": "📈",
        "titulo": "China acelera hacia la 'economía inteligente': IA en todos los sectores productivos",
        "cuerpo": (
            "El Buró Político del Comité Central analizó el balance del Q1 2026 con resultados positivos: "
            "los indicadores clave superaron las previsiones. El presidente Xi Jinping, en un seminario "
            "en Shanghái, subrayó la necesidad de fortalecer la investigación básica como motor de la "
            "innovación tecnológica. El objetivo nacional: que el 70% de la economía productiva integre "
            "IA para 2027 y el 90% para 2030. Las industrias de IA del país apuntan a superar los "
            "10 billones de yuanes en valor para 2030, consolidando a China como el 'laboratorio de "
            "innovación global' del siglo XXI."
        ),
        "fuente_label": "Prensa Latina — Análisis económico y política exterior marcan semana en China",
        "fuente_url": "https://www.prensa-latina.cu/2026/05/02/analisis-economico-y-politica-exterior-marcan-semana-en-china/",
    },
    {
        "emoji": "🌍",
        "titulo": "China abre su mercado a toda África: aranceles cero para 53 países desde el 1 de mayo",
        "cuerpo": (
            "Con entrada en vigor el 1 de mayo de 2026, China aplica arancel cero al 100% de los "
            "productos procedentes de los 53 países africanos con los que mantiene relaciones "
            "diplomáticas. Los beneficios son inmediatos: cacao de Costa de Marfil y Ghana, café y "
            "aguacates de Kenia, cítricos y vinos de Sudáfrica —que antes pagaban entre un 8% y un 30%— "
            "entran ahora sin coste arancelario. El primer lote simbólico: 24 toneladas de manzanas "
            "sudafricanas despachadas en Shenzhen. El comercio bilateral China-África alcanzó los "
            "348.080 millones de dólares en 2025, con un crecimiento del 26,8% en el Q1 2026."
        ),
        "fuente_label": "People's Daily ES — China implementa política de arancel cero para naciones africanas",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0504/c31621-20452692.html",
    },
    {
        "emoji": "🤝",
        "titulo": "Diplomacia de altura: Trump viajará a Pekín el 14 y 15 de mayo para reunirse con Xi",
        "cuerpo": (
            "El presidente de Estados Unidos Donald Trump tiene previsto visitar Pekín los días 14 y 15 "
            "de mayo para sus primeras conversaciones cara a cara con Xi Jinping desde octubre de 2025. "
            "La reunión llega en un momento de alta tensión comercial pero también de señales de diálogo: "
            "el canciller chino Wang Yi habló con el Secretario de Estado Marco Rubio, dejando claro que "
            "Taiwán sigue siendo 'el mayor riesgo' en la relación bilateral. El encuentro podría marcar "
            "un punto de inflexión en la guerra arancelaria que ha dominado el comercio global en 2026."
        ),
        "fuente_label": "La Jornada — Diplomacia China-EEUU mayo 2026",
        "fuente_url": "https://www.jornada.com.mx/2026/05/03/economia/013n2eco",
    },
    {
        "emoji": "⚡",
        "titulo": "China bate récord de producción petrolera y diversifica su estrategia energética",
        "cuerpo": (
            "China alcanzó en marzo un récord histórico de producción petrolera de 4,44 millones de "
            "barriles diarios, reduciendo su dependencia de las importaciones en un momento de alta "
            "volatilidad global. En paralelo, el gobierno anunció un plan para diversificar las "
            "importaciones de energía ante potenciales emergencias geopolíticas —respuesta directa a "
            "las sanciones estadounidenses que intentan cortar el suministro iraní—. Pekín ordenó a "
            "sus empresas energéticas ignorar esas sanciones, consolidando una política energética "
            "soberana que combina máxima producción doméstica con rutas de suministro diversificadas."
        ),
        "fuente_label": "Ambito — China diversificará sus importaciones de energía",
        "fuente_url": "https://www.ambito.com/economia/china-diversificara-mas-sus-importaciones-energia-hacer-frente-las-emergencias-n6267877",
    },
    {
        "emoji": "🏭",
        "titulo": "El futuro industrial de China ya no cuenta trabajadores, cuenta robots",
        "cuerpo": (
            "China está completando la transición de su modelo industrial: de la mano de obra masiva a "
            "plantas oscuras —fábricas que operan sin luz porque no hay humanos—, camiones autónomos y "
            "algoritmos de IA que coordinan miles de decisiones por minuto. Unitree ha escalado su "
            "capacidad a 75.000 robots humanoides y 115.000 robots cuadrúpedos anuales (49,3% de cuota "
            "de mercado en China). AgiBot, segunda empresa del sector, lanzó a finales de marzo su robot "
            "número 10.000, el Expedition A3. El sector robótico chino proyecta un crecimiento de la "
            "producción del 94% en 2026, liderando el mercado global."
        ),
        "fuente_label": "Gizmodo ES — El futuro industrial de China y sus robots",
        "fuente_url": "https://es.gizmodo.com/futuro-industrial-de-china-ya-no-depende-de-cuantas-personas-trabajan-sino-de-cuantos-robots-coordina-su-ia-asi-quiere-mantener-su-dominio-con-plantas-oscuras-camiones-autonomos-algoritmos-que-2000206715",
    },
]


def build_blocks():
    today = date.today().strftime("%d de mayo de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, vehiculos electricos, IA y diplomacia.", bold=False),
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
    title = "China Al Dia — Semana 29 Abril – 6 Mayo 2026"
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
