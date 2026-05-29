# Troubleshooting JM-ADK

Use this guide when a validation, sync, scaffold, or agent workflow fails.
Stop before guessing.
Capture evidence, keep local state local, and rerun the smallest command that reproduces the problem.

## First Response

1. Confirm you are inside the repo.

```bash
git rev-parse --show-toplevel
git status --short --branch
```

2. Run the safe baseline checks.

```bash
python3 scripts/count-components.py --check-docs
python3 scripts/validate-skills.py --strict
bash scripts/check-repo-boundaries.sh
python3 scripts/qa/run-adversarial-tests.py
```

3. If a command fails, report the command, exact output, current branch, and whether you have local changes.

## What Not to Touch

Do not commit these paths:

```text
.env*
.jm-adk.local.json
.local/
.codex/
workspace/
```

`workspace/.gitkeep` is the only workspace file that should be tracked.

Do not use `git reset --hard`, `git clean -fdx`, force push to `main`, or manual deletion to fix a validation failure.
Use a branch, inspect the diff, and prefer additive fixes.

## Common Failures

| Symptom | Likely Cause | Safe Next Step |
|---|---|---|
| `ERROR: working tree is not clean` | Safe sync refuses to run with local changes. | Commit intentional work or stash with a clear message, then retry. |
| `nested git repository detected` | A clone or `.git` directory exists inside the kit. | Move the nested repo outside JM-ADK; do not delete blindly. |
| `tracked .codex state detected` | Codex local config was staged or tracked. | Unstage it, keep it local, and rerun boundary checks. |
| `tracked workspace state detected` | Runtime files entered `workspace/`. | Move or unstage them; only `workspace/.gitkeep` belongs in Git. |
| `skill already exists` | Scaffold target slug is already present. | Pick a new name, use `--all-existing`, or use `--force` only after reviewing the diff. |
| `unknown allowed tool` | A skill declares a tool outside the supported contract. | Use one of the supported tools or an `mcp__server__tool` name. |
| `invalid JSON` | `evals/evals.json` or `knowledge/knowledge-graph.json` is malformed. | Fix the file shown in the error and rerun strict validation. |
| Component count drift | Docs or generated index no longer match real files. | Run `python3 scripts/count-components.py --check-docs`; regenerate the index if component metadata changed. |

## Report a Failure to an Agent

Paste this shape into the agent:

```md
Goal:

Repo path:

Branch:

Command that failed:

Exact output:

Files changed before failure:

What I expected:

What I need preserved:
- workspace/
- .local/
- .codex/
- .jm-adk.local.json
- .env*
```

The agent should read before writing, avoid destructive commands, reproduce the failure, apply the smallest fix, and rerun the relevant quality gate.

## Safe Update Flow

Use:

```bash
bash scripts/sync-upstream-safe.sh --remote origin
```

The script refuses dirty worktrees, shows divergence, fast-forwards only when safe, and never uses `reset --hard`.
For parallel agent work, prefer a Git worktree outside the repo instead of a nested clone.

## Safe Skill Creation

Preview first:

```bash
python3 scripts/scaffold-skill.py \
  --name my-skill \
  --description "Short description" \
  --triggers my-skill \
  --allowed-tools Read,Grep,Glob,Bash \
  --dry-run
```

Create only after reviewing the planned files.
Use `--local` for experiments that must stay ignored.
Use `--force` only when you intentionally want to overwrite existing files after reviewing the diff.
