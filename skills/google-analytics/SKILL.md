---
name: google-analytics
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Google Analytics 4 and Google Tag Manager measurement planning for web apps:
  GA4 property/data-stream readiness, event taxonomy, recommended/custom events,
  key-event planning, consent/privacy checks, GTM/Google tag debug checklists,
  and offline deterministic implementation plans. Use for "google analytics",
  "GA4", "GTM", "event tracking", "conversion tracking", "key events",
  "Measurement Protocol", "Tag Assistant", "DebugView", or analytics tagging.
status: production
tags: [google-analytics, ga4, gtm, tag-platform, measurement, analytics]
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Google Analytics

## TL;DR

Use this skill to produce a deterministic offline GA4/GTM measurement plan before
any live analytics tagging work. Start with
`scripts/compile-google-analytics.py` when the request can be represented as
structured JSON. The compiler reads only local `assets/` and fixture/input JSON;
it does not call Google Analytics, Google Tag Manager, OAuth, MCP, or the
network. [CODE]

## Source Order

1. Use `assets/source-map.md` for the official Google source set. [CODE]
2. Use `assets/ga4-gtm-plan-schema.json` as the structured input contract. [CODE]
3. Use `assets/event-taxonomy-policy.json` for event classes, naming, parameters, Measurement Protocol, and key-event rules. [CODE]
4. Use `assets/privacy-consent-policy.json` before recommending collection or tag mutations. [CODE]
5. Use `assets/tag-mutation-confirmation-policy.json` before recommending any live tag/container/key-event mutation. [CODE]
6. Use `assets/debug-checklist-policy.json` for GTM Preview, Tag Assistant, GA4 DebugView, Realtime, and publish checks. [CODE]

## Procedure

### Step 1: Discover Measurement State

- Confirm whether the GA4 account, property, web data stream, measurement ID, and enhanced measurement review are known. [DOC]
- Identify the primary business goal, reporting questions, KPIs, implementation surface, and owner. [CODE]
- Treat Measurement Protocol as supplemental to tagging, never as a standalone replacement. [DOC]

### Step 2: Design Event Taxonomy

- Classify each event as automatic, enhanced measurement, recommended, or custom. [DOC]
- Prefer official recommended events such as `login`, `sign_up`, `generate_lead`, `purchase`, and checkout events when the business action matches. [DOC]
- Use custom events only when automatic, enhanced, or recommended events do not fit. [DOC]
- Enforce lowercase snake_case event and parameter names through the local schema. [CODE]
- Reject high-risk PII parameters before producing a mutation-ready plan. [CODE]

### Step 3: Plan Key Events And Tags

- Map each key event to an event already present in the taxonomy. [CODE]
- Document business reason, value strategy, currency requirement, expected volume, and owner for every key event. [CODE]
- Plan GTM/Google tag work as a checklist first: platform, tag type, tag name, trigger, consent checks, verification, and mutation flag. [CODE]
- Require human confirmation before recommending live tag/container/key-event mutations. [CODE]

### Step 4: Validate Privacy And Debugging

- Document region profile, CMP state, Consent Mode plan, default denied behavior, ads personalization review, data redaction review, PII policy, and legal review owner. [CODE]
- Verify in GTM Preview and Tag Assistant before publish. [DOC]
- Verify event receipt and parameters in GA4 DebugView and Realtime. [DOC]
- Keep the compiler offline; live execution is a separate human-reviewed step. [CODE]

## Offline Compiler

```bash
python3 skills/google-analytics/scripts/compile-google-analytics.py \
  --input skills/google-analytics/scripts/fixtures/google-analytics-input.json
```

Run the deterministic fixture suite:

```bash
bash skills/google-analytics/scripts/check.sh
```

## Quality Criteria

- [ ] Output includes schema-stable GA4/GTM measurement strategy. [CODE]
- [ ] Event taxonomy covers event class, official recommended-event fit, trigger, parameters, privacy review, and debug expectation. [CODE]
- [ ] Key-event plan is tied to named events and business value. [CODE]
- [ ] Privacy/consent checks are explicit before collection or mutation. [CODE]
- [ ] GTM/Google tag checklist includes platform, tag type, trigger, consent checks, verification, and publish/debug gates. [CODE]
- [ ] Human-confirmation gate blocks mutating tag/container/key-event recommendations. [CODE]
- [ ] Script checks stay offline and deterministic. [CODE]
- [ ] Evidence tags are present on claims. [CODE]

## Anti-Patterns

- Treating Measurement Protocol as the only collection method for a web stream. [DOC]
- Creating custom events when an official recommended event matches the action. [DOC]
- Duplicating automatic or enhanced measurement events without a documented gap. [DOC]
- Sending email, phone, full name, raw address, or other direct PII as event parameters. [CODE]
- Recommending GTM publish or GA4 key-event changes without human confirmation. [CODE]
- Using UI copy, campaign names, or temporary labels as event names. [INFERENCE]

## Related Skills

- `funnel-analytics` for interpreting funnel performance after data collection is safe. [INFERENCE]
- `landing-pages` for conversion surface design that feeds GA4 events. [INFERENCE]
- `google-sheets-mcp` for deterministic spreadsheet reporting exports after data is read safely. [INFERENCE]

## Assumptions & Limits

- The compiler validates a plan/checklist contract; it does not prove that a GA4 property, web stream, GTM container, OAuth grant, or browser tag exists. [CODE]
- Live implementation still depends on account permissions, site code access, GTM workspace state, consent tooling, and user confirmation. [INFERENCE]
- This skill is not legal advice; privacy/legal sufficiency remains with the accountable human owner. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|---|---|
| User wants Measurement Protocol only | Reject and restate that Measurement Protocol supplements tagging. |
| User provides CamelCase or spaced event names | Reject through schema; use lowercase snake_case. |
| User asks to mark every event as key event | Require business reason, owner, expected volume, and value strategy per key event. |
| User provides PII parameter | Block plan until removed or replaced with non-PII surrogate. |
| User asks to publish GTM changes | Return confirmation gate and debug checklist before recommending live mutation. |
