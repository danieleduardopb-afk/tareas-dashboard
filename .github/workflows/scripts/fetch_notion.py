"""
Consulta la base de datos "Gestión de tareas" en Notion y escribe data.json
con la información resumida que usan los gráficos de index.html.

Variables de entorno requeridas:
  NOTION_TOKEN     -> token secreto de tu integración interna de Notion
  NOTION_DATABASE_ID -> ID de la base de datos "Gestión de tareas"
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib import request, error

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

if not NOTION_TOKEN or not DATABASE_ID:
    print("Faltan NOTION_TOKEN o NOTION_DATABASE_ID como variables de entorno.")
    sys.exit(1)


def notion_query(database_id, start_cursor=None):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    body = {"page_size": 100}
    if start_cursor:
        body["start_cursor"] = start_cursor

    req = request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_select_name(prop):
    if not prop:
        return None
    value = prop.get("select") or prop.get("status")
    return value.get("name") if value else None


def get_title(prop):
    if not prop or not prop.get("title"):
        return ""
    return "".join(t.get("plain_text", "") for t in prop["title"])


def get_date(prop):
    if not prop or not prop.get("date"):
        return None
    return prop["date"].get("start")


def extract_task(page):
    props = page.get("properties", {})
    return {
        "nombre": get_title(props.get("Nombre de la tarea")),
        "categoria": get_select_name(props.get("Categoría")),
        "prioridad": get_select_name(props.get("Prioridad")),
        "estado": get_select_name(props.get("Estado")),
        "fecha_vencimiento": get_date(props.get("Fecha de vencimiento")),
    }


def main():
    tasks = []
    cursor = None

    try:
        while True:
            data = notion_query(DATABASE_ID, cursor)
            for page in data.get("results", []):
                tasks.append(extract_task(page))
            if data.get("has_more"):
                cursor = data.get("next_cursor")
            else:
                break
    except error.HTTPError as e:
        print(f"Error consultando Notion: {e.code} {e.read().decode('utf-8')}")
        sys.exit(1)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tasks": tasks,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"data.json generado con {len(tasks)} tareas.")


if __name__ == "__main__":
    main()
