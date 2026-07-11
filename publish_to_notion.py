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
        "titulo": "Exportaciones de coches chinos se disparan un 80% en junio: camino al récord histórico",
        "cuerpo": (
            "Las exportaciones de vehículos de pasajeros de China subieron un 80% interanual en junio de 2026, "
            "impulsadas por la demanda global de vehículos eléctricos. En el primer semestre del año, el país exportó "
            "más de 4,4 millones de vehículos, un 72% más que el mismo período de 2025. China está en camino de superar "
            "los 10 millones de exportaciones totales de vehículos en 2026, un salto del 41% respecto al año anterior. "
            "Canadá acordó este mes reducir su arancel del 100% sobre coches eléctricos chinos con un cupo inicial de "
            "50.000 unidades. CATL y Sinopec están instalando 500 estaciones de intercambio de batería capaces de "
            "completar el proceso en dos minutos."
        ),
        "fuente_label": "Washington Post — China car exports up 80% in June",
        "fuente_url": "https://www.washingtonpost.com/business/2026/07/09/china-autos-exports-evs-cars/260d2fc6-7b81-11f1-b194-f872dd4ec5aa_story.html",
    },
    {
        "emoji": "📱",
        "titulo": "Alipay AI Pay supera los 100 millones de usuarios en una semana histórica",
        "cuerpo": (
            "Alipay AI Pay, el sistema de pago por inteligencia artificial de Ant Group, superó los 100 millones de "
            "usuarios y procesó más de 120 millones de transacciones en una sola semana. El servicio permite realizar "
            "pagos con comandos en lenguaje natural, sin necesidad de abrir aplicaciones ni buscar códigos QR. Este hito "
            "ilustra la velocidad con que China integra la IA en la vida cotidiana: el país ya cuenta con 602 millones "
            "de usuarios de IA generativa, más de la mitad del total mundial."
        ),
        "fuente_label": "CNBC The China Connection — AI, IPOs, Diplomacy",
        "fuente_url": "https://www.cnbc.com/2026/07/06/cnbcs-the-china-connection-newsletter-a-focus-on-ai-ipos-diplomacy.html",
    },
    {
        "emoji": "💾",
        "titulo": "DeepSeek desarrolla su propio chip de IA: autosuficiencia tecnológica total",
        "cuerpo": (
            "DeepSeek, el laboratorio de IA chino que sacudió al mundo con su modelo de bajo coste, está desarrollando "
            "su propio chip de inteligencia artificial. El movimiento supone un salto estratégico para la empresa y "
            "refleja la apuesta de China por controlar toda la cadena de valor tecnológica. En paralelo, una nueva "
            "startup china apuesta por el apilamiento 3D de chips para superar las restricciones de exportación de "
            "EE.UU. y producir aceleradores de IA de última generación de forma autónoma."
        ),
        "fuente_label": "The Wire China — Daily Roundup July 7, 2026",
        "fuente_url": "https://www.thewirechina.com/2026/07/07/the-daily-roundup-july-7-2026/",
    },
    {
        "emoji": "🤖",
        "titulo": "Conferencia Mundial de IA en Shanghái: Xi Jinping marca la agenda tecnológica global",
        "cuerpo": (
            "Shanghái acoge a mediados de julio la Conferencia Mundial de Inteligencia Artificial (WAIC), el evento "
            "tecnológico más importante de Asia. El presidente Xi Jinping pronunciará el discurso inaugural, subrayando "
            "la prioridad nacional de la IA. El evento reunirá a los gigantes tecnológicos chinos —Alibaba, Tencent, "
            "ByteDance y Huawei— que ya han integrado IA avanzada en sus servicios de uso masivo. Empresas de más de "
            "90 países acuden a Shanghái para conocer de primera mano los avances chinos en automatización, IA "
            "industrial y analítica de datos."
        ),
        "fuente_label": "TechBizHub — China Tech Advancement 2026",
        "fuente_url": "https://techbizhub.com/news/china-tech-advancement-2026-global-innovation",
    },
    {
        "emoji": "🧮",
        "titulo": "El ordenador cuántico 'Origin Wukong' supera el millón de tareas globales",
        "cuerpo": (
            "El ordenador cuántico superconductor chino 'Origin Wukong' completó en junio su tarea número un millón "
            "ejecutada por usuarios de todo el mundo. El sistema, disponible en la nube para investigadores e "
            "instituciones internacionales, se ha convertido en una plataforma de referencia global. En paralelo, "
            "investigadores chinos han demostrado la generación de claves de cifrado ultraseguras mediante fibra "
            "óptica a 11 km, validando la tecnología hasta 100 km — un paso decisivo hacia redes de comunicación "
            "cuántica a escala nacional. El Plan Quinquenal 2026-2030 establece la computación cuántica como "
            "industria estratégica prioritaria."
        ),
        "fuente_label": "The Quantum Insider — Chinese Researchers Clear Hurdles For Quantum Networks",
        "fuente_url": "https://thequantuminsider.com/2026/02/06/chinese-researchers-clear-hurdles-for-long-distance-quantum-networks/",
    },
    {
        "emoji": "📈",
        "titulo": "Banco Mundial: economía china resiliente, proyección del 4,4% de crecimiento en 2026",
        "cuerpo": (
            "El Banco Mundial publicó su actualización económica de China para julio de 2026 bajo el título "
            "'Rebalancing Growth'. La entidad confirma que la economía china se mantiene resiliente gracias a la "
            "inversión en alta tecnología y las exportaciones, y proyecta un crecimiento del 4,4% para 2026. El sector "
            "manufacturero de alta tecnología sigue siendo el motor: robots industriales y semiconductores registran "
            "crecimientos del 33% y el 24% respectivamente."
        ),
        "fuente_label": "World Bank — China Economic Update July 2026",
        "fuente_url": "https://www.worldbank.org/en/news/press-release/2026/07/07/rebalancing-growth-china-economic-update",
    },
    {
        "emoji": "🌍",
        "titulo": "Summer Davos en Dalian: 1.700 líderes mundiales reconocen el liderazgo innovador de China",
        "cuerpo": (
            "Más de 1.700 representantes de más de 90 países y regiones se reunieron en Dalian para el Foro de Verano "
            "del Foro Económico Mundial (Summer Davos). Los asistentes coincidieron en que China lidera globalmente en "
            "IA, robótica humanoide, tecnología verde, computación cuántica y biofarmacia avanzada. El evento "
            "consolidó la percepción internacional de China como nación innovadora de primer nivel, capaz de ofrecer "
            "soluciones tecnológicas y de desarrollo sostenible al resto del mundo."
        ),
        "fuente_label": "Xinhua — China's appeal grows at Summer Davos",
        "fuente_url": "https://english.news.cn/20260623/a4eb0a1e5ee64b439a176d4673a7be34/c.html",
    },
    {
        "emoji": "🛤️",
        "titulo": "Iniciativa Belt and Road: 66.200 millones invertidos y giro hacia la Ruta de la Seda Verde",
        "cuerpo": (
            "La Iniciativa Belt and Road (BRI) movilizó 66.200 millones de dólares en proyectos de construcción "
            "durante el primer semestre de 2025, cifra récord. En 2026, la iniciativa consolida su giro hacia la "
            "'Green Silk Road' (ferrocarriles, renovables) y la 'Digital Silk Road' (telecomunicaciones, centros de "
            "datos). Los proyectos del ferrocarril China-Tailandia, Hungría-Serbia y el TAV Yakarta-Bandung avanzan "
            "según el calendario. China celebrará la BRI Summit 2026 para consolidar acuerdos con los 150 países "
            "participantes."
        ),
        "fuente_label": "Observatorio Global UDLAP — BRI 2026",
        "fuente_url": "https://observatorioglobal.udlap.mx/the-belt-and-road-initiative-in-2026-from-expansion-to-strategic-high-quality-cooperation/",
    },
    {
        "emoji": "🤝",
        "titulo": "China impulsa cooperación verde e IA con Dinamarca; aranceles cero para África",
        "cuerpo": (
            "El ministro de Exteriores Wang Yi y el rey de Dinamarca Federico X confirmaron en Copenhague la voluntad "
            "de ambos países de estrechar lazos en economía verde, innovación tecnológica e inteligencia artificial. "
            "Simultáneamente, 2026 marca el 70.o aniversario de las relaciones diplomáticas entre China y los países "
            "africanos: Pekín ha extendido su política de aranceles cero a todos los países africanos menos "
            "desarrollados y ha lanzado la 'Iniciativa de Cooperación para la Modernización en África'."
        ),
        "fuente_label": "Observatorio de Política China — Resumen 3-9 julio 2026",
        "fuente_url": "https://www.politica-china.org/resumen-de-politica-exterior-miscelanea-66/",
    },
    {
        "emoji": "💊",
        "titulo": "La biofarmacia china atrae inversiones históricas: acuerdos de 33.700 millones de dólares",
        "cuerpo": (
            "La industria biomédica china alcanzó un valor de mercado de 5 billones de yuanes (700.000 millones de "
            "dólares), representando el 22% del mercado farmacéutico global, con un crecimiento anual del 8,7%. La "
            "aceleración es tal que empresas internacionales están apostando fuerte: AstraZeneca y CSPC firmaron un "
            "acuerdo de hasta 18.500 millones de dólares para terapias contra obesidad y diabetes tipo 2; y Bristol "
            "Myers Squibb y Hengrui Pharma cerraron una colaboración de hasta 15.200 millones para 13 programas en "
            "oncología, hematología e inmunología."
        ),
        "fuente_label": "Herbert Smith Freehills — China Biotech 2026",
        "fuente_url": "https://www.hsfkramer.com/notes/lifesciences/2026-posts/2026-sees-chinas-biotech-scene-continuing-its-ascent-but-could-us-developments-mean-clouds-on-the-horizon",
    },
    {
        "emoji": "⚡",
        "titulo": "China: 60% del solar mundial y 80% de las baterías de EV — líder indispensable de la transición energética",
        "cuerpo": (
            "El 15.o Plan Quinquenal (2026-2030) incluye compromisos climáticos sin precedentes: China invertirá "
            "1 billón de yuanes anuales en infraestructura de red eléctrica para integrar renovables. La capacidad "
            "de energía solar y eólica instalada superó el objetivo de 2030 con cuatro años de antelación. China ya "
            "produce más del 60% de los paneles solares del mundo y el 80% de las baterías para vehículos eléctricos, "
            "posicionándose como el proveedor indispensable de la transición energética global."
        ),
        "fuente_label": "China Briefing — China's Industries to Watch in 2026",
        "fuente_url": "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/",
    },
]

# ---- NOTICIAS ANTERIORES (semana 14-22 abril 2026) — archivo histórico ----
NOTICIAS_ABRIL_2026 = [
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
    title = "China Al Dia — Semana 4-11 Julio 2026"
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
