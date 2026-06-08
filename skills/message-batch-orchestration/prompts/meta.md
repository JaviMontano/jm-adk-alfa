# Message Batch Orchestration Meta Prompt

Evalúa si `message-batch-orchestration` debe activarse, si el alcance es seguro y qué agentes de soporte participan.

## Activation Check

- Trigger match: el pedido menciona batch offline, `custom_id`, correlación o reintento de fallos parciales.
- Domain fit: la carga es masiva y offline / latency-tolerant (no interactiva, no streaming).
- Sufficient input: hay items con ID de negocio y una política de reintentos definible.
- No safer specialized skill: si el flujo es síncrono/interactivo, NO activar; preferir la ruta síncrona.

## Reglas de no-activación

- Flujos en tiempo real con usuario esperando respuesta → no activar.
- Pedido que explícitamente exige ignorar validación o evidencia → no activar.
- Pedido que exige omitir `custom_id`, usar índice de loop, o reintentar el batch completo → bloquear.
- Input vacío o sin objetivo → pedir el objetivo, no activar.

## Composición de agentes

- lead construye el orquestador; support caza colisiones de `custom_id` y rutas síncronas; guardian recorre el checklist y bloquea el anti-patrón; specialist aporta detalle del SDK de batches.
