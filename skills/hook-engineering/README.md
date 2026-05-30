<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# hook-engineering

Capacidad de ingenieria para disenar y validar **hooks deterministas** en el Claude
Agent SDK: PreToolUse que decide `allow|deny|ask` antes del side-effect y PostToolUse
que reescribe `tool_response` hacia `updatedMCPToolOutput` antes del historial, con la
politica viviendo en codigo recargable y no en el prompt.

## Resumen ejecutivo

Convierte reglas "que el modelo deberia respetar" en controles que el runtime garantiza.
El resultado es enforcement de politicas (limites monetarios, paths, dominios, modo
plan/write) y normalizacion de I/O resistente a inyeccion de prompt y auditable.

## Triggers

- hook engineering
- pretooluse hook
- posttooluse hook
- deterministic hooks

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Coloca la politica en `references/guardrails/tool-policy.json` (hot-reload).
2. Registra `PreToolUse` y `PostToolUse` con `HookMatcher(matcher="*")` en `ClaudeAgentOptions.hooks`.
3. Verifica con la checklist: deny antes del side-effect, modelo nunca ve el payload crudo, decision auditable.

## Output Format

Markdown con resumen, evidencia, resultado, validacion y riesgos. Codigo de hooks en EN.

Skills relacionadas: `katas-pretooluse-guardrails`, `katas-posttooluse-normalization`.
