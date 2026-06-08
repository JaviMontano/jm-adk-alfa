# Quality Engineering Body of Knowledge

## Canon

Quality engineering designs how quality is built, measured, and governed across the delivery lifecycle. It is broader than test coverage and includes architecture-driven test shape, quality gates, test data, metrics, shift-left ownership, and operational feedback.

## Core Decisions

| Decision | Deterministic rule |
|---|---|
| Maturity level | Derived from the six canonical dimension scores. |
| Test shape | Selected from architecture type; percentages are not invented. |
| Gate enforcement | Commit, PR, release, and production gates block; nightly is async. |
| Metrics | Include leading and lagging metrics; coverage alone is insufficient. |
| Priority actions | Sort by largest gap to target maturity, then lower score, then canonical order. |

## Evidence Requirements

- Each maturity score needs file, command, user-provided fact, or assumption evidence.
- Missing evidence must be explicit in `assumptions` or `reduced_scope`.
- Security criteria cannot be bypassable.
- A report without gates, metrics, roadmap, and priority actions is incomplete.
