# Funnel Design - Body of Knowledge

## Canon
Funnel design defines the intended buyer journey before launch. It differs from `funnel-analytics`: design creates stage logic, content, scoring, and nurture; analytics measures what happened after instrumentation exists.

The deterministic funnel design path is:

1. Define product, offer, audience, goal, sales motion, and conversion event.
2. Map TOFU, MOFU, and BOFU stages to buyer intent.
3. Attach content assets, CTAs, metrics, owners, and evidence gaps to every stage.
4. Define lead scoring with fit, intent, and engagement dimensions.
5. Map score thresholds to lifecycle states.
6. Create nurture paths with triggers, delays, branch conditions, and exit criteria.
7. Define sales handoff and disqualification rules.

## Stage Logic

| Stage | Buyer intent | Content role | Common CTA |
|---|---|---|---|
| TOFU | Understand problem or opportunity | Educate and create relevance | Read, watch, subscribe |
| MOFU | Compare approaches and assess fit | Build trust and diagnose need | Download, attend, self-assess |
| BOFU | Decide vendor, plan, or next step | Reduce risk and trigger action | Book, trial, buy, talk to sales |

## Lead Scoring

Lead scoring must have business meaning. A score is valid only if the threshold changes treatment: content path, qualification state, owner, SLA, or sales handoff.

## Nurture Design

Every nurture path needs a trigger, message sequence, delay, branch rule, exit criteria, and owner. A path without exit criteria is an anti-pattern because contacts can remain in automation after conversion, disqualification, or inactivity.

## Required Evidence

- Audience segment and buying committee.
- Offer and conversion event.
- Sales motion: self-serve, product-led, sales-led, partner-led, or hybrid.
- Content inventory or explicit content gaps.
- CRM/email platform constraints when available.
- Consent/privacy constraints for outreach.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Stage completeness | 100% | TOFU/MOFU/BOFU all present |
| Content traceability | 100% | Every asset maps to stage, CTA, metric, owner |
| Scoring determinism | 100% | Thresholds map to lifecycle states |
| Nurture determinism | 100% | Every path has trigger, branch, exit |
| Handoff clarity | 100% | Sales-ready criteria are explicit |

## References
- `assets/funnel-design-schema.json`
- `assets/stage-content-model.json`
- `assets/lead-scoring-model.json`
- `assets/nurture-flow-schema.json`
- `assets/qualification-rules.json`
- `scripts/compile-funnel-design.py`
