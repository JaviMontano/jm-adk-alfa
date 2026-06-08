---
name: pre-tool-use-guard
author: JM Labs (Javier Montaño)
version: 1.0.0
description: "Block dangerous commands before execution using the exit-code-2 deny pattern, deterministic write-scope policy, private path protection, and offline report validation. [EXPLICIT]"
triggers:
  - pre tool use guard
  - dangerous command guard
  - exit code 2 block
  - tool call safety
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Pre Tool Use Guard

Blocks unsafe tool calls before execution. The contract is intentionally narrow: a report either allows the call, requires explicit approval, or blocks it with the exit-code-2 pattern.

## Deterministic Contract

- `assets/guard-decision-contract.json` defines the JSON report shape.
- `assets/dangerous-command-policy.json` lists command patterns that must fail closed.
- `assets/write-boundary-policy.json` defines protected and allowed write surfaces.
- `assets/private-path-policy.json` defines private path markers.
- `scripts/validate_pre_tool_use_guard.py` validates reports offline.
- `scripts/check.sh` runs positive and negative fixtures.

## Procedure

1. Parse the proposed tool call, command, cwd, and write scope.
2. Detect destructive commands, private path touches, secret exposure risk, and writes outside declared scope.
3. Set `decision.action` to `block` and `decision.exit_code` to `2` for any hard blocker.
4. Allow only read-only or explicitly scoped safe writes.
5. Validate the report before presenting the decision.

## Fail-Closed Conditions

- `git reset --hard`, `git clean -fd`, broad deletion, or equivalent destructive shell.
- Writes outside declared `allowed_write_roots`.
- Any action touching `user-context/jarvis-os`, `.env`, credentials, or secret-like paths.
- Missing evidence for an allow decision.
- Any blocker with `decision.action: allow`.

## Usage

Run the fixture gate:

```bash
bash skills/pre-tool-use-guard/scripts/check.sh
```
