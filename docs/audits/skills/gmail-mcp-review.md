# Skill Review: gmail-mcp

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/gmail-mcp`.
- [CODE] Review date: 2026-06-01.
- [CODE] Write set honored: `skills/gmail-mcp/**` and `docs/audits/skills/gmail-mcp-review.md`.

## Primary Sources

- [DOC] Local MCP setup source: `docs/google-workspace-mcp-setup.md`.
- [DOC] Local MCP integration source: `docs/mcp-integration.md`.
- [DOC] Official Google Gmail REST overview: `https://developers.google.com/workspace/gmail/api/reference/rest`.
- [DOC] Official Google Gmail scopes: `https://developers.google.com/workspace/gmail/api/auth/scopes`.
- [DOC] Official Google `users.messages.send`: `https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/send`.
- [DOC] Official MCP tools spec: `https://modelcontextprotocol.io/specification/draft/server/tools`.

## DoD Evidence

- [CODE] `assets/manifest.json` lists all Gmail MCP assets and validates asset consumers.
- [CODE] `assets/gmail-mcp-schema.json` defines the structured offline input contract.
- [CODE] `assets/operation-safety-policy.json` enforces read-only-first, confirmation gates, and no real calls from scripts.
- [CODE] `assets/scope-matrix.json` maps Gmail operations to scope review: `gmail.metadata`, `gmail.readonly`, `gmail.labels`, `gmail.compose`, `gmail.send`, and `gmail.modify`.
- [CODE] `assets/search-query-patterns.json` captures Gmail query, `labelIds[]`, max-results, and date-handling safeguards.
- [CODE] `assets/label-policy.json` captures system/user label constraints, draft-label restrictions, and bulk-label confirmation.
- [CODE] `assets/send-draft-policy.json` captures draft-first sending and human confirmation requirements.
- [CODE] `assets/privacy-redaction-policy.json` blocks repository storage of message bodies, attachments, tokens, and credentials.
- [CODE] `scripts/compile-gmail-mcp.py` compiles JSON into a deterministic Markdown plan without Gmail, OAuth, network, or MCP calls.
- [CODE] `scripts/check.sh` validates the positive fixture, expected output fragments, and the rejected direct-send-without-confirmation fixture.
- [CODE] `evals/evals.json` contains concrete Gmail MCP cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `README.md`, `SKILL.md`, examples, knowledge, prompts, templates, and evals are Gmail-specific and no longer scaffold placeholders.

## Documentation Alignment

- [DOC] Local setup documents `workspace-mcp` as the unified Google Workspace server and lists Gmail tools for search, send, draft, labels, and filters.
- [DOC] Local setup documents permission tiers including `readonly`, `organize`, `drafts`, `send`, and `full`.
- [DOC] Gmail REST resources include messages, drafts, labels, filters, attachments, and threads.
- [DOC] Gmail search supports the `q` parameter and `labelIds[]`; official docs note API/UI differences for alias expansion and thread-wide search.
- [DOC] Gmail search date strings are interpreted at PST midnight, so the skill recommends Unix seconds for timezone-sensitive searches.
- [DOC] Gmail scopes guidance says to choose the most narrowly focused scope and avoid scopes that are not required.
- [DOC] `users.messages.send` sends to `To`, `Cc`, and `Bcc` recipients and requires a send-capable Gmail scope.
- [DOC] MCP tools are exposed with names, descriptions, input schemas, and structured results, so the skill keeps tool calls explicit and plan-first.

## Safety Evidence

- [CODE] Read-only-first is required in both `SKILL.md` and `assets/operation-safety-policy.json`.
- [CODE] Send, delete/trash, filter mutation, and bulk-label mutation require a `CONFIRMED:` human confirmation phrase in deterministic fixtures.
- [CODE] The negative fixture `invalid-direct-send-without-confirmation.json` is rejected by the compiler.
- [CODE] The compiler rejects storage of email bodies or attachments and rejects disabled PII/credential redaction.
- [INFERENCE] Live Gmail execution remains dependent on local OAuth state, enabled Gmail API, and the active MCP permission tier.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill gmail-mcp
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill gmail-mcp
bash skills/gmail-mcp/scripts/check.sh
python3 -m py_compile skills/gmail-mcp/scripts/compile-gmail-mcp.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies `gmail-mcp` only and does not certify other skills being edited by parallel workers.
- [INFERENCE] The deterministic compiler produces a plan/checklist, not live mailbox evidence.
- [INFERENCE] Filter mutation may require scope review beyond the default Gmail scope set depending on the live MCP server configuration.
