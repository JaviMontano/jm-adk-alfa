# Audit Security Knowledge Graph

## Core Nodes

- `audit-security`: read-only static plugin security audit.
- `activation-policy`: activation, clarification, refusal, and false-positive routing.
- `scan-policy`: six scan categories, severities, statuses, and placeholders.
- `report-contract`: required output sections and fields.
- `evidence-policy`: evidence and remediation requirements.
- `offline-validator`: deterministic JSON report validation script.
- `remediation-plan`: actions required for CRITICAL and WARNING findings.

## Relationships

- The skill uses activation, scan, and evidence policies.
- The skill produces a report matching the local contract.
- The validator checks category coverage, finding IDs, severity counts, placeholder handling, and remediation.
- The scan policy requires remediation for CRITICAL and WARNING findings.
