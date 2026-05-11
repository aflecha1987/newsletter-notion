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
        "titulo": "China convierte los robots con IA en el núcleo de su estrategia nacional",
        "cuerpo": (
            "La Federación Internacional de Robótica (IFR) publicó el 5 de mayo un informe confirmando "
            "que China ha situado los robots impulsados por IA en el corazón de su 15.º Plan Quinquenal "
            "(2026-2030). El plan menciona la IA más de 50 veces e incluye un ambicioso 'Plan de Acción "
            "IA+' para integrar la tecnología en toda la economía. China ya tiene un stock operativo de "
            "2 millones de robots industriales, 4,5 veces más que Japón (segundo del mundo), y recibe "
            "el 54% de los robots industriales instalados en todo el planeta. El peso de los proveedores "
            "locales en instalaciones nacionales pasó del 30% en 2020 al 57% en 2024."
        ),
        "fuente_label": "IFR — China Makes AI-powered Robots Core of National Strategy",
        "fuente_url": "https://ifr.org/ifr-press-releases/news/china-makes-ai-powered-robots-core-of-national-strategy",
    },
    {
        "emoji": "🎉",
        "titulo": "Primero de Mayo: récord histórico de turismo y consumo en China",
        "cuerpo": (
            "Las vacaciones del 1 de mayo en China (1-5 de mayo) batieron todos los registros. Los ingresos "
            "por consumo crecieron un 14,3% interanual. Se registraron 325 millones de viajes domésticos "
            "(+3,6%) y el gasto turístico alcanzó los 185.490 millones de yuanes (~27.080 millones de "
            "dólares). Pekín recibió más de 18 millones de visitantes. Los sectores más dinámicos: "
            "servicios culturales (+42,3%), deportivos (+44,1%) y restaurantes de bares y salones de té "
            "(+51,5%). Con más de 1.520 millones de viajes interregionales, China demostró la fortaleza "
            "de su mercado interno."
        ),
        "fuente_label": "Spanish.china.org.cn — Ingresos por consumo durante vacaciones de mayo aumentan 14,3%",
        "fuente_url": "http://spanish.china.org.cn/txt/2026-05/07/content_118480485.htm",
    },
    {
        "emoji": "🚗",
        "titulo": "La guerra de precios de VE chinos evoluciona a carrera armamentista de IA",
        "cuerpo": (
            "La competencia en el sector del automóvil eléctrico chino ha entrado en una nueva fase: "
            "ya no es solo una guerra de precios, sino una carrera de integración de IA. Más de 50 marcas "
            "de coches utilizan el modelo Doubao de ByteDance, presente en 145 modelos y más de 7 millones "
            "de vehículos. Alibaba anunció que su modelo Qwen se integrará en BYD y la joint venture de "
            "Volkswagen, permitiendo reservar hoteles, pedir comida o comprar entradas por voz. El sector "
            "libra batallas por chips de automoción y sistemas de asistencia a la conducción más avanzados, "
            "convirtiendo cada lanzamiento en un escaparate de IA aplicada al mundo real."
        ),
        "fuente_label": "CNBC — China's EV price war turns into AI arms race beyond cheaper cars",
        "fuente_url": "https://www.cnbc.com/2026/05/01/china-ev-ai-features-price-war-bytedance-alibaba-doubao-volcano-engine.html",
    },
    {
        "emoji": "🏆",
        "titulo": "TIME sitúa tres empresas chinas entre las 10 IA más influyentes del mundo en 2026",
        "cuerpo": (
            "La revista TIME publicó su lista de las 10 empresas de IA más influyentes de 2026, en la "
            "que tres compañías chinas consiguieron entrar. Los reconocimientos incluyen aplicaciones de "
            "IA orientadas al consumidor y grandes modelos de lenguaje de código abierto desarrollados "
            "de manera independiente. El avance refuerza el peso creciente de China en la vanguardia de "
            "la inteligencia artificial global, tanto en modelos de fundación como en aplicaciones de "
            "consumo masivo, donde el país acumula ya más de 600 millones de usuarios de IA generativa."
        ),
        "fuente_label": "AN Bariloche — El hilo de la IA china no se corta por lo más delgado",
        "fuente_url": "https://www.anbariloche.com.ar/noticias/2026/05/10/105597-el-hilo-de-la-ia-china-no-se-corta-por-lo-mas-delgado",
    },
    {
        "emoji": "⚖️",
        "titulo": "Tribunal chino falla contra empresa que despidió a un trabajador por IA",
        "cuerpo": (
            "En un hito legal de gran resonancia, el Tribunal Popular Intermedio de Hangzhou —el 'Silicon "
            "Valley chino'— falló en contra de una empresa que había sustituido a un empleado por "
            "inteligencia artificial. El tribunal consideró que, aunque las empresas pueden ganar "
            "eficiencia con la IA, no pueden descargar el coste de esa transición sobre los trabajadores. "
            "La sentencia marca un precedente importante: China quiere liderar el desarrollo tecnológico "
            "pero también proteger los derechos laborales en la era de la automatización, enviando una "
            "señal clara al ecosistema empresarial sobre los límites legales del reemplazo por IA."
        ),
        "fuente_label": "Xinhua — Ministerio de Relaciones Exteriores, conferencia de prensa 8 mayo 2026",
        "fuente_url": "https://www.fmprc.gov.cn/esp/xwfw/lxjzzdh/202605/t20260510_11907959.html",
    },
    {
        "emoji": "🔋",
        "titulo": "CATL presenta batería de 1.500 km y BYD alcanza exportaciones récord",
        "cuerpo": (
            "En Auto China 2026, CATL presentó la Batería Qilin Condensada de estado semisólido: densidad "
            "energética capaz de proporcionar hasta 1.500 kilómetros de autonomía en una sola carga, y la "
            "Shenxing de tercera generación que recupera cientos de kilómetros en solo seis minutos de carga. "
            "En paralelo, BYD alcanzó un nuevo récord de exportaciones en abril 2026, con el objetivo de "
            "vender 1,5 millones de unidades en el exterior este año, medio millón más que en 2025. Los "
            "coches eléctricos e híbridos chinos ya han reducido la demanda nacional de petróleo en más de "
            "1 millón de barriles por día."
        ),
        "fuente_label": "CNN Business — What oil crisis? China's EVs are ready to dominate the 21st century",
        "fuente_url": "https://www.cnn.com/2026/05/02/business/beijing-auto-show-china-evs-intl-hnk",
    },
    {
        "emoji": "🏛️",
        "titulo": "28.ª Expo Internacional de Alta Tecnología de Beijing: robots, drones y coches voladores",
        "cuerpo": (
            "Del 8 al 10 de mayo se celebró en el Centro Nacional de Convenciones de Pekín la 28.ª edición "
            "de la CHITEC, con más de 800 expositores nacionales e internacionales y 50.000 m² de exposición. "
            "Entre los protagonistas: el RoboBus autónomo de nivel L4, sistemas de vuelo simulado de drones, "
            "robots marinos, robots jugadores de fútbol, vehículos de nueva energía, vehículos voladores y "
            "manos biónicas. La exposición reflejó la velocidad con la que China integra la IA en objetos "
            "físicos del mundo cotidiano, desde el transporte urbano hasta la atención sanitaria."
        ),
        "fuente_label": "Manila Times — The 28th China Beijing International High-Tech Expo Opens",
        "fuente_url": "https://www.manilatimes.net/2026/05/09/tmt-newswire/pr-newswire/the-28th-china-beijing-international-high-tech-expo-opens/2339731/amp",
    },
    {
        "emoji": "🌐",
        "titulo": "BEYOND Expo 2026 en Macao: la IA da el salto del mundo digital al mundo físico",
        "cuerpo": (
            "La mayor feria tecnológica de Asia, BEYOND Expo 2026, celebrada en El Venetian Macao del 27 "
            "al 30 de mayo, adoptó el tema oficial 'IA: De lo Digital a lo Físico', marcando el paso de "
            "los modelos de lenguaje al mundo tangible. Más de 30.000 asistentes esperados, con programas "
            "dedicados a IA humanoides, conducción autónoma, wearables inteligentes y robótica incorporada. "
            "El primer ponente confirmado es Deepu Talla, vicepresidente de Robótica e IA de NVIDIA. "
            "NVIDIA también presentará su ecosistema de startups con 40 empresas del programa NVIDIA Inception."
        ),
        "fuente_label": "Yanko Design — BEYOND Expo 2026: Asia's Biggest Tech Event",
        "fuente_url": "https://www.yankodesign.com/2026/05/10/beyond-expo-2026-asias-biggest-tech-event-just-told-the-world-that-ai-software-was-only-the-warm-up/",
    },
    {
        "emoji": "🚀",
        "titulo": "2026: el año del despegue de la industria espacial comercial china",
        "cuerpo": (
            "El sector espacial comercial chino vive su año de 'verificación tecnológica'. El foco está "
            "en el dominio de los cohetes reutilizables de bajo coste, con varias empresas construyendo "
            "líneas de producción en masa de satélites. En el 15.º Plan Quinquenal, China se fijó como "
            "objetivo convertirse en gran potencia espacial, con planes de construir una estación lunar "
            "de investigación antes de 2030 y desarrollar un cohete pesado reutilizable. El presupuesto "
            "en ciencia y tecnología espacial creció un 7,1% y varios municipios anunciaron planes para "
            "impulsar la industria espacial comercial local con foco en la reducción de costes."
        ),
        "fuente_label": "36kr English — 2026: The Eve of China's Commercial Space Takeoff",
        "fuente_url": "https://eu.36kr.com/en/p/3699678980272899",
    },
    # ---- Semana anterior (14-22 Abril 2026) ----
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
    today = date.today().strftime("%-d de mayo de %Y")
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
    title = "China Al Dia — Semana 4-11 Mayo 2026"
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
