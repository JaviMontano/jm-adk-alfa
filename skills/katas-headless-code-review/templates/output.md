<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review Output

## Summary

{summary}

## Workflow CI

```yaml
{workflow_yaml}
```

## Schema de anotaciones

```json
{annotations_schema}
```

## Validación y publicación

{post_annotations}

## Evidence

{evidence}

## Validation

- ¿`--output-format=json` presente? {check_json_format}
- ¿`out.json` valida contra el schema antes de publicar? {check_schema_validation}
- ¿Job falla ante JSON inválido (sin comentarios parciales)? {check_fail_on_invalid}
- ¿Cero parsing de prosa (sin grep/awk sobre la salida)? {check_no_prose}
- ¿Merge queda en el humano? {check_human_gate}

## Risks and Limits

{risks}
