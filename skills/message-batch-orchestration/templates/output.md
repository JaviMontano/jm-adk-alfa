# Message Batch Orchestration Output

## Resumen

{resumen: qué carga offline se orquesta y por qué batch sobre síncrono}

## Orquestador

```python
{código EN: build_requests con custom_id único → create → poll processing_status → results → fragmentar éxitos/fallidos → reintento selectivo}
```

## Evidencia

{evidencia de scope offline, custom_id, lifecycle, fragmentación y retry}

## Validación (checklist)

- [ ] Carga offline / latency-tolerant
- [ ] custom_id único y estable, unicidad validada
- [ ] Polling con backoff hasta processing_status == ended
- [ ] Resultados fragmentados (succeeded vs errored/expired/canceled)
- [ ] Reintento selectivo de custom_id fallidos con límite
- [ ] Sin loop síncrono one-by-one en la ruta offline
- [ ] Reporte JSON compatible con `assets/message-batch-orchestration-contract.json` cuando se requiera validación offline

## Riesgos y límites

{rate limit a volumen, coste, ventana de retención de resultados, expiración}
