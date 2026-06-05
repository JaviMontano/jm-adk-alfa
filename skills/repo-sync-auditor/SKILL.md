---
name: repo-sync-auditor
version: 1.1.0
description: Audit local and remote Git repository sync state without mutating history, including branch/base drift, dirty-tree risk, ledger-vs-skill mismatches, review-doc coverage, generated index freshness signals, and a safe reconciliation plan. Use when the user asks to resume work, prepare a PR, reconcile local vs remote state, verify what is really deployed, or diagnose repo drift before writing or merging. [EXPLICIT]
owner: "JM Labs (Javier Montano)"
triggers:
  - repo sync
  - sync auditor
  - local remote divergence
  - git baseline
  - safe fetch
  - resume repo work
  - verify deployed skills
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Repo Sync Auditor

Audit repository truth before editing, publishing, or merging. The skill is
read-only by default and focuses on preventing false state: stale branches,
dirty worktrees, ledger drift, missing review docs, stale generated indexes, or
staging PRs being treated as deployed code.

## Deterministic Contract

- Use `assets/git-safety-policy.json` before running any Git command.
- Use `assets/ledger-risk-policy.json` to classify ledger drift and review-doc
  mismatches.
- Use `assets/sync-audit-schema.json` as the report shape.
- Use `assets/remediation-plan-template.md` for the repair plan.
- Run `scripts/audit-repo-sync.py --format markdown` for a human report.
- Run `scripts/audit-repo-sync.py --format json` when another process will
  consume the result.
- Run `scripts/check.sh` before shipping changes to this skill.
- Do not run `git reset`, `git clean`, force-push, rebase, checkout over user
  work, or update remote refs from this skill.

## Procedure

### Step 1: Establish Baseline

1. Identify the repository root with `git rev-parse --show-toplevel`.
2. Read current branch, `HEAD`, upstream, and local `origin/main` if present.
3. Check dirty/untracked files with `git status --porcelain=v1`.
4. Check ahead/behind against upstream and `origin/main` with local refs only.
5. Do not fetch unless the user explicitly asks for network refresh.

### Step 2: Compare Repository Truth

Audit these surfaces:

- `docs/audits/skill-review-ledger.csv` row count, statuses, and untracked
  skill directories.
- `docs/audits/skills/*-review.md` coverage vs ledger status.
- `skills/*/scripts/check.sh` coverage vs ledger status.
- generated-file dirtiness for `.agent/skills_index.json`,
  `PRISTINO-INDEX.md`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
  `.cursorrules`, and `.windsurfrules`.
- known staging branches or PRs that must not be used as deployment evidence.

### Step 3: Classify Risk

Classify blockers without mutating the repo:

- dirty tree before branch switch or patch apply
- branch behind `origin/main`
- ledger rows missing for skills
- review docs present while ledger status remains `pending`
- skills with deterministic scripts while ledger status remains `pending`
- generated files already dirty before PR

### Step 4: Produce Plan

Return a concise report with evidence tags:

- `[CODE]` for command output, files, refs, paths, counts, and diffs.
- `[CONFIG]` for policies, remote names, branch conventions, and intentional
  exclusions.
- `[DOC]` for briefs, PR descriptions, review docs, and process records.
- `[INFERENCE]` for recommended ordering, risk classification, and next action.

## Output

Use `templates/output.md` for the human report:

```bash
python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format markdown
```

For machine consumers:

```bash
python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format json
```

## Validation

Run:

```bash
bash skills/repo-sync-auditor/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill repo-sync-auditor
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill repo-sync-auditor
```

## Limits

- The audit uses local refs. If a fresh network baseline is required, run a
  separate explicit `git fetch --prune origin` before invoking the skill.
- The audit reports ledger drift; it does not edit the ledger.
- The audit can identify likely deployment truth from files and review docs,
  but GitHub PR state still needs `gh pr view` or API verification when exact
  merge metadata matters.

## Related Skills

- `git-workflow`
- `workspace-governance`
- `workflow-orchestration`
- `agent-creator`
