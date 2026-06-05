# Recovery Source Inventory 2026-06-05

## Executive Summary

- [CONFIG] Brand scope: JM Labs / Alfa.
- [CODE] Active repo: `/Users/deonto/Documents/workspace/jm-adk-alfa`.
- [CODE] Current audited baseline: `origin/main` at `d90399310c899b47e4cae0dcb733ec36e59d49e2`.
- [CODE] Current Alfa inventory: `585` skill directories, `585` ledger rows, `0` untracked skills, `0` script-backed skills pending in ledger, and `7` review docs still mapped to non-complete ledger rows.
- [INFERENCE] Recovery should use source inventory and selective reconstruction, not direct merges from old branches or old repositories.

## Source Map

| Source | Evidence | Current Role | Recovery Decision |
|---|---|---|---|
| `/Users/deonto/Documents/workspace/jm-adk-alfa` | [CODE] Local Git repo with `origin` set to `https://github.com/JaviMontano/jm-adk-alfa`. | [CONFIG] Canonical Alfa delivery repo. | [CONFIG] All delivery PRs start from `origin/main`. |
| `/Users/deonto/Documents/jm-adk` | [CODE] Local repo reports `No commits yet on main` and only untracked `.DS_Store`. | [INFERENCE] Not a usable local source of old work. | [CONFIG] Do not recover from this local directory. |
| `JaviMontano/jm-adk` | [CODE] Public GitHub repo, default branch `main`, `160` remote `SKILL.md` files. | [INFERENCE] Old repo with recoverable skill ideas. | [CONFIG] Normalize candidates into Alfa one batch at a time. |
| `JaviMontano/skills` | [CODE] Private GitHub repo, default branch `main`, `1` remote `SKILL.md` file. | [INFERENCE] Private standalone skill source. | [CONFIG] Recover only after explicit privacy/brand review. |
| `origin/claude/doc-factory-engine` | [CODE] Remote branch with no PR and doc-factory files under `scripts/doc-factory/`. | [INFERENCE] High-value orphan branch with risky direct diff. | [CONFIG] Cherry-pick selected files into a new PR from `origin/main`; never merge the branch wholesale. |

## Transit PRs And Branches

| Ref | Evidence | Status | Decision |
|---|---|---|---|
| PR #18 `codex/skill-script-determinism` | [CODE] Open draft PR; head branch also has historical merged PR #14. | [INFERENCE] Mixed checkpoint and no-merge audit trail. | [CONFIG] Keep as checkpoint until replacements are confirmed, then close as superseded. |
| PR #17 `codex/predeploy-funnel-analytics-20260603` | [CODE] Open draft checkpoint documenting pre-deploy review only. | [INFERENCE] Not a code delivery PR. | [CONFIG] Close after a real `funnel-analytics` code PR is delivered or explicitly abandoned. |
| PR #11 `chore/skill-description-enrichment` | [CODE] Open PR touching broad skill descriptions. | [INFERENCE] Too broad for current deterministic delivery flow. | [CONFIG] Replace with smaller batches or close as superseded after inventory review. |
| PR #10 `docs/katas-info-refresh` | [CODE] Open documentation PR with limited docs/surface files. | [INFERENCE] Candidate for separate validation and merge. | [CONFIG] Revalidate from current `main` before merge. |
| PR #2 `claude/fix-ci-frontmatter` | [CODE] Open old CI/frontmatter PR. | [INFERENCE] Likely obsolete after current validators and counts. | [CONFIG] Replace with targeted fixes only if current CI proves the issue still exists. |
| `origin/claude/doc-factory-engine` | [CODE] No PR associated with this branch. | [INFERENCE] Orphan branch with useful implementation paths and dangerous whole-branch drift. | [CONFIG] Recover via new branch and scoped file selection. |

## Candidate Skill Delta

- [CODE] Alfa has `585` skill packages under `skills/*/SKILL.md`.
- [CODE] `JaviMontano/jm-adk` has `160` normalized skill names.
- [CODE] `96` old `jm-adk` skill names overlap with Alfa.
- [CODE] `64` old `jm-adk` skill names are not present in Alfa.
- [CODE] `JaviMontano/skills` contributes `1` additional private standalone candidate: `metodologia-brand-html`.

