# Recovery Source Inventory 2026-06-05

## Executive Summary

- [CONFIG] Brand scope: JM Labs / Alfa.
- [CÓDIGO] Active repo: `/Users/deonto/Documents/workspace/jm-adk-alfa`.
- [CÓDIGO] Post-doc-factory code baseline recorded before this inventory-only update: `origin/main` at `3d49ee54ec35520abe39839f0fcb35bc7e8d8344`.
- [CÓDIGO] Current Alfa inventory: `585` skill directories, `585` ledger rows, `30` rows marked `dod-complete`, `555` rows still pending lifecycle review, and `0` non-complete rows with a mapped review doc.
- [CÓDIGO] Script-backed inventory: `22` skills have `scripts/check.sh`, and `0` script-backed skills are pending DoD.
- [CÓDIGO] Open pull requests after execution: `0`.
- [CÓDIGO] Remaining remote source branch with unique historical work: `origin/claude/doc-factory-engine`.
- [INFERENCIA] Recovery should use source inventory and selective reconstruction, not direct merges from old branches or old repositories.

## Executed Cleanup

| Item | Evidence | Result |
|---|---|---|
| PR #39 `docs(skills): complete reviewed skill DoD` | [CÓDIGO] Merged into `main` before this inventory update. | [CONFIG] Seven reviewed skills moved to `dod-complete`. |
| PR #40 `docs(skills): complete funnel analytics DoD` | [CÓDIGO] Merged with `Quality Gates` success. | [CONFIG] Real `funnel-analytics` DoD delivery replaced checkpoint PR #17. |
| PR #42 `feat(scripts): recover deterministic doc factory` | [CÓDIGO] Merged with `Quality Gates` success. | [CONFIG] Core `scripts/doc-factory/**` was recovered selectively from the Claude branch with a deterministic CI gate. |
| PR #17 `codex/predeploy-funnel-analytics-20260603` | [CÓDIGO] Closed as superseded after #40 merge. | [CONFIG] Checkpoint PR removed from active transit. |
| `codex/predeploy-funnel-analytics-20260603` | [CÓDIGO] Remote branch deleted when PR #17 was closed. | [CONFIG] Stale checkpoint branch removed. |
| `codex/deploy-funnel-analytics-dod-20260603` | [CÓDIGO] `git rev-list --left-right --count origin/main...origin/codex/deploy-funnel-analytics-dod-20260603` showed `23 0` before deletion. | [CONFIG] Remote branch deleted as contained/stale. |
| `codex/skill-workflow-creator-dod` | [CÓDIGO] `git rev-list --left-right --count origin/main...origin/codex/skill-workflow-creator-dod` showed `15 0` before deletion. | [CONFIG] Remote branch deleted as contained/stale. |
| `evolution/memory-context-scaffold-multi-env` | [CÓDIGO] `git rev-list --left-right --count origin/main...origin/evolution/memory-context-scaffold-multi-env` showed `52 0` before deletion. | [CONFIG] Remote branch deleted as contained/stale. |
| `qa/adversarial-exploratory-hardening` | [CÓDIGO] `git rev-list --left-right --count origin/main...origin/qa/adversarial-exploratory-hardening` showed `54 0` before deletion. | [CONFIG] Remote branch deleted as contained/stale. |

## Source Map

| Source | Evidence | Current Role | Recovery Decision |
|---|---|---|---|
| `/Users/deonto/Documents/workspace/jm-adk-alfa` | [CÓDIGO] Local Git repo with `origin` set to `https://github.com/JaviMontano/jm-adk-alfa`. | [CONFIG] Canonical Alfa delivery repo. | [CONFIG] All delivery PRs start from `origin/main`. |
| `/Users/deonto/Documents/jm-adk` | [CÓDIGO] Previous inspection reported an empty local repo with no usable commits. | [INFERENCIA] Not a usable local source of old work. | [CONFIG] Do not recover from this local directory. |
| `JaviMontano/jm-adk` | [CÓDIGO] GitHub tree inspection reports `160` remote `SKILL.md` files. | [INFERENCIA] Old repo with recoverable skill ideas. | [CONFIG] Normalize candidates into Alfa one batch at a time. |
| `JaviMontano/skills` | [CÓDIGO] GitHub tree inspection reports `1` remote `SKILL.md` file. | [INFERENCIA] Private standalone skill source. | [CONFIG] Recover only after explicit privacy/brand review. |
| `origin/claude/doc-factory-engine` | [CÓDIGO] Remote branch has `4` commits not in `origin/main` and is `64` commits behind current `origin/main`. | [INFERENCIA] Core doc-factory code has been recovered, but the branch still contains historical schema/template material and broad drift. | [CONFIG] Treat as source-only reference; never merge the branch wholesale. |

## Transit PRs And Branches

