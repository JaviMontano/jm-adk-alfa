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

## Tool Contract Table

| Tool | Purpose | Input format | Examples | Boundary |
| --- | --- | --- | --- | --- |
| {tool} | {purpose} | {input_format} | {examples} | {boundary} |

## Repo Strategy

- Sequence: grep -> read -> edit
- Read all upfront: no
- Glob all then read all: no

## Edit Safety

- Unique anchor required: yes
- Failure mode: non_unique_anchor
- Fallback: read_write_full_rewrite

## Anti-pattern Avoided

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
- [ ] Offline validator passed.

## Risks and Limits

{risks}
