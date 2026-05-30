<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 26 · Output — Validación y Retry con Error Feedback

## Summary

{summary}

## Evidence

{evidence}

## Result

- Clasificación del error: {recoverable_or_not}
- Intentos consumidos: {attempts} / {max_retries}
- Extracción válida o escalada: {result}
- needs_human_review: {needs_human_review}
- error_chain: {error_chain}

## Validation

- El feedback de cada retry fue el error específico, no genérico: {feedback_check}
- El cap de 2-3 intentos se respetó: {cap_check}
- Ningún dato ausente en la fuente fue inventado: {hallucination_check}

## Risks and Limits

{risks}
