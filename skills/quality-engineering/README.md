# Quality Engineering

Designs deterministic quality engineering frameworks for projects and platforms.

## Use

Use this skill for:

- quality maturity assessment
- architecture-driven test strategy
- automation architecture
- quality gates
- shift-left practices
- quality metrics and dashboards

## Contract

The canonical report contract lives in `assets/`. JSON reports can be validated offline with:

```bash
bash skills/quality-engineering/scripts/check.sh
python3 -B skills/quality-engineering/scripts/validate_quality_engineering.py <report.json>
```

## Output

A complete report includes evidence summary, six maturity dimensions, test strategy shape, five gates, required metrics, roadmap, top priority actions, and Guardian decision.
