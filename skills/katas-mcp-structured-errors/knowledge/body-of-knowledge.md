<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Body of Knowledge · Kata 06 · Errores estructurados en MCP

## Canon

Un servidor MCP que falla devuelve un contrato tipado, no prosa. El payload lleva cuatro flags de control y un campo de auditoría:

- `isError` (bool): ¿la operación falló?
- `errorCategory` (enum): auth, rate_limit, not_found, validation, transient, unknown.
- `isRetryable` (bool): ¿tiene sentido reintentar?
- `retryAfterSeconds` (int): cuánto esperar antes de reintentar.
- `explanation` (string): para el humano que audita el log; el modelo no la interpreta.

La decisión del agente se reduce a tres ejes: ¿es error?, ¿es reintentable?, ¿qué categoría? La política concreta de retry (backoff exponencial, número máximo de intentos) vive en el cliente, no en el modelo.

Reglas por categoría:

- `transient` → backoff exponencial.
- `rate_limit` → esperar exactamente `retryAfterSeconds`.
- `auth` → escalar a humano (no reintentar).
- error sin categoría → tratar como `unknown`, non-retryable, loggear.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Contrato tipado | El servidor emite `isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds` |
| Control por flags | El cliente decide solo con flags; `explanation` no entra en la lógica |
| Política en el cliente | Backoff/n máximo viven en el cliente, no en el modelo |
| Caso degenerado | Error sin categoría se trata como `unknown` non-retryable y se loggea |

## Anti-patrón canónico

```python
except Exception as e:
    return {"error": f"failed: {e}"}
```

Un string genérico (`"something went wrong"`) obliga al modelo a adivinar: reintenta para siempre, abandona, o escala casos que solo necesitaban backoff.

## Quiz canónico (respuestas B·B·B)

- P2: `transient` = backoff exponencial; `rate_limit` = espera exacta de `retryAfterSeconds`.
- P3: error sin categoría → tratar como non-retryable, categorizar como `unknown`, loggear.
