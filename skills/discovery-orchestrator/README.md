# Discovery Orchestrator

Coordinates JM Labs discovery phases 0-6 by sequencing canonical skills, enforcing G1/G2/G3 gates, and preserving the separation between orchestration and analysis. It does not create domain findings, implementation plans, or prices.

## Triggers

- `discovery-orchestrator`
- `plan discovery`
- `orchestrate discovery`
- `sequence discovery skills`
- `manage G1 gate`
- `resume discovery state`
- `handoff discovery`

## Allowed Tools

- Read
- Write
- Edit
- Bash
- Glob
- Grep

## Deterministic Resources

- `assets/phase-contract.json` defines allowed phase ids and order.
- `assets/skill-sequence-contract.json` defines canonical discovery skills.
- `assets/gate-policy.json` defines G1, feasibility checkpoint, G2, and G3.
- `assets/non-analysis-boundary.json` defines forbidden analysis and pricing fields.
- `assets/report-contract.json` defines the JSON packet contract.
- `scripts/check.sh` validates deterministic packet fixtures offline.

## Quick Use

Use this skill to produce a pipeline state packet, gate decision, discovery dashboard, or handoff readiness report. Route domain analysis work to the downstream skill named in the sequence.

## Output Format

Markdown or JSON with exact date, mode, phase plan, skill sequence, gates, handoff, boundary checks, validation, and risks. Every claim requires an evidence tag.
