---
name: session-end-cleanup-deep
type: variation
version: 2.1.0
description: "Deep closeout for long sessions, PR lifecycle work, and cross-session handoff."
---

# Session End Cleanup - Deep Mode

## When To Use

Use deep mode when the session includes PR creation, CI, merge, branch cleanup,
multiple validations, durable log updates, or unresolved blockers.

## Execution

1. Read `assets/output-contract.json`, `assets/evidence-policy.json`, and
   `assets/update-policy.json`.
2. Inspect git status, diff summary, command evidence, PR/CI/merge state, and
   relevant task artifacts.
3. Capture decisions, assumptions, risks, and insights separately.
4. Review durable updates against the active tasklog/changelog boundary.
5. Run guardian validation with explicit pass/block rationale.

## Output

Return the full closeout packet plus a short first action for the next session.
Never collapse failed checks into a generic risk statement.
