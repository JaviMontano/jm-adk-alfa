# Domain Knowledge - Workflow Forge

## Overview

Workflow Forge creates repeatable slash-command workflows. It is strongest when
the user needs a reusable operational sequence with agent accountability,
phase-level checkpoints, and a deployable workflow definition.

## Workflow vs Nearby Artifacts

| Artifact | Use when | Not enough when |
|---|---|---|
| Checklist | One-off task completion | Agents, handoffs, or command routing matter |
| Runbook | Human operational procedure | Slash-command activation and agent routing matter |
| Workflow | Repeatable command flow with phases | The request is only a simple answer |
| Skill | Reusable capability and trigger contract | The user only needs one workflow inside a skill |

## Evidence Taxonomy

- `[EXPLICIT]`: directly stated in user input, repo files, or workflow spec.
- `[INFERRED]`: derived from available evidence and marked as a hypothesis.
- `[OPEN]`: unresolved dependency requiring user or catalog confirmation.

## Design Heuristics

1. Start with the command and deliverable.
2. Keep the phase map small enough to execute.
3. Make every checkpoint observable.
4. Assign agents to work, not vibes.
5. End with verification of the deliverable, not a summary of effort.

## Anti-Patterns

| Anti-pattern | Risk | Safer alternative |
|---|---|---|
| Monolithic workflow | No control point between work chunks | Split into phase map |
| Agent placeholders | No accountability | Use real agent IDs or `[OPEN]` |
| Untestable gates | False readiness | Rewrite as binary evidence checks |
| Hidden stack assumptions | Policy drift | Validate with workflow policy |
