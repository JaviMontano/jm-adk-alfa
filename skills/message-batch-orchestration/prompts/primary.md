<!--
generated-by: scripts/scaffold-skill.py
generated-for: message-batch-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Message Batch Orchestration Primary Prompt

## Objetivo

Construir un orquestador de la Message Batches API para la carga offline descrita por el usuario, con `custom_id` único por request y fragmentación selectiva de fallos.

## Inputs requeridos

- Descripción del dataset / items a procesar y su ID de negocio.
- Confirmación de que la carga es offline / latency-tolerant.
- Modelo, `max_tokens` y prompt por item.
- Política de reintentos (máximo) y destino de persistencia de éxitos.

## Proceso

1. Modela cada item con `custom_id` único y estable (ID de negocio, no índice de loop); valida unicidad.
2. Ensambla los `requests` y crea el batch con `client.messages.batches.create`.
3. Haz polling de `processing_status` con backoff hasta `ended`.
4. Recorre `results()` indexando por `custom_id`; separa `succeeded` de `errored`/`expired`/`canceled`.
5. Persiste éxitos y construye el sub-lote de reintento solo con los `custom_id` fallidos; aplica el límite.

## Output

Markdown con: resumen, código del orquestador (EN), evidencia (referencias a `scripts/batch/batch-runner.py`), validación contra el checklist y riesgos residuales.
