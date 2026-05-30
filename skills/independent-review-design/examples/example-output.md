<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El diseño actual sufre self-review en sesión compartida y quorum 2-de-3 que suprime
defectos cross-file legítimos. Rediseñamos a reviewer independiente con pases per-file y
cross-file separados y sin quorum.

## Evidence

- `review.py:12` — `Reviewer(session=gen_session)`: el revisor hereda la sesión del
  generador (sesgo de confirmación).
- `review.py:18` — `votes[f] >= 2`: el quorum descarta el hallazgo de naming entre
  `orders.py` y `money.py` que solo una pasada detectó.

## Result

ANTI (estado actual):

```python
def review_bad(artifacts, gen_session):
    reviewer = Reviewer(session=gen_session)        # self-review
    votes = collections.Counter()
    for _ in range(3):
        for f in reviewer.review_all(artifacts):    # per/cross mezclados
            votes[f.key] += 1
    return [f for f in votes if votes[f] >= 2]       # quorum suprime senal rara
```

GOOD (rediseño):

```python
def review(artifacts: list[Artifact], criteria: Criteria) -> list[Finding]:
    reviewer = Reviewer(session=Session.fresh(), criteria=criteria)  # sesion limpia
    findings: list[Finding] = []
    for art in artifacts:                            # per-file
        findings += reviewer.review_file(art)
    findings += reviewer.review_cross_file(artifacts)  # cross-file separado
    return dedupe_keep_max_severity(findings)        # sin quorum
```

## Validation

- Reviewer en sesión limpia: sí (`Session.fresh()`).
- per-file y cross-file separados: sí (dos llamadas distintas).
- Sin quorum supresivo: sí (se conserva todo hallazgo).
- Hallazgos citados con archivo:línea: sí.
- Dedupe conserva severidad máxima: sí.

## Risks and Limits

Al retirar el quorum aumentan los falsos positivos; mitigación: el humano triará por
severidad y categoría, no por frecuencia de detección.
