---
name: generate-qa-scorecard
version: 1.0.0
author: JM Labs (Javier Montano)
description: >
  Produces deterministic executive QA scorecards for plugins across 7 quality
  dimensions, with strict PASS/WARN/FAIL/N/A status, numeric score, letter
  grade, top 3 priority actions, and validation evidence. [EXPLICIT]
  Trigger: generate scorecard, qa scorecard, plugin grade, executive summary. [EXPLICIT]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Generate QA Scorecard

> "A dashboard is only as good as the decisions it enables."

## TL;DR

Use this skill when validation and audit findings must become a compact
executive scorecard with deterministic math and ranked remediation actions.
[EXPLICIT]

The output must not invent quality signals. It must map findings to the 7
approved dimensions, calculate scores from strict status rules, assign a letter
grade from the evaluated denominator, and rank the top 3 actions by expected
score improvement. [EXPLICIT]

## Procedure

### Step 1: Collect Evidence

- Gather validation and audit findings from supplied reports, logs, or reviewed
  artifacts.
- Use `assets/evidence-policy.json` to record source, severity, affected
  dimension, and whether a dimension is unevaluated.
- If no evidence exists for a dimension, mark it `na` with a reason instead of
  silently omitting it.

### Step 2: Score The 7 Dimensions

- Use `assets/dimensions-policy.json` for the canonical dimension ids and names.
- Use `assets/scoring-policy.json` for strict status and point rules:
  `pass=10`, `warn=6`, `fail=2`, and `na=excluded`.
- A dimension with one or more critical findings is `fail`.
- A dimension with no critical findings and one or more warning findings is
  `warn`.
- A dimension with only info or zero findings is `pass`.

### Step 3: Calculate Grade

- Use `assets/grade-policy.json` to calculate percent:
  `total_score / evaluated_max * 100`.
- Letter grades are deterministic: `A>=90`, `B>=80`, `C>=70`, `D>=60`, `F<60`.
- If fewer than 7 dimensions are evaluated, state the reduced scope and do not
  imply full readiness.

### Step 4: Rank Top Actions

- Use `assets/action-priority-policy.json`.
- Rank `fail` dimensions before `warn` dimensions.
- Within the same status, rank by expected score improvement, critical count,
  warning count, then stable dimension order.
- Return at most 3 priority actions.

### Step 5: Validate And Handoff

- Produce the output sections from `assets/scorecard-contract.json`.
- Validate structured JSON scorecards with
  `scripts/validate_qa_scorecard.py` or `scripts/check.sh`.
- For Markdown scorecards, preserve the same table, math, grade, and action
  ranking contract.

## Quality Criteria

- [ ] All 7 dimensions are present or explicitly marked `na`.
- [ ] Every evaluated dimension has critical, warning, and info counts.
- [ ] Status follows the strict severity rules.
- [ ] Total score, evaluated maximum, percentage, and grade are mathematically
  consistent.
- [ ] Top actions are ranked by deterministic impact rules.
- [ ] Reduced scope is disclosed when any dimension is `na`.
- [ ] Evidence tags are applied to user-facing factual claims.

## Usage

Example invocations:

- "/generate-qa-scorecard" - Generate a deterministic executive QA scorecard.
- "Create a QA scorecard from these audit findings."
- "Validate this scorecard JSON before sending it to leadership."
- "Rank the top 3 plugin quality actions by score improvement."

## Assumptions & Limits

- Read-only: this skill aggregates findings and does not modify plugin files.
  [EXPLICIT]
- Requires supplied findings or reviewed artifacts; it does not fabricate audit
  results. [EXPLICIT]
- N/A dimensions are excluded from the denominator and must be disclosed.
  [EXPLICIT]
- Security and content failures use the same numeric points; action ranking
  carries the severity nuance. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| All dimensions pass | Score 70/70, grade A, and state no critical actions needed |
| All dimensions fail | Score 14/70, grade F, and return top 3 actions only |
| Some dimensions N/A | Recalculate denominator and disclose reduced scope |
| Info-only dimension | Status remains pass and score remains 10 |
| Missing action for fail | Block scorecard readiness |
| Grade/math mismatch | Block output until corrected |
