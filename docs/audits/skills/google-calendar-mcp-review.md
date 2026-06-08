# Skill Review: google-calendar-mcp

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/google-calendar-mcp`.
- [CODE] Review date: 2026-06-01.

## Primary Sources

- [DOC] Google Calendar scopes: https://developers.google.com/workspace/calendar/api/auth.
- [DOC] Google Calendar create events guide: https://developers.google.com/workspace/calendar/api/guides/create-events.
- [DOC] Google Calendar Events resource: https://developers.google.com/calendar/api/v3/reference/events.
- [DOC] Google Calendar Events insert: https://developers.google.com/workspace/calendar/api/v3/reference/events/insert.
- [DOC] Google Calendar Events list: https://developers.google.com/calendar/api/v3/reference/events/list.
- [DOC] MCP tools specification: https://modelcontextprotocol.io/specification/draft/server/tools.
- [CODE] Local MCP setup: `docs/google-workspace-mcp-setup.md`.
- [CODE] Local MCP integration: `docs/mcp-integration.md`.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/google-calendar-operation-schema.json` defines supported operations, required fields, and validation patterns.
- [CODE] `assets/scope-policy.json` maps availability, agenda, mutation, and app-created operations to minimum Calendar scopes.
- [CODE] `assets/calendar-event-payload-policy.json` captures RFC3339 timezone, attendees, `sendUpdates`, reminders, and read-back rules.
- [CODE] `assets/conference-data-policy.json` captures Google Meet `conferenceDataVersion=1`, `hangoutsMeet`, `requestId`, and asynchronous read-back rules.
- [CODE] `assets/confirmation-policy.json` blocks mutating MCP calls without human confirmation.
- [CODE] `assets/read-only-first-checklist.md` defines the operational checklist before mutation.
- [CODE] `scripts/compile-google-calendar-mcp.py` compiles structured JSON into a safe Markdown operation plan without network, Calendar, OAuth, or MCP calls, and requires confirmed write access before mutation.
- [CODE] `scripts/check.sh` validates a positive create-event fixture plus negative fixtures for missing confirmation and broad scope.
- [CODE] `evals/evals.json` includes concrete agenda, freebusy, create, edit, cancel, negative, and false-positive cases.
- [CODE] `README.md`, `SKILL.md`, examples, knowledge, templates, and evals now contain Calendar-specific content instead of scaffold placeholders.

## Documentation Alignment

- [DOC] Official scopes guidance says apps should choose narrowly focused scopes; the skill encodes `calendar.freebusy`, `calendar.events.readonly`, `calendar.events`, and `calendar.app.created` by operation.
- [DOC] Events list supports `timeMin`, `timeMax`, `singleEvents`, `orderBy=startTime`, and `timeZone`; the skill uses those as agenda-query defaults.
- [DOC] Events insert documents `conferenceDataVersion=1`, `sendUpdates`, and insert authorization scopes; the skill requires explicit notification policy and Meet configuration.
- [DOC] Events resource documents `conferenceData.createRequest.requestId`; the skill requires a request id when Google Meet is requested.
- [DOC] MCP tools spec recommends confirmation for sensitive operations and showing tool inputs before calls; the skill gates create/edit/cancel behind confirmation and payload preview.
- [CODE] Local MCP docs identify `workspace-mcp`, `GOOGLE_WORKSPACE_CREDENTIALS_PATH`, `--read-only`, service permissions, and Calendar events/calendars/Meet/out-of-office mapping.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill google-calendar-mcp
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-calendar-mcp
bash skills/google-calendar-mcp/scripts/check.sh
python3 -B -m py_compile skills/google-calendar-mcp/scripts/compile-google-calendar-mcp.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies `google-calendar-mcp` only.
- [INFERENCE] The deterministic compiler renders safe plans; real Calendar mutations still depend on authenticated `workspace-mcp` runtime permissions.
- [INFERENCE] Google Meet creation can be asynchronous, so production use still needs post-mutation read-back verification.
