# Pipeline Modes

`assets/mode-policy.json` is authoritative for mode selection. This reference explains the policy in human-readable form.

## Quick

- Phases: A diagnostic + D report.
- Writes: never.
- Result: `DIAGNOSTIC` or `BLOCKED`.
- Use when score is already >= 8, gate is 13/13, and the user did not request changes.

## Standard

- Phases: A diagnostic + B intervention + C certification + D report.
- Writes: only after Gate B approval.
- Result: `CERTIFIED`, `CONDITIONAL`, or `BLOCKED`.
- Use for score < 7, score >= 8 with requested changes, or context-pressure fallback.

## Deep

- Phases: A + B + C + C+ trigger optimization + re-certify + D.
- Writes: only after Gate B approval.
- Requires fixed or recorded trigger queries.
- Use for score >= 7 and score < 8 when trigger optimization is the highest-leverage improvement.

## Exact Auto-Selection

| Condition | Mode |
|---|---|
| score < 5 | standard |
| score >= 5 and score < 7 | standard |
| score >= 7 and score < 8 | deep |
| score >= 8 and gate 13/13 and no requested changes | quick |
| score >= 8 and requested changes | standard |

## Fail-Closed Conditions

- Missing target path: `BLOCKED`.
- Multiple target paths: ask the user to choose one.
- Missing `SKILL.md`: `BLOCKED`.
- Gate B denied: report diagnostic only; no writes.
- Deep mode context pressure: fall back to standard and report fallback.
