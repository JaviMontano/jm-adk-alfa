<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review Quick Variation

Usar cuando el pipeline y el schema ya existen y solo se necesita la invocación correcta.

Devuelve el step de CI listo:

```yaml
- run: |
    claude -p "$REVIEW_PROMPT" --output-format=json --schema annotations.schema.json > out.json
    python scripts/post_annotations.py out.json
```

Recuerda en una línea: JSON inválido => job falla; el humano aprueba el merge.
