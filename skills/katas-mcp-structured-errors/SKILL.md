---
name: katas-mcp-structured-errors
version: 1.0.0
description: "Errores MCP tipados (isError, errorCategory, isRetryable, retryAfterSeconds); la politica de retry vive en el cliente."
owner: "JM Labs"
triggers:
  - mcp structured error
  - error category
  - retryable error
  - typed error contract
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 06 · Errores estructurados en MCP

## Qué es

Un servidor MCP que falla devuelve un payload tipado con `isError`, `errorCategory`, `isRetryable` y `retryAfterSeconds`. El agente decide entre reintentar, escalar o abortar leyendo esos flags, no la prosa del mensaje de error. El campo `explanation` existe para el humano que audita el log, no para que el modelo lo interprete. Las políticas de retry concretas (backoff exponencial, número máximo de intentos) viven en el cliente, no en el modelo.

Escenarios canónicos: Customer Support y API Integration Reliability.

## Por qué importa (falla que evita)

Un string genérico como `"something went wrong"` obliga al modelo a adivinar la intención. El resultado es uno de tres comportamientos degenerados: reintenta para siempre, abandona una operación que solo necesitaba backoff, o escala a un humano casos que se habrían resuelto solos con una espera. El error sin estructura traslada al modelo una decisión que debería ser determinista.

## Modelo mental

- Tres ejes de decisión por cada fallo: ¿es error? (`isError`), ¿es reintentable? (`isRetryable`), ¿qué categoría? (`errorCategory`: auth, rate_limit, not_found, validation, transient).
- El agente lee flags, nunca prosa. La prosa (`explanation`) es para auditoría humana del log.
- Las políticas de retry (backoff exponencial, n máximo de intentos) viven en el cliente, no en el modelo.
- `transient` → backoff exponencial; `rate_limit` → esperar exactamente `retryAfterSeconds`.
- Error sin categoría → tratar como non-retryable, categorizar como `unknown`, loggear.

## Patrón correcto

```python
# Servidor MCP: devuelve un contrato tipado
try:
    return do_work(args)
except RateLimitException as e:
    return {
        "isError": True,
        "errorCategory": "rate_limit",
        "isRetryable": True,
        "retryAfterSeconds": e.retry_after,
        "explanation": f"Rate limit alcanzado; reintentar en {e.retry_after}s",
    }

# Cliente: la política de retry vive aquí, no en el modelo
if result.get("isError") and result.get("isRetryable"):
    time.sleep(result["retryAfterSeconds"])
    return retry(args)
if result.get("errorCategory") == "auth":
    return escalate_to_human(result)
```

## Anti-patrón

```python
except Exception as e:
    return {"error": f"failed: {e}"}  # string genérico, sin flags tipados
```

## Argumento de certificación

Los errores de MCP son contratos tipados (`isError`, `errorCategory`, `isRetryable`); la política de retry vive en el cliente, no en el modelo. Quien certifica esta kata debe demostrar que el servidor emite los flags, que el cliente decide a partir de ellos y que `explanation` no participa en la lógica de control.

## Cuándo activar

- Se diseña o revisa el contrato de error de un tool o servidor MCP.
- Un agente reintenta indefinidamente, abandona prematuro, o escala fallos que solo necesitaban backoff.
- Se necesita separar la semántica del error (servidor) de la política de retry (cliente).

## Skills relacionadas

- `katas-validation-retry-error-feedback`
- `katas-error-propagation-multi-agent`
- `katas-tool-description-quality`
