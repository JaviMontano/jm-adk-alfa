<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Primary Prompt

## Objetivo

Diseñar el procesamiento masivo de una carga offline con la Message Batches API, aplicando el patrón correcto de la Kata 17.

## Inputs requeridos

- Volumen y naturaleza de la carga (número de requests, tipo de tarea).
- Confirmación de que es offline y tolerante a latencia.
- Estructura de `params` por request (model, max_tokens, messages, tools).
- Esquema de identificación de cada item para construir el `custom_id`.

## Proceso

1. Verifica elegibilidad: la carga debe ser offline y tolerante a latencia. Si requiere respuesta en tiempo real, NO uses Batch.
2. Construye el batch con una request por item, cada una con un `custom_id` único y su bloque `params`.
3. Lanza `client.messages.batches.create(requests=...)`.
4. Haz polling de `processing_status` con `retrieve(batch.id)` hasta que sea `ended`.
5. Recorre `results(batch.id)` y persiste cada resultado por su `custom_id`.
6. Ante fallos parciales, arma un sub-batch solo con las requests `failed` (por `custom_id`) y reintenta.

## Output

Devuelve el entregable en Markdown con summary, evidence, result, validation y risks. Incluye el bloque de código GOOD con el ciclo create → poll → results.
