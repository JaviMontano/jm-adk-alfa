# Google Workspace APIs — Body of Knowledge

## Canon

Google Workspace exposes REST APIs for Gmail, Calendar, Drive, Docs, Sheets,
and Slides. A reliable automation plan must name the service, method, access
mode, required scopes, resource identifiers, retry strategy, and validation
layer before runtime execution.

## Integration Model

| Layer | Purpose | Deterministic Asset |
|---|---|---|
| Service matrix | Supported Workspace services and methods | `assets/workspace-service-matrix.json` |
| Auth/scopes | Least-privilege OAuth or API-key profiles | `assets/auth-scope-policy.json` |
| MCP mapping | Tool names and allowed service actions | `assets/mcp-tool-contract.json` |
| Operations | Read-only-first, mutation, retry, idempotency | `assets/operation-policy.json` |
| Compiler | Offline plan validation and Markdown rendering | `scripts/compile-google-workspace-apis.py` |

## Service Patterns

- Gmail: search/list/get before draft/send; sending requires explicit consent.
- Calendar: list/freebusy before insert/patch/delete; invitations need payload
  review.
- Drive: list/get metadata before create/update/share; file permissions are
  security-sensitive mutations.
- Docs: get document structure before batchUpdate; create starts blank and
  content changes happen through update requests.
- Sheets: read ranges before value or structural writes; distinguish value
  updates from spreadsheet batchUpdate.
- Slides: get presentation before batchUpdate; thumbnails are read-only preview
  evidence.

## Quality Gates

- Read-only-first is mandatory for mutating workflows.
- Scopes must match the selected profile exactly.
- MCP tools must belong to the requested service and operation class.
- Mutations require `human_consent.status=confirmed`.
- Secrets must be stored outside the repository.
- Validation must include static, fixture, sandbox, and live-read-only layers.

## Official References

- Google Workspace overview: https://developers.google.com/workspace
- Workspace auth overview: https://developers.google.com/workspace/guides/auth-overview
- Google Workspace MCP guide: https://developers.google.com/workspace/guides/build-with-llms
- MCP tools spec: https://modelcontextprotocol.io/specification/draft/server/tools
- Gmail REST: https://developers.google.com/workspace/gmail/api/reference/rest
- Calendar REST: https://developers.google.com/calendar/api/v3/reference
- Drive REST: https://developers.google.com/drive/api/reference/rest/v3
- Docs REST: https://developers.google.com/workspace/docs/api/reference/rest
- Sheets REST: https://developers.google.com/workspace/sheets/api/reference/rest
- Slides REST: https://developers.google.com/workspace/slides/api/reference/rest

## Limits

The local compiler cannot verify OAuth consent screen status, enabled APIs,
organization policies, quota, billing, live permissions, or resource existence.
Those checks belong to a sandbox/live validation phase after human approval.
