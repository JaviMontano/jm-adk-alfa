# Google Workspace MCP Setup Guide

> Pipeline paso a paso para conectar Claude Code con Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks y Contacts via un solo MCP server unificado.

**Server**: [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)
**Package**: `workspace-mcp` (PyPI) | **90+ tools** | **12 servicios Google**

## Requisitos Previos

- Python 3.10+ con `uv` o `uvx` instalado
- Cuenta de Google (Gmail)
- Acceso a [Google Cloud Console](https://console.cloud.google.com)

```bash
# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Paso 1: Crear Proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Click **"Select a project"** > **"New Project"**
3. Nombre: `jm-adk-workspace` (o el que prefieras)
4. Click **"Create"**

## Paso 2: Habilitar APIs

En tu proyecto, ve a **APIs & Services > Library** y habilita:

| API | Servicio MCP | Tools |
|-----|-------------|-------|
| Gmail API | Gmail | search, send, draft, labels, filters |
| Google Drive API | Drive | files, folders, search, share |
| Google Docs API | Docs | create, edit, format, export |
| Google Sheets API | Sheets | read, write, format, create |
| Google Slides API | Slides | create, present, update |
| Google Calendar API | Calendar | events, calendars, Meet |
| Google Forms API | Forms | create, responses |
| Google Tasks API | Tasks | lists, tasks, manage |
| People API | Contacts | search, manage |

## Paso 3: Crear Credenciales OAuth 2.0

1. Ve a **APIs & Services > Credentials**
2. Click **"+ Create Credentials"** > **"OAuth client ID"**
3. Si es la primera vez, configura la **OAuth consent screen**:
   - User Type: **External** (o Internal si tienes Google Workspace org)
   - App name: `JM-ADK Workspace MCP`
   - Scopes: agregar los scopes de todas las APIs habilitadas
   - Test users: agrega tu email
4. Tipo de aplicacion: **Desktop app**
5. Nombre: `jm-adk-desktop`
6. Click **"Create"**
7. **Descarga el JSON** (boton "Download JSON")

## Paso 4: Ubicar Credenciales

```bash
# Crea directorio de config
mkdir -p ~/.config/workspace-mcp

# Mueve el archivo descargado
mv ~/Downloads/client_secret_*.json ~/.config/workspace-mcp/credentials.json
```

## Paso 5: Configurar Variable de Entorno

Agrega a tu `.bashrc`, `.zshrc` o `.env`:

```bash
export GOOGLE_WORKSPACE_CREDENTIALS_PATH="$HOME/.config/workspace-mcp/credentials.json"
```

Recarga tu shell:
```bash
source ~/.bashrc  # o ~/.zshrc
```

## Paso 6: Autenticar (Primera Vez)

```bash
# La primera ejecucion abre el navegador automaticamente
uvx workspace-mcp
```

Inicia sesion con tu cuenta de Google y acepta los permisos. El token se guarda automaticamente y se renueva solo.

## Paso 7: Verificar en Claude Code

```bash
# Desde el directorio del proyecto
cd /path/to/jm-adk-alfa

# Verificar que el MCP esta configurado
claude mcp list
```

Deberias ver:
```
workspace-mcp  stdio  uvx workspace-mcp --tool-tier extended ...
```

## Paso 8: Probar

En una sesion de Claude Code:

```
"Lista mis ultimos 5 emails de Gmail"
"Crea un evento en Calendar para manana a las 10am"
"Lista los archivos en mi Drive"
"Crea una hoja de calculo nueva"
```

---

## Tool Tiers

El server soporta 3 niveles de herramientas (configurado en `.mcp.json`):

| Tier | Tools | Uso |
|------|-------|-----|
| `core` | ~40 | Lectura + operaciones basicas (CRUD) |
| `extended` | ~65 | Core + labels, batch ops, formatting, search avanzado |
| `complete` | ~90+ | Todo: comments, admin, headers/footers, debug |

Para cambiar tier, edita `.mcp.json`:
```json
"args": ["workspace-mcp", "--tool-tier", "complete"]
```

## Permisos Granulares

Puedes controlar acceso por servicio:

```bash
# Solo lectura total
uvx workspace-mcp --read-only

# Permisos especificos por servicio
uvx workspace-mcp --permissions gmail:send drive:readonly calendar:full
```

Niveles de permiso por servicio:
- `readonly` — solo lectura
- `organize` — lectura + labels/folders (Gmail, Drive)
- `drafts` — organize + crear borradores (Gmail)
- `send` — drafts + enviar emails (Gmail)
- `full` — acceso completo

---

## Servicios y Skills MCP

| Servicio | Skill ADK | Tools Principales |
|----------|-----------|-------------------|
| Gmail | `gmail-mcp` | search, send, draft, labels, filters |
| Calendar | `google-calendar-mcp` | events, calendars, Meet, out-of-office |
| Drive | `google-drive-mcp` | files, folders, search, share, permissions |
| Docs | `google-docs-mcp` | create, edit, format, export PDF, markdown |
| Sheets | `google-sheets-mcp` | read, write, format, create, formulas |
| Slides | `google-slides-mcp` | create, update, thumbnails |
| Forms | (futuro) | create, responses |
| Tasks | (futuro) | lists, tasks, manage |
| Contacts | (futuro) | search, manage |

---

## Seguridad

- **NUNCA** commits `credentials.json` o tokens al repo
- Usa variables de entorno (`${VAR}`) en `.mcp.json`, nunca rutas hardcodeadas
- Usa `--read-only` cuando solo necesites consultar datos
- Usa `--permissions` para limitar acceso por servicio
- Los tokens se renuevan automaticamente
- Revisa los scopes OAuth: usa el minimo necesario

## Docker (Opcional)

```bash
# Para entornos de produccion o CI/CD
docker run -p 8000:8000 \
  -v ~/.config/workspace-mcp:/app/config \
  -e GOOGLE_OAUTH_CREDENTIALS=/app/config/credentials.json \
  workspace-mcp --transport streamable-http
```

## Troubleshooting

| Problema | Solucion |
|----------|----------|
| `uvx: command not found` | Instalar uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `Error: credentials not found` | Verifica `GOOGLE_WORKSPACE_CREDENTIALS_PATH` apunta al JSON descargado |
| `Error: token expired` | Re-ejecuta `uvx workspace-mcp` (reabre navegador) |
| `Error: API not enabled` | Habilita la API faltante en Google Cloud Console (paso 2) |
| `Error: access denied` | Agrega tu email como test user en OAuth consent screen |
| MCP no aparece en `claude mcp list` | Verifica que `.mcp.json` esta en la raiz del proyecto |
| `OAUTHLIB_INSECURE_TRANSPORT` | Normal en desarrollo local (HTTP). No aplica en produccion (HTTPS) |

---

Sources:
- [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)
- [workspacemcp.com](https://workspacemcp.com/)
- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
