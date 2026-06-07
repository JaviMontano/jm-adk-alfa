---
name: analytics-events
author: JM Labs (Javier Montano)
version: 1.0.1
description: >
  Event taxonomy, naming conventions, tracking plan, implementation. [EXPLICIT]
  Trigger: "analytics events"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Analytics Events

Analytics Events designs deterministic product and marketing event taxonomies, naming conventions, property contracts, identity rules, tracking plans, implementation handoffs, and validation gates. [EXPLICIT]

## When To Use

- The user asks for analytics events, event taxonomy, tracking plan, product instrumentation, funnel events, clickstream events, Segment/RudderStack/Amplitude/Mixpanel events, or naming conventions.
- The user needs event names, triggers, owners, property schemas, identity resolution, destinations, implementation handoff, QA checks, or privacy review.
- The user needs to rationalize duplicate or inconsistent events across web, mobile, backend, or server-side tracking.

## When Not To Use

- Dashboard visual design only.
- Warehouse modeling without event instrumentation.
- Ad copy, campaign strategy, or attribution modeling without tracking plan design.
- Generic SQL debugging.

## Deterministic Contract

Use the static assets in `assets/` as the contract and `scripts/` as the offline oracle. Do not depend on network access, wall-clock time, random sampling, or undocumented product assumptions. [EXPLICIT]

Required assets:
- `assets/analytics-events-contract.json` defines required report sections and validation checks.
- `assets/naming-policy.json` defines event naming rules and allowed actions.
- `assets/property-policy.json` defines property schema, types, PII classification, and required fields.
- `assets/identity-policy.json` defines user and anonymous identity requirements.
- `assets/tracking-plan-policy.json` defines destination, owner, trigger, and QA requirements.
- `assets/evidence-policy.json` defines evidence tags and provenance fields.

Offline validation:
- Use `scripts/validate_analytics_events.py` for structured JSON handoffs.
- Use `bash scripts/check.sh` to run deterministic fixture validation.
- Block final delivery when events lack owner, trigger, properties, identity policy, evidence, privacy handling, or validation checks.

## Procedure

### Step 1: Discover

- Identify product surfaces, user journeys, analytics destinations, implementation platforms, and current instrumentation.
- Extract evidence for source artifacts, product requirements, existing events, privacy constraints, and QA constraints.
- Record unknowns explicitly instead of inventing events or properties.

### Step 2: Design Taxonomy

- Define domains such as acquisition, activation, checkout, retention, billing, support, or admin.
- Use object_action names in lower snake_case.
- Prefer events that represent user-observable or system-confirmed facts.
- Avoid vague events such as `click`, `submit`, `page`, `success`, or `error` without object context.

### Step 3: Define Event Contract

For each event, specify:
- event name
- domain
- action
- trigger
- owner
- platforms
- destination tools
- required properties
- identity requirements
- privacy classification
- evidence references

### Step 4: Produce Tracking Plan

- Map each event to implementation owner, destination, QA method, rollout phase, and validation rule.
- Include server/client placement where relevant.
- Include deprecation or alias handling for duplicate events.

### Step 5: Validate

- Verify naming policy, property policy, identity policy, tracking plan policy, privacy policy, and evidence coverage.
- For structured handoffs, run `scripts/validate_analytics_events.py` or mirror its checklist.

## Quality Criteria

- [ ] Every event uses lower snake_case object_action naming.
- [ ] Every event has domain, action, trigger, owner, platforms, properties, and evidence.
- [ ] Every required property has type, description, requirement status, and PII classification.
- [ ] Identity policy covers `user_id`, `anonymous_id`, and merge behavior.
- [ ] Sensitive properties have privacy review and handling.
- [ ] Tracking plan maps every event to destination, implementation owner, and QA method.
- [ ] Validation includes naming, properties, identity, tracking plan, privacy, and evidence checks.
- [ ] If JSON handoff is requested, it passes `scripts/validate_analytics_events.py`.

## Assumptions And Limits

- Assumes the user can provide product journeys, surfaces, existing tracking, or desired funnel outcomes. [EXPLICIT]
- Does not replace legal or privacy review for regulated personal data. [EXPLICIT]
- Does not implement analytics SDK code unless explicitly requested; it defines the event contract and implementation handoff. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Empty or minimal input | Produce a gap report and minimum evidence request. |
| Conflicting event names | Preserve legacy aliases and propose canonical names with deprecation plan. |
| PII requested in properties | Mark privacy review as blocking and propose safe identifiers. |
| Multi-platform drift | Require platform coverage and QA checks per destination. |
| Server/client duplication | Choose system of record and define deduplication key. |
