# Generate QA Scorecard

Deterministic executive scorecard generation for plugin quality findings.

## Triggers

- `generate-qa-scorecard`
- `generate scorecard`
- `qa scorecard`
- `plugin grade`
- `executive summary`
- `quality scorecard`

## Allowed Tools

- Read
- Glob
- Grep
- Bash

## Quick Use

Use this skill when validation or audit findings must become a compact scorecard
with a numeric score, letter grade, and top 3 remediation actions.

## Output Format

Markdown or JSON with:

- evidence summary
- 7-dimension score table
- total score and evaluated maximum
- percentage and letter grade
- top 3 priority actions
- reduced-scope note when dimensions are `na`
- Guardian decision

Structured JSON scorecards can be validated offline with
`scripts/validate_qa_scorecard.py`.
