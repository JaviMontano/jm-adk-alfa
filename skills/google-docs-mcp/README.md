# Google Docs MCP

Use this skill to plan safe Google Docs work through the local `workspace-mcp`
server: create blank documents, inspect document structure, compile
`documents.batchUpdate` request sequences, and prepare export handoffs.

## Deterministic Resources

- `assets/google-docs-mcp-schema.json` defines the stable structured request
  contract for Docs MCP plans.
- `assets/docs-operation-policy.json` maps supported Docs API REST methods:
  `documents.create`, `documents.get`, and `documents.batchUpdate`.
- `assets/scope-policy.json` defines least-privilege scope profiles, including
  `documents.readonly`, `drive.file`, and escalation-only `documents`.
- `assets/mutation-confirmation-policy.json` defines human-confirmation gates for
  document creation and batch updates.
- `assets/mcp-tool-contract.json` maps local `workspace-mcp` Docs tools to
  read-only or mutating operation classes.
- `assets/google-docs-mcp-template.md` is the canonical Markdown report template.
- `scripts/compile-google-docs-mcp.py` renders an offline Markdown plan and
  checklist from JSON. It does not call Google Docs, OAuth, or MCP tools.

## Output Format

Markdown or HTML with evidence, MCP preflight, scope review, operation plan,
Docs API request payload checklist, mutation-confirmation gate, validation, and
residual risks.
