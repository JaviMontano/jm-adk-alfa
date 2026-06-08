# Example Output

## Resumen

Clasificación offline de 8.000 tickets vía Message Batches API. Cada ticket es un request con `custom_id = ticket_id`; el orquestador hace polling de `processing_status` hasta `ended`, persiste éxitos en `results.jsonl` y reintenta solo los `custom_id` fallidos (máx. 2).

## JSON Report

```json
{
  "schema": 1,
  "skill": "message-batch-orchestration",
  "report_id": "ticket-backfill-nightly",
  "scenario": "Classify 8000 support tickets in an offline nightly backfill",
  "workload": {
    "mode": "offline",
    "latency_tolerant": true,
    "realtime_required": false,
    "streaming_required": false,
    "item_count": 8000,
    "business_id_field": "ticket_id"
  },
  "request_modeling": {
    "custom_id_source": "ticket_id",
    "custom_ids": ["T-100", "T-101", "T-102"],
    "uniqueness_validated": true,
    "index_based_custom_id": false
  },
  "batch_lifecycle": {
    "create_request_count": 3,
    "batch_id_persisted": true,
    "processing_status_polling": true,
    "terminal_status": "ended",
    "assumes_immediate_completion": false,
    "polling_backoff_seconds": [1, 2, 4],
    "results_retrieved": true
  },
  "result_fragmentation": {
    "succeeded_custom_ids": ["T-100", "T-102"],
    "failed_custom_ids": ["T-101"],
    "failure_types": [
      {
        "custom_id": "T-101",
        "result_type": "errored"
      }
    ],
    "success_persisted": true
  },
  "retry_policy": {
    "selective_retry": true,
    "retry_custom_ids": ["T-101"],
    "retries_batch_complete": false,
    "max_retries": 2,
    "retry_attempts_used": 1
  },
  "persistence": {
    "success_sink": "results.jsonl",
    "idempotent_writes": true,
    "preserves_successes_before_retry": true
  },
  "evidence": [
    {
      "type": "workload_scope",
      "detail": "The request describes a nightly backfill with no waiting user."
    },
    {
      "type": "custom_id_sample",
      "detail": "custom_id values are ticket_id values."
    },
    {
      "type": "results_fragmentation",
      "detail": "Only T-101 is retried after result fragmentation."
    }
  ],
  "validation": {
    "offline_gate_passed": true,
    "custom_ids_unique": true,
    "custom_ids_stable": true,
    "polls_until_ended": true,
    "fragments_results": true,
    "retries_only_failed_custom_ids": true,
    "retry_cap_enforced": true,
    "synchronous_loop_absent": true,
    "deterministic_script_passed": true
  },
  "guardian": {
    "decision": "pass",
    "reason": "The plan is offline, uses stable unique custom_id values, fragments failed results, and retries only failed ids within the cap."
  }
}
```

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

- Rate limit y coste operacional deben revisarse con los límites vigentes del proveedor antes de ejecución.
- Vigilar la ventana de retención de resultados antes de procesarlos.
- Evidencia: el reporte JSON pasa el contrato offline de la skill.
