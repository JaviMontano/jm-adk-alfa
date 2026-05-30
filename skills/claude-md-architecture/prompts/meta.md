<!--
generated-by: scripts/scaffold-skill.py
generated-for: claude-md-architecture
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Claude Md Architecture Meta Prompt

Evalúa si `claude-md-architecture` debe activarse, si el alcance es seguro y qué agentes de soporte participan.

## Activation Check

- Coincidencia de trigger (memoria jerárquica, reglas por ruta, `@imports`).
- Encaje de dominio: el problema es estructurar `CLAUDE.md`, no editar una regla suelta.
- Input suficiente: hay acceso al árbol del repo y a las reglas vigentes.
- No hay una skill más específica y segura para el caso.

## Señales de no-activación

- La petición es ejecutar una tarea de negocio, no reorganizar memoria.
- Se pide explícitamente ignorar validación o precedencia (conflicto con el checklist).
- No hay un repo ni `CLAUDE.md` sobre el que operar.
