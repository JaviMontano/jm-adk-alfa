<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Body of Knowledge

## Canon

La Message Batches API procesa miles de requests offline a aproximadamente 50% del costo del modo real-time. Es el patrón correcto para cargas no interactivas: auditorías, backfills, evaluaciones de regresión y extracciones estructuradas masivas.

### Conceptos clave

- **Batch:** colección de requests independientes. Cada una lleva un `custom_id` único y un bloque `params` equivalente a una llamada `messages.create`.
- **custom_id:** clave de correlación request↔response. Es la única forma de mapear cada resultado a su input. Duplicarlo produce ambigüedad irresoluble.
- **Ciclo de vida:** `create → poll processing_status → results`. El polling continúa hasta que `processing_status == "ended"`.
- **Éxitos parciales:** un batch puede terminar `ended` con algunas requests `succeeded` y otras `errored`. El fallo de una request no detiene a las demás.
- **Fragmentación selectiva:** ante fallos masivos, dividir en sub-batches y reintentar solo las requests `failed` (identificadas por `custom_id`), nunca el lote completo.
- **Elegibilidad:** la carga debe ser offline y tolerante a latencia. Si requiere respuesta en tiempo real, Batch no aplica.

## Quality Signals

| Señal | Objetivo |
|---|---|
| custom_id único | Cada request tiene un `custom_id` distinto; cero duplicados |
| Ciclo completo | El código implementa create, poll hasta `ended` y lectura de results |
| Aislamiento de fallos | Los fallos parciales se recuperan por sub-batch, no reprocesando todo |
| Elegibilidad | Solo se usa Batch para cargas offline tolerantes a latencia |
| Ahorro | Se aprovecha el ~50% de descuento frente al modo real-time |

## Anti-patrón canónico

```python
for item in ten_thousand_items:
    r = client.messages.create(**params(item))  # tarifa real-time
    save(r)                                       # sin custom_id, rompe rate limits
```

Procesar 10000 items uno por uno en modo real-time: paga el doble, rompe rate limits, no aísla fallos parciales y tarda horas.

## Quiz canónico (respuestas B·B·B)

- **P1:** ante 10000 tickets a procesar offline, usar la Message Batches API con un `custom_id` por ticket y polling del `processing_status`.
- **P2:** ante fallos parciales, armar un sub-batch solo con las requests `failed`, identificadas por su `custom_id`.
- **P3:** el `custom_id` es la única clave para mapear response a input; un duplicado introduce ambigüedad.