| Ref | Evidence | Status | Decision |
|---|---|---|---|
| Open PR list | [CÓDIGO] `gh pr list --state open` returned `[]`. | [CONFIG] No active PR transit remains. | [CONFIG] Continue with new scoped PRs only. |
| `origin/claude/doc-factory-engine` | [CÓDIGO] Unique commits: `1bf12ea8`, `bbb78199`, `d1f54337`, `51d4042e`. | [INFERENCIA] Source-only historical branch after #42; remaining useful material should be extracted only through new scoped PRs. | [CONFIG] Do not merge or use as active delivery branch. |

## Candidate Skill Delta

- [CÓDIGO] Alfa has `585` skill packages under `skills/*/SKILL.md`.
- [CÓDIGO] `JaviMontano/jm-adk` has `160` normalized skill names.
- [CÓDIGO] `96` old `jm-adk` skill names overlap with Alfa.
- [CÓDIGO] `64` old `jm-adk` skill names are not present in Alfa.
- [CÓDIGO] `JaviMontano/skills` contributes `1` additional private standalone candidate: `metodologia-brand-html`.

### Old `jm-adk` Differentials

[CÓDIGO] `acceptance-criteria-writer`, `accessibility-implementation`, `adr-generator`, `api-designer-skill`, `api-surface-analyzer`, `architecture-design`, `architecture-mapper`, `ci-cd-analyzer`, `ci-cd-pipeline-designer`, `code-review-framework`, `code-smell-detector`, `codebase-metrics`, `data-model-analyzer`, `data-model-designer`, `data-modeling-patterns`, `debt-classifier`, `dependency-auditor`, `deployment-strategy`, `developer-experience-auditor`, `diagnostic-engine`, `disaster-recovery-planner`, `documentation-auditor`, `documentation-generator`, `event-driven-design`, `evidence-classifier`, `file-change-planner`, `friction-detector`, `implementation-planning`, `incident-analyzer`, `infrastructure-mapper`, `lessons-learned-tracker`, `maintainability-scorer`, `microservices-decomposer`, `migration-planner`, `observability-architecture`, `observability-design`, `observability-gap-analyzer`, `performance-bottleneck-identifier`, `performance-budget`, `performance-profiler`, `query-optimization`, `realtime-data-sync`, `release-planner`, `repository-scanner`, `resilience-design`, `risk-controlling`, `risk-scorer`, `root-cause-analyzer`, `scaffold-api-rest`, `scaffold-docker-dev`, `scaffold-firebase-project`, `scaffold-monorepo`, `scaffold-nextjs-app`, `scaffold-supabase-project`, `scalability-assessor`, `schema-migration-strategy`, `security-surface-scanner`, `security-threat-modeler`, `tech-debt-quantifier`, `technical-discovery`, `test-coverage-analyzer`, `test-strategy-designer`, `trade-off-analyzer`, `vector-database-design`.

## Recovery Rules

- [CONFIG] Start every recovery PR from `origin/main`.
- [CONFIG] Use one unit per PR: one skill, one tightly coupled skill batch, one doc-only PR, or one infrastructure slice.
- [CONFIG] Treat old repos and stale branches as source material, not merge targets.
- [CONFIG] A recovered skill must satisfy the Alfa DoD: assets manifest, skill-specific examples/evals, review doc, ledger row, and deterministic script checks when scripts exist.
- [CONFIG] If a source package lacks Alfa DoD artifacts, rebuild it with `scripts/scaffold-skill.py` and targeted deterministic assets instead of copying old structure.
- [CONFIG] Do not bring private or brand-specific material from `JaviMontano/skills` into public Alfa without explicit privacy and brand review.

## Recommended Next Delivery Order

1. [CONFIG] Create the first old-repo skill recovery batch with 3 to 5 low-conflict skills from the `64` differentials, each converted to Alfa DoD.
2. [CONFIG] If doc-factory needs skill-level schemas/templates, extract one skill-scoped slice from `origin/claude/doc-factory-engine` and validate it as a normal skill/content PR.
3. [CONFIG] Reassess private `metodologia-brand-html` only after explicit privacy and brand review.
4. [CONFIG] Continue one-skill or small-batch ledger closures from the remaining `555` non-DoD lifecycle rows.

## Verification Evidence

- [CÓDIGO] `git rev-parse origin/main`.
- [CÓDIGO] `gh pr list --state open --json number,title,headRefName,isDraft,mergeStateStatus,url`.
- [CÓDIGO] `git branch -r`.
- [CÓDIGO] `git rev-list --left-right --count origin/main...origin/claude/doc-factory-engine`.
- [CÓDIGO] `gh api 'repos/JaviMontano/jm-adk/git/trees/main?recursive=1'`.
- [CÓDIGO] `gh api 'repos/JaviMontano/skills/git/trees/main?recursive=1'`.
- [CÓDIGO] Ledger/status count script over `docs/audits/skill-review-ledger.csv`.
