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


NOTICIAS_ABRIL = [
    {
        "emoji": "🏃",
        "titulo": "Robot humanoide bate el récord mundial de la media maratón en Pekín",
        "cuerpo": (
            "El 19 de abril, el robot humanoide Lightning, desarrollado por Honor (spin-off de Huawei), "
            "completó los 21 km de la media maratón de E-Town en Pekín en tan solo 50 minutos y 26 segundos, "
            "superando el récord mundial humano por más de 6 minutos. Honor copó los tres primeros puestos "
            "de la categoría robótica, con todos los finalistas corriendo de forma completamente autónoma, "
            "sin control remoto. Más de 100 equipos participaron este año, casi cinco veces más que en la "
            "edición inaugural de 2025, donde el ganador tardó 2 horas y 40 minutos. Un hito que marca el "
            "ritmo vertiginoso del desarrollo robótico chino."
        ),
        "fuente_label": "NPR — Humanoid robot wins Beijing half-marathon",
        "fuente_url": "https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon",
    },
    {
        "emoji": "🚗",
        "titulo": "Exportaciones de vehículos eléctricos chinos baten récord histórico: +140%",
        "cuerpo": (
            "Las exportaciones chinas de vehículos eléctricos e híbridos se dispararon un 140% interanual "
            "en marzo de 2026, alcanzando 349.000 unidades, el nivel más alto jamás registrado. El principal "
            "catalizador fue el shock del precio del petróleo provocado por tensiones en el Estrecho de Ormuz, "
            "que empujó a compradores de Asia-Pacífico, Europa y América a pasarse al vehículo eléctrico. "
            "BYD lideró las exportaciones, seguida de Geely y Chery. La compañía china más grande del mundo "
            "en vehículos eléctricos apunta a 1,5 millones de ventas en el exterior en 2026, un 15% más de "
            "su objetivo anterior, consolidando su posición global."
        ),
        "fuente_label": "Bloomberg — China's EV Exports Jump to Record",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-09/china-ev-exports-jump-to-record-as-iran-oil-shock-entices-buyers",
    },
    {
        "emoji": "🤖",
        "titulo": "China producirá un 94% más robots con IA en 2026: el sector vive su época dorada",
        "cuerpo": (
            "Decenas de fabricantes chinos de robótica anunciaron planes para aumentar su producción de "
            "robots con inteligencia artificial incorporada en un 94% durante 2026. El sector abarca desde "
            "robots diseñados para entornos de alto riesgo (instalaciones energéticas, tanques químicos, "
            "plataformas marinas) hasta robots de servicio para el cuidado de personas mayores. Las "
            "startups chinas de humanoides ya están enviando unidades a fábricas y centros comerciales "
            "con contratos reales, mientras sus competidoras estadounidenses siguen mayoritariamente en "
            "fase de desarrollo. TechCrunch calificó este momento como 'el madrugón del mercado robótico chino'."
        ),
        "fuente_label": "TechCrunch — Why China's humanoid robot industry is winning the early market",
        "fuente_url": "https://techcrunch.com/2026/02/28/why-chinas-humanoid-robot-industry-is-winning-the-early-market/",
    },
    {
        "emoji": "🧮",
        "titulo": "Una IA china resuelve un problema matemático que llevaba más de una década sin solución",
        "cuerpo": (
            "Un sistema de inteligencia artificial desarrollado en China logró resolver un problema "
            "matemático que la comunidad científica llevaba más de 10 años sin poder descifrar. El avance, "
            "publicado el 13 de abril, refuerza la apuesta de Pekín por la IA como herramienta de "
            "investigación científica de frontera. En paralelo, en el primer trimestre de 2026 las patentes "
            "relacionadas con IA crecieron un 31,2% interanual, y China ya cuenta con 602 millones de "
            "usuarios de IA generativa —más de la mitad de los usuarios globales—. La industria central "
            "de IA del país superó el billón de yuanes en valor en 2025."
        ),
        "fuente_label": "BioBioChile — IA china resuelve problema matemático",
        "fuente_url": "https://www.biobiochile.cl/noticias/ciencia-y-tecnologia/pc-e-internet/2026/04/13/ia-china-resuelve-problema-matematico-que-llevaba-mas-de-una-decada-sin-solucion.shtml",
    },
    {
        "emoji": "🚀",
        "titulo": "Chang'e-7 llega a la base de lanzamiento: China se prepara para explorar el polo sur lunar",
        "cuerpo": (
            "El 10 de abril todos los módulos de la misión Chang'e-7 llegaron sanos y salvos a la Base "
            "Espacial de Wenchang para iniciar las pruebas previas al lanzamiento, previsto para agosto "
            "de 2026. La misión incluye un orbitador, un módulo de aterrizaje, un rover y una sonda "
            "mini-saltadora diseñada para explorar cráteres en sombra permanente del polo sur lunar, "
            "donde se sospecha la existencia de agua en forma de hielo. Además, la Agencia Espacial "
            "Nacional China (CNSA) confirmó misiones intensivas en 2026: el acercamiento de Tianwen-2 "
            "a su asteroide objetivo, las misiones tripuladas Shenzhou-23 y ensayos del cohete reutilizable "
            "Larga Marcha 10, pieza clave del programa lunar tripulado antes de 2030."
        ),
        "fuente_label": "Global Times — China unveils major 2026 space missions",
        "fuente_url": "https://www.globaltimes.cn/page/202604/1359177.shtml",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China crece un 5% en Q1 2026, superando expectativas",
        "cuerpo": (
            "La economía china arrancó 2026 con fuerza: el PIB creció un 5% interanual en el primer "
            "trimestre, por encima de las previsiones de los analistas y el ritmo más rápido en tres "
            "trimestres. El motor principal fue la manufactura de alta tecnología, que creció un 12,5%, "
            "con robots industriales y circuitos integrados disparándose un 33% y un 24% respectivamente. "
            "El comercio exterior aumento un 15% en el mismo período, con exportaciones de bienes "
            "creciendo un 18,3% en enero-febrero —el primer crecimiento de doble dígito desde marzo "
            "de 2023—, reflejando la resistencia de la segunda economía del mundo pese a las "
            "turbulencias geopolíticas."
        ),
        "fuente_label": "CGTN Español — Comercio exterior de China aumenta 15% en Q1 2026",
        "fuente_url": "https://espanol.cgtn.com/news/2026-04-15/2044294393639481345/index.html",
    },
    {
        "emoji": "💾",
        "titulo": "Semiconductores chinos baten récord histórico de ingresos impulsados por la IA",
        "cuerpo": (
            "Las empresas chinas de chips reportaron ingresos récord en el primer trimestre de 2026, "
            "impulsadas por el boom de la IA y la aceleración de la autosuficiencia tecnológica. SMIC, "
            "el mayor fabricante chino, registró 9.300 millones de dólares en ingresos en 2025 (+16%) "
            "y proyecta superar los 11.000 millones en 2026. CXMT (memoria) disparó sus ingresos un "
            "130% interanual hasta 55.000 millones de yuanes. Según Digitimes, China alcanzará el 42% "
            "de la capacidad global de producción de chips en nodos maduros (22-40nm) para 2028, frente "
            "al 37% actual, liderando un segmento clave para la industria global."
        ),
        "fuente_label": "CNBC — Chinese chip firms hit record revenue driven by AI boom",
        "fuente_url": "https://www.cnbc.com/2026/04/03/chinese-chip-firms-record-revenue-ai-boom-us-curbs.html",
    },
    {
        "emoji": "⚡",
        "titulo": "China planea doblar su energía limpia para 2035 con una inversión billonaria",
        "cuerpo": (
            "El 17 de abril, la Comisión Nacional de Desarrollo y Reforma anunció un plan para duplicar "
            "el suministro de energía no fósil de China para 2035 respecto a los niveles de 2025. El "
            "ambicioso programa incluye nuevos parques eólicos marinos, grandes plantas solares en el "
            "desierto y un macroproyecto hidroeléctrico en el Tíbet. Las dos grandes empresas estatales "
            "de la red eléctrica invertirán 1 billón de yuanes anuales (aproximadamente 146.000 millones "
            "de dólares) durante todo el 15.º Plan Quinquenal (2026-2030). State Grid ya aumentó un 50% "
            "su gasto en conexión de nuevas energías a la red solo en el primer trimestre."
        ),
        "fuente_label": "Bloomberg — China Lifts Green Push With Plan to Double Clean Energy by 2035",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-04-17/china-lifts-green-push-with-plan-to-double-clean-energy-by-2035",
    },
    {
        "emoji": "📡",
        "titulo": "5G-A cubre ya 330 ciudades chinas: 4.958 millones de estaciones base operativas",
        "cuerpo": (
            "A cierre de marzo de 2026, China contaba con 4.958 millones de estaciones base 5G, con la "
            "tecnología 5G-Advanced (5G-A, la evolución del 5G estándar) cubriendo 330 ciudades. Los "
            "usuarios de Internet de las Cosas (IoT) alcanzaron los 2.948 millones —casi tres veces la "
            "población china—. El sector de fabricación de equipos electrónicos y comunicaciones creció "
            "un 13,6% interanual en el primer trimestre. China ya planifica el despliegue de 500.000 "
            "nuevas estaciones 5G-A antes de 2030, mientras avanza en la investigación del 6G, previsto "
            "como nuevo motor de crecimiento económico global a partir de esa fecha."
        ),
        "fuente_label": "Xinhua — China boosts digital technology in push for modernization",
        "fuente_url": "http://www.shanghainews.net/news/279002526/china-boosts-digital-technology-in-push-for-modernization",
    },
    {
        "emoji": "🏥",
        "titulo": "IA y medicina tradicional china: quioscos de diagnóstico inteligente en el metro",
        "cuerpo": (
            "China ha comenzado a desplegar quioscos de diagnóstico asistido por inteligencia artificial "
            "en estaciones de metro y puntos urbanos estratégicos, combinando tecnología biomédica de "
            "vanguardia con principios de la Medicina Tradicional China. Estos dispositivos miden presión "
            "arterial, frecuencia cardíaca, saturación de oxígeno y temperatura, mientras la IA aplica "
            "criterios de la tradición médica china: análisis facial, observación de la lengua e "
            "interpretación digital del pulso mediante sensores de presión multicapa. La Comisión Nacional "
            "de Salud ha promovido la integración de herramientas de IA en los servicios médicos como "
            "parte de la estrategia de salud digital nacional."
        ),
        "fuente_label": "Mundo Global — China: IA y Medicina Tradicional",
        "fuente_url": "https://mundoglobal.org/china-avanza-hacia-un-modelo-de-salud-digital-que-une-ia-y-medicina-tradicional-china/",
    },
    {
        "emoji": "🏭",
        "titulo": "Foro Zhongguancun 2026: robots camareros y el despegue de la economía inteligente",
        "cuerpo": (
            "En el Foro Zhongguancun 2026 celebrado en Pekín, los robots camareros se convirtieron en "
            "protagonistas al atender más de 100 pedidos durante el primer día del evento. La demostración "
            "reflejó la aceleración de la 'economía inteligente' china, un concepto central del nuevo "
            "plan quinquenal. La Xinhua informó que China está impulsando activamente la integración de "
            "la IA en los sectores productivos reales, con el objetivo de que el 70% de la economía "
            "incorpore IA en sus procesos para 2027, y el 90% para 2030. Las industrias de IA del país "
            "apuntan a superar los 10 billones de yuanes en valor para 2030."
        ),
        "fuente_label": "Xinhua — China impulsa la economia inteligente",
        "fuente_url": "https://spanish.xinhuanet.com/20260403/f57625afb3ea44fbb428d542671249c5/c.html",
    },
    {
        "emoji": "🗺️",
        "titulo": "El 15.º Plan Quinquenal (2026-2030): IA, 6G, robots y biotech como pilares del futuro",
        "cuerpo": (
            "El nuevo plan quinquenal chino sitúa las llamadas 'Nuevas Fuerzas Productivas de Calidad' "
            "en el centro de su estrategia de desarrollo. Los ejes son claros: IA Plus (aplicar la IA "
            "como infraestructura transversal a toda la economía), 6G, robótica, biotecnología y economía "
            "de baja altitud (drones). Las industrias emergentes —circuitos integrados, robots inteligentes "
            "y drones— suman ya casi 6 billones de yuanes y aspiran a 10 billones para 2030. El presupuesto "
            "en Ciencia y Tecnología creció un 7,1% hasta 1,3 billones de yuanes. China no solo quiere "
            "liderar estas tecnologías: quiere que sean el motor de su desarrollo económico de las "
            "próximas dos décadas."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
    },
]

NOTICIAS = [
    {
        "emoji": "🚀",
        "titulo": "China lanza el Long March 12B: el cohete reutilizable que compite con el Falcon 9",
        "cuerpo": (
            "El 1 de junio, China lanzó sin previo aviso público el debut del Long March 12B, un cohete de "
            "72 metros y diseño reutilizable comparable al Falcon 9 de SpaceX. Despegó desde el Dongfeng "
            "Commercial Space Innovation Test Zone en Mongolia Interior y colocó en órbita baja el 10.º lote "
            "de satélites de la constelación de internet de banda ancha Qianfan ('Mil Velas'). Ha sido el "
            "35.º intento orbital de China en los primeros cinco meses de 2026, un ritmo sin precedentes."
        ),
        "fuente_label": "SpaceNews — China conducts surprise launch of Long March 12B",
        "fuente_url": "https://spacenews.com/china-conducts-surprise-launch-of-long-march-12b-delivers-qianfan-satellites-on-debut-flight/",
    },
    {
        "emoji": "🤖",
        "titulo": "La industria de robots humanoides china alcanza 28.000 unidades y abre el mercado de consumo",
        "cuerpo": (
            "El sector de robots humanoides de China ha disparado sus envíos a unas 28.000 unidades en 2026, "
            "más del doble que en 2025. Las empresas AGIBOT y Unitree lideran el segmento con más de 5.000 "
            "unidades cada una. Unitree recibió esta semana la aprobación para salir a bolsa en Shanghai. "
            "UBTech abrió pre-pedidos del primer humanoide de tamaño real para el mercado de consumo en "
            "JD.com, con lanzamiento previsto para el 30 de junio. La inversión total del sector en el "
            "Q1 2026 superó los 68.100 millones de yuanes, más que todo 2025 junto."
        ),
        "fuente_label": "Fortune — Chinese humanoid robots global market",
        "fuente_url": "https://fortune.com/2026/06/06/chinese-humanoid-robots-global-market-sales-performative-functional/",
    },
    {
        "emoji": "📋",
        "titulo": "China pone en vigor 102 estándares nacionales para IA y robótica",
        "cuerpo": (
            "El 1 de junio entraron en vigor 102 nuevas normas nacionales que regulan la robótica, la IA "
            "encarnada (embodied AI), la automatización industrial y los agentes de IA. Los fabricantes ya "
            "no pueden limitarse a demostrar capacidades: deben certificarlas y someterse a auditorías "
            "verificables. El marco legal eleva la responsabilidad de la industria y convierte a China en "
            "el primer país en normalizar a esta escala el sector de los robots inteligentes."
        ),
        "fuente_label": "EVS International — China 102 standards robotics AI",
        "fuente_url": "https://www.evsint.com/china-102-standards-robotics-ai-prove-dont-demo/",
    },
    {
        "emoji": "💾",
        "titulo": "Huawei Ascend 910C apunta a 1,6 millones de unidades: tres empresas chinas en el top 20 mundial de chips",
        "cuerpo": (
            "Huawei se ha consolidado como el principal competidor nacional de NVIDIA en China, con su "
            "acelerador Ascend 910C apuntando a la producción de 1,6 millones de unidades en 2026. Por "
            "primera vez, tres fabricantes chinos de equipos de semiconductores —ACM Research, AMEC y "
            "Naura Technology Group— entran en el top 20 mundial por ventas. China fija también para 2026 "
            "un objetivo de autosuficiencia del 70% en obleas de silicio."
        ),
        "fuente_label": "TechWire Asia — China semiconductor self-sufficiency 2026",
        "fuente_url": "https://techwireasia.com/2026/05/china-semiconductor-self-sufficiency-wafer-target-2026/",
    },
    {
        "emoji": "🧠",
        "titulo": "La carrera de datos de IA física: China moviliza trabajadores para entrenar robots humanoides",
        "cuerpo": (
            "Empresas tecnológicas chinas han puesto en marcha un ecosistema de recopilación de datos masivo: "
            "equipos de trabajadores graban millones de horas de movimiento humano en hogares y fábricas "
            "reales para entrenar sistemas de IA física. Esta estrategia de datos localizada y de bajo coste "
            "es considerada una ventaja competitiva estructural frente a enfoques occidentales, y acelera el "
            "liderazgo de China en robótica humanoide e IA encarnada."
        ),
        "fuente_label": "Rest of World — China AI robotics training data",
        "fuente_url": "https://restofworld.org/2026/china-ai-robotics-training-data/",
    },
    {
        "emoji": "📈",
        "titulo": "PIB de China: +5% en el Q1 2026; startups recaudan 16.500 millones de dólares en el trimestre",
        "cuerpo": (
            "La economía china creció un 5,0% interanual en el primer trimestre, en la parte alta del rango "
            "objetivo del Gobierno (4,5-5%). La industria manufacturera de alta tecnología siguió liderando, "
            "y el comercio exterior registró su mayor crecimiento mensual en años. En paralelo, las startups "
            "chinas captaron 16.500 millones de dólares en el Q1 2026, con la IA —StepFun, Moonshot AI, "
            "Galaxy Bot— acaparando la mayor parte. Se espera que 2026 marque un hito en monetización de IA, "
            "infraestructura cloud y publicidad tecnológica."
        ),
        "fuente_label": "China Briefing — China's economy in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-economy-in-2026-january-february-rebound/",
    },
    {
        "emoji": "⚡",
        "titulo": "La energía limpia ya supera al carbón en capacidad; solar superará al carbón en 2026",
        "cuerpo": (
            "A cierre de marzo de 2026, la capacidad combinada de eólica y solar alcanzó 1.482 GW, "
            "superando oficialmente la capacidad del carbón por primera vez en la historia. La energía limpia "
            "representó el 11,4% del PIB chino en 2025 —15,4 billones de yuanes (2,1 billones de dólares)—. "
            "El Plan Quinquenal 2026-2030 contempla 100 GW de almacenamiento hidroeléctrico por bombeo, más "
            "de 100 GW de nueva eólica marina y ampliar la transmisión de energía limpia de oeste a este "
            "hasta 420 GW (frente a los 340 GW actuales)."
        ),
        "fuente_label": "Carbon Brief — China clean energy share of economy record",
        "fuente_url": "https://www.carbonbrief.org/china-briefing-5-february-2026-clean-energys-share-of-economy-record-renewables-thawing-relations-with-uk/",
    },
    {
        "emoji": "🔌",
        "titulo": "Plan de 5 billones de yuanes para modernizar la red eléctrica nacional (2026-2030)",
        "cuerpo": (
            "China invertirá más de 5 billones de yuanes en modernizar su red eléctrica durante el "
            "15.º Plan Quinquenal, incluyendo nuevos corredores de transmisión, proyectos de ayuda mutua "
            "interprovincial y fortalecimiento de la red rural. La capacidad de almacenamiento de energía "
            "ya superó los 213 GW en 2025. La inversión total en infraestructura —red eléctrica, "
            "computación, educación y salud— superará los 7 billones de yuanes solo en 2026."
        ),
        "fuente_label": "China Briefing — China's clean energy transition 15th Five-Year Plan",
        "fuente_url": "https://www.china-briefing.com/news/chinas-clean-energy-transition-15th-five-year-plan/",
    },
    {
        "emoji": "🏗️",
        "titulo": "China renovará 770.000 km de tuberías urbanas subterráneas antes de 2030",
        "cuerpo": (
            "El 8 de junio, Xinhua anunció que China construirá y renovará aproximadamente 770.000 km de "
            "tuberías subterráneas urbanas durante el 15.º Plan Quinquenal (2026-2030). La iniciativa apunta "
            "al control de inundaciones mediante la mejora de redes de drenaje y alcantarillado, la "
            "sustitución de redes antiguas de agua y gas, y la modernización de sistemas urbanos de "
            "calefacción."
        ),
        "fuente_label": "Xinhua — China urban underground pipeline upgrades",
        "fuente_url": "https://english.news.cn/20260608/115c1021f68e4686b0ca06a0987d2193/c.html",
    },
    {
        "emoji": "🌏",
        "titulo": "China acogerá el APEC 2026 en Shenzhen: drones, robots y gobernanza de la IA",
        "cuerpo": (
            "Shenzhen se prepara para ser el epicentro global de tecnología cuando acoja el APEC 2026 "
            "(18-19 de noviembre). La ciudad ya está probando en fase final el transporte autónomo, los "
            "drones de pasajeros (economía de baja altitud) y robots humanoides en servicios públicos. "
            "La agenda del foro incluye gobernanza de la IA para el bien común, resiliencia de cadenas de "
            "suministro e infraestructura digital, posicionando a China como líder en gobernanza tecnológica "
            "global."
        ),
        "fuente_label": "Diario Financiero — China en los preparativos del APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
]


def build_blocks():
    today = date.today().strftime("%-d de %B de %Y")
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
    title = f"China Al Dia — Semana 2-9 Junio 2026"
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
