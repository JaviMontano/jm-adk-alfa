<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Path Conditional Rules Output

## Summary

{summary}

## Evidence

{evidence}

## Result

### Clasificación de reglas

| Regla | Clase | Glob de activación |
|---|---|---|
| {rule} | universal / condicional | {glob_or_dash} |

### CLAUDE.md resultante

```text
{claude_md}
```

### Ahorro estimado de tokens

{token_savings}  <!-- input_tokens editando README vs editando .py -->

## Validation

- [ ] Cada regla está clasificada como universal o condicional por glob.
- [ ] Las reglas de seguridad son universales (carga directa, sin glob).
- [ ] `python-style` NO se carga al editar un README; `security` SÍ siempre.
- [ ] Globs sin huecos ni solapes ambiguos; precedencia por subpath resuelta.
- [ ] Ahorro de tokens medido, no afirmado.

## Risks and Limits

{risks}
