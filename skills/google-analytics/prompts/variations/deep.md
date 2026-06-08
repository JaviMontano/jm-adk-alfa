---
name: google-analytics-deep
type: variation
version: 2.1.0
description: "Google Analytics deep mode for full GA4/GTM measurement architecture review."
---

# Google Analytics — Deep Mode

## When To Use

Use deep mode for new implementations, migrations, consent-sensitive work, Measurement Protocol supplements, high-impact funnel measurement, or GTM container changes.

## Execution

1. Read all deterministic assets under `assets/`.
2. Read `knowledge/body-of-knowledge.md` and `examples/example-output.md`.
3. If a JSON plan is available, run `scripts/compile-google-analytics.py`; otherwise, draft the JSON contract fields before producing the plan.
4. Review:
   - GA4 property/data-stream readiness.
   - Automatic/enhanced/recommended/custom event split.
   - Event and parameter naming.
   - Key-event business rationale.
   - Consent Mode and PII controls.
   - GTM/Google tag mutation scope.
   - Measurement Protocol supplement constraints.
   - GTM Preview, Tag Assistant, GA4 DebugView, Realtime, and network checks.
5. Block mutation-ready recommendations unless human confirmation is explicit.

## Output

- Full Markdown plan with all sections from `templates/output.md`.
- Evidence and residual risks.
- Validation commands when skill files or scripts change.
