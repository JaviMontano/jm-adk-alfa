# Design Agent Assets

These assets make plugin agent design deterministic and offline-validatable.

## Inventory

- `frontmatter-policy.json`: supported, required, forbidden, and mutually exclusive frontmatter fields.
- `constraint-policy.json`: plugin subagent constraints and correct workarounds.
- `maxturns-policy.json`: deterministic maxTurns formula.
- `report-contract.json`: JSON design spec contract.

## Deterministic Use

Validate specs with exact `reference_date` values. Do not write deployable agent files from this skill; produce a reviewable spec and validate it offline.
