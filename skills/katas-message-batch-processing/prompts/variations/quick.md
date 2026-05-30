<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Quick Variation

Úsala cuando la carga es claramente offline, el `params` por request está definido y solo hace falta el código del batch.

Devuelve el snippet GOOD del ciclo `create → poll processing_status → results` con `custom_id` único por request, más una nota de validación (sin duplicados de `custom_id`) y los riesgos residuales.
