<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Context Window Engineering Output

## Summary

{summary}

## Context Assembler (GOOD)

```python
{context_assembler}
```

## Edge Placement & Compaction

- Reglas críticas en bordes: {edge_rules}
- Estado dinámico en `<reminder>` final: {dynamic_tail}
- Umbral de compactación: {compaction_threshold}

## Evidence

- Cache-hit esperado/medido: {cache_hit}
- Prueba de retención de regla crítica: {retention_test}

## Validation

- [ ] Prefijo byte-idéntico, sin valores por-turno: {check_prefix}
- [ ] Dinámico solo en `<reminder>` final: {check_dynamic}
- [ ] Reglas críticas en bordes: {check_edges}
- [ ] Umbral de compactación fijado: {check_compaction}
- [ ] Cache-hit + retención validados: {check_validation}

## Risks and Limits

{risks}
