<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-confidence-stratified-sampling
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Un pipeline extrae `total` y `vendor` de facturas y recibos. Cada field trae `field_confidence` raw. Tenemos un labeled validation set de 240 ejemplos con truth labels. Hay que decidir qué documentos pueden ir a auto, cuáles a revisión humana y qué sampling de control ejecutar sin ocultar fallas de receipts en un promedio global.
