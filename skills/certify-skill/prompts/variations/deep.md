---
name: certify-skill-deep
type: variation
variant: deep
---
# Certify Skill Deep Analysis

Use for production readiness, re-certification, or borderline thresholds.
[EXPLICIT]

## Process

1. Load all local `assets/` files and `references/certification-checklist.md`.
2. Capture S1-S9 evidence.
3. Evaluate F/B/W, C1-C5, rubric, and M1-M5 as applicable.
4. Compare with prior certification when provided.
5. Validate JSON report with `scripts/validate_certification_report.py`.

## Guardrails

- No edits to the target skill.
- No certification level without formula evidence.
- No MOAT claim while any M-check fails or is skipped.
