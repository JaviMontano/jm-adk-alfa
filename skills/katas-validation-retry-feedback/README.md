# Kata 26 · Validación y Retry con Error Feedback

Cuando una extracción tipada falla validación, se reintenta con feedback del error específico (documento original + extracción fallida + error), no a ciegas. Máximo 2-3 intentos; luego se escala con `needs_human_review`. Se distingue error recuperable (formato) de no recuperable (dato ausente en la fuente).

## Resumen ejecutivo

- Loop `extract → validate → extract+feedback → validate`, máximo 2-3 intentos.
- El feedback es el error real de validación, no un mensaje genérico.
- Si el dato no existe en la fuente, no reintentar: escalar a humano para evitar alucinación.
- Patrón sistemático (mismo error en mayoría de casos): arreglar schema/prompt o normalizar en post-process, no subir retries.

## Contrato determinístico

La salida certificable de esta kata es un reporte JSON que cumpla `assets/validation-retry-contract.json` y que pueda validarse offline con `scripts/check.sh`.

Campos obligatorios:

- `attempts`: lista secuencial de intentos con errores de validador, feedback específico y estado final.
- `classification`: decisión explícita entre `recoverable`, `nonrecoverable` o `mixed`.
- `outcome`: `valid` o `escalated`, con `retry_count`, `max_attempts`, `needs_human_review` y `error_chain`.
- `validation`: contadores y flags que prueban que no hubo feedback genérico, reintentos fuera de cap, retry de errores no recuperables ni aceptación de salida inválida.
- `guardian`: decisión final y razón trazable.

## Triggers especializados

- validation retry
- error feedback loop
- retry with feedback
- recoverable error
- Pydantic `ValidationError`
- JSON Schema validation failure
- silent invalid output acceptance

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando una extracción tipada (Pydantic / JSON Schema) falle validación y haya que decidir cómo reintentar, en escenarios CI/CD o Structured Extraction. Ejecuta el loop con feedback específico, clasifica el error como recuperable o no recuperable, y escala con la cadena de errores tras agotar los intentos.

## Output Format

Markdown o JSON con summary, evidence, result, validation y risks. Para validación offline usa el JSON contract de `assets/` y ejecuta `bash skills/katas-validation-retry-feedback/scripts/check.sh`.
