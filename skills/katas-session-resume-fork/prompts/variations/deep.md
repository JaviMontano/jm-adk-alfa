<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 25 · Variante profunda

Úsala cuando hay ambigüedad sobre el estado del proyecto, múltiples sesiones candidatas, o riesgo de arrastrar contexto stale a trabajo de alto impacto.

Incluye:

- **Discovery:** qué cambió entre sesiones (commits, deploys, migraciones, refactors) y qué tool results quedaron stale.
- **Opciones consideradas:** resume vs fork vs fresh, con el trade-off de cada una para este caso.
- **Enfoque elegido:** comando concreto y por qué descarta los otros dos.
- **Diseño del summary** (si es fresh): qué campos tipados se inyectan desde el scratchpad y qué fuentes se recargan.
- **Validación:** confirmación de que no se pega transcript crudo y de que el contexto reanudado refleja el estado actual.
- **Riesgos:** ramas que podrían mezclarse, fuentes que podrían seguir stale.
