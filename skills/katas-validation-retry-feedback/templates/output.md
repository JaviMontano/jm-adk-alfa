# Kata 26 · Output — Validación y Retry con Error Feedback

## Summary

{summary}

## Evidence

{evidence}

## Attempts

| Attempt | Status | Error path | Error type | Feedback scope |
|---|---|---|---|---|
| {attempt_number} | {attempt_status} | {error_path} | {error_type} | {feedback_scope} |

## Result

- Clasificación del error: {recoverable_or_not}
- Intentos consumidos: {attempts} / {max_attempts}
- Extracción válida o escalada: {result}
- needs_human_review: {needs_human_review}
- error_chain: {error_chain}

## Validation

- El feedback de cada retry fue el error específico, no genérico: {feedback_check}
- El cap de 2-3 intentos se respetó: {cap_check}
- Los errores no recuperables no fueron reintentados: {nonrecoverable_retry_check}
- Ningún dato ausente en la fuente fue inventado: {hallucination_check}
- El reporte JSON cumple `assets/validation-retry-contract.json`: {contract_check}

## Risks and Limits

{risks}
