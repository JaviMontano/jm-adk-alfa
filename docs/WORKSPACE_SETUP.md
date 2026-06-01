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

## User Context Repo

Use `user-context/` for durable user context inside the developer kit. It is
recognized by `user-context/.jm-adk-context.json`, independent of the private
files the user adds later.

`user-context/` is not task state. It is for long-lived background,
preferences, memory, and private source indexes that the user explicitly wants
Alfa to reuse. Private content is ignored by git by default.

Diagnostics:

```bash
python3 scripts/diagnose-user-context.py --dry-run
```

Scaffold or repair the context repo:

```bash
python3 scripts/scaffold-user-context.py --dry-run
python3 scripts/scaffold-user-context.py --apply
```

## Quality Checklist

- Confirm Alfa repo before writing.
- Dry-run before profile setup.
- Reject secret-like input.
- Preserve existing profile unless `--force`.
- Keep durable context in `user-context/`, not `workspace/`.
- Validate JSON after setup.
