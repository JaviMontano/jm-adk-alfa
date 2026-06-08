# Mcp Engineering

Configurar MCP servers (project vs user scope, env-var expansion) y disenar contratos de error tipados con categoria y retryable.

## Triggers

- mcp engineering
- mcp server config
- mcp error contract
- mcp scope

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Capacidad de ingeniería para integrar servidores MCP en producción: scope correcto (project vs user), credenciales por expansión de variables de entorno y contratos de error tipados (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`) con la política de reintento en el cliente, no en el modelo.

## Contrato determinístico

El entregable certificable es un reporte JSON que cumpla `assets/mcp-engineering-contract.json` y pueda validarse offline con `scripts/check.sh`.

Debe incluir:

- `scope_decision`: quién hereda el servidor, target elegido y si es versionable.
- `mcp_config`: servidor MCP con secretos referenciados por `${ENV_VAR}`.
- `credentials`: inventario de env-vars, cero secretos literales y remediación si hubo fuga.
- `error_contract`: categorías `auth`, `rate_limit`, `transient` y `fatal`, con `isRetryable` mecánico.
- `retry_policy`: política propiedad del cliente, no del modelo.
- `builtin_review`: justificación de MCP frente a Read/Grep/Bash u otro built-in.
- `validation` y `guardian`: flags verificables y decisión final.

## Quick Use

Invócala cuando configures un servidor MCP para un equipo, cuando un servidor devuelva errores que el modelo reintenta a ciegas, o cuando debas decidir MCP frente a un tool built-in. Entrega: bloque `.mcp.json` versionable + contrato de error tipado + checklist de validación.

## Output Format

Markdown o JSON con summary, evidence, result, validation y risks. Config en bloques de código (`.mcp.json`, contrato de error en TS/JSON) o JSON compatible con `assets/mcp-engineering-contract.json`.
