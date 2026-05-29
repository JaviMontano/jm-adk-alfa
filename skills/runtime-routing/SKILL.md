---
name: runtime-routing
version: 1.0.0
description: "Route agentic work across Claude, Codex, Gemini, Antigravity, VS Code, and local adapters with explicit validation limits."
owner: "JM Labs"
triggers:
  - runtime-routing
  - codex
  - claude
  - antigravity
  - gemini
  - vscode
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Runtime Routing

## When To Use

- User asks where to run Alfa work.
- A task depends on hooks, MCP, multimodal input, local files, generated adapters, or IDE-specific rules.
- Portability across Claude, Codex, Gemini, Antigravity, or VS Code matters.

## When Not To Use

- The task is runtime-independent and can be completed with the current tool.
- The requested runtime capability cannot be observed or verified and the user needs a guarantee.

## Inputs

- Requested runtime or current IDE.
- Task type and output surface.
- Repo adapter evidence.
- Required capabilities and validation status.

## Outputs

- Recommended runtime path.
- Capability boundary table.
- Fallback path with `Dato requerido` or validation pending where needed.

## Workflow

1. Discover: inspect repo docs/adapters for runtime evidence.
2. Analyze: choose the lowest-permission runtime that can do the task.
3. Execute: route to the matching doc, command, skill, or script.
4. Validate: mark unverified support instead of inventing claims.

## Safety Limits

- Do not claim Antigravity, Codex, Claude, Gemini, or VS Code support beyond visible repo evidence or executed checks.
- Keep local files, workspace state, and secrets within local boundaries.

## Success Criteria

- User receives a concrete runtime recommendation.
- Unsupported capability is labeled validation pending.
- Local-first fallback exists.

## Fallback

Use Markdown-first instructions and repo-local scripts when runtime feature support is unclear.

## Examples

- "How should I run this in Codex?" -> use `CODEX.md` and `AGENTS.md`.
- "Prepare for Antigravity" -> use `.agent/` adapter evidence and mark runtime validation pending.
