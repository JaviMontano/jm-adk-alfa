# Mcp Engineering Output

## Summary

{summary — servidor integrado, scope elegido y forma del contrato de error}

## Evidence

{evidence — quién hereda el servidor, qué secretos por env-var, categorías de error soportadas}

## Result

### Config (scope: {.mcp.json | ~/.claude.json})

```jsonc
{config_block}
```

### Contrato de error

```ts
{error_contract_block}
```

### Retry Policy

- Owner: {client_or_model}
- Max attempts: {max_attempts}
- Respects `retryAfterSeconds`: {retry_after_check}
- Non-retryable action: {nonretryable_action}

## Validation

- [ ] Scope correcto ({.mcp.json equipo | ~/.claude.json personal})
- [ ] Credenciales por `${ENV}`, cero literales versionados
- [ ] Error con `errorCategory` + `isRetryable` (+ `retryAfterSeconds`)
- [ ] Política de reintento en el cliente, no en el modelo
- [ ] MCP justificado (ningún built-in aplica)
- [ ] Reporte JSON compatible con `assets/mcp-engineering-contract.json` cuando se requiera validación offline

## Risks and Limits

{risks — secretos en historial, env-vars faltantes en el entorno del equipo}
