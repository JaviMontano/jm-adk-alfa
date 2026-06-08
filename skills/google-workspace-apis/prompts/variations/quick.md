---
name: google-workspace-apis-quick
type: variation
version: 2.1.0
description: "Quick Google Workspace API integration triage."
---

# Google Workspace APIs — Quick Mode

## Use When

Use quick mode to decide whether a Workspace workflow is safe to design before
writing code or configuring MCP tools.

## Execution

1. List requested services and operations.
2. Mark each operation read-only or mutating.
3. Pick the narrowest scope profile from `assets/auth-scope-policy.json`.
4. Identify the MCP tool mapping when MCP is in scope.
5. State missing resource IDs, consent, and sandbox prerequisites.

## Output

- Short service matrix.
- Scope and consent blockers.
- Offline validation command.
- Residual live checks.
