<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Tool Use Design Output

## Summary

{summary — qué solapamientos se resolvieron y qué estrategia de lectura se codificó}

## Evidence

{evidence — descripciones vigentes vs. propuestas; pares en conflicto detectados}

## Result

```python
# GOOD — descripciones-contrato con frontera recíproca + Grep → Read → Edit
{result}
```

## Anti-pattern evitado

```python
# ANTI — descripción genérica sin frontera + Glob("**/*") + Read all
{antipattern}
```

## Validation

- [ ] Cada descripción: input format + 1–2 ejemplos + frontera recíproca.
- [ ] Overloading resuelto con rename + split, no con prosa.
- [ ] Routing inmediato (sin pedir aclaración).
- [ ] Edit failure mode (anchor no único) + fallback Read+Write documentados.
- [ ] Flujo `Grep → Read → Edit`, sin read-all upfront.

## Risks and Limits

{risks}
