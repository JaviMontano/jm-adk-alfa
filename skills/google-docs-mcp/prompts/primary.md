# Google Docs MCP Primary Prompt

## Objective

Plan or execute Google Docs work through `workspace-mcp` using the local
`google-docs-mcp` contract.

## Required Inputs

- Document goal and audience
- Target document ID or new document title
- Requested operation mode: `plan_only` or `safe_execution_checklist`
- Scope constraints and confirmation status
- Definition of done

## Process

1. Confirm whether the task is read-only or mutating.
2. Select the minimum scope profile from `assets/scope-policy.json`.
3. For creation, use `documents.create` as title-only and insert content later.
4. For edits, inspect with `documents.get` before composing ranges.
5. For mutations, require the gate in
   `assets/mutation-confirmation-policy.json`.
6. For deterministic planning, run or reference
   `scripts/compile-google-docs-mcp.py`.
7. Return evidence, operation plan, validation, and residual risks.

## Output

Return Markdown with summary, evidence, MCP preflight, scope review, Docs API
plan, batch-update checklist, human confirmation, validation, and risks.
