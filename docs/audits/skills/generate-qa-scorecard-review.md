# generate-qa-scorecard Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, examples retained scaffold wording, and `evals/evals.json` did not expose a deterministic `cases` object list.
- coverage_gaps: No offline oracle existed for seven-dimension scoring, grade thresholds, reduced scope, action ordering, or false-positive rejection.
- recommended_changes: Add deterministic assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- risk: Without these changes, scorecards could mix scoring models, overclaim unreviewed dimensions, misorder the top 3 actions, or report unverifiable grades.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval data with 10 deterministic cases covering happy paths, false positives, false negatives, degradation, limits, conflicts, and invalid scorecards.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `quality_criteria`, and the canonical seven-dimension order.
- risk: Future edits could weaken score integrity if percentage, grade, reduced-scope, or action-priority cases are removed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_qa_scorecard.py`, `scripts/check.sh`, 2 valid fixtures, and 7 invalid fixtures.
- coverage_gaps: The script validates structured JSON scorecard reports, not arbitrary free-form Markdown.
- recommended_changes: Use the JSON scorecard contract whenever a report must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: generate-qa-scorecard
- scope_allowed: `skills/generate-qa-scorecard/**`, `docs/audits/skills/generate-qa-scorecard-review.md`, and the `generate-qa-scorecard` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/generate-qa-scorecard/scripts/check.sh`: `generate-qa-scorecard check passed: valid=2 invalid=7`.
- `python3 -B scripts/validate-skill-dod.py --skill generate-qa-scorecard`: `skill=generate-qa-scorecard dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill generate-qa-scorecard`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=99 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Markdown-only scorecards require human review against the same deterministic JSON contract.
