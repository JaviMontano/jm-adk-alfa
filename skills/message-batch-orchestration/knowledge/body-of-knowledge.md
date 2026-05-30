<!--
generated-by: scripts/scaffold-skill.py
generated-for: message-batch-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Message Batch Orchestration Body of Knowledge

## Canon de la capacidad

La **Message Batches API** de Anthropic procesa cargas masivas en modo asíncrono offline, con un descuento aproximado del 50% frente al precio síncrono. El orquestador correcto descompone el trabajo en requests independientes, cada uno con un `custom_id` único, y recorre el ciclo de vida `create → poll processing_status → results → fragmentar`.

### Conceptos clave

- **Message Batches API:** endpoint asíncrono para procesamiento offline a coste reducido (~50%).
- **custom_id único:** etiqueta estable por request, derivada del ID de negocio (no de un índice de loop), que permite correlacionar input↔output, deduplicar y reintentar.
- **processing_status:** estado del batch (`in_progress` → `ended`); el orquestador hace polling con backoff hasta `ended`, nunca asume finalización inmediata.
- **Fragmentación selectiva de fallos:** al recibir resultados, se separan `succeeded` de `errored`/`expired`/`canceled`; solo los `custom_id` fallidos forman el sub-lote de reintento (fail-isolation).
- **Reintento selectivo con límite:** se reprocesan únicamente los items fallidos, con un tope de reintentos, preservando los éxitos ya persistidos.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Idoneidad offline | La carga es latency-tolerant y justifica el modo batch |
| Unicidad de custom_id | Cada request tiene `custom_id` único y estable, validado antes de enviar |
| Polling robusto | Backoff + timeout, espera a `processing_status == ended` |
| Fail-isolation | Resultados fragmentados; reintento solo de `custom_id` fallidos |
| Evidencia | Claims anclados a `scripts/batch/batch-runner.py` o marcados como supuestos |
| Update-safety | Trabajo manual existente preservado; cambios aditivos |

## Decisión de diseño

Elegir batch frente a síncrono cuando: (1) no hay un usuario esperando la respuesta en línea, (2) el volumen amortiza el descuento y el throughput asíncrono, y (3) se necesita aislamiento de fallos parciales. Si cualquiera de las tres falla, considerar la ruta síncrona o streaming.

## Anti-patrón

Loop síncrono real-time (`client.messages.create` uno por uno) sin `custom_id` y sin fail-isolation: rompe rate limits a volumen, paga precio completo, y un único fallo aborta o invalida el lote completo sin posibilidad de reintento selectivo.

## Conocimiento abierto

- Confirmar límites de tamaño de batch y ventana de retención de resultados vigentes en la documentación del SDK.
- Añadir referencias específicas del proyecto a medida que se estabilicen.
