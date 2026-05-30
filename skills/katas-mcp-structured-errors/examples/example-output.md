<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output · Kata 06 · Errores estructurados en MCP

## Summary

Se reemplaza el string genérico de `crm_lookup` por un contrato de error tipado y se mueve la política de retry al cliente.

## Anti-patrón (antes)

```python
except Exception as e:
    return {"error": f"failed: {e}"}  # el agente adivina
```

## Patrón correcto (después)

```python
# Servidor MCP: contrato tipado por categoría
try:
    return crm_lookup(args)
except RateLimitException as e:
    return {"isError": True, "errorCategory": "rate_limit",
            "isRetryable": True, "retryAfterSeconds": e.retry_after,
            "explanation": f"Rate limit; reintentar en {e.retry_after}s"}
except AuthException as e:
    return {"isError": True, "errorCategory": "auth",
            "isRetryable": False, "retryAfterSeconds": 0,
            "explanation": "Credenciales inválidas; requiere intervención"}
except NotFoundException:
    return {"isError": True, "errorCategory": "not_found",
            "isRetryable": False, "retryAfterSeconds": 0,
            "explanation": "Registro inexistente"}
except Exception as e:
    return {"isError": True, "errorCategory": "transient",
            "isRetryable": True, "retryAfterSeconds": 2,
            "explanation": f"Fallo transitorio: {e}"}

# Cliente: la política de retry vive aquí
if result.get("isError") and result.get("isRetryable"):
    if result["errorCategory"] == "rate_limit":
        time.sleep(result["retryAfterSeconds"])      # espera exacta
    else:  # transient
        time.sleep(backoff_exponencial(attempt))     # backoff
    return retry(args)
if result.get("errorCategory") == "auth":
    return escalate_to_human(result)
# error sin categoría reconocida → unknown, non-retryable, log
```

## Validation

- [x] El servidor emite flags tipados, no prosa.
- [x] El cliente decide solo con flags; `explanation` queda para el log.
- [x] `rate_limit` usa `retryAfterSeconds` exacto; `transient` usa backoff exponencial.
- [x] `auth` escala; categoría desconocida → `unknown` non-retryable + log.

## Risks and Limits

El enum de `errorCategory` debe mantenerse sincronizado entre servidor y cliente; añadir una categoría nueva sin actualizar el cliente la degrada a `unknown` non-retryable.
