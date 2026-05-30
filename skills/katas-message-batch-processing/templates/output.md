<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Output

## Summary

{summary — qué carga offline se procesa y por qué Batch es el patrón correcto}

## Evidence

{evidence — elegibilidad confirmada (offline, latency-tolerant), volumen, ahorro estimado ~50%}

## Result

{result — bloque de código con el ciclo create -> poll processing_status -> results y custom_id unico por request}

## Validation

- custom_id único por request (cero duplicados).
- Ciclo completo: create, polling hasta `ended`, lectura de results.
- Fallos parciales recuperados por sub-batch (solo las requests `failed`).

## Risks and Limits

{risks — dependencias entre requests, expiración del batch, latencia tolerada}
