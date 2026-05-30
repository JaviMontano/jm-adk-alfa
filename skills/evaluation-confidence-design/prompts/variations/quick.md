<!--
generated-by: scripts/scaffold-skill.py
generated-for: evaluation-confidence-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Evaluation Confidence Design Quick Variation

Úsala cuando ya existe labeled set etiquetado por `document_type` y categoría, y solo falta fijar el corte.

1. Calibra la confidence cruda contra el labeled set (binning sobre la precisión observada).
2. Fija el umbral sobre la confidence **calibrada**.
3. Reporta accuracy y FP rate **por categoría** y marca las que excedan el límite para disable temporal.

Devuelve: umbral calibrado, tabla FP por categoría, categorías desactivadas y riesgos residuales.
