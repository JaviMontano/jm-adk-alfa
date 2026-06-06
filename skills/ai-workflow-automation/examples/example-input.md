<!--
generated-by: scripts/scaffold-skill.py
generated-for: ai-workflow-automation
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Design an AI workflow automation plan for support ticket triage.

Inputs:

- `tickets/inbound/*.json` with customer tier, product, severity, and message.
- `docs/support/escalation-policy.md` for escalation rules.
- `docs/templates/triage-response.md` for draft response format.

Requirements:

- AI may classify tickets and draft responses.
- A human support lead must approve any P0 escalation and any outbound customer
  response.
- Failed classification can retry once, then hand off to human triage.
- Reference date: 2026-06-06.

Produce actors, step graph, approval gates, handoffs, fallback paths,
validation, and risks with evidence tags.
