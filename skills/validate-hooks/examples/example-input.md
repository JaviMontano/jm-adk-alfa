# Example Input

Audit this plugin's hooks without executing them.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "matcher": "startup",
        "command": "printf 'session start check'"
      }
    ],
    "PreToolUse": [
      {
        "type": "command",
        "matcher": "Write",
        "command": "bash scripts/artifact-placement-guard.sh",
        "description": "Placement guard for workspace and maintainer-mode writes"
      }
    ],
    "PermissionRequest": [
      {
        "type": "prompt",
        "matcher": "Bash",
        "prompt": "Assess whether the requested command is safe to approve."
      }
    ],
    "PostToolUse": [
      {
        "type": "agent",
        "matcher": "Bash",
        "agent": "validate-hooks-specialist"
      }
    ]
  }
}
```

Constraints:

- [CODE] Run offline only.
- [CODE] Do not execute hook commands.
- [CODE] Report structure, event names, hook type compatibility, ToolUseContext availability, command safety, placement guard, findings, and remediation checklist.
