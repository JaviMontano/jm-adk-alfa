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
3. Diseña el contrato de error con categorías `auth`, `rate_limit`, `transient` y `fatal`.
4. Marca `rate_limit` y `transient` como reintentables; `auth` y `fatal` no se reintentan.
5. Coloca la política de reintento en el cliente, con cap de 2-3 intentos y respeto de `retryAfterSeconds`.
6. Verifica que MCP sea necesario (ningún tool built-in aplica) y corre el checklist.
7. Si hubo secreto filtrado, incluye rotación y purga de historial con `git filter-repo`; no aceptes sólo `.gitignore`.

## Output

Markdown o JSON con summary, evidence, result, validation y risks. Cuando sea JSON, alinéalo con `assets/mcp-engineering-contract.json`.
