<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Meta Prompt · Kata 06 · Errores estructurados en MCP

Decide si `katas-mcp-structured-errors` debe activarse y con qué agentes.

## Chequeo de activación

- Trigger match: mcp structured error, error category, retryable error, typed error contract.
- Domain fit: se diseña/audita el contrato de error de un tool/servidor MCP, o un agente reintenta sin fin, abandona o escala por leer prosa en vez de flags.
- Input suficiente: hay un tool/servidor MCP y un cliente que consume el resultado.
- No hay skill más segura: si el foco es retry con feedback de validación, considerar `katas-validation-retry-error-feedback`; si es propagación entre agentes, `katas-error-propagation-multi-agent`.

## Casos negativos

- Petición ajena al dominio MCP/errores → no activar.
- Input vacío → pedir el tool/servidor y el cliente antes de proceder.
