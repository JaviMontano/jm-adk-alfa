---
name: google-analytics-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve the Google Analytics skill against official GA4/GTM sources."
---

# Google Analytics — Self-Improvement

## Evaluate

1. Check whether official GA4 collection, event, recommended-event, Measurement Protocol, Google tag, and GTM web docs changed.
2. Verify `assets/source-map.md` still contains the primary source set.
3. Confirm `assets/ga4-gtm-plan-schema.json` still supports measurement strategy, taxonomy, key events, consent/privacy, debug, and confirmation.
4. Run `bash skills/google-analytics/scripts/check.sh`.
5. Confirm examples, evals, prompts, templates, and knowledge still reference the deterministic assets.
6. Confirm no script calls Google Analytics, GTM, OAuth, MCP, or the network.

## Improve

1. Update `assets/` first when a rule changes.
2. Update the compiler and fixtures second.
3. Update examples/evals/templates/prompts/knowledge third.
4. Run the validation commands and record residual limits in the review file.

## Trigger

Run this meta-prompt when:

- Official Google Analytics or Tag Platform guidance changes.
- A user reports bad event naming, privacy, or key-event guidance.
- A new analytics implementation surface is added to JM-ADK.
- The skill has not been reviewed in 30+ days.
