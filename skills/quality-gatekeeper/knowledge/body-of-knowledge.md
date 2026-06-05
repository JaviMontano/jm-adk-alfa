# Quality Gatekeeper — Body of Knowledge

## Canon

`quality-gatekeeper` enforces JM-ADK gate decisions. Its core rule is:
no evidence, no pass; no gate order, no advance. [EXPLICIT]

The local canon lives in:

- `assets/gate-criteria.json`
- `assets/report-contract.json`
- `assets/evidence-policy.json`
- `assets/score-history-schema.json`

## Operating Rules

- Gate order is G0 -> G1 -> G2 -> G3.
- Every required criterion in scope must appear exactly once.
- Missing required evidence is `not_verified`.
- Required `fail` and required `not_verified` block advancement.
- Score history is emitted as a proposed entry unless writes are explicitly
  authorized.
- More than 30% assumption-tagged evidence requires a warning banner.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Criterion coverage | 100% | All scoped criteria represented exactly once |
| Evidence coverage | 100% | Every pass row has a recognized evidence tag |
| Blocking discipline | 100% | Required fail/not_verified forces blocked |
| Sequence discipline | 100% | G1-G3 require prior gates |
| Fixture integrity | 100% | Positive and negative fixtures validate offline |

## Anti-Patterns

- Rubber-stamping a gate because a user asks to proceed.
- Treating "almost ready" as a pass.
- Writing score history before validating the report.
- Calling a gate `pass` from missing evidence.
- Ignoring prior gate order.
