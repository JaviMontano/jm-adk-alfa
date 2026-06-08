---
name: google-slides-mcp
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Google Slides integration via workspace-mcp for deterministic, least-privilege
  presentation planning, offline safety checklists, and controlled live execution.
  Use for Google Slides decks, presentations, slide/page reads, thumbnails, or
  mutations through presentations.create, presentations.get, presentations.batchUpdate,
  presentations.pages.get, and presentations.pages.getThumbnail.
status: production
tags: [mcp, google-slides, presentations, automation, google-workspace]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__create_presentation
  - mcp__workspace-mcp__get_presentation
  - mcp__workspace-mcp__batch_update_presentation
  - mcp__workspace-mcp__get_page
  - mcp__workspace-mcp__get_page_thumbnail
---

# Google Slides MCP

## TL;DR

Use this skill to plan and execute Google Slides work through `workspace-mcp` with a read/checklist-first workflow. Start offline with `scripts/compile-google-slides-mcp.py`; use live MCP tools only after scope review and explicit human confirmation for mutations.

## Source Order

1. Read local setup docs: `docs/google-workspace-mcp-setup.md` and `docs/mcp-integration.md`.
2. Use primary Google Slides REST docs for operation shape:
   - `presentations.create`
   - `presentations.get`
   - `presentations.batchUpdate`
   - `presentations.pages.get`
   - `presentations.pages.getThumbnail`
3. Use `assets/scope-policy.json` for least-privilege scope selection.
4. Use `assets/human-confirmation-policy.json` before any `presentations.create` or `presentations.batchUpdate`.

## Offline First

Run the deterministic compiler before live tools:

```bash
python3 skills/google-slides-mcp/scripts/compile-google-slides-mcp.py \
  --input skills/google-slides-mcp/scripts/fixtures/google-slides-mcp-input.json
```

The compiler reads only local `assets/` and fixture JSON. It makes no Google, OAuth, network, or MCP calls.

## Operation Contract

Use only these Slides operations:

| Action | REST method | MCP tool | Mode |
|---|---|---|---|
| `presentations.create` | `POST /v1/presentations` | `mcp__workspace-mcp__create_presentation` | mutating |
| `presentations.get` | `GET /v1/presentations/{presentationId}` | `mcp__workspace-mcp__get_presentation` | read-only |
| `presentations.batchUpdate` | `POST /v1/presentations/{presentationId}:batchUpdate` | `mcp__workspace-mcp__batch_update_presentation` | mutating |
| `presentations.pages.get` | `GET /v1/presentations/{presentationId}/pages/{pageObjectId}` | `mcp__workspace-mcp__get_page` | read-only |
| `presentations.pages.getThumbnail` | `GET /v1/presentations/{presentationId}/pages/{pageObjectId}/thumbnail` | `mcp__workspace-mcp__get_page_thumbnail` | read-only expensive read |

## Safety Rules

- Prefer `https://www.googleapis.com/auth/drive.file` when work is limited to presentations created or opened with this app.
- Use `https://www.googleapis.com/auth/presentations.readonly` for read-only access across Slides files when `drive.file` is not enough.
- Avoid `https://www.googleapis.com/auth/drive` and `https://www.googleapis.com/auth/drive.readonly` unless a written exception explains why the narrower scopes cannot satisfy the workflow.
- Require human confirmation for every mutating operation.
- For `presentations.batchUpdate`, first prove the target presentation is known through a prior `presentations.get` or a same-plan `presentations.create`.
- Treat thumbnail `contentUrl` as ephemeral and requester-scoped; do not persist it into durable docs, logs, or examples.
- Use `writeControl.requiredRevisionId` for collaborative or high-impact updates when a current revision is available.

## Assets and Scripts

- `assets/google-slides-mcp-schema.json` defines the stable offline input contract.
- `assets/scope-policy.json` maps Slides actions to minimum OAuth scope profiles.
- `assets/mcp-tool-contract.json` maps MCP tool names to real Slides REST methods.
- `assets/human-confirmation-policy.json` defines mutation gates.
- `assets/google-slides-operation-template.md` renders deterministic Markdown output.
- `scripts/compile-google-slides-mcp.py` validates structured input and compiles the plan/checklist.
- `scripts/check.sh` runs offline fixture checks.

## Live Execution Checklist

1. Compile the offline plan and review validation.
2. Confirm `.mcp.json` exposes `workspace-mcp` with the expected tool tier.
3. Verify the granted OAuth scope matches the minimum viable scope profile.
4. Execute read-only calls first: `get_presentation`, `get_page`, or `get_page_thumbnail`.
5. Ask the user to confirm the exact mutation text before calling create or batchUpdate.
6. After mutation, read back the presentation or page and compare against the plan.

## Output

Return Markdown using `templates/output.md`, with evidence, scope review, operation checklist, validation, and residual risks. Use `templates/output.html` only when the user asks for a standalone HTML report.
