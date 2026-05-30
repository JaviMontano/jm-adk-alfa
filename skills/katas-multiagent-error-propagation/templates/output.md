<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation Output

## Summary

{summary}

## Evidence

{evidence}

## Result

{result}

### Contrato de propagación (por subagente)

| Campo | Valor |
|---|---|
| failure_type | {failure_type} |
| attempted_query | {attempted_query} |
| partial_results | {partial_results} |
| suggested_alternatives | {suggested_alternatives} |
| retryable | {retryable} |

### Coverage gap annotation

{coverage_gap}

## Validation

- [ ] Access failure (timeout/permission) separado de valid empty (0 matches, `empty_valid:True`).
- [ ] Local recovery aplicado antes de propagar.
- [ ] Ningún fallo enmascarado como `{results:[]}`.
- [ ] Coverage gap anotado explícitamente en el synthesis.

{validation}

## Risks and Limits

{risks}
