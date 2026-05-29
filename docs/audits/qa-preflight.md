# QA Preflight

Date: 2026-05-28
Branch: `qa/adversarial-exploratory-hardening`
Target: `https://github.com/JaviMontano/jm-adk-alfa`
Local checkout: `/Users/deonto/Documents/workspace/jm-adk-alfa`

## Tooling

| Tool | Result | Evidence |
|---|---|---|
| `git` | available | `/usr/bin/git` |
| `gh` | available | `/opt/homebrew/bin/gh` |
| `python3` | available | `/usr/bin/python3` |
| `bash` | available | `/bin/bash` |
| `jq` | available | `/usr/bin/jq` |
| `shellcheck` | not found in PATH | `command -v shellcheck` produced no path |

## Repository State

| Check | Result | Evidence |
|---|---|---|
| Existing clone search | no clone found in common local roots | `find /Users/deonto/Documents /Users/deonto/Desktop /Users/deonto/Downloads /Users/deonto/skills -maxdepth 5 -type d -name jm-adk-alfa` returned no paths |
| Clone target | cloned into a new safe directory | `/Users/deonto/Documents/workspace/jm-adk-alfa` |
| Initial branch | `main` | `git branch --show-current` |
| Working branch | `qa/adversarial-exploratory-hardening` | `git switch -c qa/adversarial-exploratory-hardening` |
| Remote | `origin https://github.com/JaviMontano/jm-adk-alfa` | `git remote -v` |
| Nested `.git` directories | none found in the working tree | `find . -mindepth 2 -name .git -type d -prune -print` returned no paths |
| Tracked local state | only `workspace/.gitkeep` is tracked | `git ls-files '.env*' '.jm-adk.local.json' '.codex/**' '.local/**' 'workspace/**'` |
| Local state directories | `workspace/` exists | `find . -maxdepth 3 (...)` |

## Safety Constraints

No destructive commands were used.
No push was made.
No `.env`, token, credential, or key file was opened or modified.
Secret-pattern scanning was path-only and produced no matches.
The only tracked workspace path remained `workspace/.gitkeep`.

## Baseline Quality Gates

| Command | Result |
|---|---|
| `python3 scripts/count-components.py` | `skills=524 agents=256 commands=260 prompts=256 components=1296` |
| `python3 scripts/count-components.py --check-docs` | passed |
| `python3 scripts/validate-skills.py --strict` | `skills=524 warnings=0 errors=0` |
| `bash scripts/check-repo-boundaries.sh` | `Repo boundaries OK` |
| `python3 scripts/scaffold-skill.py ... --dry-run` | planned 16 files, wrote 0 |

## Initial Risk Notes

The repo already had a hardening baseline: safe sync, component counts, strict skill validation, repo boundary checks, dry-run scaffolding, and CI.
The adversarial surface therefore focused on false-safe paths: duplicate skills that silently no-op, path-like names sanitized instead of rejected, invalid tools accepted at scaffold time, `.codex/` local state not blocked by the boundary checker, stale contribution docs, and missing adversarial regression tests.
