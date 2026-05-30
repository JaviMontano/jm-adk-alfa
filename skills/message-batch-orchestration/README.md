<!--
generated-by: scripts/scaffold-skill.py
generated-for: message-batch-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# message-batch-orchestration

Capacidad de ingeniería para construir orquestadores de la **Message Batches API** de Anthropic: cargas masivas offline con ~50% de descuento, `custom_id` único por request para correlación, y fragmentación selectiva de fallos parciales (reintento solo de los `custom_id` fallidos).

## Resumen ejecutivo

Convierte un procesamiento síncrono one-by-one en un pipeline batch asíncrono: `create → poll processing_status → results → fragmentar`. Diseñado para clasificación masiva, enriquecimiento de datasets, backfills y evaluaciones latency-tolerant.

## Triggers

- message batch orchestration
- offline batch
- custom_id correlation
- partial failure retry

## Allowed Tools

- Read
- Grep
- Glob
- Bash

(Read-only-first; el Bash se usa para inspeccionar `scripts/batch/batch-runner.py` y ejecutar validaciones.)

## Quick Use

1. Modela cada item con `custom_id` estable (ID de negocio).
2. Crea el batch y haz polling de `processing_status` hasta `ended`.
3. Fragmenta resultados: persiste éxitos, reintenta solo los fallidos.
4. Valida contra el checklist de `SKILL.md`.

Referencia de implementación: `scripts/batch/batch-runner.py`. Skill relacionada: `katas-message-batch-processing`.

## Output Format

Markdown con resumen, evidencia, resultado, validación y riesgos.
