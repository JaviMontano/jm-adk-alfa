# message-batch-orchestration

Capacidad de ingeniería para construir orquestadores de la **Message Batches API** de Anthropic: cargas masivas offline, `custom_id` único por request para correlación, y fragmentación selectiva de fallos parciales (reintento solo de los `custom_id` fallidos).

## Resumen ejecutivo

Convierte un procesamiento síncrono one-by-one en un pipeline batch asíncrono: `create → poll processing_status → results → fragmentar`. Diseñado para clasificación masiva, enriquecimiento de datasets, backfills y evaluaciones latency-tolerant.

## Contrato determinístico

El entregable certificable es un reporte JSON compatible con `assets/message-batch-orchestration-contract.json` y validable offline con `scripts/check.sh`.

Debe incluir:

- `workload`: prueba de que la carga es offline, latency-tolerant y no streaming.
- `request_modeling`: `custom_id` estable derivado del ID de negocio y validación de unicidad.
- `batch_lifecycle`: creación del batch, polling de `processing_status`, estado terminal `ended` y recuperación de resultados.
- `result_fragmentation`: separación de `succeeded` frente a `errored`, `expired` y `canceled`.
- `retry_policy`: reintento sólo de `custom_id` fallidos, con límite.
- `persistence`: persistencia idempotente de éxitos antes de cualquier retry.
- `validation` y `guardian`: flags verificables y decisión final.

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

(Read-only-first; el Bash se usa para ejecutar validaciones offline determinísticas.)

## Quick Use

1. Modela cada item con `custom_id` estable (ID de negocio).
2. Crea el batch y haz polling de `processing_status` hasta `ended`.
3. Fragmenta resultados: persiste éxitos, reintenta solo los fallidos.
4. Valida contra el checklist de `SKILL.md`.

Skill relacionada: `katas-message-batch-processing`.

## Output Format

Markdown o JSON con resumen, evidencia, resultado, validación y riesgos. Para validación offline usa el JSON contract en `assets/`.
