# Assets — mcp-engineering

Estos assets definen el contrato determinístico para configurar servidores MCP con scope, secretos y errores tipados verificables.

- `mcp-engineering-contract.json`: campos requeridos del reporte.
- `scope-policy.json`: selección de `.mcp.json` o `~/.claude.json` según herencia.
- `secret-policy.json`: env-var expansion y remediación de secretos.
- `typed-error-policy.json`: categorías y retryability esperadas.
- `client-retry-policy.json`: política de retry propiedad del cliente.
- `evidence-policy.json`: evidencia mínima aceptada.

Los assets son usados por `scripts/validate_mcp_engineering.py`, `scripts/check.sh`, `evals/evals.json` y ejemplos.
