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
        "titulo": '"Oportunidad China 2.0": Li Qiang en el Davos de Verano de Dalian',
        "cuerpo": (
            "El Foro Económico Mundial celebró su XVII Reunión Anual de los Nuevos Campeones en Dalian "
            "(China) del 23 al 25 de junio, con más de 1.700 participantes de más de 90 países. El "
            "primer ministro Li Qiang acuñó el término 'Oportunidad China 2.0' en su discurso inaugural, "
            "argumentando que los avances tecnológicos del país —vehículos eléctricos, paneles solares, "
            "chips, baterías, IA y robótica— representan una oportunidad global, no una amenaza. "
            "El mensaje fue claro: China quiere ser el motor de asequibilidad tecnológica del mundo."
        ),
        "fuente_label": "La Jornada — Avances tecnológicos de China son una oportunidad, no una amenaza",
        "fuente_url": "https://www.jornada.com.mx/noticia/2026/06/24/economia/avances-tecnologicos-de-china-son-una-oportunidad-no-una-amenaza-dice-el-premier-li-quiang",
    },
    {
        "emoji": "💾",
        "titulo": "BYD lanza el primer chip chino de 4 nm para vehículos autónomos",
        "cuerpo": (
            "BYD presentó el primer chip chino de 4 nanómetros diseñado específicamente para la "
            "conducción autónoma. El fabricante chino, ya líder mundial en vehículos eléctricos, "
            "consolida su apuesta por la integración vertical: producir sus propios chips de última "
            "generación para reducir dependencias y acelerar el desarrollo de la autoconducción. "
            "Además, la nueva generación de su batería Blade carga en menos de 10 minutos, "
            "fijando un nuevo estándar en el sector."
        ),
        "fuente_label": "Bloomberg — BYD presenta el primer chip chino de 4 nm para autos autónomos",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-05-28/byd-presenta-el-primer-chip-chino-de-4-nm-para-autos-autonomos",
    },
    {
        "emoji": "🤖",
        "titulo": "BYD entra en la carrera de los robots humanoides",
        "cuerpo": (
            "El vicepresidente ejecutivo de BYD, Li Ke, confirmó que la compañía está desarrollando "
            "sus propios robots humanoides, transfiriendo las tecnologías que ya domina en automoción: "
            "sensores, inteligencia artificial, sistemas de control y baterías. El mercado chino de "
            "robótica humanoide supera ya los 150 fabricantes nacionales, y el gobierno está impulsando "
            "la consolidación del sector para crear gigantes capaces de competir a escala global."
        ),
        "fuente_label": "Emol — BYD desafía a Tesla en un nuevo frente: robots humanoides",
        "fuente_url": "https://www.emol.com/noticias/Autos/2026/06/09/1202308/byd-desarrollo-robots-humanoides.html",
    },
    {
        "emoji": "🧠",
        "titulo": "Primera zona de IA en la IV Exposición Internacional de la Cadena de Suministro",
        "cuerpo": (
            "La IV Exposición Internacional de la Cadena de Suministro de China (CISCE), celebrada "
            "el 25 de junio en Pekín, incorporó por primera vez un área específica de Tecnología "
            "Digital con una zona de inteligencia artificial. La exhibición cubrió todo el ecosistema "
            "de la IA, desde la recopilación de datos hasta sus aplicaciones industriales reales, "
            "reuniendo a los actores tecnológicos más relevantes del país."
        ),
        "fuente_label": "Xinhua — Área de IA debuta en la cuarta CISCE en Beijing",
        "fuente_url": "http://spanish.xinhuanet.com/20260626/cf1b2ce139034221af39abe410db9cba/c.html",
    },
    {
        "emoji": "⚡",
        "titulo": "Energía solar desde el espacio: China transmite 1.180 vatios sin cables a 100 metros",
        "cuerpo": (
            "El proyecto Zhuri de la Academia China de Tecnología Espacial superó un hito importante: "
            "la transmisión inalámbrica de 1.180 vatios de energía solar a 100 metros de distancia "
            "sin un solo cable, logrando incluso cargar un dron en pleno vuelo. El plan completo "
            "contempla una estación solar en órbita de 2 GW para 2050, con versiones intermedias de "
            "500 kW en 2030 y 20 MW en 2035. Un proyecto que podría redefinir el suministro "
            "energético global."
        ),
        "fuente_label": "Ecosistema Startup — Zhuri: China logra 1.180W de energía solar espacial",
        "fuente_url": "https://ecosistemastartup.com/zhuri-china-logra-1-180w-de-energia-solar-espacial-en-2026/",
    },
    {
        "emoji": "🚄",
        "titulo": "China renueva su diagrama ferroviario desde el 1 de julio: +106 trenes de pasajeros",
        "cuerpo": (
            "A partir del 1 de julio, el sistema ferroviario nacional de China incorporó 106 nuevos "
            "servicios de trenes de pasajeros y 111 de carga, alcanzando un total de 12.174 trenes "
            "de pasajeros y 23.975 trenes de carga diarios en todo el país. El ajuste refleja la "
            "creciente demanda interna y la expansión continua de la red ferroviaria china, la más "
            "extensa del mundo en alta velocidad."
        ),
        "fuente_label": "Xinhua — Diagrama ferroviario de China ajustado a partir del 1 de julio",
        "fuente_url": "http://spanish.xinhuanet.com/20260701/f97ce80859b84bb28091589605c5637e/c.html",
    },
    {
        "emoji": "🏆",
        "titulo": "El ferrocarril Pekín-Shanghái cumple 15 años: 2.300 millones de pasajeros",
        "cuerpo": (
            "La línea de alta velocidad que une las dos mayores ciudades chinas celebró su 15.º "
            "aniversario el 1 de julio con una cifra impresionante: más de 2.300 millones de "
            "pasajeros transportados en 2,22 millones de viajes. Una de las infraestructuras más "
            "transitadas del planeta, y modelo de referencia internacional para los ferrocarriles "
            "de alta velocidad."
        ),
        "fuente_label": "People's Daily — Ferrocarril Beijing-Shanghai transporta más de 2.300 millones",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0701/c31614-20473001.html",
    },
    {
        "emoji": "🛤️",
        "titulo": "La primera línea ferroviaria privada de China alcanza 100 millones de pasajeros",
        "cuerpo": (
            "La línea Hangzhou-Taizhou (provincia de Zhejiang), la primera línea de alta velocidad "
            "de China financiada con capital privado, superó los 100 millones de pasajeros a menos "
            "de cuatro años y medio de su apertura. Un modelo innovador de colaboración público-privada "
            "que sirve como referencia para futuros proyectos de infraestructura en China."
        ),
        "fuente_label": "Xinhua — Primera línea ferroviaria privada transporta a más de 100 millones",
        "fuente_url": "http://spanish.xinhuanet.com/20260628/05e1abf0363347dd8a8d829c5211f64c/c.html",
    },
    {
        "emoji": "🚗",
        "titulo": "BYD supera de nuevo a Tesla: 557.000 vehículos eléctricos en Q2 2026",
        "cuerpo": (
            "BYD entregó 557.090 vehículos eléctricos puros en el segundo trimestre de 2026, "
            "volviendo a arrebatar el liderazgo mundial a Tesla. En junio, sus ventas totales "
            "alcanzaron 403.472 unidades, un 5,5% más interanual. El fabricante chino sigue "
            "acelerando su expansión internacional, enviando cada vez más vehículos a mercados "
            "de Asia, Europa y América."
        ),
        "fuente_label": "Bloomberg Línea — BYD está a punto de superar de nuevo a Tesla",
        "fuente_url": "https://www.bloomberglinea.com/negocios/byd-esta-a-punto-de-superar-de-nuevo-a-tesla-en-ventas-de-autos-electricos/",
    },
    {
        "emoji": "📈",
        "titulo": "Exportaciones chinas +21,8% con superávit comercial histórico de $213.600 millones",
        "cuerpo": (
            "Las exportaciones de China crecieron un 21,8% en los dos primeros meses de 2026, con "
            "un superávit comercial récord de 213.600 millones de dólares —muy por encima de los "
            "169.210 millones del mismo período de 2025—. Las exportaciones de semiconductores "
            "lideraron el crecimiento con un incremento del 66,5% interanual. El PIB chino creció "
            "un 5,0% en el Q1 2026, superando las previsiones del 4,8%."
        ),
        "fuente_label": "Ambito — Las exportaciones de China aumentaron un 21,8% en los dos primeros meses",
        "fuente_url": "https://www.ambito.com/economia/las-exportaciones-china-aumentaron-un-218-los-dos-primeros-meses-2026-n6254262",
    },
    {
        "emoji": "🎖️",
        "titulo": "105.º aniversario del PCCh: Xi Jinping otorga la Medalla 1 de Julio",
        "cuerpo": (
            "El 1 de julio, China conmemoró el 105.º aniversario de la fundación del Partido "
            "Comunista Chino. El presidente Xi Jinping presidió la ceremonia en el Gran Palacio "
            "del Pueblo en Pekín, donde otorgó la Medalla 1 de Julio —la máxima distinción del "
            "Partido— a ciudadanos destacados y pronunció un discurso sobre el rumbo del país."
        ),
        "fuente_label": "People's Daily — Xi otorgará Medalla 1 de Julio en 105.º aniversario del PCCh",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0630/c31621-20472428.html",
    },
    {
        "emoji": "🌍",
        "titulo": "IX Exposición China-Eurasia en Xinjiang: récord con 3.100 empresas participantes",
        "cuerpo": (
            "La IX Exposición China-Eurasia, celebrada del 25 al 29 de junio en Urumqi (Xinjiang), "
            "alcanzó cifras récord con más de 3.100 instituciones y empresas nacionales e "
            "internacionales participantes. El evento refuerza la apuesta china por la conectividad "
            "con Asia Central y el impulso a la Iniciativa de la Franja y la Ruta como plataforma "
            "de cooperación económica multilateral."
        ),
        "fuente_label": "People's Daily — Concluye IX Exposición China-Eurasia con cifras récord",
        "fuente_url": "http://spanish.peopledaily.com.cn/n3/2026/0701/c31620-20472993.html",
    },
    {
        "emoji": "🏭",
        "titulo": "He Lifeng insta a acelerar tecnologías clave y modernización industrial",
        "cuerpo": (
            "El viceprimer ministro He Lifeng visitó la provincia de Sichuan a finales de junio "
            "instando a acelerar el desarrollo de tecnologías fundamentales, agilizar la "
            "modernización del sistema industrial y fomentar nuevos motores de crecimiento "
            "económico. El mensaje se enmarca en la estrategia de China de construir las llamadas "
            "'Nuevas Fuerzas Productivas de Calidad', eje central del Plan Quinquenal 2026-2030."
        ),
        "fuente_label": "La Jornada — China insta a acelerar la modernización de sus industrias clave",
        "fuente_url": "https://www.jornada.com.mx/2026/06/29/economia/021n1eco",
    },
    {
        "emoji": "🗺️",
        "titulo": "XV Plan Quinquenal (2026-2030): IA, 6G, computación cuántica y energía limpia",
        "cuerpo": (
            "El XV Plan Quinquenal (2026-2030) de China integra por primera vez clima y energía en "
            "un mismo capítulo estratégico. Sus objetivos: despliegue de agentes IA con mínima "
            "supervisión humana en industria y sanidad; inversión ampliada en computación cuántica "
            "y red cuántica espacio-tierra; reducción de emisiones por unidad de PIB un 17% y "
            "elevación de energías no fósiles al 25% del consumo total para 2030; e investigación "
            "activa hacia el liderazgo en 6G."
        ),
        "fuente_label": "The Quantum Insider — China's New Five-Year Plan targets Quantum and AI",
        "fuente_url": "https://thequantuminsider.com/2026/03/05/chinas-new-five-year-plan-specifically-targets-quantum-leadership-and-ai-expansion/",
    },
]


def build_blocks():
    today = date.today().strftime("%d de %B de %Y")
    blocks = [
        callout(f"Newsletter semanal · China Al Dia · {today}", "🇨🇳"),
        p("Recopilacion de las noticias mas relevantes de China esta semana: tecnologia, economia, infraestructura, diplomatica y sociedad.", bold=False),
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
    title = "China Al Dia — Semana 26 Junio - 2 Julio 2026"
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
