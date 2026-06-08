---
name: google-workspace-apis
author: JM Labs (Javier Montaño)
version: 1.1.0
description: >
  Integrate Google Workspace APIs across Gmail, Calendar, Drive, Docs, Sheets,
  and Slides with least-privilege scopes, MCP-aware tool mapping, read-only-first
  execution, and deterministic validation. [EXPLICIT]
  Trigger: "google workspace apis", "workspace api automation", "gmail docs sheets drive api",
  "integrate google workspace", "workspace mcp api plan"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Google Workspace APIs

## TL;DR

Use this skill to design a Google Workspace automation that spans Gmail,
Calendar, Drive, Docs, Sheets, and Slides. It produces an offline integration
plan with service matrix, OAuth scopes, MCP tool-contract mapping, mutation
gates, retry/idempotency policy, secrets policy, and validation matrix.

## Deterministic Contract

- Use `assets/workspace-service-matrix.json` as the operation catalog.
- Use `assets/auth-scope-policy.json` for least-privilege scope profiles.
- Use `assets/mcp-tool-contract.json` when a workflow uses Workspace MCP tools.
- Run `scripts/compile-google-workspace-apis.py` against a structured JSON
  input before finalizing a plan.
- Run `scripts/check.sh` to verify positive and negative fixtures offline.
- Do not call Google APIs, OAuth, MCP servers, or network resources from the
  skill scripts.

## Procedure

### Step 1: Discover

- Identify target Workspace services and exact operations.
- Classify each operation as read-only or mutating.
- Determine whether the implementation path is direct REST/client library, MCP,
  or a mixed flow.
- Capture concrete resource identifiers needed for sandbox validation.

### Step 2: Analyze

- Select the narrowest scope profile from `assets/auth-scope-policy.json`.
- Prefer read-only probes before every write operation.
- Map MCP tools to the same operation intent when MCP is part of the flow.
- Define idempotency keys, rollback/compensation, and retry policy before writes.
- Confirm credential storage, token handling, and key restrictions.

### Step 3: Compile

```bash
python3 skills/google-workspace-apis/scripts/compile-google-workspace-apis.py \
  --input skills/google-workspace-apis/scripts/fixtures/google-workspace-apis-input.json
```

The compiler emits a deterministic Markdown plan. It fails if scopes are too
broad for the requested operation, a mutating operation lacks confirmation, a
write skips read-before-write, or an MCP tool does not match the service.

### Step 4: Validate

- Run `bash skills/google-workspace-apis/scripts/check.sh`.
- Validate the skill with `python3 -B scripts/validate-skill-dod.py --skill google-workspace-apis`.
- Validate runtime script contracts with `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-workspace-apis`.
- Treat live API calls as a separate sandbox/live validation phase.

## Quality Criteria

- [ ] Exact Workspace services and operations are listed.
- [ ] OAuth scopes are minimal for the operation class.
- [ ] Mutations require human confirmation and read-before-write.
- [ ] MCP tool names map to service-compatible operations.
- [ ] Secrets are never committed and tokens live in approved storage.
- [ ] Retry, idempotency, quota, and rollback are explicit.
- [ ] Validation matrix covers static, fixture, sandbox, and live-read-only layers.

## Anti-Patterns

- Requesting broad Drive/Gmail scopes for read-only tasks.
- Sending email, creating events, or changing files without confirmation.
- Treating MCP tool availability as proof of OAuth access.
- Storing OAuth clients, refresh tokens, service-account keys, or API keys in
  repo files.
- Skipping partial-response fields and then blaming quota/performance later.

## MCP Integration

For direct interactive access, prefer the specialized skills:
`gmail-mcp`, `google-calendar-mcp`, `google-drive-mcp`, `google-docs-mcp`,
`google-sheets-mcp`, and `google-slides-mcp`. Use this integrator when the
workflow crosses services or when REST/API and MCP execution paths must be
coordinated in one plan.

## Official References

- Google Workspace overview: https://developers.google.com/workspace
- Workspace auth overview: https://developers.google.com/workspace/guides/auth-overview
- Google Workspace MCP server guide: https://developers.google.com/workspace/guides/build-with-llms
- MCP tools spec: https://modelcontextprotocol.io/specification/draft/server/tools
- Gmail REST: https://developers.google.com/workspace/gmail/api/reference/rest
- Calendar REST: https://developers.google.com/calendar/api/v3/reference
- Drive REST: https://developers.google.com/drive/api/reference/rest/v3
- Docs REST: https://developers.google.com/workspace/docs/api/reference/rest
- Sheets REST: https://developers.google.com/workspace/sheets/api/reference/rest
- Slides REST: https://developers.google.com/workspace/slides/api/reference/rest

## Related Skills

- `gmail-mcp`
- `google-calendar-mcp`
- `google-drive-mcp`
- `google-docs-mcp`
- `google-sheets-mcp`
- `google-slides-mcp`
- `google-apis-integration`

## Assumptions & Limits

- The compiler validates plans offline; it does not prove OAuth, quota, billing,
  permissions, or resource existence.
- Live execution requires a separate sandbox account, explicit human approval,
  and provider-side validation.
