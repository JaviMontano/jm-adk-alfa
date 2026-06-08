# Mcp Engineering Meta Prompt

Decide si `mcp-engineering` debe activarse, si el alcance es seguro y qué agentes de apoyo intervienen.

## Activation Check

- ¿La tarea involucra configurar un servidor MCP, su scope, credenciales o contrato de error?
- ¿Un tool built-in (Read/Grep/Bash) resolvería el caso sin MCP? Si sí, no actives.
- ¿Hay riesgo de secreto literal en archivo versionado? Activa al guardian de inmediato.
- ¿El input define quién hereda el servidor y qué errores devuelve?

## No activar cuando

- La tarea es sólo lectura, búsqueda o shell local ya cubierta por Read/Grep/Bash.
- El pedido exige secretos literales en archivos versionados o errores genéricos sin contrato tipado.
- No hay servidor MCP, scope, credenciales ni contrato de error que diseñar.

## Routing de agentes

- lead: construye config + contrato de error.
- support: caza secretos en historial y categorías de error faltantes.
- guardian: corre el checklist y bloquea el anti-patrón.
- specialist: detalle de SDK MCP / Claude Code y remediación de secretos.
