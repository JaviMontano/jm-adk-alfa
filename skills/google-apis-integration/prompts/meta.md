---
name: google-apis-integration-meta
type: meta
version: 2.0.0
description: "Meta-prompt for routing multi-service Google API integration planning."
---

# Google APIs Integration - Meta Prompt

Activate this skill when the user asks for:

- A backend or web integration involving multiple Google APIs.
- OAuth scope selection across Sheets, Docs, Calendar, YouTube, or Workspace APIs.
- Maps JavaScript API loading, key restriction, or browser integration policy.
- A plan/checklist for Google API quota, retries, idempotency, secrets, or consent.
- Direct invocation: `/google-apis-integration`.

Do not activate for a single live MCP action when a narrower MCP skill such as
`google-sheets-mcp`, `google-docs-mcp`, or `google-calendar-mcp` is the better
fit. [CODE]
