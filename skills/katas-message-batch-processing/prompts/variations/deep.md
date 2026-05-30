<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Deep Variation

Úsala cuando el lote es grande, hay fallos parciales que recuperar o hay que diseñar la estrategia de fragmentación.

Incluye: análisis de elegibilidad (offline, latency-tolerant), diseño del esquema de `custom_id`, intervalo de polling justificado, manejo de estados por request (`succeeded`, `errored`, `expired`, `canceled`), lógica de sub-batches que reintenta solo las requests `failed`, estimación del ahorro frente a real-time, validación y riesgos.
