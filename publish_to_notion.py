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

def p_links(sources):
    rich_text = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(sources):
        rich_text.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
        if i < len(sources) - 1:
            rich_text.append({"type": "text", "text": {"content": "  ·  "}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text}}

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
        "titulo": "DeepSeek: la IA china que sacudió al mundo recibe inversión de 45.000 millones de dólares",
        "cuerpo": (
            "El fondo estatal de chips chino (China Integrated Circuit Investment Fund) está en conversaciones "
            "para liderar una ronda de financiación para DeepSeek valorada en 45.000 millones de dólares "
            "(~300.000 millones de yuanes). La operación convertiría a DeepSeek, creadora del modelo de IA "
            "de código abierto que en enero de 2026 revolucionó la industria global, en una de las empresas "
            "de IA más valiosas del mundo. Su modelo V4-Pro y V4-Flash, lanzados con licencia MIT, ofrecen "
            "precios de API hasta 10 veces más baratos que sus equivalentes occidentales. El respaldo estatal "
            "reforzaría la capacidad de entrenamiento de DeepSeek y su alcance comercial dentro de China."
        ),
        "fuentes": [
            ("Bloomberg", "https://www.bloomberg.com/news/articles/2026-05-06/china-chip-fund-in-talks-to-lead-mega-deepseek-funding-ft-says"),
            ("Winbuzzer", "https://winbuzzer.com/2026/05/06/chinas-chip-fund-in-talks-to-lead-deepseek-funding-xcxwbn/"),
        ],
    },
    {
        "emoji": "🦾",
        "titulo": "Robots chinos dominan el mundo: el 87% de los humanoides fabricados son chinos",
        "cuerpo": (
            "Un informe de mayo de 2026 revela que de los más de 13.000 robots humanoides enviados globalmente "
            "en 2025, entre el 87% y el 90% fueron fabricados por empresas chinas. China cuenta ya con más de "
            "140 fabricantes nacionales y más de 330 modelos de humanoides en el mercado, frente a un puñado "
            "de compañías occidentales aún en fase de prototipo. En paralelo, el stock operativo de robots "
            "industriales en las fábricas chinas supera los 2 millones de unidades —4,5 veces más que Japón—, "
            "con el 54% de los nuevos robots industriales instalados en el planeta siendo desplegados en China."
        ),
        "fuentes": [
            ("ETC Journal", "https://etcjournal.com/2026/05/21/the-widening-gap-chinas-humanoid-robotics-dominance-may-2026/"),
            ("IFR", "https://ifr.org/ifr-press-releases/news/china-makes-ai-powered-robots-core-of-national-strategy"),
            ("People's Daily", "https://en.people.cn/n3/2026/0506/c90000-20453012.html"),
        ],
    },
    {
        "emoji": "📱",
        "titulo": "Huawei lanza la serie Mate 80 y una docena de dispositivos en su evento global de mayo",
        "cuerpo": (
            "En su evento internacional celebrado en Bangkok el 7 de mayo, Huawei presentó la serie Mate 80, "
            "la MatePad Mini y una nueva generación de wearables. Uno de los dispositivos más llamativos es "
            "el nova 15 Max, con una batería de 8.500 mAh. La apuesta de Huawei por su ecosistema HarmonyOS "
            "continúa con fuerza, mientras Xiaomi avanza en paralelo con su propio chip XRING y planea la "
            "'gran convergencia tecnológica' con una inversión de 40.000 millones de yuanes solo en 2026."
        ),
        "fuentes": [
            ("Notebookcheck", "https://www.notebookcheck.net/Huawei-confirms-2026-global-launch-event-with-at-least-half-a-dozen-new-devices-rumoured.1284561.0.html"),
            ("El Destape", "https://www.eldestapeweb.com/tecnologia/huawei-presento-novedades-2026-lanzara-gigante-chino-2026522141440"),
            ("Xataka", "https://www.xataka.com/empresas-y-economia/xiaomi-quiere-ser-nueva-huawei-primer-paso-esta-claro-desarrollar-sus-propios-chips"),
        ],
    },
    {
        "emoji": "🚗",
        "titulo": "Las exportaciones chinas de autos de pasajeros suben un 85% en abril",
        "cuerpo": (
            "Las exportaciones chinas de automóviles de pasajeros se dispararon un 85% interanual en abril "
            "de 2026, impulsadas por la demanda internacional de vehículos de nueva energía. La Agencia "
            "Internacional de la Energía (AIE) proyecta que el 30% de todos los autos vendidos en el mundo "
            "en 2026 serán eléctricos —unos 23 millones de unidades—, con China como motor indiscutible: "
            "el país produjo el 75% del total mundial en 2025 y duplicó sus exportaciones hasta superar "
            "los 2,5 millones de vehículos al exterior."
        ),
        "fuentes": [
            ("La Jornada", "https://www.jornada.com.mx/noticia/2026/05/11/economia/suben-casi-85-las-exportaciones-chinas-de-autos-de-pasajeros-en-abril"),
            ("BioBioChile", "https://www.biobiochile.cl/noticias/economia/mercado-automotriz/2026/05/20/con-china-liderando-preven-que-casi-uno-de-cada-tres-autos-vendidos-a-nivel-global-seran-electricos.shtml"),
        ],
    },
    {
        "emoji": "🌍",
        "titulo": "China elimina aranceles a 53 países africanos: nueva era del libre comercio Sur-Sur",
        "cuerpo": (
            "Desde el 1 de mayo de 2026, China suspendió todos sus aranceles a los 53 países africanos con "
            "los que mantiene relaciones diplomáticas, en una medida vigente hasta 2028. El primer cargamento "
            "histórico bajo esta política fue el de 24 toneladas de manzanas sudafricanas llegadas a China "
            "con arancel cero. En paralelo, Brasil estudia impulsar el primer acuerdo comercial parcial entre "
            "el Mercosur y China, lo que marcaría un hito en la relación entre la mayor economía de América "
            "Latina y Pekín."
        ),
        "fuentes": [
            ("Infobae", "https://www.infobae.com/america/agencias/2026/02/14/china-suspendera-todos-sus-aranceles-a-mas-de-medio-centenar-de-paises-de-africa-a-partir-del-1-de-mayo/"),
            ("La República", "https://larepublica.pe/mundo/2026/05/01/un-pais-africano-desafia-las-barreras-comerciales-y-envia-24-toneladas-de-manzanas-a-china-con-arancel-cero-72201"),
        ],
    },
    {
        "emoji": "⚡",
        "titulo": "Hito histórico: la energía solar en China supera al carbón por primera vez en capacidad instalada",
        "cuerpo": (
            "En 2026, China alcanza un punto de inflexión en su historia energética: la energía solar supera "
            "por primera vez al carbón en capacidad instalada. La potencia renovable ya en funcionamiento "
            "supera 1,6 teravatios, con 448 GW adicionales en construcción —la mitad del total mundial en "
            "esa fase—. Para finales de 2026, las energías no fósiles representarán el 63% de la capacidad "
            "instalada total. China también instaló 120,5 GW de nueva capacidad eólica en 2025: 3 de cada "
            "4 megavatios de nueva eólica instalados en el planeta fueron chinos."
        ),
        "fuentes": [
            ("Ecoticias", "https://www.ecoticias.com/energias-renovables/china-lidera-la-energia-solar-superando-al-carbon-por-primera-vez"),
            ("Ember", "https://ember-energy.org/es/analisis/global-electricity-review-2026/"),
            ("Energy News ES", "https://www.energynews.es/record-capacidad-eolica-y-solar-2026/"),
        ],
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 se prepara para su lanzamiento en agosto: China cazará agua en el polo sur lunar",
        "cuerpo": (
            "Todos los módulos de la misión Chang'e-7 han llegado a la Base Espacial de Wenchang para las "
            "pruebas previas al lanzamiento previsto para agosto de 2026. La misión incluye un orbitador, "
            "un módulo de aterrizaje, un rover y una sonda mini-saltadora diseñada para explorar los "
            "cráteres en sombra permanente del polo sur lunar, donde se cree que existe hielo. La misión "
            "llevará 21 cargas científicas, incluyendo 6 internacionales, en lo que la CNSA describe como "
            "la primera búsqueda real de hielo lunar para la humanidad. Es una pieza clave del plan chino "
            "de establecer una base lunar permanente antes de 2035."
        ),
        "fuentes": [
            ("Space.com", "https://www.space.com/the-universe/moon/hopping-robot-will-hunt-for-moon-water-on-chinas-2026-lunar-mission"),
            ("China In Space", "https://www.china-in-space.com/p/change-7-to-start-searching-for-lunar"),
            ("Planetary.org", "https://www.planetary.org/space-missions/change-7"),
        ],
    },
]


def build_blocks():
    blocks = [
        callout("Newsletter semanal · China Al Dia · 22-29 mayo 2026", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, IA, economia, energia y espacio."),
        divider(),
    ]

    for n in NOTICIAS:
        blocks.append(h2(f"{n['emoji']}  {n['titulo']}"))
        blocks.append(p(n["cuerpo"]))
        blocks.append(p_links(n["fuentes"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 22-29 Mayo 2026"
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
