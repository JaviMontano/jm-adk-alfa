# QA Scorecard - 7 Quality Dimensions

This reference mirrors `assets/dimensions-policy.json` and
`assets/scoring-policy.json`.

## Dimensions

| Order | ID | Name | Measures |
|-------|----|------|----------|
| 1 | `structure` | Structure Conformance | Directory layout, naming, file placement |
| 2 | `manifest` | Manifest Quality | Manifest completeness and correctness |
| 3 | `components` | Component Standards | Skill, agent, command, and prompt contract integrity |
| 4 | `hooks` | Hook Safety | Hook validity, type-event compatibility, and safe actions |
| 5 | `references` | Reference Integrity | Cross-reference validity and orphan detection |
| 6 | `security` | Security Posture | Path traversal, secret leakage, injection, and unsafe writes |
| 7 | `content` | Content Quality | Procedure clarity, examples, anti-patterns, and output usefulness |

## Status Rules

| Status | Rule | Points |
|--------|------|--------|
| `pass` | 0 critical and 0 warning findings | 10 |
| `warn` | 0 critical and 1+ warning findings | 6 |
| `fail` | 1+ critical findings | 2 |
| `na` | Dimension not evaluated with explicit reason | Excluded |

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

## Action Ranking

Rank failed dimensions before warning dimensions, then by expected improvement,
critical count, warning count, and dimension order.
