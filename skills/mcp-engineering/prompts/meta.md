<!--
generated-by: scripts/scaffold-skill.py
generated-for: mcp-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Mcp Engineering Meta Prompt

Decide si `mcp-engineering` debe activarse, si el alcance es seguro y qué agentes de apoyo intervienen.

## Activation Check

- ¿La tarea involucra configurar un servidor MCP, su scope, credenciales o contrato de error?
- ¿Un tool built-in (Read/Grep/Bash) resolvería el caso sin MCP? Si sí, no actives.
- ¿Hay riesgo de secreto literal en archivo versionado? Activa al guardian de inmediato.
- ¿El input define quién hereda el servidor y qué errores devuelve?

## Routing de agentes

- lead: construye config + contrato de error.
- support: caza secretos en historial y categorías de error faltantes.
- guardian: corre el checklist y bloquea el anti-patrón.
- specialist: detalle de SDK MCP / Claude Code y remediación de secretos.
