# Git Sync Local Safe

This guide keeps JM-ADK easy to update from GitHub without breaking local work.

## Remote Model

`origin` is the remote you push your working branch to. If you have write access to `JaviMontano/jm-adk-alfa`, `origin` can point directly to that repo. If you do not have write access, `origin` should be your fork and `upstream` should point to `https://github.com/JaviMontano/jm-adk-alfa`.

Use a direct branch when you are a maintainer. Use a fork when you are an external contributor or when repository permissions are uncertain.

## Keep `main` Clean

Do not work directly on `main`.

```bash
git switch main
git pull --ff-only origin main
git switch -c hardening/my-change
```

If `main` has local changes, stop and inspect them. Do not use `git reset --hard`.

## Protect Local State

These paths are local and should not be committed:

- `.jm-adk.local.json`
- `.local/`
- `.codex/`
- `.env*`
- `workspace/` except `workspace/.gitkeep`

Run:

```bash
bash scripts/check-repo-boundaries.sh
```

## Fast-Forward Safely

Use the safe sync script from a clean working tree:

```bash
bash scripts/sync-upstream-safe.sh --remote origin
```

The script:

- detects repo root with `git rev-parse --show-toplevel`;
- refuses dirty working trees;
- fetches all remotes with prune and tags;
- shows local/remote/base SHAs;
- fast-forwards only when safe;
- never runs `git reset --hard`;
- never touches `workspace/` or `.jm-adk.local.json`;
- never pushes unless `--push-branch` is explicit.

## When Local Changes Exist

Prefer committing intentional work on a branch. If you must stash, include untracked files and a clear message:

```bash
git stash push -u -m "WIP before syncing jm-adk: <reason>"
```

After syncing:

```bash
git stash list
git stash show --stat stash@{0}
git stash pop stash@{0}
```

Resolve conflicts by reading the files and keeping local overrides in local-only paths.

## Force Push Policy

Do not force push to `main`.

Use `--force-with-lease` only on your own feature branch, only after checking the remote branch state, and only when replacing your own branch history is intentional:

```bash
git fetch origin
git log --oneline --graph --decorate origin/hardening/my-change..hardening/my-change
git push --force-with-lease origin hardening/my-change
```

## Worktree Option

Use `git worktree` when you need multiple concurrent branches without nested clones:

```bash
git worktree add ../jm-adk-alfa-hardening hardening/skill-scaffold-sync-safe
```

Do not clone another copy inside the repo. Detect nested repositories with:

```bash
bash scripts/check-repo-boundaries.sh
```

## PR Flow

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
git status --short
git push -u origin hardening/skill-scaffold-sync-safe
gh pr create --base main --head hardening/skill-scaffold-sync-safe --title "Harden skill scaffolding and safe sync" --body "Adds upgrade-safe skill scaffolding, validators, local-state boundaries, and sync documentation."
```
