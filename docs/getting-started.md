# Getting Started with JM-ADK

## Prerequisites

| Tool | Check |
|---|---|
| Git | `git --version` |
| Python 3 | `python3 --version` |
| Bash | `bash --version` |
| Claude Code or compatible agent runner | environment-specific |

## Clone

```bash
git clone https://github.com/JaviMontano/jm-adk-alfa.git
cd jm-adk-alfa
```

## Validate the Kit

```bash
python3 scripts/count-components.py
python3 scripts/validate-skills.py --strict
bash scripts/check-repo-boundaries.sh
python3 scripts/qa/run-adversarial-tests.py
```

Expected component inventory:

| Component | Count |
|---|---:|
| Skills | 524 |
| Agents | 256 |
| Commands | 260 |
| Prompts | 256 |

## Initialize Local Workspace

`workspace/` is local runtime state. It is ignored by git except for `workspace/.gitkeep`.

```bash
bash scripts/workspace-manager.sh create "first-local-session"
```

Use `.jm-adk.local.json` for local overrides. Do not commit it.

## Create a Skill

Preview first:

```bash
python3 scripts/scaffold-skill.py \
  --name example-skill \
  --description "Example generated skill" \
  --triggers example-skill \
  --allowed-tools Read,Grep,Glob,Bash \
  --owner "JM Labs" \
  --version 0.1.0 \
  --dry-run
```

Create after reviewing the planned files:

```bash
python3 scripts/scaffold-skill.py \
  --name example-skill \
  --description "Example generated skill" \
  --triggers example-skill \
  --allowed-tools Read,Grep,Glob,Bash \
  --owner "JM Labs" \
  --version 0.1.0
```

Create an ignored local experiment:

```bash
python3 scripts/scaffold-skill.py --name local-experiment --description "Local only" --local
```

## Update from GitHub

Read [Git Sync Local Safe](git-sync-local-safe.md), then run from a clean tree:

```bash
bash scripts/sync-upstream-safe.sh --remote origin
```

## When Something Fails

Use [Troubleshooting JM-ADK](troubleshooting.md).
Do not use destructive Git commands to recover.
Capture the failed command, output, current branch, and local changes before asking an agent to fix the issue.

## Contribute

1. Create a branch.
2. Keep local overrides in ignored paths.
3. Run validation.
4. Regenerate `PRISTINO-INDEX.md` when component metadata changes.
5. Open a pull request.
