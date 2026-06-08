# Example Output

## Summary

El ARR Q3 2025 queda corroborado por `doc-A` y `doc-B`. El headcount end-2025 queda en conflicto entre `doc-A` y `doc-C`, así que se preservan ambas posturas y se escala a humano.

## Source Registry

```json
[
  {"source_id": "doc-A", "source_name": "Annual Report", "publication_date": "2025-12-01"},
  {"source_id": "doc-B", "source_name": "Investor Deck", "publication_date": "2025-09-15"},
  {"source_id": "doc-C", "source_name": "Press Release", "publication_date": "2026-01-10"}
]
```

## Claims

```json
[
  {
    "claim_id": "claim-arr-q3-2025",
    "claim": "ARR Q3 2025 = 12M USD",
    "sources": [
      {"source_id": "doc-A", "value": "12M USD"},
      {"source_id": "doc-B", "value": "12M USD"}
    ],
    "conflict": false
  },
  {
    "claim_id": "claim-headcount-2025",
    "claim": "Headcount end-2025",
    "sources": [
      {"source_id": "doc-A", "value": "450"},
      {"source_id": "doc-C", "value": "462"}
    ],
    "conflict": true,
    "needs_human_review": true,
    "escalation_route": "human_review"
  }
]
```

## Conflicts

- `claim-headcount-2025`: `doc-A=450` y `doc-C=462`; no se promedia ni se elige fuente más reciente.

## Validation

- `claims_without_sources=0`.
- `unknown_source_refs=0`.
- `conflicts_silenced=0`.
- `structural_test_passed=true`.

## Risks And Limits

- Provenance no verifica por sí sola el cálculo numérico; debe combinarse con verificación numérica cuando haya operaciones.
