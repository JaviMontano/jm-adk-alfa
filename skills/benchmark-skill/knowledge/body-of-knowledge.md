# Benchmark Skill Body Of Knowledge

## Canon

Benchmark Skill answers one question: did a skill state improve, regress, stay
lateral, transform, or remain below a standard? The answer must be derived from
inventory counts, 10 rubric scores, 13 gates, and explicit evidence.

## Scoring Discipline

- Score State A completely before State B.
- Reuse State A scores for unchanged evidence.
- Every score needs a file, section, command, or explicit observation.
- A delta is valid only when it equals `state_b - state_a`.
- A gate regression blocks `IMPROVED`.
- Against-standard mode reports gaps, not regressions.
- Transformed mode avoids direct "better/worse" claims unless the caveat is
  visible.

## Quality Metrics

| Metric | Target | How To Measure |
|---|---:|---|
| Dimension coverage | 10/10 | Report has every rubric dimension |
| Gate coverage | 13/13 | Report has every gate row |
| Delta correctness | 100% | Validator recomputes each score delta |
| Evidence coverage | 100% | Every score and gate has evidence |
| Label consistency | 100% | Net assessment matches policy |
| Local validation | Pass | `bash skills/benchmark-skill/scripts/check.sh` |

## Anti-Patterns

| Anti-pattern | Failure | Correction |
|---|---|---|
| Inflated improvement | Positive label despite gate regression | Use `REGRESSED` or fix gate |
| Missing baseline | Scores invented for State A | Stop and ask for baseline |
| Opinion-only score | No file or command evidence | Add evidence or mark unknown |
| Hidden transformed state | Rewrite treated as direct delta | Use `TRANSFORMED` and parallel scorecards |
| Runtime overclaim | Structural score claims behavior proof | Add caveat and request eval transcripts |
