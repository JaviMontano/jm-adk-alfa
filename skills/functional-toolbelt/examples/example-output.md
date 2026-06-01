<!--
generated-by: scripts/scaffold-skill.py
generated-for: functional-toolbelt
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The Loan Origination analysis uses all six functional toolbelt techniques and produces a traceable package from events to acceptance tests.

## Deterministic Report

- Run: `python3 skills/functional-toolbelt/scripts/compile-functional-toolbelt.py --input skills/functional-toolbelt/scripts/fixtures/toolbelt-input.json`
- Output sections: Event Storming, Story Mapping, Business Rule Extraction, Acceptance Criteria, Traceability Matrix, Anti-Pattern Detection.

## Key Outputs

- Event storming identifies `Application Submitted`, `Credit Checked`, and `Offer Accepted`.
- Story map includes `US-001` through `US-004` across MVP and Phase 2.
- Business rules `BR-001` and `BR-002` link to use cases.
- Traceability rows connect `REQ-001` and `REQ-002` to flows, tests, and acceptance criteria.
- Anti-pattern scan flags ambiguity and missing-exception risks with concrete fixes.

## Validation

- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill functional-toolbelt`
- `python3 -B scripts/validate-skill-dod.py --skill functional-toolbelt`
