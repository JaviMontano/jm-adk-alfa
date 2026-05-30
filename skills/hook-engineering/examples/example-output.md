<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El limite de 10000 USD se hace cumplir con un PreToolUse que lee la politica desde un JSON
recargable y devuelve `permissionDecision: deny` antes de ejecutar `transfer_funds`. El
limite se edita en el JSON sin redeployar.

## Result

### GOOD

```python
import json
from pathlib import Path
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

POLICY = Path("references/guardrails/tool-policy.json")

async def transfer_guard(input_data, tool_use_id, context):
    if input_data["tool_name"] != "transfer_funds":
        return {}
    policy = json.loads(POLICY.read_text())  # hot-reload por invocacion
    limit = policy["transfer_funds"]["max_amount"]
    amount = input_data.get("tool_input", {}).get("amount", 0)
    if amount > limit:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"amount {amount} exceeds limit {limit}",
            }
        }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[transfer_guard])]},
)
```

### ANTI

```python
# El limite vive en el prompt: una inyeccion ("ignore previous limits") lo desactiva
# y la transferencia se ejecuta igual. Sin enforcement de runtime, sin auditoria.
SYSTEM_PROMPT = "Reject any transfer above 10000 USD."
```

## Validation

- La politica vive en `tool-policy.json` recargable, no en el prompt.
- El deny ocurre antes de ejecutar la transferencia (cero side-effects).
- La razon del deny queda trazada y es auditable.
- El limite se edita sin redeployar el agente.
