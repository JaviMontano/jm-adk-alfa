# Design Skill Assets

These assets make skill design deterministic and offline-validatable.

## Inventory

- `frontmatter-policy.json`: required fields, supported fields, name pattern, and allowed substitutions.
- `body-policy.json`: procedure, quality, anti-pattern, and edge-case thresholds.
- `tool-policy.json`: least-privilege tool profiles.
- `report-contract.json`: JSON design spec contract.

## Deterministic Use

Validate specs with exact `reference_date` values. Produce a reviewable design spec only; do not write final skill files from this skill.
