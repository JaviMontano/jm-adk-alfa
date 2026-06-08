# Google Analytics — Body of Knowledge

## Canon

- [DOC] GA4 setup begins with account, property, data stream, and tagging readiness before API or reporting work.
- [DOC] GA4 events measure user interactions and feed reports.
- [DOC] GA4 event classes are automatic, enhanced measurement, recommended, and custom.
- [DOC] Recommended events should be used when the business action matches the official reference because they unlock standardized reporting behavior.
- [DOC] Custom events are appropriate only when no automatic, enhanced, or recommended event fits.
- [DOC] Measurement Protocol sends server-to-server or offline events, but it is intended to augment tagging, not replace gtag, GTM, or Firebase tagging.
- [DOC] Consent and privacy compliance are implementation responsibilities; Consent Mode adjusts Google tag behavior based on user consent choices.
- [DOC] Google Tag Manager supports tag management with error checking, security controls, versioning, and team collaboration utilities.
- [DOC] GTM Preview and Tag Assistant support pre-publish debugging; GA4 DebugView and Realtime support event receipt checks.

## Local Skill Contract

- [CODE] `assets/ga4-gtm-plan-schema.json` is the stable structured input contract.
- [CODE] `assets/event-taxonomy-policy.json` encodes event taxonomy, naming rules, key-event rules, and Measurement Protocol limits.
- [CODE] `assets/privacy-consent-policy.json` blocks high-risk PII and unresolved consent/privacy ownership.
- [CODE] `assets/tag-mutation-confirmation-policy.json` requires `human_confirmation.status=confirmed` before mutation-ready recommendations.
- [CODE] `assets/debug-checklist-policy.json` defines GTM Preview, Tag Assistant, DebugView, Realtime, and publish gates.
- [CODE] `scripts/compile-google-analytics.py` renders a deterministic offline plan and never calls Google, OAuth, MCP, or the network.

## Event Taxonomy Rules

| Rule | Evidence | Handling |
|---|---|---|
| Prefer automatic/enhanced coverage before custom events | [DOC] | Inventory built-in coverage first. |
| Prefer recommended events for matching business actions | [DOC] | Use official names such as `sign_up`, `login`, `generate_lead`, `purchase`, and checkout events. |
| Use custom events only for product-specific gaps | [DOC] | Require `custom_event_justification`. |
| Use lowercase snake_case names | [CODE] | Enforced by local schema for deterministic reporting hygiene. |
| Keep PII out of parameters | [CODE] | High-risk PII blocks compilation. |

## Key-Event Rules

- [CODE] A key event must reference an event already present in the taxonomy.
- [CODE] A key event must include business reason, value strategy, currency requirement, expected volume, and owner.
- [CODE] Monetary key events require `currency_required=true`.
- [INFERENCE] Marking too many events as key events reduces reporting signal and should be challenged.

## Consent And Privacy

- [DOC] Implementers are responsible for applicable consent and privacy compliance.
- [DOC] Consent Mode is the Google tag mechanism for adjusting behavior based on user consent choices.
- [CODE] The local contract requires region profile, CMP state, Consent Mode plan, default denied behavior, ads personalization review, data redaction review, PII policy, and legal review owner.
- [CODE] Email, phone, full name, address, government ID, credit card, password, raw IP, and high-risk PII parameters are blocked by policy.

## Debug And Release

- [DOC] GTM Preview launches Tag Assistant so the implementer can inspect tags that fired and firing order before publish.
- [DOC] Tag Assistant debug mode shows tag firing and data layer exchanges.
- [DOC] GA4 DebugView and Realtime support event/parameter verification.
- [CODE] The offline plan requires debug and publish gates before live mutation recommendations.

## Quality Metrics

| Metric | Target | How to Measure |
|---|---|---|
| Schema validity | 100% | `scripts/check.sh` and `validate-skill-scripts.py` |
| Evidence coverage | 100% | Claims tagged with evidence markers |
| Offline determinism | 100% | No network/API/OAuth/MCP calls in scripts |
| Mutation safety | 100% | Human confirmation required for tag/container/key-event mutations |

## References

- [DOC] `assets/source-map.md`
- [CODE] `assets/manifest.json`
