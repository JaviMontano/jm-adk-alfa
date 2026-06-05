# Certify Skill — Knowledge Graph

## Core Concepts

- `certify-skill`: read-only certification gate.
- `certification-phases`: S/F/B/W/C/M check inventory.
- `level-policy`: MOAT/CERTIFIED/CONDITIONAL/BLOCKED formulas.
- `rubric-scores`: 10-dimension score table.
- `report-contract`: required certification report structure.
- `false-pass`: report whose level violates formula evidence.

## Dependencies

- Upstream: target skill directory and optional prior certification.
- Internal: assets, checklist, fixtures, validator.
- Downstream: release decision, review doc, ledger closure.

## Skill Relationships

- Complements `quality-gatekeeper`.
- Complements `benchmark-skill`.
- Complements `surgeon-skill` for repair before re-certification.
