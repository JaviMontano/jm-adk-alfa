# Quality Gatekeeper — Knowledge Graph

## Core Concepts

- `quality-gatekeeper`: read-only gate decision skill.
- `gate-criteria`: G0-G3 criterion map.
- `report-contract`: required report structure.
- `evidence-policy`: evidence tags and assumption threshold.
- `score-history-entry`: proposed ledger output.
- `sequential-gate-order`: G0 before G1 before G2 before G3.
- `false-pass`: blocked report that incorrectly claims allow.

## Dependencies

- Upstream: artifacts, prior gate records, PR checks, command outputs.
- Internal: assets, fixtures, validator, templates.
- Downstream: release packet, score-history update, PR merge decision.

## Skill Relationships

- Complements `constitution-compliance`.
- Complements `output-contract-enforcer`.
- Must not replace generic quality writing or Lighthouse-only skills.
