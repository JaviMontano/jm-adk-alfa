# Quality Metrics

Measures and gates code coverage, cyclomatic complexity, duplication, Lighthouse scores, bundle size, and Firestore I/O.

## Use

Use this skill for:

- quality metric baselines
- CI threshold design
- regression tracking
- bundle and Lighthouse budgets
- Firestore read/write cost guardrails
- compact metric scorecards

## Contract

The deterministic report contract lives in `assets/`. JSON reports can be validated offline with:

```bash
bash skills/quality-metrics/scripts/check.sh
python3 -B skills/quality-metrics/scripts/validate_quality_metrics.py <report.json>
```

## Output

A complete report includes evidence summary, six canonical metrics, gate matrix, trend assessment, priority actions, and Guardian decision.
