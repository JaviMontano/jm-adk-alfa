<!--
generated-by: scripts/scaffold-skill.py
generated-for: mcp-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Servidor `billing` integrado a nivel de equipo en `.mcp.json` con la API key inyectada por `${BILLING_API_KEY}`. Contrato de error tipado que distingue `rate_limit`/`transient` (reintentables) de `auth`/`fatal`, con la política de reintento movida al cliente.

## Result — Patrón correcto (GOOD)

```jsonc
// .mcp.json — versionado para el equipo
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
