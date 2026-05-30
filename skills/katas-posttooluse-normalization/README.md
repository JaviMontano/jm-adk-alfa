<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Posttooluse Normalization

Normalizacion de outputs heterogeneos via hook PostToolUse y updatedMCPToolOutput antes de entrar al historial del modelo.

## Triggers

- posttooluse normalization
- output normalization
- updatedmcptooloutput
- legacy payload

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Kata 03 del kit JM-ADK. Un hook `PostToolUse` reescribe el `tool_response` heterogéneo (XML legacy, códigos arcanos) a JSON canónico vía `updatedMCPToolOutput` antes de que entre al historial del modelo. La garantía es del runtime, no de cada tool: una sola regla central cubre todas las tools que matcheen, en vez de confiar en que cada handler recuerde normalizar. `additionalContext` anexa metadatos auditables sin ensuciar el payload limpio. Escenarios: Customer Support, Legacy ERP Integration.

## Quick Use

Activa esta skill cuando una tool devuelva payloads legacy o heterogéneos y quieras una normalización garantizada por runtime. Lee `STATUS_MAP` y el handler del hook, aplica el patrón de `SKILL.md` (`hookSpecificOutput.updatedMCPToolOutput`), y verifica que el modelo nunca reciba el XML crudo. El argumento de cierre: la normalización es responsabilidad del runtime vía `PostToolUse`, no convención por-tool.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
