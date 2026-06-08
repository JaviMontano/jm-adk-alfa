# Example Output

## Summary

- [CODE] Plan `slides-plan-2026-qbr` covers `Build QBR draft deck with safe thumbnail preview`.

## Evidence

- [DOC] google_slides_rest: Slides REST v1 supports presentations.create/get/batchUpdate and presentations.pages.get/getThumbnail.
- [DOC] google_slides_scopes: drive.file is the recommended narrow app-file scope; presentations.readonly and presentations are Slides-specific alternatives.
- [DOC] local_docs: docs/google-workspace-mcp-setup.md and docs/mcp-integration.md define workspace-mcp setup for JM-ADK.

## Operation Table

| ID | Action | MCP Tool | Scope Profile | Confirmation |
|---|---|---|---|---|
| read-template | presentations.get | `mcp__workspace-mcp__get_presentation` | app_file | not-required |
| read-title-page | presentations.pages.get | `mcp__workspace-mcp__get_page` | app_file | not-required |
| preview-title-page | presentations.pages.getThumbnail | `mcp__workspace-mcp__get_page_thumbnail` | app_file | not-required |
| create-draft | presentations.create | `mcp__workspace-mcp__create_presentation` | app_file | required |
| write-core-slides | presentations.batchUpdate | `mcp__workspace-mcp__batch_update_presentation` | app_file | required |

## Safety Gates

- [CODE] Read-only-first status: `complete`.
- [CODE] Mutation confirmation prefix: `CONFIRM GOOGLE SLIDES MUTATION:`.
- [CODE] `create-draft` confirmation: `confirmed` by `javier`.
- [CODE] `write-core-slides` confirmation: `confirmed` by `javier`.

## Validation

- [CODE] Structured input passed local schema and policy validation.
- [CODE] All operations map to real Slides REST methods and declared MCP tools.
- [CODE] The compiler performed no network, OAuth, Google Slides, or MCP calls.

## Risks and Limits

- [INFERENCE] Live execution can still fail because of OAuth grants, Drive ownership, domain policy, or missing file access.
- [DOC] Thumbnail `contentUrl` is temporary and requester-scoped; do not persist it.
