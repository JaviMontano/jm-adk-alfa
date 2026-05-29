# Adversarial Test Plan

Date: 2026-05-28
Branch: `qa/adversarial-exploratory-hardening`
Runner: `python3 scripts/qa/run-adversarial-tests.py`

## Implemented Safe Tests

| Test | Purpose | Risk Protected | Fixture | Expected Result | Actual Result |
|---|---|---|---|---|---|
| `scaffold_rejects_path_traversal` | Reject path-like skill names. | Path traversal or accidental writes outside `skills/`. | Repo root, dry-run. | Non-zero exit with slug-like-name error. | PASS |
| `scaffold_rejects_duplicate_without_force` | Refuse duplicate skill slug without explicit force. | Silent no-op or overwrite ambiguity. | Existing `skills/bmad-method`. | Non-zero exit with existing-skill error. | PASS |
| `scaffold_rejects_unknown_tool` | Reject unavailable tools at scaffold time. | Skill contracts advertise tools the runner cannot provide. | Repo root, dry-run. | Non-zero exit with unknown-tool error. | PASS |
| `scaffold_local_dry_run_stays_local` | Confirm local skill mode targets ignored `.local/skills`. | Experimental skill enters versioned kit paths. | Repo root, dry-run. | Zero exit with `.local/skills/...` output. | PASS |
| `validator_rejects_unknown_tool_strict` | Fail strict validation on invalid tool contract. | CI passes unusable skills. | Temporary git repo with `Destroy` tool. | Non-zero exit and unknown-tool error. | PASS |
| `validator_detects_duplicate_high_risk_trigger` | Detect duplicated generic triggers. | False activation across skills. | Temporary git repo with two `deploy` triggers. | Non-zero exit and duplicate-trigger error. | PASS |
| `validator_reports_invalid_json` | Fail invalid eval JSON with a concrete path. | Broken evals/knowledge graph reaches users. | Temporary git repo with invalid `evals/evals.json`. | Non-zero exit and invalid JSON path. | PASS |
| `boundaries_detect_tracked_codex` | Reject tracked `.codex/` state. | Agent local config leaks into repo. | Temporary git repo with staged `.codex/config.toml`. | Non-zero exit and `.codex` boundary error. | PASS |
| `boundaries_detect_nested_git` | Reject nested `.git` directories. | Nested clone corrupts update/sync mental model. | Temporary git repo with `fixtures/nested/.git`. | Non-zero exit and nested-git error. | PASS |
| `sync_aborts_dirty_tree` | Abort safe sync before remote operations when dirty. | Local work gets mixed with update flow. | Temporary git repo with untracked file. | Non-zero exit and dirty-tree error. | PASS |
| `scripts_run_from_subdirectory` | Confirm scripts resolve repo root. | Commands fail when vibe coder runs from `docs/` or a skill folder. | Real repo `docs/` cwd. | Zero exit and component counts. | PASS |

## Minimum Case Coverage

| Required Case | Status | Evidence or Backlog |
|---|---|---|
| Nested repo accidental | implemented | `boundaries_detect_nested_git` |
| Repo cloned inside repo | partially covered | `scripts/check-repo-boundaries.sh` checks clone-like directory names; backlog richer fixture for `.git/config` remote detection |
| Working tree dirty | implemented | `sync_aborts_dirty_tree` |
| Local config versioned accidentally | implemented for `.codex/`; existing checks for `.env`, `.jm-adk.local.json`, `.local/`, `workspace/` | Boundary script and `boundaries_detect_tracked_codex` |
| Skill slug duplicated | implemented | `scaffold_rejects_duplicate_without_force` |
| Trigger duplicated or too generic | implemented for duplicate high-risk triggers | `validator_detects_duplicate_high_risk_trigger`; backlog warnings for short/generic non-duplicate triggers |
| Frontmatter invalid | covered by existing validator, not isolated in new suite | Backlog: add malformed-frontmatter fixture |
| JSON invalid | implemented | `validator_reports_invalid_json` |
| Generated output stale | covered by `count-components.py --check-docs` and CI index freshness | Backlog: add explicit stale-index fixture |
| Script from subdirectory | implemented | `scripts_run_from_subdirectory` |
| Path with spaces | not implemented | Backlog: clone/temp repo path with spaces and run scripts |
| Windows path risk | not implemented | Backlog: document macOS/Linux primary support and add Windows CI if required |
| Large file | not implemented | Backlog: fixture with generated large input and max-size behavior |
| Path traversal | implemented | `scaffold_rejects_path_traversal` |
| Silent overwrite | implemented for duplicate skill without `--force`; scaffold already skips existing files unless forced | `scaffold_rejects_duplicate_without_force` |
| Secrets leakage | partially covered | CI path scans tracked files; no secret contents printed in this audit |
| Dependency absent | partially covered | `shellcheck` optional in CI; backlog explicit missing-tool fixtures for `gh`, `jq`, `python3` |
| Agent hallucinates dependency | documented through troubleshooting | Backlog stronger halt-and-report examples in skill templates |
| Context saturation | not implemented | Backlog context-sharding guidance in runner compatibility docs |
| Unsafe update | implemented | `sync_aborts_dirty_tree`; safe sync uses ff-only and never `reset --hard` |

## Execution

Run:

```bash
python3 scripts/qa/run-adversarial-tests.py
python3 scripts/qa/run-adversarial-tests.py --json
```

Expected summary:

```text
summary: passed=11 failed=0 total=11
```

Every test reports its name, purpose, protected risk, fixture, expected result, actual result, pass/fail status, and fix recommendation.
