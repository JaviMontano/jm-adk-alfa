# Example Input

Run `session-manager` for feature `billing-export`.

Available local artifacts:

- `.specify/context.json` exists and records stage `specified`.
- `.specify/plans/plan-20260606-billing-export.md` exists.
- `tasks.md` is missing.
- `tests/features/billing-export.feature` is missing.

Return the current stage, evidence, authorized persistence actions, Guardian
decision, and next action. Do not write files unless the stage update is
authorized by the repo workflow.
