<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review Meta Prompt

Decide si `katas-headless-code-review` debe activarse y si el scope es seguro.

## Chequeo de activación

- ¿La tarea pide code review automatizado en CI/CD con `claude -p` (modo headless)?
- ¿Se necesita salida JSON estructurada validada contra schema para anotar un PR?
- ¿El objetivo es reemplazar parsing de prosa por un contrato declarado?
- ¿El input alcanza (repo, reglas, prompt, schema)?

## No activar si

- Es code review interactivo en local sin pipeline.
- El objetivo es aprobar o mergear automáticamente sin humano (viola el gate final de merge).
- La tarea es extracción genérica sin relación con CI/anotaciones de PR.
