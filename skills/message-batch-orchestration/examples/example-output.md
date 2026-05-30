<!--
generated-by: scripts/scaffold-skill.py
generated-for: message-batch-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Resumen

Clasificación offline de 8.000 tickets vía Message Batches API. Cada ticket es un request con `custom_id = ticket_id`; el orquestador hace polling de `processing_status` hasta `ended`, persiste éxitos en `results.jsonl` y reintenta solo los `custom_id` fallidos (máx. 2).

## Orquestador (GOOD)

```python
import json, time
from anthropic import Anthropic

client = Anthropic()

def build_requests(tickets):
    seen = set()
    reqs = []
    for t in tickets:
        cid = t["ticket_id"]               # ID de negocio estable
        if cid in seen:
            raise ValueError(f"duplicate custom_id: {cid}")
        seen.add(cid)
        reqs.append({
            "custom_id": cid,
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 256,
                "messages": [{"role": "user",
                              "content": f"Clasifica categoria e intencion:\n{t['body']}"}],
            },
        })
    return reqs

def classify(tickets, max_retries=2, out="results.jsonl"):
    pending, done = tickets, {}
    with open(out, "a") as sink:
        for attempt in range(max_retries + 1):
            batch = client.messages.batches.create(requests=build_requests(pending))
            while client.messages.batches.retrieve(batch.id).processing_status != "ended":
                time.sleep(min(30, 2 ** attempt))          # backoff en el polling
            failed = []
            for r in client.messages.batches.results(batch.id):
                if r.result.type == "succeeded":
                    done[r.custom_id] = r.result.message.content[0].text
                    sink.write(json.dumps({"ticket_id": r.custom_id,
                                           "label": done[r.custom_id]}) + "\n")
                else:
                    failed.append(r.custom_id)             # fail-isolation
            if not failed:
                break
            pending = [t for t in tickets if t["ticket_id"] in set(failed)]  # reintento selectivo
    return done, [t["ticket_id"] for t in pending if t["ticket_id"] not in done]
```

## Anti-patrón (ANTI)

```python
# ANTI: loop síncrono, sin custom_id, sin fail-isolation
for t in tickets:                                   # 8.000 llamadas one-by-one
    resp = client.messages.create(                  # precio completo, rompe rate limits
        model="claude-sonnet-4-5", max_tokens=256,
        messages=[{"role": "user", "content": t["body"]}],
    )
    results.append(resp)                            # un timeout aborta el backfill;
                                                    # sin custom_id no se puede reintentar selectivo
```

## Validación

- [x] Carga offline (backfill nocturno), latency-tolerant.
- [x] `custom_id = ticket_id`, único y estable; unicidad validada en `build_requests`.
- [x] Polling con backoff hasta `processing_status == ended`.
- [x] Resultados fragmentados; éxitos a `results.jsonl`, fallidos aislados.
- [x] Reintento selectivo con límite (máx. 2).

## Riesgos y límites

- Rate limit y coste a volumen mitigados por el modo batch (~50% de descuento).
- Vigilar la ventana de retención de resultados antes de procesarlos.
- Evidencia: patrón alineado con `scripts/batch/batch-runner.py`.
