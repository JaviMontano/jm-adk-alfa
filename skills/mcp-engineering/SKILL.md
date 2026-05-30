---
name: mcp-engineering
version: 1.0.0
description: "Configurar MCP servers (project vs user scope, env-var expansion) y disenar contratos de error tipados con categoria y retryable."
owner: "JM Labs"
triggers:
  - mcp engineering
  - mcp server config
  - mcp error contract
  - mcp scope
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Mcp Engineering

## Capacidad

Diseñar e implementar la integración de servidores MCP de forma productiva: elegir el **scope** correcto (project vs user), inyectar credenciales por **expansión de variables de entorno** y diseñar **contratos de error tipados** (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`) para que el modelo y el cliente sepan cuándo reintentar sin adivinar.

El entregable es una configuración de servidores versionable por el equipo más un contrato de error que el cliente puede consumir mecánicamente: la política de reintento vive en el código del cliente, nunca en el juicio del modelo.

## Cuándo usarla

- Conectar un servidor MCP a un equipo y decidir si la config va en `.mcp.json` (compartida, versionada) o `~/.claude.json` (personal).
- Un servidor MCP devuelve errores que el modelo "interpreta" como prosa y reintenta a ciegas.
- Hay un token literal en un archivo versionado y necesitas rotarlo y purgar el historial.
- Necesitas decidir si una capacidad debe ser un servidor MCP o si un tool built-in ya la cubre.

No la uses cuando un tool built-in (Read, Grep, Bash) ya resuelve la necesidad: MCP solo cuando ningún built-in aplica.

## Cómo construir

1. **Decide el scope.** Config compartida del equipo → `.mcp.json` versionado en el repo. Config personal del desarrollador → `~/.claude.json` fuera del repo. El criterio: ¿quién debe heredar este servidor?
2. **Inyecta credenciales por env-var.** Referencia `${ENV_VAR}` en la config; nunca el secreto literal. El valor real vive en el entorno del proceso, no en el archivo.
3. **Diseña el contrato de error tipado.** Cada respuesta de error expone `isError`, `errorCategory` (auth/rate_limit/transient/fatal), `isRetryable` (bool) y `retryAfterSeconds` cuando aplica. El modelo no infiere: lee campos.
4. **Coloca la política de reintento en el cliente.** El cliente decide reintentar según `isRetryable` y respeta `retryAfterSeconds`. El modelo no implementa backoff con prosa.
5. **Si se filtró un secreto, rótalo y purga.** Rotar la credencial comprometida + reescribir historia con `git filter-repo`. Un `.gitignore` posterior NO borra lo ya commiteado.
6. **Justifica MCP frente al built-in.** Antes de añadir un servidor, confirma que ningún tool built-in cubre el caso.

## Patrón correcto

```jsonc
// .mcp.json — versionado para el equipo, secreto por env-var
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
// Error contract returned by the server — typed, machine-readable
function toolError(category: ErrorCategory, retryAfter?: number) {
  return {
    isError: true,
    errorCategory: category,            // "auth" | "rate_limit" | "transient" | "fatal"
    isRetryable: category === "rate_limit" || category === "transient",
    retryAfterSeconds: retryAfter ?? null,
  };
}

// Retry policy lives in the CLIENT, not in the model's judgement
async function callTool(req: Req) {
  const res = await invoke(req);
  if (res.isError && res.isRetryable) {
    await sleep((res.retryAfterSeconds ?? 1) * 1000);
    return invoke(req); // bounded retry, client-owned
  }
  return res;
}
```

## Anti-patrón

```jsonc
// ANTI: token literal en archivo versionado — fuga garantizada
{
  "mcpServers": {
    "billing": { "env": { "BILLING_API_KEY": "sk-live-9f3c...a21" } }
  }
}
```

```ts
// ANTI: error como string genérico — el modelo debe adivinar si reintenta
function toolError() {
  return { content: "Something went wrong, please try again" };
}
// El modelo reintenta a ciegas un fatal, o no reintenta un transient.
// Y "git rm + gitignore" NO purga el secreto del historial.
```

## Checklist de validación

- ¿El scope es correcto (`.mcp.json` equipo / `~/.claude.json` personal)?
- ¿Las credenciales se inyectan por `${ENV}` y no hay secretos literales en archivos versionados?
- ¿Cada error expone categoría + `isRetryable` (+ `retryAfterSeconds` cuando aplica)?
- ¿La política de reintento vive en el cliente, no en el modelo?
- ¿Se recurre a MCP solo cuando ningún tool built-in aplica?
- ¿Ante fuga de secreto el plan es rotar + `filter-repo`, no solo `.gitignore`?

## Katas y skills relacionadas

- Katas: 06, 22.
- Skills relacionadas: `katas-mcp-structured-errors`, `katas-mcp-server-configuration`, `tool-use-design`, `custom-tooling-extension`.
