<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Deep · Kata 06 · Errores estructurados en MCP

Úsala cuando el servidor lanza muchas excepciones heterogéneas, varios clientes consumen el resultado o el comportamiento de retry es crítico (Customer Support, API Integration Reliability).

Incluye:

- Inventario de excepciones y su mapeo completo al enum de `errorCategory` (auth, rate_limit, not_found, validation, transient, unknown).
- Tabla de decisión del cliente por categoría: retry exacto (`rate_limit`), backoff exponencial (`transient`), escalada (`auth`), aborto, y tope de intentos.
- Manejo del caso degenerado: error sin categoría → `unknown` non-retryable + log.
- Verificación de que `explanation` no entra en la lógica de control.
- Notas de descubrimiento, opciones consideradas, enfoque elegido, validación y riesgos.
