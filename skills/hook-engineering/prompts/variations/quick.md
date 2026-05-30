<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Hook Engineering Quick Variation

Usar cuando el limite es claro y de bajo riesgo (un solo tool, una sola regla).

1. Lee la regla desde la politica recargable.
2. Implementa solo el PreToolUse con `permissionDecision: deny` cuando se exceda el limite.
3. Registra con `HookMatcher` por-tool.

Devuelve unicamente el codigo del hook (EN), el estado de la checklist y los riesgos residuales.
