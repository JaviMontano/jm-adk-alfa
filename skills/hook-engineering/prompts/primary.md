<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Hook Engineering Primary Prompt

## Objetivo

Disenar e implementar hooks deterministas para la tarea del usuario: un PreToolUse que
decida `allow|deny|ask` antes del side-effect y, cuando aplique, un PostToolUse que
normalice `tool_response` hacia `updatedMCPToolOutput` antes del historial, con la
politica en codigo recargable.

## Inputs requeridos

- Regla o limite a hacer cumplir (monetario, path, dominio, modo plan/write).
- Tools afectadas (o `*` si es global) y shape de su `tool_input`/`tool_response`.
- Ubicacion de la politica recargable (`references/guardrails/tool-policy.json`).
- Definicion de hecho: que decision deny y que normalizacion deben quedar garantizadas.

## Proceso

1. Descubre el limite y la fuente de politica; confirma que no debe vivir en el prompt.
2. Disena el PreToolUse: inspeccion pura de `tool_name` + `tool_input`, sin side-effects.
3. Disena el PostToolUse: contrato unico de salida hacia `updatedMCPToolOutput`.
4. Registra con `HookMatcher(matcher="*")` o por-tool en `ClaudeAgentOptions.hooks`.
5. Valida contra la checklist y deja traza auditable de cada deny.

## Output

Entrega el codigo de los hooks (EN) mas notas (ES): resumen, evidencia, resultado de la
checklist, estado de validacion y riesgos residuales.
