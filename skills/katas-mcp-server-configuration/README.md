<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Mcp Server Configuration

Configuracion de MCP servers: project vs user scope, env-var expansion para credenciales y rotacion ante secreto leakeado.

## Triggers

- mcp server configuration
- mcp scope
- env var credentials
- mcp json config

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Kata 22 del kit JM-ADK. Ensena a configurar MCP servers en Claude Code con criterio de scope: `.mcp.json` (project, versionado, sirve a la flota) vs `~/.claude.json` (user, personal). Credenciales siempre por env-var expansion (`${GITHUB_TOKEN}`), nunca hardcodeadas. Cubre la respuesta correcta ante un secreto filtrado: rotar credencial + reemplazar por `${ENV}` + purgar historial con git filter-repo, nunca `.gitignore`.

## Quick Use

Activa esta skill al editar o revisar `.mcp.json` o `~/.claude.json`, al decidir el scope de un server (equipo vs personal), al manejar credenciales de un server externo, o al responder a un token filtrado en config versionada. El patron canonico GOOD/ANTI vive en `SKILL.md`.

## Output Format

Markdown con summary, evidence, result, validation y risks.
