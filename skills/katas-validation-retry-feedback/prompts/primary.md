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
3. Si falla: registra `validator_error.error_type`, `path`, `expected` y `actual`.
4. Clasifica el error: recuperable (formato, tipo, estructura) o no recuperable (dato ausente, policy/auth/unsafe).
5. Para errores recuperables: construye feedback con path, expectativa, valor previo y "corrige SOLO lo que el error señala"; reintenta sólo esos paths.
6. Para errores no recuperables: no reintentes el campo; escala con `needs_human_review=True` y `error_chain`.
7. Respeta `max_attempts` total de 2-3. Al agotarlo sin salida válida: escalar, no aceptar la extracción fallida.
8. Si el mismo error domina los casos: recomendar fix estructural (schema/prompt/post-process), no subir retries.

## Output

Markdown o JSON con summary, evidence, attempts, classification, outcome, validation, guardian y risks. Cuando sea JSON, alinéalo con `assets/validation-retry-contract.json`.
