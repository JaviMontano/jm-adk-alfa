---
name: katas-message-batch-processing
version: 1.0.0
description: "Procesamiento masivo con Message Batches API, custom_id unico por request y fragmentacion selectiva de fallos parciales."
owner: "JM Labs"
triggers:
  - message batches
  - batch processing
  - custom_id
  - offline batch
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 17 · Procesamiento Masivo con Message Batches API

## Qué es

Para cargas no interactivas (auditorías, backfills, evaluaciones de regresión, extracciones estructuradas masivas), la Message Batches API procesa miles de requests offline a aproximadamente 50% del costo del modo real-time. Cada request lleva un `custom_id` único que correlaciona request con response y aísla los fallos parciales: si una request falla, las demás siguen su curso y se identifican exactamente cuáles reprocesar.

Escenarios objetivo: CI/CD Automation y Structured Extraction.

## Por qué importa (falla que evita)

Pagar tarifa real-time por trabajo offline es desperdicio puro. Y procesar 10000 prompts uno por uno con un `for` rompe los rate limits, no maneja fallos parciales y tarda horas. El batch es el patrón correcto: 50% de ahorro, aislamiento de fallos por request y escalabilidad real. Sin `custom_id`, un fallo parcial obliga a reprocesar todo el lote y no hay forma fiable de mapear cada response a su input.

## Modelo mental

- Un batch es una colección de requests independientes, cada una con un `custom_id` único.
- Ciclo de vida: `create → poll processing_status → results`.
- El batch puede terminar en estado `ended` con éxitos parciales (algunas requests `succeeded`, otras `errored`).
- `custom_id` es la única clave para mapear response a input; duplicarlo introduce ambigüedad irresoluble.
- Para fallos masivos: fragmentar en sub-batches y reintentar solo las requests `failed` (identificadas por su `custom_id`), nunca todo el batch.
- Elegibilidad: la carga debe ser offline y tolerante a latencia (resultados en minutos/horas, no en tiempo real).

## Patrón correcto

```python
batch = client.messages.batches.create(
    requests=[
        {"custom_id": f"audit-{i}", "params": {...}}
        for i, _ in enumerate(items)
    ]
)
while batch.processing_status != "ended":
    sleep(30)
    batch = client.messages.batches.retrieve(batch.id)
for r in client.messages.batches.results(batch.id):
    save(r.custom_id, r.result)
```

## Anti-patrón

```python
for item in ten_thousand_items:
    r = client.messages.create(**params(item))  # tarifa real-time
    save(r)                                       # sin custom_id, rompe rate limits
```

Procesa cada item en modo real-time, paga el doble, no aísla fallos parciales y se estrella contra los rate limits.

## Argumento de certificación

- Identificar qué cargas son elegibles para Batch (offline, tolerantes a latencia).
- Describir el ciclo `create → poll → results`.
- Justificar la importancia del `custom_id` como clave de correlación request↔response.
- Explicar la fragmentación selectiva: reintentar solo las requests `failed` para recuperar fallos parciales sin reprocesar el lote completo.

## Cuándo activar

- El usuario habla de procesar miles de prompts, backfills, auditorías masivas o evaluaciones offline.
- Aparecen términos como `message batches`, `batch processing`, `custom_id`, `offline batch`.
- El trabajo no requiere respuesta interactiva en tiempo real y el costo importa.

## Skills relacionadas

- `katas-multipass-prompt-chaining`
- `katas-validation-retry-feedback`
- `katas-confidence-stratified-sampling`
