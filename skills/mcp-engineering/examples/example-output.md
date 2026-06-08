# Example Output

## Summary

Servidor `billing` integrado a nivel de equipo en `.mcp.json` con la API key inyectada por `${BILLING_API_KEY}`. Contrato de error tipado que distingue `rate_limit`/`transient` (reintentables) de `auth`/`fatal`, con la política de reintento movida al cliente.

## JSON Report

```json
{
  "schema": 1,
  "skill": "mcp-engineering",
  "report_id": "billing-team-mcp",
  "scenario": "Team billing MCP server with typed retryable errors",
  "scope_decision": {
    "requested_inheritance": "team",
    "config_target": ".mcp.json",
    "versioned": true,
    "reason": "Every developer on the repository should inherit the billing server."
  },
  "mcp_config": {
    "server_name": "billing",
    "config_path": ".mcp.json",
    "mcpServers": {
      "billing": {
        "command": "node",
        "args": ["./servers/billing/index.js"],
        "env": {
          "BILLING_API_KEY": "${BILLING_API_KEY}"
        }
      }
    }
  },
  "credentials": {
    "env_vars": ["BILLING_API_KEY"],
    "literal_secret_count": 0,
    "leaked_secret_detected": false,
    "remediation_steps": []
  },
  "error_contract": {
    "categories": [
      {
        "errorCategory": "auth",
        "isRetryable": false,
        "retryAfterSeconds": null,
        "http_statuses": [401, 403]
      },
      {
        "errorCategory": "rate_limit",
        "isRetryable": true,
        "retryAfterSeconds": 30,
        "http_statuses": [429]
      },
      {
        "errorCategory": "transient",
        "isRetryable": true,
        "retryAfterSeconds": 2,
        "http_statuses": [500, 502, 503]
      },
      {
        "errorCategory": "fatal",
        "isRetryable": false,
        "retryAfterSeconds": null,
        "http_statuses": [400, 404]
      }
    ],
    "generic_error_string_allowed": false
  },
  "retry_policy": {
    "owner": "client",
    "max_attempts": 2,
    "respects_retry_after_seconds": true,
    "model_decides_retry": false,
    "nonretryable_action": "return typed error without retry"
  },
  "builtin_review": {
    "builtin_covers_need": false,
    "checked_tools": ["Read", "Grep", "Bash"],
    "justification": "Billing API access is an external domain capability not covered by built-in file or shell tools."
  },
  "evidence": [
    {
      "type": "inheritance_scope",
      "detail": "The request says the server is for the whole team."
    },
    {
      "type": "env_var_reference",
      "detail": "BILLING_API_KEY is referenced as ${BILLING_API_KEY}."
    },
    {
      "type": "error_mapping",
      "detail": "429 maps to rate_limit and 500-series maps to transient."
    }
  ],
  "validation": {
    "scope_matches_inheritance": true,
    "env_var_expansion_only": true,
    "literal_secret_count": 0,
    "typed_error_categories_complete": true,
    "retry_policy_in_client": true,
    "builtin_not_sufficient": true,
    "deterministic_script_passed": true
  },
  "guardian": {
    "decision": "pass",
    "reason": "Team scope, env-var credentials, typed errors and client-owned retry policy are all machine-checkable."
  }
}
```

## Config Block

```jsonc
{
  "mcpServers": {
    "billing": {
      "command": "node",
      "args": ["./servers/billing/index.js"],
      "env": { "BILLING_API_KEY": "${BILLING_API_KEY}" }
    }
  }
}
```

```ts
// Contrato de error tipado — el cliente decide el reintento
function toolError(category: "auth" | "rate_limit" | "transient" | "fatal", retryAfter?: number) {
  return {
    isError: true,
    errorCategory: category,
    isRetryable: category === "rate_limit" || category === "transient",
    retryAfterSeconds: retryAfter ?? null,
  };
}

async function callBilling(req: Req) {
  const res = await invoke(req);
  if (res.isError && res.isRetryable) {
    await sleep((res.retryAfterSeconds ?? 1) * 1000);
    return invoke(req); // reintento acotado, propiedad del cliente
  }
  return res;
}
```

## Anti-patrón evitado (ANTI)

```jsonc
// ANTI: token literal versionado — fuga garantizada
{ "mcpServers": { "billing": { "env": { "BILLING_API_KEY": "sk-live-9f3c...a21" } } } }
```

```ts
// ANTI: error genérico — el modelo adivina si reintenta un fatal o ignora un transient
return { content: "Something went wrong, please try again" };
```

## Validation

- Scope correcto: config de equipo en `.mcp.json`.
- Credencial por `${BILLING_API_KEY}`; cero secretos literales versionados.
- Error con `errorCategory` + `isRetryable` + `retryAfterSeconds`.
- Política de reintento en el cliente, no en el modelo.
- MCP justificado: ningún tool built-in expone la API de facturación.

## Risks and Limits

- Si `BILLING_API_KEY` se filtró antes, rotar la credencial y purgar el historial con `git filter-repo` (no basta `.gitignore`).
- El entorno de cada miembro del equipo debe exportar `BILLING_API_KEY` o el servidor no arrancará.
