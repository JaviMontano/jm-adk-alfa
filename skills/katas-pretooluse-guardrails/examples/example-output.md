# Example Output

## Summary

La política de reembolso se mueve del `system_prompt` a una política externa recargable y un hook `PreToolUse`. El caso `amount=4500` retorna `permissionDecision: "deny"` antes de ejecutar `process_refund`; el caso `amount=800` queda permitido.

## Policy

```python
POLICY = {"max_refund_amount": 1000}
```

## PreToolUse Hook

```python
async def policy_gate(input, tool_use_id, ctx):
    if input["tool_name"] != "process_refund":
        return {}

    amount = input["tool_input"].get("amount", 0)
    if amount > POLICY["max_refund_amount"]:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"Refund amount {amount} exceeds policy limit "
                    f"{POLICY['max_refund_amount']}."
                ),
            }
        }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[policy_gate])]},
)
```

## Decision Matrix

| tool | input | expected decision | side-effects |
|---|---:|---|---|
| `process_refund` | `{"amount": 4500}` | `deny` | none |
| `process_refund` | `{"amount": 800}` | `allow` | expected |

## Validation

- `deny` se decide antes de la tool, por lo que `process_refund` no ejecuta para 4500.
- `allow` conserva la ruta válida para 800.
- Un prompt injection no cambia la decisión porque la política no vive en el prompt.

## Risks And Limits

- El hook debe cubrir todas las tools con side-effects relevantes.
- Si la política se lee desde JSON, el reporte debe probar recarga o snapshot de versión.
