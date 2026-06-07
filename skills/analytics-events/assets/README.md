# Analytics Events Assets

These static JSON assets define the deterministic contract for analytics event taxonomy and tracking plan outputs.

## Files

- `manifest.json`: DoD asset manifest.
- `analytics-events-contract.json`: Required report sections and validation checks.
- `naming-policy.json`: Event naming convention and allowed actions.
- `property-policy.json`: Event property fields, types, PII classes, and handling.
- `identity-policy.json`: Identity and deduplication requirements.
- `tracking-plan-policy.json`: Destination, implementation, QA, and rollout fields.
- `evidence-policy.json`: Evidence tags and provenance requirements.

## Determinism

Assets are static and offline. They do not use network calls, time, or randomness.
