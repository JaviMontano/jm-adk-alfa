# Constitution Compliance — Body of Knowledge

## Canon

`constitution-compliance` audits artifacts against JM-ADK Constitution v6.0.0,
not v5-era runtime instructions. [EXPLICIT] The canonical machine-readable
surface is `assets/constitution-v6-principles.json`; the canonical prose source
is `references/ontology/constitution-v6.0.0.md`.

## Operating Rules

- Every report covers all 18 principles exactly once.
- Missing evidence is `not_verified`.
- A P0/P1 finding blocks delivery.
- A required G0-G3 gate with missing evidence blocks delivery.
- `not_applicable` is valid only when the artifact type excludes a principle.
- Evidence must cite a file, command output, PR check, review doc, or explicit
  user statement.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Principle coverage | 18/18 | Matrix row count and unique principle IDs |
| Gate coverage | G0-G3 | Gate impact table includes all four gates |
| Evidence coverage | 100% | Each row has a recognized evidence tag |
| Blocking discipline | 100% | P0/P1 or required missing evidence forces `blocked` |
| False-pass prevention | 100% | Negative fixtures fail validator |

## Anti-Patterns

- Declaring "no issues found" before building the 18-row matrix.
- Treating an omitted gate as a pass.
- Using stale Constitution targets as authoritative.
- Mixing JM Labs compliance with unrelated legal constitution analysis.
- Auditing runtime behavior without evidence from files, commands, or review
  packets.
