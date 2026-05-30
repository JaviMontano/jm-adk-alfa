<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Primary Prompt · Kata 06 · Errores estructurados en MCP

## Objetivo

Diseñar o auditar el contrato de error de un tool/servidor MCP de modo que cada fallo devuelva un payload tipado y el cliente decida retry, escalada o aborto leyendo flags.

## Inputs requeridos

- El tool o servidor MCP y las excepciones que puede lanzar.
- El cliente/agente que consume el resultado.
- Restricciones de retry (tope de intentos, ventanas de backoff).

## Proceso

1. Mapear cada excepción a una `errorCategory` del enum (auth, rate_limit, not_found, validation, transient, unknown).
2. Para cada categoría, fijar `isError`, `isRetryable` y `retryAfterSeconds`; redactar `explanation` solo para auditoría.
3. Implementar el cliente: si `isError` y `isRetryable`, esperar `retryAfterSeconds` y reintentar; `transient` → backoff exponencial; `rate_limit` → espera exacta; `auth` → escalar a humano.
4. Tratar el error sin categoría como `unknown` non-retryable y loggear.

## Output

Markdown con summary, evidence (contrato del servidor + lógica del cliente), result, validation y risks. La política de retry queda en el cliente, no en el modelo.
