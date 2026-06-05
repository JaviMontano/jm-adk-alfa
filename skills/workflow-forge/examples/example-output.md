# Example Output

## Summary

Workflow `/jm:skill-audit-ready` is a four-phase skill-readiness workflow that
clarifies the target, inspects the package, applies scoped improvements, and
verifies PR readiness.

## Frontmatter

```yaml
description: Review one skill and prepare a granular PR readiness decision.
command: /jm:skill-audit-ready
skills_involved:
  - x-ray-skill
  - certify-skill
agents_coordinated:
  - workflow-forge-lead
  - workflow-forge-support
  - workflow-forge-guardian
```

## Phase Map

| # | Phase | Agents | Output | Checkpoint |
|---:|---|---|---|---|
| 1 | Clarify Target | workflow-forge-lead | Confirmed skill, branch, write scope | Skill path and branch are explicit |
| 2 | Inspect Package | workflow-forge-support | Gap list with evidence | All core files and scripts inspected |
| 3 | Apply Scoped Improvements | workflow-forge-lead | Updated skill package and review doc | Diff contains only approved paths |
| 4 | Verify Readiness | workflow-forge-guardian | PR readiness verdict | DoD, script checks, check.sh, and scoped diff check pass |

## Quality Gates

- Frontmatter has command, description, skills, and agents.
- Every phase has agents, inputs, outputs, and checkpoint.
- Final phase is verification.
- Ledger remains untouched.

## Validation

- `scripts/compile-workflow-forge.py` can compile the structured workflow spec.
- Invalid one-phase, missing-verification, and prohibited-stack fixtures fail
  closed.
