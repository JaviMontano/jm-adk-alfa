<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Perfil KYC consolidado con provenance tipada. Cada claim transporta su documento de origen y fecha; el conflicto de ingresos (USD 4.2M vs USD 4.8M) queda marcado y escalado al analista, no promediado.

## Evidence (claims con provenance)

| attribute | value | source_id | locator | as_of | conflict |
|---|---|---|---|---|---|
| address | Carrera 7 #71-21, Bogotá | doc-A, doc-B | p.1 / p.3 | 2021-03-12, 2024-09-30 | false |
| revenue | USD 4.2M \| USD 4.8M | doc-B, doc-C | p.5 / p.2 | 2024-09-30, 2025-02-15 | true |

## Result (GOOD)

```python
@dataclass(frozen=True)
class Claim:
    attribute: str
    value: str
    sources: tuple[Source, ...]
    conflict: bool = False

    def __post_init__(self) -> None:
        if not self.sources:
            raise ValueError(f"claim '{self.attribute}' has no source")  # GOOD: invariant by construction

revenue = merge("revenue", [claim_b, claim_c])  # conflict=True, both sources kept
escalate_to_human(revenue)  # GOOD: not averaged, routed to analyst with as_of visible
```

## Anti-pattern (ANTI — lo que el pipeline hacía antes)

```python
# ANTI: prose summary, no source_id, no date, conflict averaged away
revenue = (4.2 + 4.8) / 2          # 4.5M — a number no source ever stated
return f"Revenue is USD {revenue}M."  # analyst cannot audit origin or see the disagreement
```

## Validation

- [x] Cada claim con `source[]` no vacío (id + ubicación + fecha)
- [x] Conflicto de ingresos marcado `conflict=true` con ambas fuentes
- [x] Conflicto escalado al analista, no promediado
- [x] `as_of` visible en el render
- [x] Test estructural de provenance en verde (`assert_provenance`)

## Risks and Limits

- La normalización de direcciones ("Carrera 7" vs "Cra 7") podría enmascarar un conflicto real si la regla es laxa; revisada como equivalente, documentada.
- El analista debe resolver el conflicto de ingresos antes de aprobar; el pipeline no decide.
