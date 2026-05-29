# Exploratory QA Charter

Date: 2026-05-28
Branch: `qa/adversarial-exploratory-hardening`

## Charter A: New User Onboarding

| Field | Notes |
|---|---|
| Objective | Verify a new user can clone, understand local-state boundaries, and run the first validation commands. |
| Setup | Fresh clone at `/Users/deonto/Documents/workspace/jm-adk-alfa`. |
| Steps | Read `README.md`, `AGENTS.md`, `docs/getting-started.md`; run count, strict skill validation, boundary check, and scaffold dry-run. |
| Observations | README gives a short install path and current counts. Getting started documents `workspace/` and `.jm-adk.local.json`. `AGENTS.md` is concise but assumes the reader already understands Pristino/JM-ADK. |
| Bugs | `CONTRIBUTING.md` still referenced the older `jm-agentic-development-kit` repo and `.agent/scripts/*` validation commands. |
| Improvements | Update contribution commands and add troubleshooting flow linked from README. |
| Evidence | `python3 scripts/count-components.py` returned `components=1296`; `python3 scripts/validate-skills.py --strict` returned `warnings=0 errors=0`; `bash scripts/check-repo-boundaries.sh` returned `Repo boundaries OK`. |
| Decision | fix now |

## Charter B: Existing User Update

| Field | Notes |
|---|---|
| Objective | Verify update flow protects dirty worktrees and local state. |
| Setup | Existing branch plus isolated temporary repo fixture for dirty-tree simulation. |
| Steps | Review `docs/git-sync-local-safe.md`, run `bash scripts/sync-upstream-safe.sh --help`, simulate dirty worktree. |
| Observations | Safe sync refuses dirty worktrees before remote operations and avoids `reset --hard`. |
| Bugs | Dirty-tree behavior was not covered by automated adversarial tests before this branch. |
| Improvements | Add `sync_aborts_dirty_tree` to `scripts/qa/run-adversarial-tests.py` and CI. |
| Evidence | Test output: `PASS sync_aborts_dirty_tree`; actual result included `ERROR: working tree is not clean`. |
| Decision | fix now |

## Charter C: Skill Lifecycle

| Field | Notes |
|---|---|
| Objective | Validate dry-run, real creation risk, duplicate slug behavior, frontmatter, evals, triggers, and allowed tools. |
| Setup | Existing `skills/bmad-method` plus temporary skill fixtures. |
| Steps | Run scaffold dry-run; attempt duplicate slug dry-run; attempt path-like name; attempt invalid allowed tool; validate temp skills. |
| Observations | The scaffold creates a rich canonical structure with evals, examples, prompts, agents, and knowledge files. |
| Bugs | Duplicate slugs could previously return a successful no-op. Path-like names were normalized instead of rejected. Unknown tools were accepted at scaffold time. |
| Improvements | Reject existing slugs without `--force`, reject path-like names, reject unknown tools, and test all paths. |
| Evidence | Tests `scaffold_rejects_duplicate_without_force`, `scaffold_rejects_path_traversal`, `scaffold_rejects_unknown_tool`, `validator_rejects_unknown_tool_strict` passed. |
| Decision | fix now |

## Charter D: Skill as Operational Rail

| Field | Notes |
|---|---|
| Objective | Check whether a skill can carry reusable process, examples, evals, scripts/tools, and validation. |
| Setup | Scaffold output plan and existing skills. |
| Steps | Review canonical scaffold files, eval JSON, knowledge graph, output template, and examples. |
| Observations | Scaffolded skills include the minimum rail artifacts. Existing validators parse JSON and links. |
| Bugs | No generic output contract validator exists for CSV/HTML/Excel deliverables. |
| Improvements | Backlog fixture-based checks for representative output artifacts. |
| Evidence | `scaffold-smoke-test --dry-run` planned 16 files and wrote 0. |
| Decision | backlog |

## Charter E: Adaptation Between Environments

| Field | Notes |
|---|---|
| Objective | Review portability across Codex, Antigravity, Claude/Gemini, and compatible runners. |
| Setup | Root docs, `.agent/`, `GEMINI.md`, `AGENTS.md`, `.claude-plugin/`, adapter scripts. |
| Steps | Review environment docs and adapter scripts inventory. |
| Observations | The repo contains multiple runner-facing surfaces. The default README now favors stdlib scripts and safe local state. |
| Bugs | Some contribution docs used older Claude Code/plugin commands as if they were current defaults. |
| Improvements | Refresh `CONTRIBUTING.md`; backlog a concise compatibility matrix for runner-specific commands. |
| Evidence | `CONTRIBUTING.md` had `jm-agentic-development-kit` and `.agent/scripts/validate_skills.py` references before this branch. |
| Decision | fix now + backlog |

