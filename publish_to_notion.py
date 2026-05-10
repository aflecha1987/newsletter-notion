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
    """sources: list of (label, url) tuples"""
    rich_text = [{"type": "text", "text": {"content": "Fuentes: "}}]
    for i, (label, url) in enumerate(sources):
        rich_text.append({
            "type": "text",
            "text": {"content": label, "link": {"url": url}},
            "annotations": {"italic": True, "color": "blue"}
        })
        if i < len(sources) - 1:
            rich_text.append({"type": "text", "text": {"content": " · "}})
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
        "emoji": "🧠",
        "titulo": "DeepSeek V4: la IA china que no necesita a Nvidia sacude el mercado global",
        "cuerpo": (
            "El 8 de mayo, DeepSeek redujo un 75% el precio de su nuevo modelo V4-Pro —hasta el 31 de mayo—, "
            "disparando su adopción masiva. V4-Pro (1,6 billones de parámetros totales, 49.000 millones activos) "
            "y V4-Flash, su versión rápida y económica, fueron entrenados íntegramente con chips Ascend de Huawei, "
            "sin hardware de Nvidia. El modelo lidera benchmarks de código, es solo ligeramente superado por "
            "Gemini-3.1-Pro en conocimiento mundial y llega como código abierto en Hugging Face. El precio del "
            "millón de tokens de entrada cae a 0,435 dólares, hasta 7 veces más barato que Claude Opus. "
            "Alibaba, ByteDance y Tencent ya realizaron pedidos masivos de chips Ascend ante la demanda desbordante."
        ),
        "fuentes": [
            ("Expansion.mx", "https://expansion.mx/tecnologia/2026/05/08/deepseek-baja-precio-de-su-nuevo-modelo"),
            ("Xataka", "https://www.xataka.com/empresas-y-economia/deepseek-v4-ha-dado-a-china-impulso-que-necesita-frente-a-eeuu-cuatro-fabricantes-chips-grandes-ganadores"),
            ("ITSitio", "https://www.itsitio.com/inteligencia-artificial/deepseek-v4-pro-irrumpe-en-la-ia-hasta-7-veces-mas-barato-que-claude-opus-y-con-rendimiento-lider-en-programacion/"),
        ],
    },
    {
        "emoji": "💾",
        "titulo": "DeepSeek V4 dispara la producción de chips chinos: Huawei y Cambricon son los grandes ganadores",
        "cuerpo": (
            "El éxito de DeepSeek V4 está teniendo un efecto multiplicador sobre el ecosistema doméstico de "
            "semiconductores. Por primera vez, varios fabricantes chinos garantizan compatibilidad total con "
            "un modelo de vanguardia desde el día cero: Huawei, Cambricon, Moore Threads e Hygon. Huawei planea "
            "fabricar alrededor de 600.000 chips Ascend 910C en 2026, el doble de su producción anterior. "
            "Cambricon apunta a entregar 500.000 aceleradores de IA este año, con planes de triplicar su "
            "producción. Las exportaciones de chips chinos crecieron un 72,6% en los dos primeros meses de "
            "2026, marcando un récord histórico y un reposicionamiento estructural en el mapa tecnológico global."
        ),
        "fuentes": [
            ("Que.es", "https://www.que.es/2026/05/07/deepseek-v4-impulsa-chips-chinos-huawei/"),
            ("Tom's Hardware", "https://www.tomshardware.com/tech-industry/semiconductors/cambricon-targets-500000-ai-chips-in-2026-as-china-accelerates-domestic-hardware-push"),
            ("Bloomberg Línea", "https://www.bloomberglinea.com/negocios/huawei-duplicara-su-produccion-de-chips-de-ia-en-2026-para-desafiar-a-nvidia/"),
        ],
    },
    {
        "emoji": "🏥",
        "titulo": "IA médica china rompe los 4 grandes cuellos de botella de los modelos de lenguaje",
        "cuerpo": (
            "El 8 de mayo, el Instituto de Salud Prome (Zhejiang) presentó un sistema de IA médica con "
            "arquitectura de cognición jerárquica que aborda los cuatro problemas sistémicos de los grandes "
            "modelos de lenguaje: razonamiento de caja negra inexplicable, alucinaciones de contenido, "
            "dependencia excesiva de potencia computacional y olvido catastrófico. Si las pruebas de terceros "
            "confirman los resultados, este avance podría acelerar de forma significativa la adopción de la "
            "IA en sectores de alta fiabilidad como la sanidad."
        ),
        "fuentes": [
            ("Submit My Press Release", "https://newsroom.submitmypressrelease.com/2026/05/08/china-tackles-core-technical-bottlenecks-of-large-language-models-original-hierarchical-cognition-ai-forges-a-new-industrial-paradigm_2381126.html"),
        ],
    },
    {
        "emoji": "🤖",
        "titulo": "Robots e IA en el corazón del Plan Quinquenal: China lidera el mercado real de la robótica",
        "cuerpo": (
            "La Federación Internacional de Robótica confirmó que China ha situado los robots con inteligencia "
            "artificial como eje central de su estrategia industrial nacional. El país ya cuenta con un parque "
            "operativo de aproximadamente 2 millones de robots industriales, y el 54% de todos los robots "
            "industriales instalados en el mundo en 2025 se desplegaron en China. Los fabricantes de vehículos "
            "eléctricos (GAC, BYD, XPeng y Xiaomi) aceleran su entrada en humanoides para uso fabril y "
            "comercial; GAC planea producción en serie de su robot GoMate en 2026. BYD ya tiene el robot "
            "humanoide Walker S1 trabajando en sus fábricas."
        ),
        "fuentes": [
            ("IFR", "https://ifr.org/ifr-press-releases/news/china-makes-ai-powered-robots-core-of-national-strategy"),
            ("WardsAuto", "https://www.wardsauto.com/news/chinese-automakers-continue-advancements-in-humanoid-robots/799172/"),
            ("MIT Technology Review", "https://www.technologyreview.com/2025/02/14/1111920/chinas-electric-vehicle-giants-pivot-humanoid-robots/"),
        ],
    },
    {
        "emoji": "📈",
        "titulo": "Comercio exterior de China crece 14,9% en los primeros cuatro meses de 2026",
        "cuerpo": (
            "China mantuvo un ritmo de expansión sólido en su comercio exterior: 14,9% interanual en los "
            "primeros cuatro meses del año, hasta los 16,23 billones de yuanes (2,24 billones de dólares). "
            "En abril, las exportaciones subieron un 9,8% y las importaciones un 20,6%, reflejo de la "
            "recuperación de la demanda interna. Destacan las exportaciones de vehículos eléctricos (+68,1%), "
            "baterías de litio (+43,2%) y turbinas eólicas (+40,7%). La ASEAN se consolida como primer socio "
            "comercial (+15,7%), seguida de la UE (+13,2%). El comercio con África superó por primera vez "
            "los 800.000 millones de yuanes en solo cuatro meses, un salto del 19,4%."
        ),
        "fuentes": [
            ("Prensa Latina", "https://www.prensa-latina.cu/2026/05/09/china-mantiene-estable-su-crecimiento-en-comercio-exterior/"),
            ("People's Daily Español", "http://spanish.peopledaily.com.cn/n3/2026/0509/c31621-20454569.html"),
            ("La Jornada", "https://www.jornada.com.mx/2026/05/06/economia/015n1eco"),
        ],
    },
    {
        "emoji": "🚄",
        "titulo": "China supera los 50.000 km de alta velocidad ferroviaria y sigue creciendo",
        "cuerpo": (
            "China alcanzó el hito histórico de más de 50.000 kilómetros de red ferroviaria de alta velocidad "
            "en operación, la más extensa del mundo por un amplio margen. La nueva línea Xi'an–Yan'an (Shaanxi), "
            "diseñada para trenes a 350 km/h, recorre los 299 kilómetros entre ambas ciudades en 68 minutos. "
            "Solo en el primer trimestre de 2026, los ferrocarriles chinos invirtieron 20.900 millones de "
            "dólares en activos fijos. El plan prevé poner en servicio 2.000 km adicionales durante 2026. "
            "En paralelo, China impulsa un megaproyecto ferroviario en Sudamérica valorado en más de 4.000 "
            "millones de dólares, previsto para 2027."
        ),
        "fuentes": [
            ("Excélsior", "https://www.excelsior.com.mx/internacional/china-50-mil-km-trenes-alta-velocidad-tecnologia-mexico"),
            ("Canal26", "https://www.canal26.com/internacionales/2026/05/04/megaingenieria-china-asi-es-el-tren-de-alta-velocidad-que-conectara-7-estaciones-clave-en-menos-de-60-minutos/"),
            ("La República", "https://larepublica.pe/mundo/2026/05/04/china-reta-a-eeuu-con-un-megaproyecto-que-transformara-el-transporte-ferroviario-de-un-pais-de-sudamerica-por-mas-de-us4000-millones-235940"),
        ],
    },
    {
        "emoji": "🌕",
        "titulo": "Chang'e-7 en cuenta atrás: invernaderos lunares para misiones prolongadas en el polo sur",
        "cuerpo": (
            "Con el lanzamiento previsto para agosto de 2026, la misión Chang'e-7 avanza en sus preparativos. "
            "Esta semana, la CNSA difundió el plan de invernaderos en la superficie lunar: estructuras "
            "autosuficientes capaces de producir alimentos en la Luna para sostener misiones de larga duración. "
            "La misión incluye un orbitador, aterrizador, rover y sonda mini-saltadora para explorar cráteres "
            "en sombra permanente del polo sur, donde podría existir agua en forma de hielo. El cohete Long "
            "March 5 despegará desde la isla de Hainan con un total de ocho toneladas de carga útil, "
            "convirtiéndola en la misión lunar más compleja de China hasta la fecha."
        ),
        "fuentes": [
            ("Canal26", "https://www.canal26.com/ciencia-y-espacio/2026/05/05/megaingenieria-fuera-de-la-tierra-china-avanza-en-invernaderos-lunares-para-cultivar-alimentos-en-la-luna/"),
            ("OKDiario Ciencia", "https://okdiario.com/ciencia/china-luna-2026-misiones-logros-objetivos-16568199"),
            ("Global Security", "https://www.globalsecurity.org/space/library/news/2026/space-260417-globaltimes01.htm"),
        ],
    },
    {
        "emoji": "☀️",
        "titulo": "Proyecto Zhuri: energía solar desde el espacio, las Tres Gargantas en órbita",
        "cuerpo": (
            "China avanza en su proyecto Zhuri (cazasol): una planta solar de 1 kilómetro de anchura en "
            "órbita geoestacionaria a 36.000 km de la Tierra, que captaría energía solar de forma continua "
            "—sin nubes, sin noche— y la transmitiría a la superficie mediante microondas. El científico jefe "
            "Long Lehao lo compara con situar las Tres Gargantas en el espacio. Su eficiencia supera en 10 "
            "veces a los paneles solares terrestres. La hoja de ruta prevé: test en órbita baja (10 kW) en "
            "2027-2028, estación de megavatio en órbita geoestacionaria en 2030, y despliegue de gigavatios "
            "en 2040-2050, con capacidad para producir más energía en un año que todo el petróleo de la Tierra."
        ),
        "fuentes": [
            ("Sustainability Magazine", "https://sustainabilitymag.com/articles/chinas-1km-solar-array-the-manhattan-project-of-energy"),
            ("Live Science", "https://www.livescience.com/space/space-exploration/china-plans-to-build-enormous-solar-array-in-space-and-it-could-collect-more-energy-in-a-year-than-all-the-oil-on-earth"),
            ("SCMP", "https://www.scmp.com/opinion/china-opinion/article/3347692/why-chinas-space-based-solar-power-next-frontier-green-energy"),
        ],
    },
    {
        "emoji": "💊",
        "titulo": "250 quioscos de diagnóstico con IA en el metro de Shanghái: medicina del futuro, hoy",
        "cuerpo": (
            "China ha desplegado más de 250 quioscos de diagnóstico asistido por IA en estaciones de metro, "
            "centros comerciales y zonas de alta afluencia de Shanghái. Los dispositivos miden presión "
            "arterial, frecuencia cardíaca, saturación de oxígeno y temperatura, mientras la IA integra "
            "criterios de la Medicina Tradicional China: análisis facial, observación de la lengua y lectura "
            "digital del pulso. El país cuenta ya con aproximadamente 300 grandes modelos médicos de IA y "
            "sus servicios de diagnóstico por imagen a distancia gestionaron más de 68 millones de casos "
            "el pasado año. El XV Plan Quinquenal sitúa la salud digital como área estratégica de liderazgo "
            "global para 2030."
        ),
        "fuentes": [
            ("Mundo Global", "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/"),
            ("People's Daily Español", "http://spanish.peopledaily.com.cn/n3/2026/0316/c31621-20436430.html"),
        ],
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
        blocks.append(p_links(n["fuentes"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 4-10 Mayo 2026"
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
