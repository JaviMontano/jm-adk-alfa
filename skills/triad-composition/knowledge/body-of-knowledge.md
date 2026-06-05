# Triad Composition — Body of Knowledge

## Canon

Triad composition turns an intent classification into a deterministic execution team:

- Lead produces the primary domain deliverable.
- Support reviews blind spots and cross-cutting risks.
- Guardian validates evidence, Constitution compliance, G0-G3 gates, and assumptions.

## Deterministic Selection

Use `assets/composition-matrix.json` as the only local matrix. If a runtime mirror has a different matrix, treat it as drift and record the discrepancy instead of blending rows.

Confidence policy:

- `>=0.85`: select one triad and execute.
- `0.60-0.84`: present top 3 options and ask user to choose.
- `<0.60`: ask for clarification.

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| Matrix fidelity | 100% | Selected triad matches one matrix row |
| Guardian presence | 100% | Every triad/committee output names Guardian |
| Threshold compliance | 100% | Action matches confidence band |
| Evidence coverage | 100% | Classification claims tagged `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` |
| False-positive rejection | 100% | Non-orchestration triad requests do not return agents |

## Anti-Patterns

| Anti-pattern | Risk | Required response |
|---|---|---|
| Applying defaults to missing context | Overconfident routing | Ask for missing Goal, Context, Constraints, Definition of done |
| Skipping Guardian | Unvalidated delivery | Block or mark `[PARTIAL]` |
| Silent tie-break | Hidden ambiguity | Present top 3 options when confidence is 0.60-0.84 |
| Matrix blending | Non-reproducible triad | Use one source and report drift |
| Music triad activation | False-positive routing | Route away from this skill |
