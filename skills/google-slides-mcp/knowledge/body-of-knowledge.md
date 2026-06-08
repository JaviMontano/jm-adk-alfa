# Google Slides MCP Body of Knowledge

## Canon

This skill supports Google Slides through `workspace-mcp` and the Slides REST API. It is intentionally deterministic before live execution: local assets define the operation contract, scopes, tool mapping, and confirmation gates.

## Primary Operations

| Operation | Purpose | Safety posture |
|---|---|---|
| `presentations.create` | Create a blank presentation from a title and optional presentation ID. | Mutating; human confirmation required. |
| `presentations.get` | Retrieve the latest presentation resource. | Read-only. |
| `presentations.batchUpdate` | Apply one or more update requests atomically. | Mutating; human confirmation required. |
| `presentations.pages.get` | Retrieve the latest page resource. | Read-only. |
| `presentations.pages.getThumbnail` | Generate a thumbnail URL for a page. | Read-only but expensive; content URL is temporary and requester-scoped. |

## Scope Rules

- Prefer `drive.file` for app-created or user-opened presentations because it is the narrow recommended non-sensitive profile.
- Use `presentations.readonly` for read-only Slides-wide access when `drive.file` cannot reach the target file.
- Use `presentations` only when mutation across Slides files is required and `drive.file` is insufficient.
- Treat `drive` and `drive.readonly` as broad exceptions requiring a written reason.
- Do not add Sheets scopes unless the plan explicitly includes chart-linked Sheets data.

## Mutation Rules

- `presentations.create` and `presentations.batchUpdate` require `human_confirmation.status=confirmed`.
- Confirmation text must start with `CONFIRM GOOGLE SLIDES MUTATION:`.
- `presentations.batchUpdate` must target a presentation already read by `presentations.get` or created earlier in the same offline plan.
- Use `writeControl.requiredRevisionId` when a revision is available for collaborative or high-impact edits.
- Read back the presentation or page after live mutation.

## Thumbnail Rules

- `getThumbnail` may return `width`, `height`, and `contentUrl`.
- Thumbnail URL handling must be explicit: `do_not_persist`, `short_lived_preview`, or `discard_after_review`.
- Default thumbnail MIME type is PNG when unspecified.
- Use `SMALL`, `MEDIUM`, or `LARGE` deliberately; avoid unspecified size in durable plans unless the user accepts variable output.

## Local Resources

- `assets/google-slides-mcp-schema.json`: stable input contract.
- `assets/mcp-tool-contract.json`: mapping from MCP tools to real Slides methods.
- `assets/scope-policy.json`: least-privilege scope policy.
- `assets/human-confirmation-policy.json`: confirmation gate.
- `assets/slides-batchupdate-request-policy.json`: supported batchUpdate request keys.
- `assets/google-slides-operation-template.md`: Markdown report template.
- `scripts/compile-google-slides-mcp.py`: offline compiler and validator.

## Quality Signals

| Signal | Target |
|---|---|
| API fidelity | Every planned action maps to a real Slides REST method. |
| Least privilege | Scope profile is the narrowest viable option or includes an exception reason. |
| Offline determinism | Script output depends only on local JSON assets and fixture input. |
| Mutation safety | Human confirmation is required before create or batchUpdate. |
| Thumbnail hygiene | `contentUrl` is treated as temporary and not persisted. |
| Verification | Post-mutation readback is included in the live checklist. |
