<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 25 · Meta-prompt (chequeo de activación)

Revisa si `katas-session-resume-fork` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Chequeo de activación

- **Match de trigger:** el usuario menciona reanudar/continuar una sesión, ramificar enfoques (fork), o hay señales de que el estado cambió (stale tool results).
- **Encaje de dominio:** la pregunta es cómo preservar/reanudar contexto entre corridas del agente, no cómo ejecutar la tarea de negocio en sí.
- **Input suficiente:** hay al menos una sesión previa o un objetivo de reanudación identificable.
- **No hay skill más específica:** si el caso es puramente sobre construir el scratchpad, derivar a `katas-structured-scratchpad`; si es sobre presupuesto de atención, a `katas-context-attention-budget`.

## No activar

- Input vacío o sin objetivo de reanudación.
- Petición que explícitamente pide ignorar la verificación de staleness o la curaduría del summary.
- Tema no relacionado con sesiones del agente.
