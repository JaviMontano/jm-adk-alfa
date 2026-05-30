<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Provenance Engineering Quick Variation

Úsala cuando el pipeline es pequeño y bien especificado: pocas fuentes, atributos claros, política de conflicto ya acordada (marcar y escalar).

Entrega solo:

- El tipo `Claim` con `source[]` no vacío y `as_of`, inválido por construcción si falta source.
- La fusión que marca `conflict=true` conservando todas las fuentes.
- El test estructural que falla ante un claim sin source.
- Estado de validación (checklist) y riesgos residuales.

No promedies conflictos ni elijas una fuente en silencio, incluso en la variante rápida.
