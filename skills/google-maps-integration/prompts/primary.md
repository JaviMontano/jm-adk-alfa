---
name: google-maps-integration-primary
type: execution
version: 2.0.0
description: "Execute the Google Maps Integration workflow with triad orchestration."
triad:
  lead: "google-maps-integration-lead"
  support: "google-maps-integration-support"
  guardian: "google-maps-integration-guardian"
---

# Google Maps Integration — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. **Load knowledge**: Read `knowledge/body-of-knowledge.md`
2. **Load assets**: Read `assets/manifest.json`, `assets/maps-platform-plan-schema.json`, and the policy asset relevant to the request.
3. **Check guardrails**: Read `references/guardrails/*.json` when available.
4. **Lead** (`google-maps-integration-lead`): Build or validate a schema-compliant offline plan input for `{{task}}`.
   - [CODE] Select APIs and libraries from `assets/api-selection-policy.json`.
   - [CODE] Apply key restrictions from `assets/api-key-restriction-policy.json`.
   - [CODE] Apply Places, Geocoding, and Directions data-flow controls from `assets/data-flow-policy.json`.
   - [CODE] Apply marker/accessibility controls from `assets/marker-accessibility-policy.json`.
5. **Support** (`google-maps-integration-support`): Review for security, accessibility, privacy, billing/quota exposure, and offline determinism.
6. **Guardian** (`google-maps-integration-guardian`): Validate.
   - [CODE] Evidence tags complete.
   - [CODE] No monetary prices.
   - [CODE] Human confirmation is present.
   - [CODE] External API calls remain disabled.
   - [CODE] Output follows `templates/output.md` or `templates/output.html`.

## Output

- [CODE] Primary deliverable for `{{task}}` in `{{output_format}}`.
- [CODE] Evidence tags on every claim.
- [CODE] API selection, key restrictions, data flow, marker clustering, accessibility, privacy, billing/quota checklist, human confirmation, and residual risks.
- [CONFIG] No external API calls.
- [CONFIG] No monetary prices.
- [CODE] Confidence score (>= 0.95).
