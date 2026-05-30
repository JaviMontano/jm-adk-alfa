<!--
generated-by: scripts/scaffold-skill.py
generated-for: mcp-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Mcp Engineering Primary Prompt

## Objective

Diseña la integración de un servidor MCP en producción: scope correcto, credenciales por env-var y contrato de error tipado con política de reintento en el cliente.

## Required Inputs

- Servidor MCP a integrar y quién debe heredarlo (equipo vs personal).
- Credenciales requeridas y nombres de las variables de entorno.
- Categorías de error que el servidor puede devolver.
- Definition of done (config versionable + contrato de error + checklist verde).

## Process

1. Decide el scope: `.mcp.json` (equipo) o `~/.claude.json` (personal).
2. Escribe la config con `${ENV_VAR}`; cero secretos literales.
3. Diseña el contrato de error (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`).
4. Coloca la política de reintento en el cliente y respeta `retryAfterSeconds`.
5. Verifica que MCP sea necesario (ningún tool built-in aplica) y corre el checklist.

## Output

Markdown con summary, evidence, result, validation y risks. Incluye el bloque `.mcp.json` y el contrato de error en código (EN), prosa en ES.
