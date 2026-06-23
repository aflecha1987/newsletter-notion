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
        "emoji": "🌐",
        "titulo": "El 'Davos de Verano' se celebra en Dalian: China, epicentro de la innovación global",
        "cuerpo": (
            "Del 23 al 25 de junio, Dalian acoge la 17ª Reunión Anual de los Nuevos Campeones del Foro "
            "Económico Mundial bajo el lema 'Innovating at Scale'. Más de 1.700 líderes de más de 90 países "
            "debaten sobre IA, transición energética, el futuro del empleo y el comercio global. Un dato "
            "destacado: China ya cuenta con más de 6.000 empresas de IA y su industria central supera los "
            "1,2 billones de yuanes (~176.000 millones de dólares). La propia logística del foro muestra el "
            "compromiso verde del país: más del 80% de la flota de transporte son vehículos de nueva energía "
            "y el recinto principal funciona íntegramente con electricidad verde."
        ),
        "fuente_label": "WEF — Global Leaders Gather in Dalian for Summer Davos",
        "fuente_url": "https://www.weforum.org/press/2026/06/global-leaders-gather-in-dalian-for-summer-davos-to-unlock-innovation-at-scale/",
    },
    {
        "emoji": "💻",
        "titulo": "Huawei desafía la Ley de Moore con LogicFolding: chips de 1,4 nm en 2031",
        "cuerpo": (
            "El 25 de mayo, el presidente del negocio de semiconductores de Huawei presentó en la IEEE ISCAS "
            "de Shanghái la Ley Tau de Escalado y la arquitectura LogicFolding. La nueva teoría desplaza el "
            "foco de miniaturización de transistores (Ley de Moore) hacia la reducción del tiempo de propagación "
            "de señales dentro del chip. Huawei proyecta tener chips de 1,4 nanómetros para 2031 con tecnología "
            "propia, y sus primeros Kirin con LogicFolding llegarán al mercado antes de fin de año. La noticia "
            "generó 40 millones de visualizaciones en redes sociales chinas."
        ),
        "fuente_label": "Fortune — Huawei touts chip breakthrough to shorten gap with TSMC",
        "fuente_url": "https://fortune.com/2026/05/25/huawei-touts-chip-breakthrough-to-shorten-gap-with-tsmc/",
    },
    {
        "emoji": "🔗",
        "titulo": "4ª Expo de Cadenas de Suministro en Beijing: IA, apertura y 670 empresas globales",
        "cuerpo": (
            "El 22 de junio se inauguró en Beijing la 4ª Expo Internacional de Cadenas de Suministro de China "
            "(CISCE), bajo el lema 'Connecting the World for a Shared Future'. Con más de 670 empresas —un "
            "tercio extranjeras, incluyendo Nvidia, Intel y Qualcomm— y más de 1.200 entidades participantes, "
            "la expo incorpora por primera vez una zona dedicada exclusivamente a la inteligencia artificial. "
            "La feria abarca manufactura avanzada, energía limpia, vehículos inteligentes, tecnología digital, "
            "bioeconomía y las industrias del futuro: drones, inteligencia encarnada y biofabricación."
        ),
        "fuente_label": "CGTN — China's 2026 Supply Chain Expo debuts dedicated AI zone",
        "fuente_url": "https://news.cgtn.com/news/2026-05-22/China-s-2026-Supply-Chain-Expo-to-debut-dedicated-AI-zone-1Nm5GSmtcdO/index.html",
    },
    {
        "emoji": "🤖",
        "titulo": "Robots humanoides chinos: del espectáculo a los contratos reales",
        "cuerpo": (
            "China controla el 85% de las instalaciones mundiales de robots humanoides y produce unidades a "
            "un coste aproximado de 50.000 dólares, prácticamente la mitad que los competidores occidentales. "
            "En 2026 el sector da el salto decisivo: intralogística, ensamblaje simple e inspección industrial "
            "son los primeros casos de uso con valor comercial real. Las startups chinas de humanoides ya "
            "tienen contratos firmados con fábricas y centros comerciales, mientras la mayoría de sus rivales "
            "estadounidenses permanecen en fase de desarrollo o demostración."
        ),
        "fuente_label": "Rest of World — How China is using human labor to win the humanoid robot data race",
        "fuente_url": "https://restofworld.org/2026/china-ai-robotics-training-data/",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD: 'El 80% de los coches en China serán eléctricos pronto'",
        "cuerpo": (
            "El CEO de BYD declaró esta semana que espera que 4 de cada 5 automóviles vendidos en China "
            "sean de nueva energía en el futuro cercano, señalando que la transición eléctrica ha superado "
            "el punto de inflexión. En mayo, BYD puso fin a ocho meses de caída en ventas, impulsado por el "
            "SUV premium Da Tang —más de 100.000 reservas en sus primeras dos semanas— y el Sealion 06 DM-i. "
            "BYD prepara además su entrada en el mercado de camiones eléctricos y evalúa expansión en "
            "Canadá y Europa, donde avanza con su planta en Hungría."
        ),
        "fuente_label": "CNBC — BYD predicts 80% of China car sales will soon be electric",
        "fuente_url": "https://www.cnbc.com/2026/06/09/electric-vehicle-giant-byd-predicts-80percent-of-china-car-sales-will-soon-be-electric.html",
    },
    {
        "emoji": "🏭",
        "titulo": "Chongqing: la ciudad que produce más coches inteligentes que ninguna otra en el mundo",
        "cuerpo": (
            "El Foro Automotriz de China 2026 en Chongqing evidenció por qué esta megalópolis se ha convertido "
            "en el mayor productor automovilístico del planeta: en 2025 fabricó 2,788 millones de vehículos, "
            "incluyendo 1,296 millones de nueva energía —30 veces más que en 2020—. Changan Automobile obtuvo "
            "el primer lote de permisos chinos para conducción autónoma de nivel L3 en condiciones reales. "
            "La industria de IA de la ciudad creció un 23,6% en 2025 y Chongqing cuenta ya con cuatro "
            "'fábricas faro' certificadas por el Foro Económico Mundial."
        ),
        "fuente_label": "Gasgoo — China Auto Chongqing Summit: Auto Industry Competition Is Being Redefined",
        "fuente_url": "https://autonews.gasgoo.com/articles/news/china-auto-chongqing-summit-changan-auto-industry-competition-is-being-fundamentally-redefined-2067097399812816897",
    },
    {
        "emoji": "☀️",
        "titulo": "El 'sol artificial' chino logra 1.066 segundos de plasma: récord mundial absoluto",
        "cuerpo": (
            "El reactor de fusión nuclear EAST (Experimental Advanced Superconducting Tokamak), apodado el "
            "'sol artificial', mantuvo un bucle estable de plasma en confinamiento de alta energía durante "
            "1.066 segundos —más de 17 minutos—, duplicando su récord anterior de 403 segundos (2023). El "
            "hito, logrado el 20 de enero y publicado en Science Advances, es decisivo: los 1.000 segundos "
            "se consideran el umbral mínimo de viabilidad industrial para la fusión. La fusión nuclear figura "
            "ya como sector prioritario en el 15.º Plan Quinquenal, con planes para un reactor piloto en 2035 "
            "y uno de demostración para 2045."
        ),
        "fuente_label": "New Atlas — China sets new fusion endurance record of over a thousand seconds",
        "fuente_url": "https://newatlas.com/energy/china-east-fusion-endurance-record-1000-seconds/",
    },
    {
        "emoji": "🛸",
        "titulo": "China lleva la energía solar al espacio: primeros paneles orbitales en 2026",
        "cuerpo": (
            "La Academia China de Tecnología Espacial (CAST) planea desplegar sus primeros paneles solares "
            "de 10 kW en órbita geoestacionaria —a 36.000 kilómetros de la Tierra— para demostrar la "
            "transmisión inalámbrica de energía hacia la superficie terrestre. La Estación Solar Espacial "
            "permitiría generar electricidad 24 horas al día sin nubes ni noche y enviarla a tierra mediante "
            "microondas o láser, con una eficiencia estimada 8 veces superior a los paneles terrestres. "
            "En paralelo, China ya supera 1.230 GW de capacidad solar instalada en tierra, con un crecimiento "
            "interanual del 33,2%."
        ),
        "fuente_label": "Xataka — China ha puesto fecha a su estación solar espacial",
        "fuente_url": "https://www.xataka.com/energia/china-ha-puesto-fecha-a-mayor-obra-ingenieria-proyectada-a-36-000-km-tierra-su-estacion-solar-espacial",
    },
    {
        "emoji": "🌎",
        "titulo": "China lleva energía solar a Cuba y América Latina en plena crisis energética global",
        "cuerpo": (
            "En el contexto del bloqueo energético a Cuba y los apagones masivos en la isla, China anunció "
            "el envío de tecnología solar para ayudar a restaurar el suministro eléctrico cubano. Asimismo, "
            "China y Ecuador sellaron una inversión de 400 millones de dólares de Power China en proyectos "
            "de energías renovables. En conjunto, China ha invertido casi 34.000 millones de dólares en 70 "
            "proyectos renovables en América Latina desde 2010, con ocho de los diez principales proveedores "
            "de paneles solares de la región de origen chino, consolidando su papel como motor de la "
            "transición energética en el Sur Global."
        ),
        "fuente_label": "SCMP — China to help Cuba with solar energy amid US oil blockade",
        "fuente_url": "https://www.scmp.com/economy/china-economy/article/3346978/china-help-cuba-solar-energy-amid-us-oil-blockade-and-total-power-outage",
    },
    {
        "emoji": "🤝",
        "titulo": "XI Diálogo Estratégico China-Reino Unido: cooperación en IA, finanzas y comercio",
        "cuerpo": (
            "El canciller chino Wang Yi participó esta semana en el XI Diálogo Estratégico China-Reino Unido, "
            "donde pidió a Londres garantizar un entorno empresarial justo para las compañías chinas y "
            "profundizar la cooperación bilateral en comercio, finanzas e inteligencia artificial. El "
            "encuentro refleja la disposición de Pekín a construir puentes con socios europeos, reforzando "
            "su política de apertura multilateral como eje del 15.º Plan Quinquenal. En paralelo, el "
            "Ministerio de Comercio chino añadió diez entidades estadounidenses a su lista de controles "
            "de exportación, calibrando firmeza con apertura selectiva."
        ),
        "fuente_label": "Observatorio de Política China — Cronología junio 2026",
        "fuente_url": "https://www.politica-china.org/cronologia-opch-119/",
    },
]


def build_blocks():
    today = "23 de junio de 2026"
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, energia, espacio y cooperacion internacional.", bold=False),
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
    title = "China Al Dia — Semana 16-23 Junio 2026"
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
