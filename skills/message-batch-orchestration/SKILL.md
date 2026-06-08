---
name: message-batch-orchestration
version: 1.0.0
description: "Orquestar Message Batches API para cargas offline con custom_id unico y fragmentacion selectiva de fallos parciales."
owner: "JM Labs"
triggers:
  - message batch orchestration
  - offline batch
  - custom_id correlation
  - partial failure retry
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Message Batch Orchestration

## Capacidad

Esta skill construye orquestadores de la **Message Batches API** de Anthropic para procesar cargas masivas en modo offline. El patrón asigna un `custom_id` único a cada request para correlacionar resultados, y aísla los fallos: cuando una fracción del lote falla, solo se reintentan esos `custom_id`, nunca el batch completo. El ciclo de vida es `create → poll processing_status → recuperar results → fragmentar selectivamente`.

## Cuándo usarla

- Cuando la carga es **offline / latency-tolerant** (clasificación masiva, enriquecimiento de datasets, evaluaciones, backfills) y no requiere respuesta en tiempo real.
- Cuando el volumen justifica procesamiento asíncrono y aislamiento de fallos frente a llamadas síncronas una por una.
- Cuando necesitas **reintento selectivo** de items fallidos sin reprocesar los que ya tuvieron éxito.
- NO usarla para flujos interactivos, streaming, o cualquier ruta donde el usuario espera la respuesta en línea.

## Cómo construir

1. **Modela la unidad de trabajo.** Define cada item como un request con `custom_id` único y estable (deriva del ID de negocio, no de un índice de loop) para poder correlacionar y deduplicar.
2. **Ensambla el batch.** Construye la lista de `requests`, valida unicidad de `custom_id` antes de enviar, y respeta los límites de tamaño del endpoint.
3. **Crea el batch** con `client.messages.batches.create(requests=...)` y persiste el `batch.id`.
4. **Haz polling de `processing_status`** con backoff hasta `ended`; nunca asumas finalización inmediata.
5. **Recupera los resultados** vía streaming de `results()`, indexando por `custom_id`.
6. **Fragmenta por resultado:** separa `succeeded` de `errored`/`expired`/`canceled`. Persiste éxitos; agrupa los fallidos por `custom_id` en un sub-lote de reintento.
7. **Reintenta solo los fallidos** creando un nuevo batch con los `custom_id` afectados, aplicando límite de reintentos.

## Contrato determinístico

Usa los assets de `assets/` para certificar planes de batch:

- `assets/message-batch-orchestration-contract.json`: campos JSON obligatorios del reporte.
- `assets/workload-policy.json`: criterios offline, latency-tolerant y no streaming.
- `assets/custom-id-policy.json`: unicidad y estabilidad de `custom_id`.
- `assets/lifecycle-policy.json`: lifecycle `create → poll processing_status → results`.
- `assets/retry-fragmentation-policy.json`: fragmentación y retry selectivo con cap.
- `assets/evidence-policy.json`: evidencia mínima aceptada.

Cuando el entregable sea JSON, valida offline con `scripts/validate_message_batch_orchestration.py`. Para la smoke determinística completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas.

## Patrón correcto

```python
# GOOD: batch offline con custom_id único + fragmentación selectiva de fallos
import time
from anthropic import Anthropic

client = Anthropic()

def build_requests(items):
    seen = set()
    requests = []
    for it in items:
        cid = it["id"]  # ID de negocio estable, no índice de loop
        if cid in seen:
            raise ValueError(f"duplicate custom_id: {cid}")
        seen.add(cid)
        requests.append({
            "custom_id": cid,
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": it["prompt"]}],
            },
        })
    return requests

def run_batch(items, max_retries=2):
    pending = items
    succeeded = {}
    for attempt in range(max_retries + 1):
        batch = client.messages.batches.create(requests=build_requests(pending))
        while True:
            status = client.messages.batches.retrieve(batch.id).processing_status
            if status == "ended":
                break
            time.sleep(min(30, 2 ** attempt))  # backoff en el polling

        failed = []
        for result in client.messages.batches.results(batch.id):
            if result.result.type == "succeeded":
                succeeded[result.custom_id] = result.result.message
            else:
                failed.append(result.custom_id)  # aísla solo el fallo

        if not failed:
            break
        pending = [it for it in items if it["id"] in set(failed)]  # reintento selectivo
    return succeeded, [it["id"] for it in pending if it["id"] not in succeeded]
```

## Anti-patrón

```python
# ANTI: loop síncrono real-time, sin custom_id, sin fail-isolation
for item in items:                          # llama uno por uno: caro y lento
    resp = client.messages.create(          # rompe rate limits a volumen
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": item["prompt"]}],
    )
    results.append(resp)                     # un fallo aborta todo el lote;
                                             # sin custom_id no hay reintento selectivo
```

## Checklist de validación

- ¿La carga es offline / latency-tolerant y justifica el modo batch?
- ¿Cada request tiene un `custom_id` único y estable derivado del ID de negocio?
- ¿Se valida la unicidad de `custom_id` antes de enviar?
- ¿El polling de `processing_status` usa backoff y espera el estado `ended`?
- ¿Los resultados se fragmentan en éxitos vs fallidos por `custom_id`?
- ¿El reintento es selectivo (solo fallidos) y tiene límite de reintentos?
- ¿No queda ningún loop síncrono one-by-one en la ruta offline?
- ¿El reporte pasa `scripts/check.sh` si se requiere evidencia offline?

## Katas y skills relacionadas

- Kata 17.
- Skill relacionada: `katas-message-batch-processing`.
