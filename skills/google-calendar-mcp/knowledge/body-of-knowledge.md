# Google Calendar MCP — Body of Knowledge

## Canon

- [DOC] Google Calendar API scopes should be as narrow as possible; the official scope table includes `calendar.freebusy`, `calendar.events.readonly`, `calendar.events`, and `calendar.app.created`.
- [DOC] `events.list` returns events for a calendar and supports bounded date windows with `timeMin`, `timeMax`, `singleEvents`, `orderBy`, and `timeZone`.
- [DOC] `events.insert` creates an event on `calendarId`; `primary` targets the authenticated user's primary calendar.
- [DOC] Timed events use `start.dateTime` and `end.dateTime`; the create-events guide examples pair those values with `timeZone`.
- [DOC] `timeMin` and `timeMax` must be RFC3339 timestamps with mandatory timezone offsets.
- [DOC] Attendees included in a created event receive calendar copies; `sendUpdates` controls whether guests receive email notifications.
- [DOC] `sendUpdates=none` can have adverse sync effects for some users, so the user should explicitly approve that choice when attendees exist.
- [DOC] Google Meet generation uses `conferenceData.createRequest`; Calendar event modification requests must set `conferenceDataVersion=1` to persist conference changes.
- [DOC] `conferenceData.createRequest.requestId` is client-generated and unique for the request; Calendar ignores a repeated id from the previous request.
- [DOC] MCP tools are discovered through `tools/list` and invoked through `tools/call`; tool execution errors can be returned with `isError: true`.
- [DOC] MCP clients should prompt for confirmation on sensitive operations and show tool inputs before calling the server.
- [CODE] Local `docs/google-workspace-mcp-setup.md` defines `workspace-mcp`, `GOOGLE_WORKSPACE_CREDENTIALS_PATH`, `--read-only`, and service-level permissions such as `calendar:full`.
- [CODE] Local `docs/mcp-integration.md` maps `google-calendar-mcp` to `workspace-mcp` and Calendar events, calendars, Meet, and out-of-office tooling.

## Scope Selection

| Operation | Minimum Scope | Notes |
|---|---|---|
| Availability only | `https://www.googleapis.com/auth/calendar.freebusy` | Use when the user only needs busy/free status. |
| Agenda or event read | `https://www.googleapis.com/auth/calendar.events.readonly` | Use for bounded event listing and event inspection. |
| Create/edit/cancel event | `https://www.googleapis.com/auth/calendar.events` | Use for normal event mutation on accessible calendars. |
| App-created calendars/events | `https://www.googleapis.com/auth/calendar.app.created` | Use when the app only manages calendars and events it created. |

## Read-Only-First Flow

1. [CODE] List or identify the target calendar before mutation.
2. [CODE] Query relevant events for the requested time window.
3. [CODE] Confirm write access for create/edit/cancel operations.
4. [CODE] Check conflicts or target event identity.
5. [CODE] Present the proposed payload and notification behavior.
6. [CODE] Request explicit human confirmation.
7. [CODE] Mutate through MCP only after confirmation.
8. [CODE] Read back the result after mutation.

## Failure Modes

| Failure | Deterministic Guard |
|---|---|
| Wrong timezone | Require IANA timezone plus RFC3339 date-time offset. |
| Duplicate Meet request | Require a unique `conferenceData.createRequest.requestId` for every new conference request. |
| Silent attendee notifications | Require explicit `sendUpdates` whenever attendees are present. |
| Mutating without consent | Reject structured operation unless `human_confirmation.status=confirmed`. |
| Broad OAuth scope | Reject operation scopes outside the minimum-scope policy unless documented as a local MCP limitation. |
| Scripts touching live Calendar | Keep scripts offline; fixture checks only read JSON and render Markdown. |

## Source Snapshot

- [DOC] Google Calendar scopes: https://developers.google.com/workspace/calendar/api/auth (last updated 2026-04-20 UTC).
- [DOC] Create events guide: https://developers.google.com/workspace/calendar/api/guides/create-events.
- [DOC] Events resource: https://developers.google.com/calendar/api/v3/reference/events.
- [DOC] Events insert: https://developers.google.com/workspace/calendar/api/v3/reference/events/insert.
- [DOC] Events list: https://developers.google.com/calendar/api/v3/reference/events/list.
- [DOC] MCP tools specification: https://modelcontextprotocol.io/specification/draft/server/tools.
- [CODE] Local MCP setup: `docs/google-workspace-mcp-setup.md`.
- [CODE] Local MCP integration: `docs/mcp-integration.md`.
