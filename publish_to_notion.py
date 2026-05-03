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
        "emoji": "🧠",
        "titulo": "DeepSeek V4: el modelo de IA más barato del mundo, entrenado con chips chinos",
        "cuerpo": (
            "El 24 de abril, DeepSeek presentó V4-Pro y V4-Flash, su nuevo modelo insignia, un año después "
            "de haber sacudido la industria global con DeepSeek-R1. Las claves: arquitectura Hybrid Attention "
            "que procesa hasta 1 millón de tokens en un único prompt; precio un 97% inferior al de GPT-5.5 de "
            "OpenAI; y código open source. Lo más significativo: V4 es el primer modelo de DeepSeek optimizado "
            "íntegramente para chips Huawei Ascend 950, un hito en la ruta de independencia tecnológica de "
            "China. El país ya procesa 140 billones de tokens al día, frente a los 100.000 millones de "
            "principios de 2024."
        ),
        "fuente_label": "CNBC — DeepSeek releases V4 model preview",
        "fuente_url": "https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html",
    },
    {
        "emoji": "🤖",
        "titulo": "AgiBot: 4 robots humanoides completan turno de 8 horas en fábrica real",
        "cuerpo": (
            "El 14 de abril, AgiBot retransmitió en directo cómo cuatro robots humanoides G2 completaron "
            "un turno de 8 horas ininterrumpidas en la línea de producción de electrónica de Longcheer, en "
            "Nanchang (Jiangxi), a una velocidad comparable a la humana. Acumulan ya 140 horas de operación "
            "continua tras solo cuatro meses de despliegue. La compañía planea escalar a 100 unidades en "
            "fábricas en el tercer trimestre de 2026, y expandirse a automoción, semiconductores y energía. "
            "En marzo ya había salido de línea el robot número 10.000, marcando un hito en la "
            "industrialización de la IA encarnada."
        ),
        "fuente_label": "Xinhua — Humanoid robots complete live factory shift",
        "fuente_url": "https://english.news.cn/20260418/3755db523eff40ae92bf3785c62f3e26/c.html",
    },
    {
        "emoji": "🚗",
        "titulo": "Auto China 2026: el mayor salón del automóvil del mundo celebra en Pekín la era del vehículo inteligente",
        "cuerpo": (
            "El Salón Internacional del Automóvil de Pekín 2026 (24 abril - 3 mayo) batió todos los récords: "
            "380.000 m² de exposición, 1.451 vehículos, 181 estrenos mundiales y más de 278 NEV (el 80%+ de "
            "los nuevos modelos). Más de 2.000 empresas de 21 países participaron, mientras los grandes "
            "salones europeos y norteamericanos siguen en declive. Protagonismo compartido para los robots "
            "humanoides: XPeng presentó a Iron, capaz de imitar movimientos humanos con precisión; Chery "
            "desplegó perros robot y humanoides que interactuaron con el público. China ya no compite solo "
            "en coches: compite en máquinas inteligentes."
        ),
        "fuente_label": "Electrek — Beijing Auto Show 2026: a glimpse at the future",
        "fuente_url": "https://electrek.co/2026/04/26/beijing-auto-show-2026-insane-glimpse-future-auto-industry/",
    },
    {
        "emoji": "🌍",
        "titulo": "China aplica arancel cero a 53 países africanos: la mayor apertura comercial unilateral de la historia",
        "cuerpo": (
            "Desde el 1 de mayo de 2026, China aplica arancel cero a las exportaciones de los 53 países "
            "africanos con los que mantiene relaciones diplomáticas. Productos que antes tributaban entre el "
            "8% y el 30% acceden ahora sin coste al mayor mercado de consumo del mundo. China se convierte en "
            "la primera gran economía en conceder un trato arancelario cero, unilateral y de cobertura total "
            "a todos sus socios africanos. La medida, vigente hasta abril de 2028, supone un impulso "
            "histórico para el comercio Sur-Sur. El comercio total China-Africa supera ya los "
            "348.000 millones de dólares anuales."
        ),
        "fuente_label": "Xinhua Español — Arancel cero a países africanos",
        "fuente_url": "http://spanish.xinhuanet.com/20260429/9adcc0263e144ef994a1257bff362d71/c.html",
    },
    {
        "emoji": "🚕",
        "titulo": "Pony.ai inaugura el primer robotaxi comercial de Europa en Zagreb, Croacia",
        "cuerpo": (
            "El 8 de abril, la empresa china de conducción autónoma Pony.ai lanzó en Zagreb (Croacia) el "
            "primer servicio comercial de robotaxi de Europa, en alianza con Uber y Verne (Grupo Rimac). "
            "El servicio opera de 7:00 a 21:00 h en un área de 90 km² que incluye el aeropuerto de Zagreb. "
            "El lanzamiento llega tras alcanzar el punto de equilibrio económico en dos ciudades tier-1 de "
            "China. Pony.ai apunta a 3.000 vehículos en operación antes de finales de 2026, ejecutando su "
            "estrategia de crecimiento de doble motor: expansión simultánea en China y mercados internacionales."
        ),
        "fuente_label": "Pony.ai — Europe's first commercial robotaxi in Zagreb",
        "fuente_url": "https://blog.pony.ai/pony-ai-advances-global-deployment-with-launch-of-europes-first-commercial-robotaxi-service-in-zagreb/",
    },
    {
        "emoji": "🏛️",
        "titulo": "Xi Jinping en Shanghái: innovación básica y autosuficiencia industrial como prioridades estratégicas",
        "cuerpo": (
            "En un seminario en Shanghái, el presidente Xi Jinping subrayó la necesidad de fortalecer la "
            "investigación científica básica como palanca para la innovación de largo plazo. Las autoridades "
            "consensuaron medidas concretas para afrontar los retos externos: construir cadenas industriales "
            "seguras y autosuficientes, aplicar una política fiscal más proactiva y una política monetaria "
            "acomodaticia con foco de precisión, y fortalecer el consumo interno como motor principal del "
            "crecimiento. La semana cerró con la confirmación de que el PIB chino inició 2026 por encima "
            "de las previsiones en todos los indicadores clave."
        ),
        "fuente_label": "Prensa Latina — Análisis económico y política exterior marcan semana en China",
        "fuente_url": "https://www.prensa-latina.cu/2026/05/02/analisis-economico-y-politica-exterior-marcan-semana-en-china/",
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
        blocks.append(p_link(n["fuente_label"], n["fuente_url"]))
        blocks.append(divider())

    blocks.append(p("China al Dia · Newsletter semanal en espanol · Fuentes internacionales verificadas", bold=True))
    return blocks


def create_notion_page():
    title = "China Al Dia — Semana 27 Abril - 3 Mayo 2026"
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
