<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 22 · Primary Prompt · Configuracion de MCP Servers

## Objective

Configura uno o mas MCP servers en Claude Code aplicando el patron correcto: scope adecuado y credenciales por env-var expansion.

## Required Inputs

- Servers a declarar (`command`, `args`, credenciales necesarias).
- Alcance: el server es de equipo (toda la flota) o un experimento personal.
- Constraints: que built-ins ya cubren parte de la necesidad.
- Definition of done: config funcional sin secretos literales.

## Process

1. Decide el scope: equipo -> `.mcp.json` versionado; personal -> `~/.claude.json`.
2. Escribe el bloque `mcpServers` con `command`/`args` y `env` usando `${ENV_VAR}` para cada credencial.
3. Verifica que ningun built-in (Grep, Read, Glob) ya resuelva el caso antes de agregar el MCP.
4. Documenta las variables de entorno que deben existir.
5. Si detectas un secreto literal en config versionada: rota la credencial, reemplaza por `${ENV}` y purga el historial con git filter-repo.

## Output

Devuelve el `.mcp.json` (o `~/.claude.json`) resultante en Markdown con summary, evidence, result, validation y risks.
