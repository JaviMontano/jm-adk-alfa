---
name: google-analytics-quick
type: variation
version: 2.1.0
description: "Google Analytics quick mode for a compact GA4/GTM checklist."
---

# Google Analytics — Quick Mode

## When To Use

Use quick mode for a compact readiness or review checklist when the user does not need a full structured JSON compile.

## Execution

1. Load `SKILL.md` and `assets/event-taxonomy-policy.json`.
2. Produce only:
   - Property/data-stream readiness.
   - Event taxonomy summary.
   - Key-event candidates.
   - Privacy/consent blockers.
   - Debug checklist.
   - Human-confirmation gate.
3. Ask for missing critical inputs if the user requests mutation-ready GTM or GA4 key-event recommendations.

## Output

- Markdown.
- Evidence tags.
- No live Google Analytics, GTM, OAuth, MCP, or network calls.
