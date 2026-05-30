<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Plan Mode Exploration Meta Prompt

Evalúa si `katas-plan-mode-exploration` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿La tarea implica operar sobre un repo desconocido o crítico antes de mutarlo?
- ¿Se requiere exploración + propuesta de arquitectura previa a la escritura?
- ¿Existe un mecanismo de aprobación humana del plan?
- ¿Hay intención explícita de barrera dura contra escritura accidental?

## No activar cuando

- La tarea es solo lectura sin intención de escribir después.
- El repo ya es conocido y el cambio es trivial y reversible.
- La petición contradice el contrato (p. ej. pide ignorar la aprobación o saltarse la validación) -> no activar.
- Input vacío -> pedir el objetivo, no activar.
