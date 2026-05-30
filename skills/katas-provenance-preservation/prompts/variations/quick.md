<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Provenance Preservation Quick Variation

Úsala cuando hay pocas fuentes y bajo riesgo de conflicto.

Emite directamente `claims[]` con `sources[]` tipadas (`source_id`, `name`, `date`). Marca `conflict=true` solo si detectas contradicción. Devuelve el deliverable, el estado de validación estructural (cada claim tiene fuente) y los riesgos residuales.
