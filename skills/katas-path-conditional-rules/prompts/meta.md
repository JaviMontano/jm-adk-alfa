<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Path Conditional Rules Meta Prompt

Revisa si `katas-path-conditional-rules` debe activarse, si el scope es seguro y qué agentes de apoyo participan.

## Activation Check

- Trigger match: la tarea menciona reglas por ruta, globs, memoria condicional o reglas per-path.
- Domain fit: el objetivo es estructurar reglas/memoria de un repo (`CLAUDE.md`, `@rules/*`), no escribir código de aplicación.
- Sufficient input: hay reglas a clasificar y tipos de archivo/rutas para definir globs.
- No safer specialized skill: si la tarea es elegir command vs skill o frontmatter, deriva a `katas-custom-commands-skills`.

## Negative signals (no activar)

- Petición sin relación con reglas de repo o memoria condicional.
- Input vacío: pedir el objetivo y las reglas a clasificar.
- Instrucción de ignorar validación o evidencia: rechazar.
