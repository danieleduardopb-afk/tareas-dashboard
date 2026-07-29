# Dashboard de Tareas (Notion → GitHub Pages)

Este repo lee tu base de datos "Gestión de tareas" de Notion cada hora y
muestra gráficos gratis en una página estática, para insertarla en Notion
con un bloque `/embed` (sin límite de gráficos del plan gratis).

## Configuración (una sola vez)

### 1. Crear una integración interna en Notion
1. Ve a https://www.notion.so/my-integrations
2. "New integration" → dale un nombre, por ejemplo `Dashboard Tareas`.
3. Copia el "Internal Integration Secret" (empieza con `ntn_...` o `secret_...`).
4. Ve a tu base de datos "Gestión de tareas" en Notion → botón `•••` (arriba
   derecha) → "Connections" → conecta la integración que creaste.

### 2. Obtener el ID de la base de datos
Es la parte de la URL de la base de datos entre la última `/` y el `?`:
```
https://www.notion.so/workspace/9567bc979e0c8320991201d4f25fa1b5?v=...
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                 este es el Database ID
```

### 3. Agregar los secretos en GitHub
En tu repo: Settings → Secrets and variables → Actions → "New repository secret"
- `NOTION_TOKEN` → el secreto que copiaste en el paso 1
- `NOTION_DATABASE_ID` → el ID del paso 2

### 4. Activar GitHub Pages
Settings → Pages → Source: "Deploy from a branch" → Branch: `main` / `(root)` → Save.
Tu página quedará en algo como:
```
https://<tu-usuario>.github.io/<nombre-del-repo>/
```

### 5. Ejecutar el Action por primera vez
Pestaña "Actions" del repo → selecciona "Actualizar datos de Notion" →
"Run workflow" (botón manual). Esto genera el primer `data.json` real.
Después correrá solo cada hora.

### 6. Insertar en Notion
En tu página de Notion, escribe `/embed` y pega la URL de GitHub Pages del paso 4.

## Archivos
- `index.html` — la página con los gráficos (Chart.js).
- `data.json` — los datos que lee `index.html` (se regenera solo).
- `scripts/fetch_notion.py` — trae los datos desde la API de Notion.
- `.github/workflows/update-data.yml` — el Action programado.
