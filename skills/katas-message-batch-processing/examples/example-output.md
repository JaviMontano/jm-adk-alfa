<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

La carga (10000 tickets, offline, tolerante a latencia, costo sensible) es elegible para la Message Batches API. Procesarla en batch ahorra aproximadamente 50% frente al modo real-time, aísla los fallos por request mediante `custom_id` y permite recuperación selectiva sin reprocesar todo el lote.

## Evidence

- Carga offline confirmada: la auditoría no requiere respuesta interactiva.
- Volumen: 10000 requests, muy por encima del umbral donde el `for` real-time rompe rate limits.
- Cada ticket tiene `ticket_id`, base natural para un `custom_id` único.

## Result (GOOD)

```python
batch = client.messages.batches.create(
    requests=[
        {"custom_id": f"audit-{t.ticket_id}", "params": params(t)}
        for t in tickets
    ]
)
while batch.processing_status != "ended":
    sleep(30)
    batch = client.messages.batches.retrieve(batch.id)

results = list(client.messages.batches.results(batch.id))
for r in results:
    save(r.custom_id, r.result)

# Recuperación de fallos parciales: sub-batch solo con los failed
failed = [r.custom_id for r in results if r.result.type == "errored"]
# reconstruir requests para esos custom_id y reintentar en un nuevo batch
```

## Anti-patrón rechazado (ANTI)

```python
for ticket in tickets:
    r = client.messages.create(**params(ticket))  # tarifa real-time
    save(r)                                         # sin custom_id, rompe rate limits
```

Paga el doble, no aísla fallos parciales, rompe rate limits y tarda horas.

## Validation

- `custom_id` único por ticket (`audit-{ticket_id}`), cero duplicados.
- Ciclo completo: create, polling hasta `ended`, lectura de results.
- Fallos parciales recuperados por sub-batch con solo las requests `errored`.

## Risks and Limits

- Si algún ticket dependiera de otro, las requests no serían independientes y el batch no aplicaría.
- El batch puede expirar; verificar la ventana de vigencia antes de un polling muy largo.
- La latencia de batch es de minutos a horas: válido solo porque la auditoría es offline.
