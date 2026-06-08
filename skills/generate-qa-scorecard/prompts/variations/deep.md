---
name: generate-qa-scorecard-deep
type: execution
version: 2.0.0
description: "Full QA scorecard synthesis from multi-source validation evidence."
---

# Deep QA Scorecard

Use when findings come from multiple validators, audit reports, or partial
evidence.

## Steps

1. Build an evidence register with source, dimension, severity, and finding id.
2. Normalize findings into the 7 canonical dimensions.
3. Mark missing evidence as `na` with reason instead of inventing counts.
4. Apply `assets/scoring-policy.json` and `assets/grade-policy.json`.
5. Apply `assets/action-priority-policy.json`.
6. For JSON output, validate with `scripts/validate_qa_scorecard.py`.

## Output

Return a complete scorecard with evidence summary, table, grade, top actions,
reduced-scope note, and Guardian decision.
