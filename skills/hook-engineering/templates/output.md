<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Hook Engineering Output

## Summary

{summary: que limite/normalizacion se hace cumplir y por que via hook y no prompt}

## Evidence

{evidence: politica recargable, eventos PreToolUse/PostToolUse y registro en ClaudeAgentOptions.hooks}

## Result

```python
{result: codigo del PreToolUse y/o PostToolUse + HookMatcher}
```

## Validation

- [ ] La politica vive en codigo recargable, no en el system prompt.
- [ ] El deny ocurre antes de cualquier side-effect.
- [ ] El modelo nunca ve el payload crudo (PostToolUse normaliza antes del historial).
- [ ] Cada decision deny queda auditada.

## Risks and Limits

{risks: huecos de cobertura, handlers sin normalizar, JSON de politica corrupto}
