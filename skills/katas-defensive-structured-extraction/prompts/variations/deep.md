<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction Deep Variation

Úsala cuando la fuente es ambigua, hay muchos opcionales, o el dominio de los enums no está cerrado.

Incluye: análisis campo por campo de qué es realmente `required` vs nullable; diseño de cada enum con su válvula de escape (`'other'`/`'unclear'`) y campo `details`; justificación de por qué cada opcional es union nullable; decisión explícita sobre si forzar `tool_choice` o no (descartar si el modelo debe elegir entre tools o responder híbrido); y validación final de que no hay defaults `''` ni valores fuera de dominio.
