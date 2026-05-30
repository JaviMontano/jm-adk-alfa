<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Provenance Preservation Meta Prompt

Revisa si `katas-provenance-preservation` debe activarse, si el alcance es seguro y qué agentes de soporte participan.

## Activation Check

- ¿El output es un reporte factual derivado de múltiples fuentes y debe ser auditable?
- ¿Hay agregación tras subagentes paralelos (Kata 4) donde se pierde el "quién dijo qué"?
- ¿Existe riesgo de contradicción entre fuentes que deba marcarse en vez de resolverse en silencio?
- ¿La petición pide explícitamente prosa libre sin trazabilidad? Si es así y no se puede preservar provenance, NO activar.

## No activar cuando

- La petición es ajena al dominio (no involucra claims con fuentes).
- El input está vacío.
- Se pide explícitamente ignorar validación y evidencia (conflicto con el invariante de la kata).
