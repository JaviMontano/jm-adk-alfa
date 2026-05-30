<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Posttooluse Normalization Output

## Summary

{Qué tools se normalizan y por qué el hook PostToolUse es la garantía de runtime.}

## STATUS_MAP y esquema

{Mapa de códigos legacy -> valores canónicos y shape del JSON objetivo.}

## Hook (código)

```python
{handler normalize_legacy con retorno hookSpecificOutput.updatedMCPToolOutput y additionalContext}
```

## Evidence

{Citas al código del hook, al matcher y al shape de updatedMCPToolOutput.}

## Validation

- [ ] El XML crudo nunca entra al historial del modelo.
- [ ] El matcher cubre todas las tools legacy (no por-tool).
- [ ] Códigos sin mapear caen en fallback explícito.
- [ ] additionalContext solo lleva metadatos auditables.

## Risks and Limits

{Tools nuevas fuera del matcher, códigos no contemplados, hot-reload de STATUS_MAP.}
