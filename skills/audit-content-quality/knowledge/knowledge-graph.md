# Audit Content Quality Knowledge Graph

## Core Nodes

- `audit-content-quality`: read-only skill for structural `SKILL.md` quality scoring.
- `activation-policy`: positive, negative, and clarification routing.
- `six-dimension-rubric`: score bounds, grade thresholds, bottom ordering, and gap threshold.
- `report-contract`: required output sections and fields.
- `evidence-policy`: rationale and evidence-tag requirements.
- `offline-validator`: deterministic report validation script.
- `bottom-skill-priorities`: bottom performers ordered by total score.
- `systematic-gap-detection`: dimension averages below `6.0`.

## Relationships

- The skill uses activation, rubric, and evidence policies.
- The skill produces a report matching the local contract.
- The validator checks formula-derived totals, grades, averages, bottom skills, and gaps.
- Bottom priorities and systematic gaps come from the rubric policy, not reviewer preference.
