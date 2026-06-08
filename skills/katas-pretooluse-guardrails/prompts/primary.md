# Primary Prompt

## Objective

Convierte una política crítica en un guardarraíl determinístico `PreToolUse` con política externa recargable y `permissionDecision` estructurado.

## Required Inputs

- Regla dura de negocio.
- Tool objetivo y shape de `tool_input`.
- Fuente de política: `dict` o JSON.
- Casos mínimos: uno denegado y uno permitido.

## Process

1. Extrae la política fuera del `system_prompt`.
2. Define reglas con `target_tool`, `field`, `operator`, `value` y `decision`.
3. Implementa `policy_gate(input, tool_use_id, ctx)` para `PreToolUse`.
4. Registra el hook con `HookMatcher`.
5. Prueba `deny` sin side-effects, `allow` válido y prompt injection bloqueado.

## Output

Entrega `Summary`, `Policy`, `PreToolUse Hook`, `Decision Matrix`, `Validation` y `Risks And Limits`.
