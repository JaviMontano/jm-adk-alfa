---
name: code-review-checklist-primary
type: execution
version: 2.1.0
description: "Execute deterministic Code Review Checklist with read-only triad orchestration."
triad:
  lead: "code-review-checklist-lead"
  support: "code-review-checklist-support"
  guardian: "code-review-checklist-guardian"
---

# Code Review Checklist - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{review_target}}` | PR, diff, changed files, Firestore rules, package manifest, audit output, or CI output | Yes | User/codebase |
| `{{mode}}` | standard / hotfix / dependency-only / deep | No | Auto |
| `{{intent}}` | Stated change intent or acceptance criteria | No | User/issue |
| `{{review_date}}` | Caller-supplied date for dated reports | No | User |

## When To Activate

Activate only for code-review checklist requests with code artifacts. Return
`needs_context` when minimum inputs are absent.

## Execution

1. Read `assets/activation-policy.json`.
2. Read `assets/checklist-taxonomy.json`.
3. Read `assets/evidence-policy.json`.
4. Read `assets/report-contract.json`.
5. Establish scope and missing inputs.
6. Run applicable checklist IDs and record pass/fail/not-applicable/not-verified.
7. Apply decision rules.
8. Guardian validates evidence and decision consistency.

## Output

Return Markdown sections from `templates/output.md` or JSON matching
`assets/report-contract.json`. Do not use current time unless `{{review_date}}`
was supplied.

## Validation Gate

For skill changes, run:

```bash
bash skills/code-review-checklist/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill code-review-checklist
```
