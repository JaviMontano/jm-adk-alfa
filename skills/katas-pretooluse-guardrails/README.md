<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-pretooluse-guardrails
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Pretooluse Guardrails

Guardarrailes deterministas en hook PreToolUse con permissionDecision deny desde politica recargable, no en el system prompt.

## Triggers

- pretooluse guardrail
- permission decision
- policy gate
- deterministic guardrail

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Kata 02 del kit JM-ADK. Enseña a mover las políticas críticas (límites monetarios, dominios prohibidos, paths protegidos) desde el `system_prompt` hacia un hook `PreToolUse` que emite `permissionDecision: 'deny'`. El SDK aplica el bloqueo ANTES de que la tool produzca side-effects, por lo que el guardarraíl es determinista y no depende de que el modelo obedezca. La política vive en un `dict` o JSON recargable en caliente.

## Quick Use

Invoca `katas-pretooluse-guardrails` cuando exista un límite de negocio que no puede romperse y debas bloquear una tool antes de que ejecute. El patrón registra un `HookMatcher(matcher="*", hooks=[policy_gate])` en `ClaudeAgentOptions.hooks["PreToolUse"]` y retorna `deny` con un `permissionDecisionReason` legible.

## Output Format

Markdown con el patrón GOOD (hook + `permissionDecision`), el anti-patrón (política solo en prompt), el argumento de certificación y el estado de validación.
