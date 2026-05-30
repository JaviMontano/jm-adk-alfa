<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Code review headless en GitHub Actions: `claude -p` corre sin TTY, emite JSON validado contra schema y publica anotaciones deterministas. JSON inválido => job falla. El humano aprueba el merge.

## Patrón correcto (GOOD)

`annotations.schema.json`:

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["file", "line", "severity", "rule_id", "message"],
    "properties": {
      "file": { "type": "string" },
      "line": { "type": "integer" },
      "severity": { "type": "string", "enum": ["error", "warning", "info"] },
      "rule_id": { "type": "string" },
      "message": { "type": "string" }
    }
  }
}
```

`.github/workflows/review.yml`:

```yaml
- name: LLM review
  run: |
    claude -p "$REVIEW_PROMPT" \
      --output-format=json \
      --schema annotations.schema.json > out.json
    python scripts/post_annotations.py out.json
```

`scripts/post_annotations.py` valida `out.json` contra el schema; si no valida, sale con código distinto de cero y el job falla antes de publicar nada.

## Anti-patrón (ANTI)

```bash
claude -p "$REVIEW_PROMPT" > review.txt
grep -E 'ERROR|WARNING|issue' review.txt | awk '{...}' | xargs gh pr comment
```

Parsea prosa: se rompe en cuanto el modelo cambie de redacción o idioma.

## Validation

- `--output-format=json` presente: sí.
- `out.json` valida contra `annotations.schema.json` antes de publicar: sí.
- Job falla ante JSON inválido, sin comentarios parciales: sí; el humano investiga.
- Cero parsing de prosa: sí.
- Merge queda en el humano (el LLM puede tener FP/FN y no asume responsabilidad del merge): sí.
