<!--
generated-by: scripts/scaffold-skill.py
generated-for: claude-md-architecture
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Claude Md Architecture Deep Variation

Úsala cuando el `CLAUDE.md` es monolítico grande, hay muchos módulos o reglas contradictorias entre niveles.

Incluye: inventario completo de reglas con su clasificación, mapa de qué se mueve a dónde y por qué, opciones de precedencia consideradas (y la elegida), tratamiento de casos borde (módulos anidados, imports cíclicos, reglas en conflicto), validación contra el checklist y riesgos. Documenta la mecánica de `@imports` y el impacto en el cache KV.
