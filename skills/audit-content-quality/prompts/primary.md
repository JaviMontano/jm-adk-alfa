---
name: audit-content-quality-primary
type: execution
version: 2.0.1
description: "Execute the deterministic Audit Content Quality workflow."
triad:
  lead: "audit-content-quality-lead"
  support: "audit-content-quality-support"
  guardian: "audit-content-quality-guardian"
---

# Audit Content Quality Execute

## Dynamic Parameters

| Parameter | Description | Required |
|---|---|---|
| `{{target}}` | Plugin root, skill directory, or explicit `SKILL.md` paths | Yes |
| `{{scope}}` | Optional subset or ranking request | No |
| `{{format}}` | Markdown or JSON report | No |

## Execution Steps

1. Confirm activation with `assets/activation-policy.json`.
2. Load `assets/scoring-rubric.json`, `assets/evidence-policy.json`, and `assets/report-contract.json`.
3. Discover all target `SKILL.md` files.
4. Score all six dimensions and write evidence-tagged rationales.
5. Compute formula-derived totals, percentages, grades, averages, bottom skills, and systematic gaps.
6. Report coverage for discovered, scored, and skipped files.
7. Validate JSON reports with the local validator when available.
