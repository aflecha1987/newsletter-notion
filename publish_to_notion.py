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

def p_links(links):
    rich = [{"type": "text", "text": {"content": "Fuentes: "}, "annotations": {"bold": True}}]
    for i, (label, url) in enumerate(links):
        if i > 0:
            rich.append({"type": "text", "text": {"content": " · "}})
        rich.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}}

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
        "emoji": "⚛️",
        "titulo": "China logra producción masiva de silicio-28: hito para la computación cuántica",
        "cuerpo": (
            "El 15 de junio, el Instituto de Investigación de Ingeniería Física y Química Nuclear de China "
            "(RIPCENI/CNNC) anunció la producción masiva independiente de silicio-28 con pureza isotópica "
            "superior al 99,99%, la primera vez que China produce a escala industrial este material sin "
            "dependencia extranjera. El silicio-28 tiene espín nuclear cero, lo que reduce drásticamente "
            "el ruido ambiental en los cálculos cuánticos. Conocido como el «silicio más puro», es el "
            "material indispensable para los chips cuánticos basados en silicio. El avance cierra un "
            "eslabón crítico en la cadena de suministro cuántica china y allana el camino hacia "
            "procesadores cuánticos de alta fidelidad fabricados íntegramente en el país."
        ),
        "fuentes": [
            ("CGTN", "https://news.cgtn.com/news/2026-06-16/China-makes-breakthrough-in-material-for-silicon-quantum-chips-1O0W3x6yRLq/p.html"),
            ("Xinhua", "https://english.news.cn/20260615/1c859c2798b943b1bf1bedf28455f135/c.html"),
            ("SCMP", "https://www.scmp.com/tech/article/3357170/china-reaches-mass-production-key-isotope-quantum-computing-beijing-says"),
            ("Global Times", "https://www.globaltimes.cn/page/202606/1363574.shtml"),
        ],
    },
    {
        "emoji": "🤖",
        "titulo": "Los modelos de IA chinos alcanzan la frontera global: GLM-5.2 supera a Claude en programación",
        "cuerpo": (
            "El ecosistema chino de IA llega a junio de 2026 en su punto más competitivo. Zhipu AI lanzó "
            "GLM-5.2, que encabeza el ranking BenchLM con una puntuación de 94 y supera a Claude Opus 4.6 "
            "en benchmarks clave de programación (SWE-bench: 77,8%). Qwen 3-Max de Alibaba lidera "
            "Arena-Hard con un 90,5 y ofrece hasta 1 millón de tokens de contexto; DeepSeek V3.2 mantiene "
            "el trono de la relación precio/rendimiento. China cuenta con 602 millones de usuarios de IA "
            "generativa, más de la mitad del total mundial, y el sector creció un 33% adicional esta semana "
            "tras la restricción de EE.UU. sobre modelos extranjeros. Los laboratorios chinos de IA han "
            "alcanzado la frontera global, compitiendo de tú a tú con OpenAI, Google y Anthropic."
        ),
        "fuentes": [
            ("SCMP – GLM-5", "https://www.scmp.com/tech/tech-trends/article/3343225/deepseek-boosts-ai-model-10-fold-token-addition-zhipu-ai-gears-glm-5-launch"),
            ("BenchLM", "https://benchlm.ai/best/chinese-models"),
            ("TokenMix", "https://tokenmix.ai/blog/best-chinese-ai-models-2026-comparison-guide"),
        ],
    },
    {
        "emoji": "🚀",
        "titulo": "Shenzhou-23 en órbita: primer astronauta de Hong Kong y un año en el espacio",
        "cuerpo": (
            "El 24 de mayo, China lanzó la Shenzhou-23 con tres astronautas a la estación espacial Tiangong. "
            "Un astronauta permanecerá en órbita durante un año completo para estudiar la adaptación humana "
            "a los vuelos de larga duración, ensayo crucial de cara al viaje tripulado a la Luna antes de 2030. "
            "Entre la tripulación figura Lai Ka-ying, la primera astronauta procedente de Hong Kong en llegar "
            "al espacio. La misión ejecutará más de 100 nuevos proyectos científicos en biología espacial, "
            "ciencia de materiales, física de fluidos en microgravedad y medicina aeroespacial. Esta semana "
            "la estación Tiangong superó los 1.800 días consecutivos de operación tripulada ininterrumpida."
        ),
        "fuentes": [
            ("Xinhua", "https://english.news.cn/20260525/e71e193dd1d14e1193edc9173f3f0477/c.html"),
            ("NPR", "https://www.npr.org/2026/05/25/g-s1-124179/china-launches-shenzhou-23-spacecraft"),
            ("Space.com", "https://www.space.com/space-exploration/human-spaceflight/china-shenzhou-23-astronaut-launch-tiangong-space-station"),
        ],
    },
    {
        "emoji": "🚗",
        "titulo": "Los vehículos eléctricos ya son el 67% de las ventas de coches en China en junio",
        "cuerpo": (
            "En la primera semana de junio de 2026, los NEV representaron el 67% de las ventas de turismos "
            "en China. En mayo, el ranking de los diez más vendidos quedó dominado completamente por eléctricos "
            "e híbridos enchufables, sin un solo modelo de combustión. BYD registró en junio 352.081 NEV "
            "vendidos (+25,7% interanual, cuota del 31,7%), y sus exportaciones internacionales alcanzaron "
            "en mayo el récord histórico de 160.644 unidades (+80% interanual). Según la IEA, la flota "
            "eléctrica e híbrida china ha reducido la demanda nacional de petróleo en más de 1 millón de "
            "barriles diarios. China lidera la mayor transición energética del transporte de la historia."
        ),
        "fuentes": [
            ("Global China EV – BYD mayo", "https://www.globalchinaev.com/post/byd-leads-chinas-record-may-nev-month-with-377000-units-and-surging-exports"),
            ("Power Peak Digest", "https://powerpeakdigest.com/china-top-10-car-sales-fully-electric-may-2026/"),
            ("IEA – Global EV Outlook 2026", "https://www.iea.org/reports/global-ev-outlook-2026/trends-in-electric-cars"),
        ],
    },
    {
        "emoji": "🔋",
        "titulo": "CATL apunta a baterías litio-aire con densidad energética comparable a la gasolina",
        "cuerpo": (
            "CATL, el mayor fabricante mundial de baterías, reveló en junio su apuesta estratégica por "
            "las baterías de litio-aire, con una densidad energética teórica de 12.000 Wh/kg, comparable "
            "a la gasolina (~13.000 Wh/kg). Los prototipos actuales ya alcanzan más de 1.200 Wh/kg, cuatro "
            "veces la de las baterías comerciales actuales. En paralelo, la empresa presentó en abril su nueva "
            "gama: baterías de carga en 6 minutos y modelos de hasta 1.500 km de autonomía. Abu Dabi firmó "
            "esta semana acuerdos con CATL y otras 21 empresas chinas para cooperar en almacenamiento "
            "energético, VE y energías renovables. El dominio chino en tecnología de baterías se proyecta "
            "como uno de los ejes de la economía global de la próxima década."
        ),
        "fuentes": [
            ("CleanTechnica", "https://cleantechnica.com/2026/06/06/catl-developing-12000-wh-per-kg-lithium-air-battery/"),
            ("CarNewsChina", "https://carnewschina.com/2026/06/03/catl-sets-sights-on-lithium-air-technology-with-theoretical-gasoline-level-12000-wh-kg-energy-density/"),
            ("The Driven", "https://thedriven.io/2026/04/22/catl-debuts-six-stunning-battery-innovations-including-1500km-ev-option-and-6-minute-charge/"),
        ],
    },
    {
        "emoji": "📈",
        "titulo": "El comercio exterior de China supera los 20 billones de yuanes en los primeros 5 meses",
        "cuerpo": (
            "Datos oficiales publicados el 9 de junio revelan que el comercio exterior chino en los cinco "
            "primeros meses de 2026 alcanzó 20,68 billones de yuanes (~2,86 billones de dólares), con un "
            "crecimiento interanual del 15,3%. Las exportaciones crecieron un 11,8% y las importaciones "
            "un 20,5%, señal de recuperación de la demanda interna. Las exportaciones de abril batieron el "
            "récord mensual histórico: 359.440 millones de dólares (+14,1% interanual), impulsadas por "
            "semiconductores, equipos de procesamiento de datos y productos de IA. Morgan Stanley, Deutsche "
            "Bank y otras entidades internacionales han revisado al alza sus previsiones de crecimiento del "
            "PIB chino para 2026, apuntando a un desempeño por encima del objetivo oficial del 4,5-5%."
        ),
        "fuentes": [
            ("Últimas Noticias", "https://ultimasnoticias.com.ve/opinion/comercio-exterior-chino-crece-mas-de-lo-esperado-en-los-primeros-cinco-meses-de-2026/"),
            ("China Briefing", "https://www.china-briefing.com/news/chinas-economy-in-2026-january-february-rebound/"),
            ("Unbox Future", "https://www.unboxfuture.com/2026/06/chinas-economy-in-5-numbers-growth-debt.html"),
        ],
    },
    {
        "emoji": "💡",
        "titulo": "Chips fotónicos sin litografía DUV: China reduce costes un 90% en semiconductores avanzados",
        "cuerpo": (
            "La industria china de chips fotónicos vive su «ventana dorada». CHIPX (Shanghai Jiao Tong "
            "University) produce ya obleas de silicato de niobato de litio de 6 pulgadas con ancho de "
            "banda de modulación superior a 110 GHz, superando el límite de 60 GHz de la fotónica de "
            "silicio tradicional. Una startup china fue más lejos aún: fotolitografía sin DUV mediante "
            "nanoimprenta, reduciendo los costes un 90% y fabricando obleas de 8 pulgadas sin equipamiento "
            "occidental. Estos chips son críticos para centros de datos de IA, infraestructura 6G y "
            "computación cuántica. El conjunto de avances posiciona a China como potencia emergente en "
            "fotónica de alta gama, el segmento de mayor valor añadido de la cadena de semiconductores."
        ),
        "fuentes": [
            ("Tom's Hardware", "https://www.tomshardware.com/tech-industry/semiconductors/chinese-startup-claims-photonic-chip-production-without-duv-lithography-says-nanoimprint-process-cuts-costs-by-90-percent-8-inch-wafers-produced-without-conventional-optical-lithography"),
            ("The Quantum Insider", "https://thequantuminsider.com/2025/06/13/china-ramps-up-photonic-chip-production-with-eye-on-ai-and-quantum-computing/"),
            ("Pandaily", "https://pandaily.com/china-optical-chip-golden-window-high-end-jun2026"),
        ],
    },
    {
        "emoji": "⚡",
        "titulo": "Viento y solar superan el 25% de la electricidad mensual de China por primera vez en la historia",
        "cuerpo": (
            "En el último mes registrado, la energía eólica y solar generaron más de una cuarta parte de "
            "toda la electricidad consumida en China, un hito histórico según Ember. La capacidad acumulada "
            "de viento y solar supera ya 1.840 GW, representando el 47,3% de la capacidad total instalada "
            "y superando por primera vez a la térmica. China instaló 370 GW de solar fotovoltaica y 117 GW "
            "de eólica solo en 2025, y el ritmo de 2026 continúa al alza. El plan de doblar la energía "
            "limpia para 2035 ya parece conservador dado el ritmo actual de despliegue. Las dos grandes "
            "eléctricas estatales invertirán 1 billón de yuanes anuales durante el 15.º Plan Quinquenal "
            "(2026-2030), consolidando a China como el mayor instalador de energía renovable de la historia."
        ),
        "fuentes": [
            ("Ember", "https://ember-energy.org/latest-updates/wind-and-solar-generate-over-a-quarter-of-chinas-electricity-for-the-first-month-on-record/"),
            ("IEA – Global Energy Review 2026", "https://www.iea.org/reports/global-energy-review-2026/technology-solar-pv-and-wind"),
            ("SolarQuarter", "https://solarquarter.com/2026/01/30/china-sets-new-solar-pv-installation-record-reaches-halfway-to-2035-renewable-goals/"),
        ],
    },
]


def build_blocks():
    blocks = [
        callout("Newsletter semanal · China Al Dia · Semana del 11 al 17 de junio de 2026", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: computacion cuantica, IA, espacio, vehiculos electricos, baterias, economia y energia renovable.", bold=False),
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
    title = "China Al Dia — Semana 11-17 Junio 2026"
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
