---
name: workflow-forge-primary
type: execution
version: 2.0.0
triad:
  lead: "workflow-forge-lead"
  support: "workflow-forge-support"
  guardian: "workflow-forge-guardian"
---

# Workflow Forge - Execute

1. Read `SKILL.md` sections `When to Activate`, `Before Forging`,
   `Workflow Contract`, and `Validation Gate`.
2. If a structured spec is available, run
   `scripts/compile-workflow-forge.py` or `scripts/check.sh` for deterministic
   validation.
3. If the request is free form, extract command, deliverable, agents, skills,
   phases, checkpoints, and quality gates before writing.
4. Mark unknown agents or skills as `[OPEN]`; do not invent catalog entries.
5. Produce a workflow definition with frontmatter, phase map, checkpoints,
   quality gates, failure handling, example dialogue, and validation evidence.
6. Validate that the first phase clarifies/plans, the final phase verifies, and
   every phase has agents, inputs, outputs, and checkpoints.
