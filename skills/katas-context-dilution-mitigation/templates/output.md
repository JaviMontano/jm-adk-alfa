<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation Output

## Summary

{summary}

## Evidence

{evidence}

## Result

```python
SYSTEM:<rules>{critical_policy}</rules>
...
USER:{question}
...
REMINDER:<rules>{critical_policy}</rules>

if usage_fraction(history) > 0.55:
    history = compact(history, preserve=['rules', 'decisions', 'escalations'])
```

{result}

## Validation

- [ ] Reglas críticas presentes al inicio del prompt.
- [ ] Mismas reglas repetidas al final como `<reminder>`.
- [ ] Datos ricos ubicados en el centro.
- [ ] Gate de compactación con umbral 50-60% definido.
- [ ] Compactación preserva reglas, decisiones y escaladas.

{validation}

## Risks and Limits

{risks}
