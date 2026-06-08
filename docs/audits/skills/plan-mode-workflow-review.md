# plan-mode-workflow Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals did not require `assets` or `deterministic_scripts`. Existing content described the gate well but lacked an offline oracle for signed plan, hook enforcement, read-only exploration, write-tool coverage, re-sign on plan change, and Guardian decisions.
- coverage_gaps: Mutating Bash in Plan Mode, missing write-tool block coverage, unsigned execution, hash mismatch, disabled hook, `bypassPermissions`, and Guardian pass on blocked cases were not machine-checkable.
- recommended_changes: Add deterministic assets, specialized eval checks, offline scripts, fixtures, review doc, and ledger reconciliation.
- risk: Without these changes, the skill could describe Plan Mode correctly while still allowing non-verifiable execution before signed approval.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval checks with 10 deterministic scenarios covering signed happy path, explicit trigger, compliance approval gate, shared workspace write risk, re-sign after plan change, unrelated false positive, empty input, bypass anti-pattern, mutating Bash, and upgrade safety.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `read_only_exploration`, `plan_hash_signature`, `hook_enforcement`, `plan_change_resign`, `no_bypass_permissions`, and `bash_mutation_blocked`.
- risk: Future eval edits could weaken the guarantee that write attempts remain blocked until the exact plan hash is signed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_plan_mode_workflow.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON reports; prose-only process descriptions still require Guardian review against the same contract.
- recommended_changes: Use the JSON contract whenever Plan Mode evidence must be reproducible offline.
- risk: Free-form Markdown can drift unless reviewers enforce the same field-level gate evidence.

## HardeningBrief

- skill: plan-mode-workflow
- scope_allowed: `skills/plan-mode-workflow/**`, `docs/audits/skills/plan-mode-workflow-review.md`, and the `plan-mode-workflow` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, scaffold metadata cleanup, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/plan-mode-workflow/scripts/check.sh`: `plan-mode-workflow check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill plan-mode-workflow`: `skill=plan-mode-workflow dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill plan-mode-workflow`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=111 warnings=0 errors=0`.
- `bash scripts/adapt.sh all`: `ADAPTER-COMPLETE` for antigravity, vscode, cursor+windsurf, and agents+gemini with no core files modified.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, adapter freshness evidence, a reconciled ledger row, and passing local validation.
- remaining_risks: Prose-only Plan Mode workflow descriptions require human review against the JSON contract before they can be treated as deterministic evidence.
