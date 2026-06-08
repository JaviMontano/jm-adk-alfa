# Google Calendar MCP Assets

These assets make the skill deterministic without calling Google Calendar or MCP.

## Files

- `google-calendar-operation-schema.json`: supported operation types and required structured fields.
- `scope-policy.json`: minimum OAuth scopes by operation.
- `calendar-event-payload-policy.json`: event field, timezone, attendee, and notification rules.
- `conference-data-policy.json`: Google Meet `conferenceData` and idempotency rules.
- `confirmation-policy.json`: human-confirmation gates for mutation.
- `read-only-first-checklist.md`: checklist to complete before create/edit/cancel.
- `google-calendar-operation-template.md`: Markdown template rendered by the compiler.

## Source Boundary

- [DOC] Google Calendar API official docs define scopes, event fields, insert/list parameters, attendees, timezone, and `conferenceData`.
- [DOC] MCP official tools spec defines `tools/list`, `tools/call`, tool errors, and sensitive-operation confirmation guidance.
- [CODE] Local MCP docs define `workspace-mcp`, service permissions, and the `google-calendar-mcp` mapping.
