# ai-software-architecture Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, examples retained scaffold language, and `evals/evals.json` did not expose a `cases` list.
- coverage_gaps: No offline oracle existed for validating architecture report completeness.
- recommended_changes: Add deterministic assets, specific examples, structured eval cases, and a local JSON report validator.
- risk: Without these changes, reports could omit layers, quality scenarios, ADRs, debt, or evidence while still appearing complete.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval array with 10 deterministic cases covering happy paths, false positives, false-negative guards, degraded input, boundary conditions, conflicts, and invalid output.
- coverage_gaps: None remaining for DoD hardening scope.
- recommended_changes: Keep evals tied to assets, deterministic scripts, and quality criteria.
- risk: Future edits could weaken activation guards if false-positive cases are removed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_ai_architecture_report.py`, `scripts/check.sh`, 2 valid fixtures, and 8 invalid fixtures.
- coverage_gaps: The script validates JSON handoffs, not arbitrary free-form Markdown.
- recommended_changes: Use JSON handoff validation whenever a report must be checked offline.
- risk: Markdown-only deliveries still require Guardian review against the same checklist.

## HardeningBrief

- skill: ai-software-architecture
- scope_allowed: `skills/ai-software-architecture/**`, `docs/audits/skills/ai-software-architecture-review.md`, and the `ai-software-architecture` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/ai-software-architecture/scripts/check.sh`: pass; 2 valid fixtures accepted and 8 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-dod.py --skill ai-software-architecture`: `skill=ai-software-architecture dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-software-architecture`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=90 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize repo-level validation and PR only after the ledger row is updated and all repo checks pass.
- remaining_risks: Markdown-only architecture reports require human review against the same deterministic contract.
