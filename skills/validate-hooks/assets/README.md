# Assets for validate-hooks

[CODE] These assets define the deterministic offline contract for hook audits.

## Files

- [CODE] `hooks-audit-schema.json` defines required audit input fields and supported audit modes.
- [CODE] `hook-compatibility-matrix.json` defines the 22 events, 4 hook types, and ToolUseContext compatibility.
- [CODE] `command-safety-policy.json` defines command string patterns that must be reported without executing commands.
- [CODE] `placement-guard-expectations.json` defines the expected PreToolUse placement guard shape.
- [CODE] `validate-hooks-template.md` defines the stable Markdown report layout used by the compiler.
