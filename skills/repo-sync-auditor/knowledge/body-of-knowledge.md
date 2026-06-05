# Repo Sync Auditor Body of Knowledge

## Core Principle

Repository sync work is a truth-maintenance problem before it is a Git problem.
The audit must separate four states:

1. local files in the working tree;
2. local branch history;
3. local remote-tracking refs such as `origin/main`;
4. GitHub truth such as merged PR state.

Never infer deployment from a draft/staging PR when `origin/main` lacks the
files. Never infer ledger truth from local patches that were intentionally
excluded from a PR.

## Safe Baseline

- Read `git status --porcelain=v1` before switching branches.
- Read `HEAD`, branch, upstream, and `origin/main` before applying patches.
- Treat dirty generated files as a PR hygiene issue, not as proof of corruption.
- Treat stale ledger rows as process drift until a dedicated reconciliation PR
  updates them.

## Alfa-Specific Drift Signals

- `docs/audits/skill-review-ledger.csv` can lag behind real merged skill slices
  because large ledger rewrites have been deferred for transport safety.
- `docs/audits/skills/*-review.md` present in `main` is stronger evidence than
  a ledger `pending` row, but the ledger still controls cursor reporting.
- `skills/*/scripts/check.sh` present in `main` means a skill has deterministic
  automation that should be cross-checked against ledger status.
- `PRISTINO-INDEX.md` and `.agent/skills_index.json` must be regenerated when a
  skill frontmatter description changes.

## Anti-Patterns

- Merging a batch PR that was only meant as staging.
- Counting local prepared patches as deployed code.
- Applying a patch from a branch that is behind `origin/main`.
- Editing the ledger inside every skill PR when the ledger delta is broad or
  stale.
