# Assets — message-batch-orchestration

Estos assets definen el contrato determinístico para certificar planes de Message Batches offline.

- `message-batch-orchestration-contract.json`: campos requeridos del reporte.
- `workload-policy.json`: criterios offline, latency-tolerant y no streaming.
- `custom-id-policy.json`: unicidad y estabilidad de `custom_id`.
- `lifecycle-policy.json`: ciclo `create → poll processing_status → results`.
- `retry-fragmentation-policy.json`: separación de resultados y retry selectivo.
- `evidence-policy.json`: evidencia mínima aceptada.

Los assets son usados por `scripts/validate_message_batch_orchestration.py`, `scripts/check.sh`, `evals/evals.json` y ejemplos.
