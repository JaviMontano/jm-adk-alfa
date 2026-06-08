# message-batch-orchestration Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals lacked `assets` and `deterministic_scripts`. Public files retained scaffold headers and unverified pricing language.
- coverage_gaps: No offline oracle existed for realtime misuse, duplicate or index-derived `custom_id`, immediate-completion assumptions, missing terminal status, full-batch retry, retrying succeeded ids, unbounded retries, or unpersisted successes.
- recommended_changes: Add deterministic assets, specialized eval cases, examples, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- risk: Without these changes, a batch plan could silently reprocess the whole workload, lose correlation, or accept a synchronous route for an offline workload.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval checks with 11 deterministic cases covering ticket backfill, explicit lifecycle, `custom_id` correlation, partial failure retry, checkpointing, realtime false positive, duplicate `custom_id`, missing `custom_id`, upgrade safety, and expired/canceled fragmentation.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `custom_id_uniqueness`, `batch_lifecycle`, `fragmentation`, `selective_retry`, `retry_cap`, and `offline_gate`.
- risk: Future edits could weaken guarantees if evals stop testing failed-id-only retry.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_message_batch_orchestration.py`, `scripts/check.sh`, 2 valid fixtures, and 9 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON batch orchestration reports, not arbitrary prose-only Markdown.
- recommended_changes: Use the JSON contract whenever batch lifecycle and retry behavior must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: message-batch-orchestration
- scope_allowed: `skills/message-batch-orchestration/**`, `docs/audits/skills/message-batch-orchestration-review.md`, and the `message-batch-orchestration` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, runtime batch scripts, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/message-batch-orchestration/scripts/check.sh`: `message-batch-orchestration check passed: valid=2 invalid=9`.
- `python3 -B scripts/validate-skill-dod.py --skill message-batch-orchestration`: `skill=message-batch-orchestration dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill message-batch-orchestration`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `bash scripts/adapt.sh all` plus adapter diff check: `adapter freshness OK`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=108 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Prose-only batch plans require human review against the JSON contract before they can be treated as deterministic evidence.
