<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-pretooluse-guardrails
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

La regla "no reembolsos mayores a $1000" se mueve del `system_prompt` a un hook `PreToolUse`. El SDK bloquea `process_refund` antes de ejecutar cuando `amount` supera el umbral, así un cliente insistente o un prompt injection ya no puede romperla.

## Patrón correcto (GOOD)

```python
POLICY = {"max_amount": 1000.0}

async def policy_gate(input, tool_use_id, ctx):
    if input["tool_name"] == "process_refund":
        amount = input["tool_input"].get("amount", 0)
        if amount > POLICY["max_amount"]:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Refund {amount} exceeds policy limit {POLICY['max_amount']}"
                    ),
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[policy_gate])]},
)
```

## Anti-patrón descartado

```python
options = ClaudeAgentOptions(
    system_prompt="No apruebes reembolsos mayores a $1000.",
    # sin hooks: un prompt injection o un usuario insistente ejecuta el reembolso igual
)
```

## Argumento de certificación

Las políticas críticas (límites monetarios, dominios prohibidos, paths protegidos) viven en hooks `PreToolUse` con `permissionDecision` estructurado, no en system prompts. El `deny` corre ANTES de ejecutar la tool, garantizando cero side-effects; un `raise` correría DESPUÉS.

## Validation

- El reembolso de $4500 ahora retorna `deny` y `process_refund` no ejecuta.
- Un reembolso de $800 pasa con `{}` (sin bloqueo).
- La política se actualiza mutando `POLICY` o releyendo el JSON, sin reiniciar el agente.
