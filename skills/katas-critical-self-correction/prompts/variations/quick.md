<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 15 · Variante rápida

Úsala cuando hay un único campo numérico claro (un total) y un epsilon obvio.

1. Extrae `stated`, recalcula `computed`.
2. `mismatch = abs(stated - computed) > epsilon`.
3. Devuelve `stated`, `computed`, `delta`, `mismatch`, `needs_human_review`.

Sin corregir en silencio. Si discrepan, `needs_human_review=true` y se escala.
