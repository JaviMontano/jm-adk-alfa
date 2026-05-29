# QA Run Log

Date: 2026-05-28
Branch: `qa/adversarial-exploratory-hardening`

No destructive commands were used.
No push was made.
No secret contents were printed.

## Preflight

| Command | Result |
|---|---|
| `pwd` | `/Users/deonto/Library/Mobile Documents/com~apple~CloudDocs/Documents/Cosas con IA` before target clone |
| `git rev-parse --show-toplevel` | `/Users/deonto/Library/Mobile Documents/com~apple~CloudDocs/Documents/Cosas con IA` before target clone |
| `command -v git` | `/usr/bin/git` |
| `command -v gh` | `/opt/homebrew/bin/gh` |
| `command -v python3` | `/usr/bin/python3` |
| `command -v bash` | `/bin/bash` |
| `command -v jq` | `/usr/bin/jq` |
| `command -v shellcheck` | no path returned |
| `find ... -name jm-adk-alfa` | no existing clone found in common local roots |
| `git clone https://github.com/JaviMontano/jm-adk-alfa /Users/deonto/Documents/workspace/jm-adk-alfa` | completed |
| `git switch -c qa/adversarial-exploratory-hardening` | branch created |

## Baseline Repository Checks

| Command | Output summary | Status |
|---|---|---|
| `git status --short --branch` | `## main...origin/main` before branch, then `## qa/adversarial-exploratory-hardening` after branch | pass |
| `git remote -v` | `origin https://github.com/JaviMontano/jm-adk-alfa` fetch/push | pass |
| `find . -mindepth 2 -name .git -type d -prune -print` | no output | pass |
| `find . -maxdepth 3 (...)` | `./workspace` | pass |
| `git ls-files '.env*' '.jm-adk.local.json' '.codex/**' '.local/**' 'workspace/**'` | `workspace/.gitkeep` only | pass |
| path-only tracked secret pattern scan | no matching file paths | pass |

## Baseline Quality Gates

| Command | Output summary | Status |
|---|---|---|
| `python3 scripts/count-components.py` | `skills=524 agents=256 commands=260 prompts=256 components=1296` | pass |
| `python3 scripts/count-components.py --check-docs` | `skills=524 agents=256 commands=260 prompts=256 components=1296` | pass |
| `python3 scripts/validate-skills.py --strict` | `skills=524 warnings=0 errors=0` | pass |
| `bash scripts/check-repo-boundaries.sh` | `Repo boundaries OK` | pass |
| `python3 scripts/scaffold-skill.py --name scaffold-smoke-test ... --dry-run` | planned 16 files, wrote 0 | pass |
| `bash scripts/sync-upstream-safe.sh --help` | printed safe-sync usage and non-reset policy | pass |

## Post-Implementation Quality Gates

| Command | Output summary | Status |
|---|---|---|
| `python3 scripts/validate-skills.py --strict` | `skills=524 warnings=0 errors=0` | pass |
| `python3 scripts/count-components.py --check-docs` | `skills=524 agents=256 commands=260 prompts=256 components=1296` | pass |
| `bash scripts/check-repo-boundaries.sh` | `Repo boundaries OK` | pass |
| `python3 scripts/scaffold-skill.py --name scaffold-smoke-test ... --dry-run` | planned 16 files, wrote 0 | pass |
| `python3 scripts/qa/run-adversarial-tests.py` | `summary: passed=11 failed=0 total=11` | pass |
| `python3 scripts/qa/run-adversarial-tests.py --json` | 11 JSON result objects, all `"passed": true` | pass |
| `bash scripts/generate-pristino-index.sh` | `Generated: PRISTINO-INDEX.md`; counts stayed `Agents: 256 | Skills: 524 | Commands: 260 | Prompts: 256 | Components: 1296` | pass |
| `python3 -m json.tool .claude-plugin/marketplace.json` | JSON parsed successfully | pass |
| `git diff --check` | no whitespace errors | pass |
| `git diff --quiet -- PRISTINO-INDEX.md` | no generated index diff after regeneration | pass |

## Adversarial Test Summary

| Test | Result |
|---|---|
| `scaffold_rejects_path_traversal` | PASS |
| `scaffold_rejects_duplicate_without_force` | PASS |
| `scaffold_rejects_unknown_tool` | PASS |
| `scaffold_local_dry_run_stays_local` | PASS |
| `validator_rejects_unknown_tool_strict` | PASS |
| `validator_detects_duplicate_high_risk_trigger` | PASS |
| `validator_reports_invalid_json` | PASS |
| `boundaries_detect_tracked_codex` | PASS |
| `boundaries_detect_nested_git` | PASS |
| `sync_aborts_dirty_tree` | PASS |
| `scripts_run_from_subdirectory` | PASS |

## Known Limits

ShellCheck was not run locally because the binary was not available in PATH; only the CI conditional skip behavior was inspected.
Windows path support, large-file behavior, malformed-frontmatter isolation, and CSV/HTML/Excel output contract tests remain backlog items.
