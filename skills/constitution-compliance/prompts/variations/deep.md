---
name: constitution-compliance-deep
type: variation
version: 2.0.0
description: "Constitution Compliance deep evidence mode."
---
# Constitution Compliance Deep Mode

Use when the artifact is high-risk, spans multiple gates, has conflicting
requirements, or needs a release decision. [EXPLICIT]

## Execution

1. Read the artifact and cited evidence before scoring.
2. Load the v6.0.0 principles, report contract, and severity policy.
3. Produce the 18-row matrix and G0-G3 impact table.
4. Add violation and missing-evidence tables.
5. Explain confidence; cap confidence below `0.80` when any required evidence is
   missing.
6. Validate JSON reports with the local validator when available.

## Guardrails

- No network, time, or random dependency.
- No stale target version except as a finding.
- No release allow decision while P0/P1 findings or required missing evidence
  remain.
