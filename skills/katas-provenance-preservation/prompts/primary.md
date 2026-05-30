<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Provenance Preservation Primary Prompt

## Objective

Producir un output factual auditable aplicando la Kata 20: cada claim con su provenance tipada, los conflictos marcados y escalados.

## Required Inputs

- Las fuentes a agregar (documentos, resultados de subagentes, datasets), cada una con un identificador estable.
- Las afirmaciones o preguntas factuales a responder.
- El formato de salida esperado (JSON de `claims[]` o markdown auditable).

## Process

1. Para cada afirmación factual, localiza la(s) fuente(s) que la sustentan y captura `source_id`, `source_name`, `publication_date`.
2. Emite un objeto `claim` con `sources[]` no vacío. Si no hay fuente, no emitas el claim.
3. Si dos fuentes contradicen un dato, registra ambas, fija `conflict=true` y `needs_human_review=true`, y escala vía Kata 16. No promedies ni elijas.
4. Valida estructuralmente: cada `claim` tiene `sources[]` con `source_id` existente.

## Output

Retorna `claims[]` tipados. Por cada claim: `claim`, `sources[]` (con `id`/`name`/`date` o `value`), `conflict`, y cuando aplique `needs_human_review`.
