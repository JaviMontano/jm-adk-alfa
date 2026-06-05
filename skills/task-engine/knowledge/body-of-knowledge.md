# Task Engine — Body of Knowledge

## Canon

Task Engine applies DSVSR:

1. Decompose into independent sub-problems.
2. Solve each sub-problem with confidence and evidence.
3. Verify logic, facts, completeness, and bias.
4. Synthesize a weighted global confidence.
5. Reflect when confidence is below target or evidence is missing.

## Deterministic Rules

- Use `assets/activation-policy.json` before deciding full DSVSR vs fast path.
- Use `assets/confidence-scale.json` for all confidence labels.
- Use `assets/reflection-policy.json` when global confidence is below target.
- Use `assets/dsvsr-packet-contract.json` for final packet shape.

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| Stage completeness | 100% | Decompose, Solve, Verify, Synthesize, Reflect, Metadata present |
| Confidence evidence | 100% | Every score has justification and missing-info condition |
| Verification coverage | 100% | LOGIC, FACTS, COMPLETENESS, BIAS checked |
| Weakness disclosure | 100% | Weakest sub-problem and gaps named |
| False-certainty prevention | 100% | No 0.95+ score without direct evidence |

## Anti-Patterns

| Anti-pattern | Risk | Required response |
|---|---|---|
| Skipping Verify | False confidence | Block delivery |
| "No weaknesses" | Hidden uncertainty | Name at least one weakness or limitation |
| Over-decomposition | Latency without value | Group into 3-7 sub-problems |
| Raw 0.95 confidence | Inflated certainty | Lower confidence or cite direct evidence |
| Under-specified problem | Fabricated reasoning | Ask for clarification |
