<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop Output

## Summary

{summary}

## Evidence

{evidence}

## Result

```python
# Bucle determinista: control por stop_reason
{result}
```

## Validation

- [ ] El halt depende de `stop_reason`, no de prosa del modelo.
- [ ] `tool_use` despacha y reinyecta `tool_result` como `role=user`.
- [ ] `end_turn` finaliza el bucle.
- [ ] Todo `stop_reason` no manejado eleva error explícito.
- [ ] Budget configurable presente; eleva `BudgetExceeded`.

{validation}

## Risks and Limits

{risks}
