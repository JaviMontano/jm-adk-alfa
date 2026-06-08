# Message Batch Orchestration Quick Variation

Úsala cuando el caso es estándar y bien especificado: dataset claro con ID de negocio, modelo fijo, política de reintentos simple.

Devuelve solo:

- El orquestador mínimo (`create → poll processing_status → results → fragmentar`) con `custom_id` único.
- El reintento selectivo de los `custom_id` fallidos.
- Persistencia idempotente de éxitos antes de retry.
- Estado de validación contra el checklist y riesgos residuales.
