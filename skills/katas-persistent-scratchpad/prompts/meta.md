<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-persistent-scratchpad
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Persistent Scratchpad Meta Prompt

Decide si `katas-persistent-scratchpad` debe activarse: ¿la tarea es una investigación larga o multisesión cuyo detalle no puede perderse al compactar?

## Activation Check

- Coincide un trigger (`persistent scratchpad`, `investigation scratchpad`, `durable memory`, `scratchpad file`).
- El problema involucra memoria durable que debe sobrevivir a `/compact` o a reinicios.
- Hay un objetivo de investigación concreto (no input vacío).
- No aplica mejor otra skill (p. ej. compactación pura → `katas-compaction-boundary`; flujo de investigación → `katas-adaptive-investigation`).

## No activar cuando

- Input vacío o fuera de dominio.
- La instrucción pide explícitamente ignorar validación/evidencia (contradice el principio de curar solo conclusiones validadas).
