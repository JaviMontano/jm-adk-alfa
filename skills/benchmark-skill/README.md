# Benchmark Skill

Compares skill states with deterministic evidence: inventory deltas,
10-dimension rubric scores, 13 quality gates, regressions, trade-offs, top
improvements, and net assessment.

## Activation

Use this skill for skill-version comparison, before/after proof, diffing skill
states, regression analysis, or gap-to-standard evaluation. Do not use it for
generic product comparisons, certification verdicts, or issue discovery without
a comparison target.

## Deterministic Resources

- `assets/benchmark-rubric.json`: scoring dimensions and evidence rules.
- `assets/gate-policy.json`: 13 gate checks.
- `assets/net-assessment-policy.json`: classification rules.
- `assets/report-contract.json`: required report shape and blocked phrases.
- `scripts/validate_benchmark_report.py`: offline report validator.
- `scripts/check.sh`: deterministic fixture checks.

## Local Checks

```bash
bash skills/benchmark-skill/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill benchmark-skill
python3 -B scripts/validate-skill-dod.py --skill benchmark-skill
```
