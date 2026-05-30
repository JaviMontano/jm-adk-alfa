<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review

Code review headless con `claude -p --output-format=json` validado contra un schema declarado de anotaciones por línea (`file,line,severity,rule_id,message`). El pipeline publica comentarios deterministas en el PR; si el JSON no valida, el job falla. El LLM anota, el humano sigue siendo el gate final de merge.

## Triggers

- headless code review
- claude p json
- output format json
- ci annotations

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Aplica esta skill cuando se necesita correr code review LLM en CI/CD sin TTY y publicar anotaciones estructuradas en un PR. Genera la invocación `claude -p ... --output-format=json --schema annotations.schema.json`, valida la salida contra el schema y publica solo si valida. Nunca parsees la prosa del modelo con `grep`/`awk`.

## Output Format

Markdown con summary, evidence, result, validation y risks: incluye el snippet del workflow, el schema de anotaciones y la justificación de por qué el humano sigue siendo gate de merge.
