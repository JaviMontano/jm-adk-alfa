<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review Primary Prompt

## Objetivo

Montar un code review headless en CI/CD que corra `claude -p` sin TTY, emita JSON estructurado validado contra schema y publique anotaciones deterministas en el PR, con el humano como gate final de merge.

## Inputs requeridos

- Repo y plataforma de CI (p. ej. GitHub Actions).
- Reglas o convenciones de review (severities, `rule_id` esperados).
- Prompt de review (`$REVIEW_PROMPT`) y schema de anotaciones (`annotations.schema.json`).
- Definición de done: validación dura, fallo del job ante JSON inválido, gate humano de merge.

## Proceso

1. Construir la invocación: `claude -p "$REVIEW_PROMPT" --output-format=json --schema annotations.schema.json > out.json`.
2. Validar `out.json` contra el schema en `post_annotations.py`; si no valida, salir con error y fallar el job.
3. Publicar anotaciones `{file, line, severity, rule_id, message}` desde el JSON validado.
4. Nunca parsear la prosa del modelo con `grep`/`awk`/regex.
5. Dejar el merge en manos del humano.

## Output

Entrega en Markdown: snippet del workflow, schema de anotaciones, script de validación/publicación, y nota explícita de que el LLM anota y el humano aprueba.
