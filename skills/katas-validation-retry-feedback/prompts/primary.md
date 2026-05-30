<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 26 · Prompt de producción — Validación y Retry con Error Feedback

## Objetivo

Aplicar retry-with-error-feedback a una extracción tipada que falla validación: reintentar con el error específico, distinguir recuperable de no recuperable, capar a 2-3 intentos y escalar cuando se agotan.

## Inputs requeridos

- Documento o fuente original de la extracción.
- Schema esperado (Pydantic / JSON Schema).
- Extracción fallida y el error de validación específico.
- `max_retries` (default 2).

## Proceso

1. Ejecuta `extract` contra el documento con `tools=[schema]` y `tool_choice` forzado.
2. `validate` la extracción contra el schema.
3. Si falla: construye feedback = error específico + output previo + "corrige SOLO lo que el error señala", y reintenta.
4. Clasifica el error: recuperable (formato) → reintentar; no recuperable (dato ausente en la fuente) → escalar de inmediato, no inventar.
5. Al agotar `max_retries`: devolver `needs_human_review=True` con la `error_chain`.
6. Si el mismo error domina los casos: recomendar fix estructural (schema/prompt/post-process), no subir retries.

## Output

Markdown con summary, evidence, result (extracción válida o registro de escalada), validation y risks.
