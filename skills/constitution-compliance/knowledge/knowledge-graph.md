# Constitution Compliance — Knowledge Graph

## Core Concepts

- `constitution-compliance`: read-only audit skill.
- `constitution-v6-principles`: 18-principle source map.
- `report-contract`: required sections and allowed statuses.
- `severity-policy`: P0-P3 and delivery decision mapping.
- `gate-impact`: G0-G3 release effect.
- `missing-evidence`: fail-closed proof gap.
- `false-pass`: blocked assurance without matrix evidence.

## Dependencies

- Upstream: artifact, gate context, evidence sources.
- Internal: assets, templates, fixtures, validator.
- Downstream: release packet, PR gate decision, remediation plan.

## Skill Relationships

- Complements `quality-gatekeeper` for delivery readiness.
- Complements `constitution-compliance` review docs and ledger closure.
- Must not replace `agent-constitution-creator` or generic legal analysis.
