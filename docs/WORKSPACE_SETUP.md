# Workspace Setup

## Purpose

Alfa separates versioned kit files from local runtime state. First-use setup creates or previews local preferences without changing tracked files.

## Local Profile

`.jm-adk.local.json` is the local profile. It is ignored by git and may include:

- Primary goal.
- Project type and stack.
- Preferred runtime.
- Autonomy level.
- Command policy.
- Privacy constraints.
- Workspace area.
- Output format.

It must not include credentials, tokens, API keys, private keys, passwords, or customer secrets.

## Commands

Preview:

```bash
python3 scripts/setup-workspace-profile.py --dry-run
```

Apply:

```bash
python3 scripts/setup-workspace-profile.py --apply
```

Overwrite only after review:

```bash
python3 scripts/setup-workspace-profile.py --apply --force
```

## Workspace State

Use `workspace/` for runtime state. The workspace manager owns task logs, changelogs, plans, and artifact folders. Do not commit generated workspace contents.

## Quality Checklist

- Confirm Alfa repo before writing.
- Dry-run before profile setup.
- Reject secret-like input.
- Preserve existing profile unless `--force`.
- Validate JSON after setup.
