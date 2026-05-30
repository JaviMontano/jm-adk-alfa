<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Provenance Preservation Deep Variation

Úsala cuando se agregan muchas fuentes vía subagentes paralelos (Kata 4), hay alto riesgo de conflicto o el resultado debe ser auditable para decisión humana.

Incluye:

- Notas de descubrimiento: inventario de fuentes con `source_id`, `name`, `date`.
- Contrato de agregación: cómo cada subagente devuelve claims ya con fuente, y cómo el agregador rechaza claims huérfanos.
- Tabla de conflictos: cada dato contradicho con ambas posturas, `conflict=true`, `needs_human_review=true` y ruta de escalado (Kata 16).
- Verificación numérica adyacente (Kata 15) cuando los claims son cifras.
- Test estructural ejecutado y validación de que cada claim tiene `sources[]` con `source_id` existente.
- Riesgos y límites.
