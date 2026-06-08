---
name: google-maps-integration-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the Google Maps Integration skill."
---

# Google Maps Integration — Self-Improvement

## Evaluate

1. [DOC] Is `knowledge/body-of-knowledge.md` current against official Google Maps Platform docs?
2. [CODE] Does `assets/maps-platform-plan-schema.json` still match compiler validation?
3. [CODE] Do positive and negative fixtures cover API selection, key restrictions, human confirmation, and no-price policy?
4. [CODE] Are templates producing useful API selection, data-flow, marker, accessibility, privacy, and billing/quota sections?
5. [INFERENCE] Are the 4 sub-agents covering security, accessibility, privacy, and offline determinism?
6. [INFERENCE] Has the related skill landscape changed?

## Improve

1. [DOC] Update body of knowledge with new official-doc findings.
2. [CODE] Update schema and fixtures together when the compiler contract changes.
3. [CODE] Refine quality criteria based on validation failures.
4. [CODE] Update knowledge graph with new APIs, libraries, or gates.
5. [CODE] Test templates with edge-case inputs.
6. [INFERENCE] Propose governance update only if ambiguity repeats.

## Trigger

Run this meta-prompt when:
- Skill hasn't been reviewed in 30+ days
- User reports unexpected output quality
- New related skills added to the kit
- Insights file updated with relevant patterns
