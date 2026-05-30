<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-pretooluse-guardrails
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Pretooluse Guardrails Primary Prompt

## Objective

Aplica la Kata 02: traslada una política crítica desde el `system_prompt` a un hook `PreToolUse` que emita `permissionDecision: 'deny'` antes de que la tool ejecute.

## Required Inputs

- La regla de negocio dura (por ejemplo "no procesar reembolsos mayores a $1000").
- La tool a controlar y la forma de su `tool_input` (por ejemplo `process_refund` con campo `amount`).
- Dónde vive la política: `dict` en memoria o JSON en disco recargable.
- Definition of done: la tool denegada no ejecuta y el modelo recibe la razón.

## Process

1. Define `POLICY` como `dict` o JSON recargable.
2. Escribe `policy_gate(input, tool_use_id, ctx)` que inspeccione `tool_name` y `tool_input` y retorne `hookSpecificOutput` con `permissionDecision: 'deny'` y `permissionDecisionReason` cuando se viole la política.
3. Registra `hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[policy_gate])]}` en `ClaudeAgentOptions`.
4. Valida que el `deny` corra ANTES de la tool (cero side-effects) y que el caso permitido pase con `{}`.

## Output

Devuelve: el patrón GOOD (hook + registro), el anti-patrón descartado (política solo en prompt), el argumento de certificación y el estado de validación.
