<!--
generated-by: scripts/scaffold-skill.py
generated-for: discovery-orchestration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The discovery pipeline is ready to run after G0 because dependencies are acyclic,
phase gates are explicit, and all deliverables have owners and validation
criteria. [CONFIG][INFERENCIA]

## Pipeline

| phase | skills | gate | status |
|-------|--------|------|--------|
| P1 Intake | input-analysis | G0 | ready |
| P2 Discovery | stakeholder-analysis, current-state-analysis | G1 | ready |
| P3 Requirements | requirements-engineering | G2 | ready |
| P4 Architecture | system-architecture, risk-analysis | G3 | ready |
| P5 Package | discovery-reporting | G4 | ready |

## Dependencies

- `input-analysis` -> `requirements-engineering` [CONFIG]
- `stakeholder-analysis` -> `requirements-engineering` [CONFIG]
- `requirements-engineering` -> `system-architecture` [CONFIG]
- `risk-analysis` -> `discovery-reporting` [CONFIG]

## Quality Gates

- G0: briefing files exist and input gaps are listed. [DOC]
- G1: stakeholder and current-state outputs have owners and evidence. [DOC]
- G2: requirements brief is validated before architecture starts. [DOC]
- G3: architecture and risk outputs cross-reference requirements. [DOC]
- G4: discovery report includes all validated deliverables. [DOC]

## Deliverables

| id | owner | source_skill | status | validation |
|----|-------|--------------|--------|------------|
| D1 | Discovery Lead | input-analysis | validated | gap list and assumptions tagged |
| D2 | Product Lead | stakeholder-analysis | validated | stakeholder roles and decisions listed |
| D3 | BA Lead | requirements-engineering | validated | requirements trace to input sources |
| D4 | Architect | system-architecture | validated | context diagram links requirements |
| D5 | Delivery Lead | discovery-reporting | validated | package references all prior outputs |

## Validation

- Dependency graph has no cycle. [CONFIG]
- Each phase transition has an explicit pass/block gate. [CONFIG]
- Remaining risk: stakeholder availability may block D2 if notes are stale.
  [SUPUESTO]
