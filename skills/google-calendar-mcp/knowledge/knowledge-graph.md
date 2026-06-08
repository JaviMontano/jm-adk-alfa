# Google Calendar MCP Knowledge Graph

| Node | Role |
|---|---|
| `google-calendar-mcp` | Skill entry point for Calendar agenda, availability, and event mutation through MCP. |
| `scope-policy` | Maps operations to minimum official Calendar scopes. |
| `read-only-first` | Gate that requires listing calendars/events before mutation. |
| `confirmation` | Gate that requires human confirmation before create/edit/cancel/out-of-office. |
| `timezone` | Contract for RFC3339 date-times with offsets and IANA timezone names. |
| `attendees` | Contract for attendee email review and explicit `sendUpdates`. |
| `conference-data` | Google Meet policy for `conferenceDataVersion=1` and `createRequest.requestId`. |
| `offline-compiler` | Deterministic script that renders a safe operation plan without live calls. |
| `mcp-tools` | Local `workspace-mcp` Calendar tools used after gates pass. |
