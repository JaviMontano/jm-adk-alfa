# Find Skills Assets

These assets make skill discovery recommendation reports deterministic and offline-validatable.

## Inventory

- `source-policy.json`: source scopes, source types, and remote evidence requirements.
- `scoring-rubric.json`: stable score dimensions, weights, tiers, and confidence labels.
- `install-policy.json`: confirmation and auto-installation guardrails.
- `report-contract.json`: report schema used by the offline validator.

## Deterministic Use

Use exact `reference_date` values. Do not use moving terms such as `today`, `tomorrow`, `soon`, or `TBD`. Remote candidates must include a frozen snapshot date; scripts validate fixtures only and must not call the network.