## Charter F: Inputs and Outputs

| Field | Notes |
|---|---|
| Objective | Verify clear paths for input files and generated outputs. |
| Setup | README, docs, workspace manager, skills. |
| Steps | Inspect `workspace/`, `.local/`, output templates, and docs. |
| Observations | `workspace/` is identified as local runtime state. Scaffolded skills include `templates/output.md` and examples. |
| Bugs | No repo-wide acceptance tests were found for PDF, CSV, Markdown, image fixture, Word, Excel, or HTML output contracts. |
| Improvements | Backlog fixtures under a future output-contract suite. |
| Evidence | `workspace/.gitkeep` is the only tracked workspace file. |
| Decision | backlog |

## Charter G: Security and Privacy

| Field | Notes |
|---|---|
| Objective | Confirm local config, secrets, and private runtime state are protected. |
| Setup | `.gitignore`, boundary checker, tracked-file query, path-only secret-pattern scan. |
| Steps | Query tracked local paths; run boundary checker; run path-only secret pattern scan. |
| Observations | `.gitignore` protects `.env*`, `.jm-adk.local.json`, `.local/`, `.codex/`, and workspace contents except `.gitkeep`. |
| Bugs | Boundary checker did not fail tracked `.codex/` state before this branch. |
| Improvements | Add `.codex/` tracked-state check and adversarial fixture. |
| Evidence | `PASS boundaries_detect_tracked_codex`; `git ls-files ...` returned only `workspace/.gitkeep`; secret-pattern path scan produced no matches. |
| Decision | fix now |

## Charter H: Cognitive Friction

| Field | Notes |
|---|---|
| Objective | Detect long, contradictory, duplicated, or stale docs that slow the vibe coder. |
| Setup | README, getting started, contributing, sync docs, audit docs. |
| Steps | Read the main onboarding path and contribution docs. |
| Observations | README is compact; `docs/getting-started.md` is usable; `CONTRIBUTING.md` lagged behind current repo names and commands. |
| Bugs | Stale contribution instructions could send contributors to a different repo and non-current validation scripts. |
| Improvements | Update contribution commands and add troubleshooting. |
| Evidence | Before this branch, contribution setup used `gh repo fork JaviMontano/jm-agentic-development-kit --clone` and `python3 .agent/scripts/validate_skills.py`. |
| Decision | fix now |

## Charter I: Concurrent Agents

| Field | Notes |
|---|---|
| Objective | Assess collision risk when two agents or branches work in parallel. |
| Setup | Safe sync docs, workspace rules, scaffold force policy. |
| Steps | Review branch guidance, worktree option, local state policy, duplicate skill flow. |
| Observations | `docs/git-sync-local-safe.md` recommends worktrees and refuses dirty sync. Duplicate skill guard now prevents accidental shared-path ambiguity. |
| Bugs | No lock file or generated-output collision protocol exists for multi-agent writes beyond Git/worktree discipline. |
| Improvements | Backlog: document optional per-branch worktree convention for agent runs. |
| Evidence | `docs/git-sync-local-safe.md` includes a worktree option; `scaffold_rejects_duplicate_without_force` passed. |
| Decision | backlog |

## Charter J: Recovery

| Field | Notes |
|---|---|
| Objective | Confirm errors are actionable for invalid JSON, frontmatter/tool contracts, duplicate skills, subdirectory commands, and missing optional tools. |
| Setup | Temporary fixtures and repo scripts. |
| Steps | Run adversarial tests for invalid JSON, unknown tools, duplicate triggers, duplicate slug, dirty tree, nested git, `.codex`, and subdirectory scripts. |
| Observations | The new suite reports purpose, risk, expected result, actual result, pass/fail, and fix guidance. |
| Bugs | Before this branch, these recovery cases were not consolidated in a repeatable test command. |
| Improvements | Add `scripts/qa/run-adversarial-tests.py` and run it in CI. |
| Evidence | `summary: passed=11 failed=0 total=11`. |
| Decision | fix now |
