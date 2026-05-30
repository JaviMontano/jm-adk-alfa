<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 22 · Body of Knowledge · Configuracion de MCP Servers

## Canon

Conceptos clave de la kata:

- **Dos scopes de declaracion.** `.mcp.json` (project) viaja con el repo y se descubre al conectar; sirve a toda la flota. `~/.claude.json` (user) es personal y no se replica al equipo.
- **Env-var expansion para credenciales.** Las credenciales se inyectan con `${ENV_VAR}` (ej. `${GITHUB_TOKEN}`), nunca como literal en el archivo. Claude Code resuelve la variable desde el entorno al conectar el server.
- **Descubrimiento simultaneo.** Multiples servers en el bloque `mcpServers` se descubren a la vez al conectar.
- **MCP resources vs tools.** Los resources (catalogos) reducen llamadas exploratorias frente a invocar tools repetidamente.
- **MCP solo cuando un built-in no aplica.** Grep, Read, Glob ya cubren busqueda y lectura en filesystem local; un MCP para eso es overkill.

## Quality Signals

| Signal | Target |
|---|---|
| Scope correcto | Config de equipo en `.mcp.json` versionado; experimento personal en `~/.claude.json` |
| Credenciales seguras | Toda credencial via `${ENV_VAR}`, cero literales en archivos versionados |
| MCP justificado | Se prefiere un built-in cuando cubre el caso; el MCP se defiende |
| Respuesta a leak | Rotar credencial + `${ENV}` + purgar historial; nunca `.gitignore` |

## Anti-patron canonico

```json
{ "env": { "GITHUB_TOKEN": "ghp_AbCdEfG123456789" } }
```

Token literal hardcodeado en `.mcp.json` versionado. Queda en el historial de git de forma permanente; `.gitignore` no remueve lo ya versionado. La unica respuesta correcta es rotar la credencial, reemplazarla por `${GITHUB_TOKEN}` y purgar el historial con git filter-repo.
