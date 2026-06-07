# alerting-strategy Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, examples retained scaffold language, and `evals/evals.json` did not expose a `cases` list.
- coverage_gaps: No offline oracle existed for severity, alert rules, escalation paths, or fatigue controls.
- recommended_changes: Add deterministic assets, examples, eval cases, and a local JSON alerting strategy validator.
- risk: Without these changes, strategies could define noisy or unowned alerts without escalation evidence.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval array with 10 deterministic cases covering happy paths, false positives, degraded input, boundary conditions, conflicts, and invalid output.
- coverage_gaps: None remaining for DoD hardening scope.
- recommended_changes: Keep evals tied to assets, deterministic scripts, and quality criteria.
- risk: Future edits could weaken activation guards if false-positive cases are removed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_alerting_strategy.py`, `scripts/check.sh`, 2 valid fixtures, and 6 invalid fixtures.
- coverage_gaps: The script validates JSON handoffs, not arbitrary free-form Markdown.
- recommended_changes: Use JSON handoff validation whenever an alerting strategy must be checked offline.
- risk: Markdown-only deliveries still require Guardian review against the same checklist.

## HardeningBrief

- skill: alerting-strategy
- scope_allowed: `skills/alerting-strategy/**`, `docs/audits/skills/alerting-strategy-review.md`, and the `alerting-strategy` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/alerting-strategy/scripts/check.sh`: pass; 2 valid fixtures accepted and 6 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-dod.py --skill alerting-strategy`: `skill=alerting-strategy dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill alerting-strategy`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=92 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize repo-level validation and PR only after the ledger row is updated and all repo checks pass.
- remaining_risks: Markdown-only alerting strategies require human review against the same deterministic contract.
