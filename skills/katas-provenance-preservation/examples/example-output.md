<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Dos claims factuales. El ARR está corroborado por dos fuentes sin conflicto. El headcount entra en conflicto entre `doc-A` (450) y `doc-C` (462): se registran ambas posturas y se escala a humano. No se promedia ni se elige.

## GOOD (patrón correcto)

```python
claims = [
    {
        "claim": "ARR Q3 2025 = 12M USD",
        "sources": [
            {"id": "doc-A", "name": "Annual Report", "date": "2025-12-01"},
            {"id": "doc-B", "name": "Investor Deck", "date": "2025-09-15"},
        ],
        "conflict": False,
    },
    {
        "claim": "Headcount end-2025",
        "sources": [
            {"id": "doc-A", "value": "450"},
            {"id": "doc-C", "value": "462"},
        ],
        "conflict": True,
        "needs_human_review": True,
    },
]
```

## ANTI (lo que se evita)

```python
summary = "La empresa tiene ARR de 12M USD y 462 empleados..."
# sin source_id, sin fecha, sin conflicto marcado: eligió 462 en silencio
```

## Validation

- Test estructural: cada claim tiene `sources[]` no vacío con `source_id` existente. PASA.
- El conflicto de headcount está marcado `conflict=true` y enrutado a humano (Kata 16), no resuelto por el modelo.
- Las fechas de publicación están presentes para que el humano juzgue (la más reciente, `doc-C`, no gana automáticamente).
