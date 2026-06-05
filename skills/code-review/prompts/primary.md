---
name: code-review-primary
type: execution
version: 2.1.0
description: "Execute deterministic Code Review with read-only triad orchestration."
triad:
  lead: "code-review-lead"
  support: "code-review-support"
  guardian: "code-review-guardian"
---

# Code Review - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{review_target}}` | PR, diff, patch, branch, commit range, file path, or code excerpt | Yes | User/codebase |
| `{{intent}}` | Stated change intent or acceptance criteria | No | User/issue |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{validation_evidence}}` | Tests, CI, logs, or command output | No | User/codebase |
| `{{review_date}}` | Caller-supplied date for dated reports | No | User |

## When To Activate

Activate when `{{review_target}}` contains code artifacts or explicit PR/diff
review language. If the request is a non-code review, do not activate. If
minimum code context is missing, return `needs_context`.

## Execution

1. Read `assets/activation-policy.json`.
2. Read `assets/review-taxonomy.json`.
3. Read `assets/evidence-policy.json`.
4. Read `assets/report-contract.json`.
5. Establish scope and missing inputs.
6. Lead drafts findings with exact evidence.
7. Support calibrates severity and false positives.
8. Guardian checks evidence tags, file/line coverage, and decision consistency.

## Output

Return the Markdown sections from `templates/output.md` or a JSON report that
matches `assets/report-contract.json`. Do not use current time unless
`{{review_date}}` was supplied.

## Validation Gate

For skill changes, run:

```bash
bash skills/code-review/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill code-review
```
