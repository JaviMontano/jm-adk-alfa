<!--
generated-by: scripts/scaffold-skill.py
generated-for: message-batch-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Message Batch Orchestration Deep Variation

Úsala cuando el lote es grande, de alto impacto, o cruza varios sistemas: reanudación de lotes largos, idempotencia estricta, presupuesto de coste, o múltiples destinos de persistencia.

Incluye:

- Notas de discovery: volumen, latency-tolerance, límites de tamaño del batch y ventana de retención de resultados.
- Estrategia de `custom_id` idempotente y de checkpoint para reanudar tras interrupciones.
- Manejo exhaustivo de estados: `in_progress`/`ended` y resultados `succeeded`/`errored`/`expired`/`canceled`.
- Política de reintentos con límite y backoff, y aislamiento de fallos por `custom_id`.
- Opciones consideradas (batch vs síncrono vs streaming), enfoque elegido, validación contra el checklist y riesgos (rate limit, coste, expiración de resultados).
