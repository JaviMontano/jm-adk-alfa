# Generate QA Scorecard - Body of Knowledge

## Canon

A scorecard is deterministic only when every dimension is present, every count
comes from evidence, status rules are strict, math is reproducible, and actions
are ranked by explicit impact. Executive compactness must not hide missing
dimensions or grade inflation.

## Dimension Order

1. Structure Conformance
2. Manifest Quality
3. Component Standards
4. Hook Safety
5. Reference Integrity
6. Security Posture
7. Content Quality

## Status And Points

| Status | Rule | Points |
|--------|------|--------|
| pass | 0 critical and 0 warning findings | 10 |
| warn | 0 critical and 1+ warning findings | 6 |
| fail | 1+ critical findings | 2 |
| na | Not evaluated with explicit reason | Excluded |

Info findings do not reduce score.

## Grade Rules

Percentage is `total_score / evaluated_max * 100`.

| Grade | Range |
|-------|-------|
| A | 90-100 |
| B | 80-89 |
| C | 70-79 |
| D | 60-69 |
| F | 0-59 |

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Dimension coverage | 100% | All 7 dimensions present or marked `na` |
| Math accuracy | 100% | Total, max, percent, and grade match policy |
| Evidence coverage | 100% | Each evaluated dimension names evidence source |
| Action priority | 100% | Actions rank fail before warn and max 3 actions |
| Reduced-scope disclosure | 100% | Any `na` dimension produces a reduced-scope note |

## References

- `references/scorecard-dimensions.md`
- `assets/scorecard-contract.json`
- `assets/dimensions-policy.json`
- `assets/scoring-policy.json`
- `assets/grade-policy.json`
- `assets/action-priority-policy.json`
- `assets/evidence-policy.json`
- `scripts/validate_qa_scorecard.py`
