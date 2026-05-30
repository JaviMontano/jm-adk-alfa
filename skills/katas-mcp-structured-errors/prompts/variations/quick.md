<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Quick · Kata 06 · Errores estructurados en MCP

Úsala cuando el contrato es simple y conocido (pocas excepciones, una sola categoría dominante).

Entrega solo: el payload tipado del servidor (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`), la rama de decisión del cliente, el estado de validación y los riesgos residuales. No reintroduzcas la política de retry en el modelo.
