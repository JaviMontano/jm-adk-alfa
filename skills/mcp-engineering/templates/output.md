<!--
generated-by: scripts/scaffold-skill.py
generated-for: mcp-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

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

## Validation

- [ ] Scope correcto ({.mcp.json equipo | ~/.claude.json personal})
- [ ] Credenciales por `${ENV}`, cero literales versionados
- [ ] Error con `errorCategory` + `isRetryable` (+ `retryAfterSeconds`)
- [ ] Política de reintento en el cliente, no en el modelo
- [ ] MCP justificado (ningún built-in aplica)

## Risks and Limits

{risks — secretos en historial, env-vars faltantes en el entorno del equipo}
