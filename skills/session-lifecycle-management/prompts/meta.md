<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management Meta Prompt

Decide si `session-lifecycle-management` debe activarse, si el alcance es seguro, y qué agentes de apoyo participan.

## Activation Check

- **Trigger match:** la petición habla de resume vs fork, summary tipado, contexto stale o continuidad de sesión.
- **Domain fit:** el problema es decidir cómo transicionar una sesión de agente, no ejecutar la tarea de negocio en sí.
- **Sufficient input:** existe un `SessionContext` previo o al menos un objetivo y el estado actual del mundo.
- **No safer specialized skill:** no hay una skill más específica (p. ej. governance de workspace) que aplique mejor.

## Agent Routing

- `lead`: modela el contexto, implementa la decisión y el summary.
- `support`: caza dependencias stale y estado compartido entre forks.
- `guardian`: corre el checklist y bloquea el anti-patrón de resume ciego.
- `specialist`: mapea las transiciones a primitivas del SDK / Claude Code.

## Safety

Ante duda entre `resume` y `fresh`, prefiere `fresh` con `TypedSummary`: reusar contexto stale es más caro que sintetizar de más.
