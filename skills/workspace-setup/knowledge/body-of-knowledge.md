# Workspace Setup Body of Knowledge

## Canon

`workspace-setup` designs local profile setup plans. It does not require live credentials, remote accounts, network calls, or random values. The default outcome is a dry-run plan for `.jm-adk.local.json`; applying the profile requires explicit approval.

## Deterministic Profile Fields

| Field | Requirement |
|---|---|
| `target_file` | Must be `.jm-adk.local.json` |
| `mode` | `dry-run` by default; `apply` only when explicit |
| `profile.goal` | Non-empty user goal |
| `profile.runtime` | Named runtime such as Codex, Claude Code, or local CLI |
| `profile.autonomy` | Human-readable autonomy rule |
| `profile.workspace_area` | Local workspace path such as `workspace/` |
| `profile.output_format` | Deterministic response format |

## Safety Invariants

- Preserve existing local profile state unless overwrite is requested with `force=true`.
- Reject secret storage and require a completed secret scan in the plan.
- Keep `.jm-adk.local.json` local-only and gitignored.
- Encode dangerous commands as prohibited or escalation-required, not allowed.
- Validate offline before any apply step.

## Quality Signals

| Signal | Target |
|---|---|
| Evidence coverage | Every setup claim has an evidence tag and source |
| Command policy | Allowed commands are narrow; destructive commands are prohibited |
| Privacy boundary | No secrets, local-only storage, explicit redactions |
| Write safety | Dry-run default, explicit apply, force required for overwrite |
| Validation | Assets and deterministic scripts are referenced by evals and review evidence |
