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
        "titulo": "China lanza la Shenzhou-23: primer astronauta que pasará un año en órbita",
        "cuerpo": (
            "El 24 de mayo, China lanzó con éxito la nave tripulada Shenzhou-23 desde el Centro de "
            "Lanzamiento de Satélites de Jiuquan, en el desierto de Gobi. La misión es comandada por "
            "Zhu Yangzhu e incluye a Lai Ka-ying, primera astronauta procedente de Hong Kong y doctora "
            "en informática forense. El hito más destacado: uno de los astronautas permanecerá 365 días "
            "en órbita, un récord para China que permitirá estudiar en profundidad los efectos de la "
            "microgravedad, información clave de cara a las misiones lunares tripuladas previstas para "
            "antes de 2030."
        ),
        "fuente_label": "Eureka / Daniel Marín — Despega la Shenzhou-23",
        "fuente_url": "https://danielmarin.naukas.com/2026/05/25/despega-la-shenzhou-23-con-el-primer-astronauta-chino-que-pasara-un-ano-en-el-espacio/",
    },
    {
        "emoji": "⚡",
        "titulo": "La ventaja secreta de China en la carrera IA: energía eléctrica barata y abundante",
        "cuerpo": (
            "Mientras Silicon Valley compite por megavatios, China ya resolvió el problema. El país "
            "genera más del doble de electricidad que Estados Unidos, con una red subvencionada que "
            "permite a sus centros de datos pagar menos de la mitad por kilovatio-hora que sus "
            "competidores americanos. Pekín incrementa estas subvenciones energéticas hasta en un 50% "
            "para los grandes centros de datos, mientras su capacidad de racks crece al 30% anual. "
            "Los modelos de IA chinos pueden entrenar y ejecutar inferencias a una fracción del coste "
            "occidental, convirtiendo la energía en el arma competitiva más poderosa de China en "
            "la guerra tecnológica del siglo XXI."
        ),
        "fuente_label": "Al Jazeera — China's secret weapon in AI race: cheap energy",
        "fuente_url": "https://www.aljazeera.com/economy/2026/5/28/chinas-secret-weapon-in-ai-race-with-us-lots-of-cheap-energy",
    },
    {
        "emoji": "💎",
        "titulo": "Diamantes de laboratorio chinos: el inesperado ganador del boom de la IA",
        "cuerpo": (
            "La inteligencia artificial abre un mercado totalmente nuevo para los diamantes sintéticos "
            "fabricados en China. Estos materiales están siendo adoptados como disipadores térmicos de "
            "última generación en chips de alta potencia para IA y centros de datos. Los diamantes "
            "conducen el calor hasta cinco veces mejor que el cobre, permitiendo diseños de "
            "semiconductores más densos y potentes. China, que ya domina la producción global de "
            "diamantes de laboratorio con más del 60% del mercado, está posicionada para convertir "
            "esta industria en un eslabón clave de su cadena de suministro tecnológico."
        ),
        "fuente_label": "Bloomberg — China's Lab-Grown Diamonds Emerge as Unlikely Winner in AI Boom",
        "fuente_url": "https://www.bloomberg.com/news/articles/2026-06-02/china-s-lab-grown-diamonds-emerge-as-unlikely-winner-in-ai-boom",
    },
    {
        "emoji": "🔐",
        "titulo": "Nueva ley: algoritmos e IA pasan a ser secretos comerciales en China",
        "cuerpo": (
            "El 1 de junio entró en vigor en China la nueva normativa de protección de secretos "
            "comerciales, que por primera vez incluye explícitamente algoritmos, conjuntos de datos de "
            "entrenamiento y códigos fuente de modelos de IA dentro de la categoría de secreto "
            "comercial. Cualquier base de datos usada para entrenar modelos de lenguaje o código fuente "
            "de IA queda protegido frente a transferencia no autorizada. La ley regula el trabajo a "
            "distancia y la colaboración transfronteriza con medidas de confidencialidad específicas. "
            "El objetivo: evitar que el talento local transfiera conocimientos estratégicos al exterior."
        ),
        "fuente_label": "China.org.cn — Nueva normativa sobre protección de secretos comerciales",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-06/01/content_118526701.htm",
    },
    {
        "emoji": "🤝",
        "titulo": "China y EE.UU. sellan un acuerdo histórico de reducción arancelaria",
        "cuerpo": (
            "Tras la cumbre bilateral celebrada en Pekín a mediados de mayo, China y Estados Unidos "
            "anunciaron un entendimiento comercial que incluye la reducción de aranceles sobre "
            "productos relevantes, la creación de un nuevo Consejo de Comercio e Inversiones como "
            "canal permanente de diálogo y acuerdos sobre compra de aeronaves e intercambio de "
            "componentes. El acuerdo llega después de más de dos años de escalada arancelaria y "
            "supone el primer descongelamiento estructural de las relaciones comerciales, abriendo "
            "la puerta a ampliar el comercio bilateral en sectores como la agricultura, energía "
            "y tecnología civil."
        ),
        "fuente_label": "El Informador MX — China y EU sorprenden con acuerdo sobre aranceles",
        "fuente_url": "https://www.informador.mx/economia/china-y-eu-sorprenden-con-acuerdo-sobre-aranceles-buscan-impulsar-comercio-bilateral-20260516-0072.html",
    },
    {
        "emoji": "💾",
        "titulo": "Mercado global de semiconductores camino al billón y medio de dólares en 2026",
        "cuerpo": (
            "Las estadísticas mundiales de semiconductores (WSTS) proyectan que el mercado global "
            "alcanzará los 1,51 billones de dólares en 2026, un incremento del 89,9% respecto al año "
            "anterior, la mayor revisión al alza de toda la historia del sector. En China, Huawei "
            "proyecta que sus ingresos por chips de IA crecerán un 60% interanual hasta los "
            "12.000 millones de dólares, mientras el país avanza en su objetivo de que el 70% de los "
            "wafers de silicio que consumen sus fabricantes sea de producción nacional antes de "
            "finales de 2026."
        ),
        "fuente_label": "BigGo Finance / WSTS — 2026 Semiconductor Market to Surge 90% to $1.5 Trillion",
        "fuente_url": "https://finance.biggo.com/news/-JapiZ4BYH_ypPqOMIcM",
    },
    {
        "emoji": "🌏",
        "titulo": "China anfitriona de la APEC 2026: Shenzhen como laboratorio del futuro",
        "cuerpo": (
            "Shenzhen acogerá la Cumbre de Líderes de la APEC el 18-19 de noviembre de 2026. China, "
            "como anfitriona, ha fijado el tema 'Construir una Comunidad Asia-Pacífico para Prosperar "
            "Juntos' con tres pilares: apertura comercial (reactivar el FTAAP), cooperación en "
            "infraestructura digital —con el puerto peruano de Chancay como caso emblematico— e "
            "innovación con IA, economía digital y transición verde. Shenzhen ya despliega soluciones "
            "de vanguardia: transporte autónomo, drones de pasajeros en fase final de prueba y robots "
            "humanoides integrados en servicios públicos."
        ),
        "fuente_label": "Diario Financiero CL — China despliega potencial tecnológico para APEC 2026",
        "fuente_url": "https://www.df.cl/economia-y-politica/macro/china-despliega-su-potencial-tecnologico-y-comercial-en-los-preparativos-de",
    },
    {
        "emoji": "🤖",
        "titulo": "CISCE 4: la cadena de suministro robótico chino se muestra al mundo",
        "cuerpo": (
            "La IV Exposición Internacional de Cadena de Suministro de China (CISCE), celebrada en "
            "Pekín en junio, estrena por primera vez una zona dedicada exclusivamente a Inteligencia "
            "Artificial. El evento da visibilidad a Zhejiang, uno de los principales polos robóticos "
            "del país. Con envíos globales de humanoides estimados en 35.000 unidades en 2026 (+94% "
            "interanual), China está pasando de la demostración tecnológica a la comercialización a "
            "gran escala, con contratos reales en fábricas, centros comerciales y entornos "
            "industriales peligrosos."
        ),
        "fuente_label": "PRNewswire — Behind CISCE: How China's supply chain is building tomorrow's robots",
        "fuente_url": "https://www.prnewswire.com/news-releases/behind-cisce-with-jason-how-chinas-supply-chain-is-building-tomorrows-robots-302789738.html",
    },
    # --- NOTICIAS SEMANA ANTERIOR (archivo histórico) ---
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
    title = "China Al Dia — Semana 27 Mayo - 3 Junio 2026"
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
