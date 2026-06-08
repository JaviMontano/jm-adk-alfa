# Katas Pretooluse Guardrails

Kata para convertir reglas críticas de negocio en controles determinísticos de `PreToolUse`. La política vive en código o JSON recargable, el hook inspecciona `tool_name` y `tool_input`, y el retorno estructurado usa `permissionDecision: "deny"` antes de que la tool produzca efectos.

## Triggers

- pretooluse guardrail
- permission decision
- policy gate
- deterministic guardrail

## Use When

- Una política no puede depender de obediencia al `system_prompt`.
- Una tool con side-effects debe bloquearse antes de ejecutar.
- La política debe recargarse sin reiniciar el agente.
- El reporte debe probar casos `deny` y `allow` con evidencia offline.

## Output Contract

El entregable debe incluir:

- Política externa al prompt (`dict` o JSON).
- Hook `PreToolUse` registrado con `HookMatcher`.
- Retorno `hookSpecificOutput` con `hookEventName`, `permissionDecision` y `permissionDecisionReason`.
- Caso denegado sin side-effects y caso permitido que ejecuta.
- Evidencia de que prompt injection no puede saltarse la política.

## Offline Validation

```bash
bash skills/katas-pretooluse-guardrails/scripts/check.sh
python3 -B skills/katas-pretooluse-guardrails/scripts/validate_pretooluse_guardrails.py skills/katas-pretooluse-guardrails/scripts/fixtures/valid-refund-limit.json
```
