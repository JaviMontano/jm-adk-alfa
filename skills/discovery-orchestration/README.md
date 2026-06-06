<!--
generated-by: scripts/scaffold-skill.py
generated-for: discovery-orchestration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Discovery Orchestration

Sequence a discovery pipeline with explicit phases, dependencies, quality gates,
deliverables, owners, blockers, and validation evidence.

## Triggers

- discovery-orchestration
- discovery pipeline
- orchestrate discovery
- gate enforcement
- deliverable tracking
- discovery dashboard

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a discovery engagement needs a deterministic operating plan:
which skills run, in what order, which outputs unblock the next phase, and what
evidence proves completion.

## Output Format

Markdown or JSON with:

- Pipeline summary and scope
- Phase and skill sequence
- Dependency graph
- Quality gates with pass/block criteria
- Deliverable register
- Blockers and next actions
- Validation evidence
- Risks and assumptions

JSON orchestration packets can be validated offline with:

```bash
bash skills/discovery-orchestration/scripts/check.sh
```
