# Analytics Events

Use this skill to design product analytics event taxonomies and tracking plans that are specific, implementable, testable, and privacy-aware.

## Trigger Signals

- Event taxonomy or event naming conventions.
- Tracking plan for Segment, RudderStack, Amplitude, Mixpanel, GA4, Snowplow, warehouse events, mobile SDKs, web SDKs, or backend events.
- Funnel instrumentation, product activation events, checkout events, onboarding events, lifecycle events, or account/billing events.
- Event property schema, identity resolution, anonymous/user id merge policy, privacy handling, or QA validation.

## Deliverable

The skill produces a tracking plan with:

- product surfaces and domains
- event names and triggers
- event owners
- platforms and destinations
- required properties and types
- identity policy
- privacy classification
- implementation owner and QA method
- validation checks and risks

## Assets

`assets/` contains static JSON policies for naming, properties, identity, tracking plans, evidence, and validation. These files are the deterministic contract for the skill.

## Scripts

Run `bash skills/analytics-events/scripts/check.sh` to validate JSON fixtures offline. The script accepts valid tracking plans and rejects missing evidence, bad naming, missing identity, unknown properties, sensitive properties without privacy review, and incomplete validation checks.
