<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 26 · Validación y Retry con Error Feedback

Cuando una extracción tipada falla validación, se reintenta con feedback del error específico (documento original + extracción fallida + error), no a ciegas. Máximo 2-3 intentos; luego se escala con `needs_human_review`. Se distingue error recuperable (formato) de no recuperable (dato ausente en la fuente).

## Resumen ejecutivo

- Loop `extract → validate → extract+feedback → validate`, máximo 2-3 intentos.
- El feedback es el error real de validación, no un mensaje genérico.
- Si el dato no existe en la fuente, no reintentar: escalar a humano para evitar alucinación.
- Patrón sistemático (mismo error en mayoría de casos): arreglar schema/prompt o normalizar en post-process, no subir retries.

## Triggers

- validation retry
- error feedback loop
- retry with feedback
- recoverable error

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando una extracción tipada (Pydantic / JSON Schema) falle validación y haya que decidir cómo reintentar, en escenarios CI/CD o Structured Extraction. Ejecuta el loop con feedback específico, clasifica el error como recuperable o no recuperable, y escala con la cadena de errores tras agotar los intentos.

## Output Format

Markdown con summary, evidence, result (decisión de retry/escalada), validation y risks.
