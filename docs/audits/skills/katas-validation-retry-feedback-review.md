# katas-validation-retry-feedback Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, evals lacked `assets` and `deterministic_scripts`, and scaffold markers remained in public files.
- coverage_gaps: No offline oracle existed for generic feedback, retry caps, nonrecoverable retries, missing error paths, accepted invalid output, retry-count mismatch, or unknown validator error types.
- recommended_changes: Add deterministic assets, specialized eval cases, domain examples, prompts, agents, template, knowledge, offline validator, fixtures, review doc, and ledger update.
- risk: Without these changes, a retry loop could look plausible while retrying absent data, accepting invalid output, or hiding weak feedback.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval data with 11 deterministic cases covering recoverable format retries, source-absent escalation, mixed errors, generic feedback rejection, retry-cap rejection, invalid-output rejection, systematic errors, false positives, false negatives, degraded inputs, and upgrade safety.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep eval checks tied to `assets`, `deterministic_scripts`, `quality_criteria`, specific feedback, nonrecoverable no-retry, and escalation.
- risk: Future edits could weaken guarantees if cases stop distinguishing recoverable and nonrecoverable failures.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_validation_retry_feedback.py`, `scripts/check.sh`, 2 valid fixtures, and 8 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON retry reports, not arbitrary prose-only Markdown.
- recommended_changes: Use the JSON contract whenever a retry-with-feedback report must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: katas-validation-retry-feedback
- scope_allowed: `skills/katas-validation-retry-feedback/**`, `docs/audits/skills/katas-validation-retry-feedback-review.md`, and the `katas-validation-retry-feedback` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/katas-validation-retry-feedback/scripts/check.sh`: `katas-validation-retry-feedback check passed: valid=2 invalid=8`.
- `python3 -B scripts/validate-skill-dod.py --skill katas-validation-retry-feedback`: `skill=katas-validation-retry-feedback dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-validation-retry-feedback`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `bash scripts/adapt.sh all` plus adapter diff check: `adapter freshness OK`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=106 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Prose-only retry reports require human review against the JSON contract before they can be treated as deterministic evidence.
