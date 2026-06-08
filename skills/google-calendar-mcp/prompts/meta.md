# Google Calendar MCP Meta Prompt

Review whether `google-calendar-mcp` should activate and whether the requested operation is safe.

## Activation Check

- Activate for Calendar agenda, availability, event creation/edit/cancel, attendees, invites, out-of-office, or Google Meet requests.
- Prefer `gmail-mcp` for email-only follow-up and `google-workspace-apis` for programmatic API implementation outside MCP.
- If the request asks for mutation without date/time, timezone, target calendar, or confirmation, gather missing inputs first.

## Safety Check

- Read-only-first must precede mutation.
- Minimum scope must match the operation.
- Human confirmation is mandatory for create/edit/cancel/out-of-office.
- Google Meet requires `conferenceDataVersion=1` and a unique request id.
- Scripts and fixtures must remain offline.
