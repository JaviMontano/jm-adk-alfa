<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Provenance Engineering Deep Variation

Úsala cuando el pipeline es complejo: muchas fuentes heterogéneas, claims derivados (sumas, joins, dedupe), extracción en subagentes/sesiones fork, y consecuencias altas de auditoría (KYC, due diligence).

Incluye:

- **Notas de discovery**: inventario de fuentes con tipo y fecha, atributos a consolidar, dónde puede perderse la provenance.
- **Opciones consideradas**: schema del `Claim` (dataclass frozen vs pydantic vs JSON schema), formato de la cola de conflictos, propagación de `source[]` en derivados.
- **Enfoque seleccionado**: invariante por construcción, marcado de conflicto, escalación a humano y test estructural como gate de CI.
- **Casos límite**: claim derivado que no hereda fuentes, conflicto de formato vs conflicto real, `as_of` heredada al fusionar.
- **Validación**: checklist completo y evidencia del test estructural en verde.
- **Riesgos**: normalización que esconde conflictos, fugas de claims sin source por rutas no testeadas.
