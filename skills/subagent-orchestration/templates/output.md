<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration Output

## Summary

{summary}

## Spoke design

| Spoke | Subtarea | Tools | Modelo |
|---|---|---|---|
| {spoke_id} | {subtask} | {tools} | {model} |

## Coordinator (GOOD pattern)

```python
{coordinator_code}
```

## Error contract

- failure_type: {failure_types}
- distingue access_failure vs valid_empty: {yes_no}
- local recovery antes de propagar: {recovery_policy}

## Result

{result}

## Validation

- Aislamiento estructural: {check}
- Blast radius acotado: {check}
- access_failure != valid_empty: {check}
- Coverage gap explícito: {check}
- Sin error swallowed como success vacío: {check}

## Risks and limits

{risks}
