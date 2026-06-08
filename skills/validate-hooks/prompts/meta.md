---
name: validate-hooks-meta
type: meta
version: 3.0.0
description: "Route hook safety and hooks.json audit requests to Validate Hooks."
---

# Validate Hooks Meta Prompt

Activate this skill when the user asks for:

- [CODE] `validate-hooks` or `/validate-hooks`.
- [CODE] `validate hooks`, `check hooks.json`, `hooks audit`, or `hook safety check`.
- [CODE] ToolUseContext compatibility for hook types.
- [CODE] Placement guard or PreToolUse hook validation.
- [CODE] Offline review of hook commands and script references.

Do not activate for general Git hooks unless the request concerns plugin/runtime `hooks.json` or ToolUseContext behavior.
