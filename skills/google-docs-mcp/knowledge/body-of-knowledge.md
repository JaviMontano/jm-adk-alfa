# Google Docs MCP Body of Knowledge

## Canon

`google-docs-mcp` plans Google Docs work through `workspace-mcp` without making
network, OAuth, or MCP calls during deterministic checks. The skill uses local
assets to turn a structured JSON request into a stable Markdown checklist.

## Docs API Contract

| Method | Use | Safety Rule |
|---|---|---|
| `documents.create` | Create a blank document with metadata such as title | Do not send body content; insert content later with `documents.batchUpdate` |
| `documents.get` | Inspect document content, structure, tabs, and revision data | Run before an edit that depends on indexes or revision state |
| `documents.batchUpdate` | Apply ordered update requests | Require prior `documents.get`, `writeControl.requiredRevisionId`, and human confirmation |

## Minimum Scopes

| Profile | Scope | Use |
|---|---|---|
| `docs_readonly` | `https://www.googleapis.com/auth/documents.readonly` | Inspect Docs content only |
| `drive_file` | `https://www.googleapis.com/auth/drive.file` | Create or mutate app-created or user-opened files |
| `docs_full` | `https://www.googleapis.com/auth/documents` | Escalation-only full Docs access |

## Batch Update Request Types

The deterministic compiler supports `insertText`, `deleteContentRange`,
`replaceAllText`, `updateTextStyle`, `updateParagraphStyle`,
`createParagraphBullets`, `insertTable`, and `insertPageBreak`.

Range-based requests require concrete indexes from `documents.get`. Text and
table insertion require explicit locations. Style requests require `fields` so
the update does not implicitly modify unrelated style attributes.

## Human-Confirmation Gate

The policy in `assets/mutation-confirmation-policy.json` blocks live mutation
until the confirmation text starts with `CONFIRM GOOGLE DOCS MUTATION:` and
records operation ID, target document, Docs API method, scope profile, request
count, and live-execution intent.

## Quality Signals

| Signal | Target |
|---|---|
| Evidence coverage | Local docs and official Docs/MCP sources are cited |
| Scope control | `documents.readonly` or `drive.file` selected before broader scopes |
| Mutation safety | `documents.create` and `documents.batchUpdate` require human confirmation |
| Structural safety | Batch update ranges derive from a prior read-only inspection |
| Offline determinism | Scripts do not call Docs, OAuth, network, or MCP tools |

## Residual Limits

- Live execution can still fail because of document ACLs, OAuth grants, stale
  revision IDs, Workspace admin policy, or changed indexes.
- The offline compiler validates the requested contract; it cannot prove a live
  Google Doc exists.
- Export to PDF or Markdown is read-only from this skill's perspective, but it
  does not prove mutation success unless paired with a fresh `documents.get`.
