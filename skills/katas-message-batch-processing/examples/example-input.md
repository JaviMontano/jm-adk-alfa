<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Tenemos un backlog de 10000 tickets de soporte que hay que clasificar y resumir de forma offline esta noche para una auditoría. No necesitamos respuesta en tiempo real y el costo importa. Cada ticket tiene un `ticket_id`.

Diseña cómo procesar esta carga con la Message Batches API: cómo construir el batch, cómo correlacionar cada resultado con su ticket y qué hacer si parte del lote falla.

## Escenario ANTI a evitar

El equipo propuso un script que hace:

```python
for ticket in tickets:
    r = client.messages.create(**params(ticket))
    save(r)
```

Es decir, procesar los 10000 tickets uno por uno en modo real-time. Explica por qué esto está mal y cuál es el patrón correcto.
