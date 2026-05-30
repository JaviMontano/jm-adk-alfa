<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction Quick Variation

Úsala cuando el schema es simple y la fuente está bien estructurada.

Define el tool con `required` reales, opcionales nullable y enums con `'other'`/`'unclear'`; llama con `tool_choice` forzado y devuelve solo el tool-use block conforme al schema, marcando los campos `null`/`unclear`.
