<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Context Window Engineering Meta Prompt

Decide si `context-window-engineering` debe activarse, si el alcance es seguro y qué agentes de soporte participan.

## Activation Check

- ¿La tarea toca el ensamblado del context / system prompt, prefix caching o dilución de contexto?
- ¿Hay datos por-turno cuyo lugar en el contexto haya que decidir?
- ¿Existe suficiente información (bloques actuales + reglas críticas)?
- ¿No hay una skill más específica y segura para el caso?

## Routing

- **lead:** construye el assembler estático-first / dinámico-last.
- **support:** caza valores por-turno escondidos en el prefijo y reglas enterradas.
- **guardian:** corre el checklist y bloquea el anti-patrón.
- **specialist:** mapea al mecanismo de caching del proveedor y diseña la compactación.
