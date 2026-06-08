# Validate Hooks

[CODE] Validates `hooks.json` structure, event names, hook type compatibility, ToolUseContext availability, command safety, and placement guard expectations.

## Triggers

- validate-hooks
- validate hooks
- check hooks.json
- hooks audit
- hook safety check

## Allowed Tools

- Read
- Glob
- Grep
- Bash

## Quick Use

```bash
python3 skills/validate-hooks/scripts/compile-validate-hooks.py \
  --hooks-json hooks/hooks.json \
  --plugin-root .
```

[CODE] The script reads configuration and script paths only. It does not execute hook commands and does not mutate config.

## Output Format

Markdown or HTML hooks audit with summary, evidence, findings, ToolUseContext compatibility, command safety, placement guard status, remediation checklist, validation, and residual limits.

## Deterministic Assets

- [CODE] `assets/hook-compatibility-matrix.json` is the executable source for the 22 events and 4 hook types.
- [CODE] `assets/command-safety-policy.json` defines offline command-string checks.
- [CODE] `assets/placement-guard-expectations.json` defines the expected PreToolUse placement guard registration.
- [CODE] `scripts/check.sh` validates positive and negative fixtures.
