---
name: certify-skill-primary
type: execution
version: 2.0.0
description: "Execute the Certify Skill workflow."
triad:
  lead: "certify-skill-lead"
  support: "certify-skill-support"
  guardian: "certify-skill-guardian"
---

# Certify Skill Execute

## Objective

Certify one skill directory with the deterministic phase inventory, rubric, and
certification formula. [EXPLICIT]

## Execution Steps

1. Confirm the target is a skill directory or explicit skill artifact.
2. Load `assets/` contracts and `references/certification-checklist.md`.
3. Run or inspect S1-S9 structural checks.
4. Evaluate F/B/W content checks and C1-C5 systemic checks.
5. Score all 10 rubric dimensions with evidence.
6. Apply the exact certification formula.
7. Evaluate M1-M5 only when phases 1-4 are CERTIFIED.
8. Validate JSON reports with the local script when available.
