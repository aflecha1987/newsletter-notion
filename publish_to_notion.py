#!/usr/bin/env python3
"""
Publica la newsletter semanal de China Al Día en Notion.
Uso: python publish_to_notion.py
"""

import json
import os
import urllib.request
import urllib.error
import sys
from datetime import date

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
PARENT_PAGE_ID = os.environ.get("PARENT_PAGE_ID", "34ae9ac6c5268056bd3cfeddc772dddc")
API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


def notion_request(method, endpoint, data=None):
    url = f"{API_BASE}{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error HTTP {e.code}: {e.read().decode('utf-8')}")
        sys.exit(1)


def heading1(text):
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def heading2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def heading3(text):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def paragraph(text, bold=False):
    annotations = {"bold": bold}
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text},
                                         "annotations": annotations}]}}


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def callout(text, emoji="📌"):
    return {"object": "block", "type": "callout",
            "callout": {"icon": {"type": "emoji", "emoji": emoji},
                        "rich_text": [{"type": "text", "text": {"content": text}}]}}


def bullet(text, url=None):
    rich = [{"type": "text", "text": {"content": text, "link": {"url": url} if url else None}}]
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich}}


def build_newsletter_blocks():
    today = date.today().strftime("%d de abril de 2026")
    blocks = [
        callout("Newsletter generada automáticamente por China Al Día · " + today, "🇨🇳"),
        divider(),

        # PORTADA
        heading1("PORTADA DE LA SEMANA"),
        heading2("🏃 Un robot humanoide bate el récord mundial de la media maratón en Pekín"),
        paragraph(
            "El 19 de abril, Lightning, un robot humanoide de Honor (spin-off de Huawei), "
            "completó los 21 km de la media maratón de E-Town en 50 minutos y 26 segundos, "
            "superando el récord mundial humano por más de 6 minutos. Honor copó los tres "
            "primeros puestos, todos completados de forma autónoma. Más de 100 equipos "
            "participaron, casi cinco veces más que en la edición inaugural de 2025."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("Xinhua", "https://english.news.cn/20260419/74fc74a78dc64d959fbd4c1f244f6561/c.html"),
        bullet("NPR", "https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon"),
        bullet("Al Jazeera", "https://www.aljazeera.com/sports/2026/4/19/humanoid-robot-breaks-half-marathon-world-record-in-beijing"),
        bullet("CNBC", "https://www.cnbc.com/2026/04/21/china-humanoid-robots-us-investors.html"),
        divider(),

        # TECNOLOGÍA
        heading1("TECNOLOGÍA E INTELIGENCIA ARTIFICIAL"),

        heading2("🤖 China duplicará su producción de robots IA en 2026"),
        paragraph(
            "Decenas de fabricantes chinos anunciaron planes para aumentar la producción de "
            "robots IA un 94% este año. Robots para entornos de alto riesgo, cuidado de "
            "ancianos y humanoides para fábricas ya compiten en presencia de mercado real "
            "con sus equivalentes estadounidenses, que siguen en fase de desarrollo."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("El Chapuzas Informático", "https://elchapuzasinformatico.com/2026/04/china-produccion-robots-ia-2026/"),
        bullet("TechCrunch", "https://techcrunch.com/2026/02/28/why-chinas-humanoid-robot-industry-is-winning-the-early-market/"),

        heading2("🧮 Una IA china resuelve un problema matemático sin solución en una década"),
        paragraph(
            "Un sistema de IA desarrollado en China resolvió un problema matemático sin "
            "respuesta durante más de 10 años. En Q1 2026, las patentes de IA crecieron un "
            "31,2% interanual. China ya cuenta con 602 millones de usuarios de IA generativa."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("BioBioChile", "https://www.biobiochile.cl/noticias/ciencia-y-tecnologia/pc-e-internet/2026/04/13/ia-china-resuelve-problema-matematico-que-llevaba-mas-de-una-decada-sin-solucion.shtml"),
        bullet("La Jornada", "https://www.jornada.com.mx/noticia/2026/04/19/economia/inteligencia-artificial-en-el-centro-de-la-politica-china-de-desarrollo"),

        heading2("📡 Infraestructura digital sin precedentes: 5G-A en 330 ciudades"),
        paragraph(
            "A cierre de marzo, China cuenta con 4.958 millones de estaciones base 5G, con "
            "5G-Advanced cubriendo 330 ciudades. Usuarios de IoT: 2.948 millones. El sector "
            "electrónico y de comunicaciones creció un 13,6% interanual en Q1 2026."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("Xinhua / Shanghai News", "http://www.shanghainews.net/news/279002526/china-boosts-digital-technology-in-push-for-modernization"),
        divider(),

        # ECONOMÍA
        heading1("ECONOMÍA"),

        heading2("📈 PIB de China crece un 5% en Q1 2026, superando expectativas"),
        paragraph(
            "La economía china creció un 5% interanual en el primer trimestre, por encima "
            "de las previsiones. El comercio exterior aumentó un 15% en el mismo período, "
            "con exportaciones de bienes creciendo un 18,3% en enero-febrero —primer "
            "crecimiento de doble dígito desde marzo de 2023—."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("CGTN Español", "https://espanol.cgtn.com/news/2026-04-15/2044294393639481345/index.html"),
        bullet("Interborders", "https://interborders.com/actualidad-mundial/el-comercio-exterior-de-china-crece-con-fuerza-en-los-primeros-meses-de-2026"),

        heading2("💾 Semiconductores chinos baten récords históricos de ingresos"),
        paragraph(
            "SMIC: $9.300 millones en 2025 (+16%), proyectando $11.000 millones en 2026. "
            "CXMT: +130% interanual hasta 55.000 millones de yuanes. China alcanzará el "
            "42% de la capacidad global de chips en nodos maduros para 2028."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("CNBC", "https://www.cnbc.com/2026/04/03/chinese-chip-firms-record-revenue-ai-boom-us-curbs.html"),
        bullet("Digitimes", "https://www.digitimes.com/news/a20260327PD205/semicon-china-semiconductors-capacity-equipment-china-2030.html"),
        divider(),

        # ENERGÍA
        heading1("ENERGÍA Y MEDIO AMBIENTE"),

        heading2("⚡ China planea doblar su energía limpia para 2035"),
        paragraph(
            "La Comisión Nacional de Desarrollo y Reforma anunció el 17 de abril un plan "
            "para duplicar el suministro de energía no fósil de China para 2035 respecto a "
            "2025. Incluye parques eólicos marinos, solares en el desierto y un gran "
            "proyecto hidroeléctrico en el Tíbet. Inversión: 1 billón de yuanes anuales "
            "(≈$146.000M) durante el 15.º Plan Quinquenal. State Grid aumentó un 50% "
            "su inversión en conexión de nuevas energías."
        ),
        paragraph("Fuentes:", bold=True),
        bullet("Bloomberg", "https://www.bloomberg.com/news/articles/2026-04-17/china-lifts-green-push-with-plan-to-double-clean-energy-by-2035"),
        bullet("Carbon Brief", "https://www.carbonbrief.org/china-briefing-16-april-2026-billions-for-grid-petrochemical-plan-chinas-high-seas-bid/"),
        bullet("CleanTechnica", "https://cleantechnica.com/2026/04/17/china-plans-to-double-renewable-energy-by-2035-thats-the-good-news/"),
        divider(),

        # PLAN QUINQUENAL
        heading1("PLAN ESTRATÉGICO 2026-2030"),

        heading2("🗺️ El 15.º Plan Quinquenal: IA, 6G, robots y biotech como ejes del futuro"),
        paragraph("Objetivos clave:", bold=True),
        bullet("IA Plus: 70% de la economía integrada con IA para 2027; 90% para 2030. Industrias de IA > 10 billones de yuanes para 2030."),
        bullet("6G: Investigación activa + 500.000 estaciones 5G-A desplegadas antes de 2030."),
        bullet("Industrias emergentes: circuitos integrados, economía de baja altitud (drones), robots inteligentes. De 6 a 10 billones de yuanes en 2030."),
        bullet("Ciencia y Tecnología: presupuesto de 1,3 billones de yuanes (+7,1%)."),
        paragraph("Fuentes:", bold=True),
        bullet("La Jornada", "https://www.jornada.com.mx/noticia/2026/04/20/economia/inteligencia-artificial-cimienta-revolucion-industrial-en-china"),
        bullet("Global Times", "https://www.globaltimes.cn/page/202601/1353864.shtml"),
        bullet("Gizmodo ES", "https://es.gizmodo.com/china-ya-puso-fecha-a-su-proximo-gran-salto-tecnologico-su-nuevo-plan-quinquenal-revela-como-quiere-dominar-la-ia-los-robots-la-energia-del-futuro-y-hasta-prepararse-para-un-mundo-mas-hostil-2000230003"),
        bullet("China Briefing", "https://www.china-briefing.com/news/chinas-industries-to-watch-in-2026/"),
        divider(),

        paragraph("China al Día · Newsletter semanal en español · Semana 14-22 abril 2026", bold=True),
    ]
    return blocks


def create_notion_page():
    today = date.today().isoformat()
    title = f"🇨🇳 China Al Día — Semana 14-22 Abril 2026"

    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🇨🇳"},
        "cover": {"type": "external", "external": {
            "url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
        }},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        "children": build_newsletter_blocks(),
    }

    print(f"Creando página en Notion: {title}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "").replace("-", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id}")
    print(f"\n✅ Página creada con éxito!")
    print(f"🔗 URL: {page_url}")
    return page_url


if __name__ == "__main__":
    create_notion_page()
