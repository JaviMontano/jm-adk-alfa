# analytics-engineering Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, example files retained scaffold language, and `evals/evals.json` did not expose a `cases` list.
- coverage_gaps: No offline oracle existed for evidence, sources, model layers, materializations, mart tests, data contracts, lineage, documentation, or validation checks.
- recommended_changes: Add deterministic assets, examples, eval cases, prompts, agents, templates, and a local JSON analytics engineering validator.
- risk: Without these changes, a deliverable could name marts without owners, tests, contracts, or lineage evidence.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced the five-case generic array with 10 deterministic cases covering happy paths, false positives, false-negative guards, degradation, conflicts, boundaries, and invalid outputs.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, and `quality_criteria`.
- risk: Future edits could weaken activation guards if dashboard-design or SQL-debug false positives are removed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_analytics_engineering.py`, `scripts/check.sh`, 2 valid fixtures, and 6 invalid fixtures.
- coverage_gaps: The script validates structured JSON handoffs, not arbitrary free-form Markdown.
- recommended_changes: Use JSON handoff validation when an analytics engineering plan must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: analytics-engineering
- scope_allowed: `skills/analytics-engineering/**`, `docs/audits/skills/analytics-engineering-review.md`, and the `analytics-engineering` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/analytics-engineering/scripts/check.sh`: pass; 2 valid fixtures accepted and 6 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-dod.py --skill analytics-engineering`: `skill=analytics-engineering dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill analytics-engineering`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=93 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Markdown-only analytics engineering plans require human review against the same deterministic contract.
