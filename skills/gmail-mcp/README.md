# Gmail MCP

Use this skill to operate Gmail through the local `workspace-mcp` server with read-only-first discovery, least-scope review, draft-first sending, label/filter safeguards, privacy controls, and evidence-tagged validation.

## Deterministic Resources

- `assets/gmail-mcp-schema.json` defines required structured input.
- `assets/operation-safety-policy.json` defines read-only-first and confirmation gates.
- `assets/scope-matrix.json` maps Gmail operations to minimum scope review.
- `assets/search-query-patterns.json` captures safe Gmail search query patterns.
- `assets/label-policy.json` captures system/user label constraints and bulk label rules.
- `assets/send-draft-policy.json` captures draft-first and send-confirmation checks.
- `assets/privacy-redaction-policy.json` captures redaction and no-storage rules.
- `scripts/compile-gmail-mcp.py` renders an offline plan/checklist from JSON without calling Gmail or MCP.

## Safe Workflow

1. Search metadata first with a narrow query and bounded result count.
2. Read selected message/thread content only when the task requires it.
3. Review minimum Gmail scope for every planned operation.
4. Draft outbound email before sending whenever possible.
5. Require explicit human confirmation for send, delete/trash, filter mutation, and bulk label changes.
6. Return evidence, tool sequence, validation status, and residual risks without storing email content.

## Output Format

Markdown with summary, evidence, scope review, safety gates, tool sequence, confirmation checklist, privacy controls, and residual risks.
