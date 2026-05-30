---
name: katas-pretooluse-guardrails
version: 1.0.0
description: "Guardarrailes deterministas en hook PreToolUse con permissionDecision deny desde politica recargable, no en el system prompt."
owner: "JM Labs"
triggers:
  - pretooluse guardrail
  - permission decision
  - policy gate
  - deterministic guardrail
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 02 · Guardarrailes deterministas con PreToolUse

## Qué es

Un hook `PreToolUse` registrado en `ClaudeAgentOptions.hooks` inspecciona `tool_name` y `tool_input` ANTES de que la tool se ejecute, y emite `permissionDecision: 'deny'` cuando una política externa (un `dict` o un JSON recargable) lo dicta. La política de negocio vive en código, no en el prompt, y el SDK garantiza que la tool denegada nunca corre.

Escenarios canónicos: Customer Support (reembolsos por encima de un umbral) y Financial Compliance (límites monetarios, dominios prohibidos, paths protegidos).

## Por qué importa (falla que evita)

Pedir en el `system_prompt` "no aprueben reembolsos mayores a $1000" es solo una sugerencia. Un prompt injection o un usuario insistente la rompe y la tool ejecuta el reembolso de todas formas. El guardarraíl en system prompt no es determinista: depende de que el modelo elija obedecer. El hook `PreToolUse` convierte esa intención en un control estructurado que el SDK aplica fuera del alcance del modelo.

## Modelo mental

- La política vive en código (un `dict` recargable o un JSON en disco), no en el prompt.
- El SDK garantiza que la tool NO corre si el hook retorna `deny`: cero side-effects.
- El modelo recibe el `permissionDecisionReason` y replanea con esa información.
- `permissionDecision` es estructurado: `allow` / `deny` / `ask`, no texto libre.
- Complementa al `stop_reason` del Kata 01: ese controla el bucle, este controla cada llamada a tool.
- Recarga en caliente: modificar el `dict` o releer el JSON cambia la política sin reiniciar el agente.

## Patrón correcto

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

## Anti-patrón

```python
# La política vive SOLO en el system prompt, sin hooks.
options = ClaudeAgentOptions(
    system_prompt="No apruebes reembolsos mayores a $1000.",
    # hooks ausentes
)
# Un prompt injection o un usuario insistente rompe la regla
# y process_refund ejecuta de todas formas.
```

## Argumento de certificación

Las políticas críticas (límites monetarios, dominios prohibidos, paths protegidos) viven en hooks `PreToolUse` con `permissionDecision` estructurado, no en system prompts. Un guardarraíl es determinista solo si el SDK puede aplicarlo sin depender de que el modelo elija obedecer.

## Cuándo activar

- Hay un límite duro de negocio (montos, dominios, rutas) que NO puede romperse.
- Se necesita bloquear una tool ANTES de que produzca side-effects.
- Una política debe recargarse en caliente sin reiniciar el agente.
- Se audita un agente cuya seguridad descansa solo en el prompt.

## Skills relacionadas

- `katas-deterministic-agentic-loop`
- `katas-posttooluse-normalization`
- `katas-mcp-structured-errors`
