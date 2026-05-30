<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Builtin Tool Selection Meta Prompt

Decide si `katas-builtin-tool-selection` debe activarse, si el scope es seguro y qué agentes de soporte participan.

## Activation Check

- Trigger match: el pedido menciona seleccionar built-in tools, estrategia `Grep`/`Read`/`Edit`, anchors de `Edit` o exploración de codebase.
- Domain fit: la tarea es elegir entre `Grep`, `Glob`, `Read`, `Edit`, `Write`, `Bash` o corregir un plan que carga todo el repo.
- Sufficient input: hay un objetivo concreto y un codebase/archivos de referencia.
- No safer specialized skill: si la tarea es Plan Mode o skills/commands, derivar a `katas-plan-mode-exploration` o `katas-custom-commands-skills`.

## No activar cuando

- El pedido no toca selección de tools ni exploración de codebase.
- El input está vacío o no hay objetivo accionable.