### Old `jm-adk` Differentials

[CODE] `acceptance-criteria-writer`, `accessibility-implementation`, `adr-generator`, `api-designer-skill`, `api-surface-analyzer`, `architecture-design`, `architecture-mapper`, `ci-cd-analyzer`, `ci-cd-pipeline-designer`, `code-review-framework`, `code-smell-detector`, `codebase-metrics`, `data-model-analyzer`, `data-model-designer`, `data-modeling-patterns`, `debt-classifier`, `dependency-auditor`, `deployment-strategy`, `developer-experience-auditor`, `diagnostic-engine`, `disaster-recovery-planner`, `documentation-auditor`, `documentation-generator`, `event-driven-design`, `evidence-classifier`, `file-change-planner`, `friction-detector`, `implementation-planning`, `incident-analyzer`, `infrastructure-mapper`, `lessons-learned-tracker`, `maintainability-scorer`, `microservices-decomposer`, `migration-planner`, `observability-architecture`, `observability-design`, `observability-gap-analyzer`, `performance-bottleneck-identifier`, `performance-budget`, `performance-profiler`, `query-optimization`, `realtime-data-sync`, `release-planner`, `repository-scanner`, `resilience-design`, `risk-controlling`, `risk-scorer`, `root-cause-analyzer`, `scaffold-api-rest`, `scaffold-docker-dev`, `scaffold-firebase-project`, `scaffold-monorepo`, `scaffold-nextjs-app`, `scaffold-supabase-project`, `scalability-assessor`, `schema-migration-strategy`, `security-surface-scanner`, `security-threat-modeler`, `tech-debt-quantifier`, `technical-discovery`, `test-coverage-analyzer`, `test-strategy-designer`, `trade-off-analyzer`, `vector-database-design`.

## Recovery Rules

- [CONFIG] Start every recovery PR from `origin/main`.
- [CONFIG] Use one unit per PR: one skill, one tightly coupled skill batch, one doc-only PR, or one infrastructure slice.
- [CONFIG] Treat old repos and stale branches as source material, not merge targets.
- [CONFIG] A recovered skill must satisfy the Alfa DoD: assets manifest, skill-specific examples/evals, review doc, ledger row, and deterministic script checks when scripts exist.
- [CONFIG] If a source package lacks Alfa DoD artifacts, rebuild it with `scripts/scaffold-skill.py` and targeted deterministic assets instead of copying old structure.
- [CONFIG] Do not bring private or brand-specific material from `JaviMontano/skills` into public Alfa without explicit privacy and brand review.

## Recommended Next Delivery Order

1. [CONFIG] Revalidate and merge PR #10 if it remains clean against current `main`.
2. [CONFIG] Create `codex/recover-doc-factory-engine-20260605` from `origin/main` and copy only `scripts/doc-factory/**` plus the minimum schema/template files needed for validation.
3. [CONFIG] Create the first old-repo skill recovery batch with 3 to 5 low-conflict skills from the `64` differentials, each converted to Alfa DoD.
4. [CONFIG] Close #17 and #18 only after their replacement PRs are merged or explicitly marked no-longer-needed.
5. [CONFIG] Reassess #11 and #2 after current CI and docs refresh, then replace or close instead of merging stale broad diffs.

## Verification Evidence

- [CODE] `python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format markdown`.
- [CODE] `gh pr list --state open --json number,title,headRefName,isDraft,mergeStateStatus,updatedAt,url --limit 30`.
- [CODE] `git branch -r --no-merged origin/main` cross-checked with `gh pr list --state all`.
- [CODE] `gh api repos/JaviMontano/jm-adk/git/trees/main?recursive=1`.
- [CODE] `gh api repos/JaviMontano/skills/git/trees/main?recursive=1`.
- [CODE] `git diff --name-only origin/main..origin/claude/doc-factory-engine`.
