# Message Batch Orchestration Body of Knowledge

## Canon de la capacidad

La **Message Batches API** de Anthropic procesa cargas masivas en modo asíncrono offline. El orquestador correcto descompone el trabajo en requests independientes, cada uno con un `custom_id` único, y recorre el ciclo de vida `create → poll processing_status → results → fragmentar`.

### Conceptos clave

- **Message Batches API:** endpoint asíncrono para procesamiento offline y latency-tolerant.
- **custom_id único:** etiqueta estable por request, derivada del ID de negocio (no de un índice de loop), que permite correlacionar input↔output, deduplicar y reintentar.
- **processing_status:** estado del batch (`in_progress` → `ended`); el orquestador hace polling con backoff hasta `ended`, nunca asume finalización inmediata.
- **Fragmentación selectiva de fallos:** al recibir resultados, se separan `succeeded` de `errored`/`expired`/`canceled`; solo los `custom_id` fallidos forman el sub-lote de reintento (fail-isolation).
- **Reintento selectivo con límite:** se reprocesan únicamente los items fallidos, con un tope de reintentos, preservando los éxitos ya persistidos.

## Contrato de resultado

| Sección | Objetivo |
|---|---|
| `workload` | Demostrar que el caso es offline y no streaming |
| `request_modeling` | Probar `custom_id` estable, único y no basado en índice de loop |
| `batch_lifecycle` | Probar create, polling hasta `ended` y recuperación de resultados |
| `result_fragmentation` | Separar éxitos de `errored`/`expired`/`canceled` |
| `retry_policy` | Reintentar sólo fallidos con cap de 1-3 |
| `persistence` | Preservar éxitos antes del retry para evitar duplicados |

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Idoneidad offline | La carga es latency-tolerant y justifica el modo batch |
| Unicidad de custom_id | Cada request tiene `custom_id` único y estable, validado antes de enviar |
| Polling robusto | Backoff + timeout, espera a `processing_status == ended` |
| Fail-isolation | Resultados fragmentados; reintento solo de `custom_id` fallidos |
| Evidencia | Claims anclados al reporte JSON o marcados como supuestos |
| Update-safety | Trabajo manual existente preservado; cambios aditivos |
| Script offline | `scripts/check.sh` acepta fixtures válidos y rechaza mutaciones inválidas |

## Decisión de diseño

Elegir batch frente a síncrono cuando: (1) no hay un usuario esperando la respuesta en línea, (2) el volumen requiere throughput asíncrono, y (3) se necesita aislamiento de fallos parciales. Si cualquiera de las tres falla, considerar la ruta síncrona o streaming.

## Anti-patrón

Loop síncrono real-time (`client.messages.create` uno por uno) sin `custom_id` y sin fail-isolation: rompe rate limits a volumen, paga precio completo, y un único fallo aborta o invalida el lote completo sin posibilidad de reintento selectivo.

## Conocimiento abierto

- Añadir referencias específicas del proyecto a medida que se estabilicen.
