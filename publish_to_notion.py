#!/usr/bin/env python3
"""
Publica la newsletter semanal de China Al Dia en Notion.
Uso: NOTION_TOKEN=<token> python publish_to_notion.py [YYYY-MM-DD]
     Si no se pasa fecha, se usa la mas reciente en newsletters/.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
PARENT_PAGE_ID = os.environ.get("PARENT_PAGE_ID", "34ae9ac6c5268056bd3cfeddc772dddc")

if not NOTION_TOKEN:
    print("ERROR: define la variable de entorno NOTION_TOKEN antes de ejecutar.")
    sys.exit(1)

API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
NEWSLETTERS_DIR = Path(__file__).parent / "newsletters"


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

def h3(text):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

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

def bulleted(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def quote(text):
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


# --- Parser de Markdown a bloques Notion ---

def parse_md_to_blocks(md_text):
    """Convierte markdown de newsletter a bloques Notion."""
    blocks = []
    lines = md_text.splitlines()
    i = 0
    first_h1_done = False

    while i < len(lines):
        line = lines[i]

        # H1 — titulo principal
        if line.startswith("# ") and not first_h1_done:
            first_h1_done = True
            title = line[2:].strip()
            blocks.append(callout(title, "🇨🇳"))
            i += 1
            continue

        # H2 — seccion (## Texto)
        if line.startswith("## "):
            text = line[3:].strip()
            # subtitulo de semana justo bajo el H1
            if text.startswith("Tu resumen"):
                blocks.append(p(text))
            else:
                blocks.append(h2(text))
            i += 1
            continue

        # H3 — noticia individual
        if line.startswith("### "):
            text = line[4:].strip()
            blocks.append(h3(text))
            i += 1
            continue

        # Negrita sola en linea (**Texto**)
        if line.startswith("**") and line.endswith("**") and len(line) > 4:
            text = line[2:-2]
            blocks.append(p(text, bold=True))
            i += 1
            continue

        # Separador ---
        if line.strip() == "---":
            blocks.append(divider())
            i += 1
            continue

        # Lista de fuentes: "- Texto: url" o "- [Texto](url)"
        if line.startswith("- "):
            content = line[2:].strip()
            # formato markdown link: [label](url)
            md_link = re.match(r'\[(.+?)\]\((.+?)\)', content)
            if md_link:
                blocks.append(p_link(md_link.group(1), md_link.group(2)))
            # formato "Label: url"
            elif ': http' in content:
                parts = content.split(': ', 1)
                if len(parts) == 2:
                    blocks.append(p_link(parts[0], parts[1]))
                else:
                    blocks.append(bulleted(content))
            else:
                blocks.append(bulleted(content))
            i += 1
            continue

        # Linea vacia
        if line.strip() == "":
            i += 1
            continue

        # Linea de texto italica (*texto*)
        if line.startswith("*") and line.endswith("*"):
            text = line.strip("*")
            blocks.append(p(text))
            i += 1
            continue

        # Parrafo normal
        if line.strip():
            # Eliminar formato markdown basico (**bold**, *italic*)
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            clean = re.sub(r'\*(.+?)\*', r'\1', clean)
            blocks.append(p(clean.strip()))

        i += 1

    return blocks


def pick_newsletter_file(date_arg=None):
    if date_arg:
        path = NEWSLETTERS_DIR / f"{date_arg}.md"
        if not path.exists():
            print(f"ERROR: no se encuentra {path}")
            sys.exit(1)
        return path
    # La mas reciente
    files = sorted(NEWSLETTERS_DIR.glob("*.md"), reverse=True)
    if not files:
        print("ERROR: no hay archivos en newsletters/")
        sys.exit(1)
    return files[0]


def extract_title_and_week(md_text, file_stem):
    """Extrae titulo de la newsletter del markdown."""
    for line in md_text.splitlines():
        if line.startswith("**Semana del "):
            week = line.strip("*").strip()
            return f"China Al Dia — {week}", week
    return f"China Al Dia — {file_stem}", file_stem


def create_notion_page(date_arg=None):
    md_file = pick_newsletter_file(date_arg)
    md_text = md_file.read_text(encoding="utf-8")

    title, week = extract_title_and_week(md_text, md_file.stem)
    blocks = parse_md_to_blocks(md_text)

    # Notion limita a 100 bloques por peticion
    CHUNK = 100
    first_chunk = blocks[:CHUNK]
    rest_chunks = [blocks[j:j+CHUNK] for j in range(CHUNK, len(blocks), CHUNK)]

    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🇨🇳"},
        "cover": {"type": "external", "external": {
            "url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
        }},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": first_chunk,
    }

    print(f"Publicando: '{title}'")
    print(f"Bloques totales: {len(blocks)}")
    result = notion_request("POST", "/pages", payload)
    page_id = result.get("id", "")
    page_url = result.get("url", f"https://www.notion.so/{page_id.replace('-', '')}")

    # Añadir bloques restantes en chunks
    for chunk in rest_chunks:
        notion_request("PATCH", f"/blocks/{page_id}/children", {"children": chunk})

    print(f"\nListo!")
    print(f"URL: {page_url}")
    return page_url


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    create_notion_page(date_arg)
