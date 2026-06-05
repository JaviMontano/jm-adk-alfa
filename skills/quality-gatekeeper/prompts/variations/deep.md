---
name: quality-gatekeeper-deep
type: variation
variant: deep
---
# Quality Gatekeeper Deep Analysis

Use when the release decision spans multiple gates, has conflicting evidence,
or will be used as PR/merge evidence. [EXPLICIT]

## Process

1. Read all supplied artifacts and prior gate records.
2. Load the local assets in `assets/`.
3. Evaluate each scoped criterion.
4. Calculate assumption ratio.
5. Build violations, missing evidence, and remediation tables.
6. Validate the JSON report with `scripts/validate_gate_report.py` when a JSON
   report exists.

## Guardrails

- No network, current-time, or random dependency.
- No `allow` decision while required criteria are failed or missing.
- No out-of-sequence gate approval.
