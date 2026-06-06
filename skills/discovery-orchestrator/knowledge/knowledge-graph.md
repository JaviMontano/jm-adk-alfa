# Discovery Orchestrator — Knowledge Graph

## Core Concepts

- `discovery-orchestrator`: governance skill that coordinates discovery phases 0-6.
- `phase-plan`: ordered state register for phases `0`, `1`, `2`, `3`, `3b`, `4`, `4b`, `5a`, `5b`, and `6`.
- `skill-sequence`: canonical downstream skills with owners, dependencies, statuses, and outputs.
- `gate`: explicit G1, feasibility, G2, or G3 decision.
- `handoff`: next skill and evidence required before continuing.
- `boundary-check`: assertion that the packet contains no domain analysis, downstream execution, or prices.

## Relationships

- `discovery-orchestrator` coordinates `phase-plan`.
- `phase-plan` orders `skill-sequence`.
- `skill-sequence` produces `deliverables`.
- `gate` validates phase transitions.
- `boundary-check` blocks analysis leakage.
- `scripts/check.sh` validates `assets/report-contract.json` fixtures offline.
