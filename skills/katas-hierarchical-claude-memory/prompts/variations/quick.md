<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hierarchical Claude Memory · Variación Quick

Usar cuando la decisión es de bajo riesgo y está bien especificada (p. ej. "¿dónde colocó esta única convención?").

- Clasificar la convención por nivel: personal → home, equipo → repo, local → módulo.
- Si va en el repo y es larga, sugerir `@import` a `docs/`.
- Devolver solo la ubicación recomendada, el bloque `CLAUDE.md` resultante y los riesgos residuales.
