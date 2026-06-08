# katas-pretooluse-guardrails Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals did not include `assets` or `deterministic_scripts`. Multiple files retained scaffold headers.
- coverage_gaps: No offline oracle existed for prompt-only policies, missing `PreToolUse`, denied side-effects, missing denial reason, missing allow path, hot reload, or prompt injection bypass.
- recommended_changes: Add deterministic assets, eval cases, specialized examples, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- risk: Without these changes, policies could remain prompt-only or post-execution while being described as deterministic guardrails.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced eval data with 10 deterministic cases covering refund limits, allow paths, prompt-only rejection, prompt injection, hot reload, domain blocklists, path protection, ask decisions, false positives, and related-skill boundaries.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, and `quality_criteria`.
- risk: Future edits could weaken the control if deny-before-side-effects or allow-path cases are removed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_pretooluse_guardrails.py`, `scripts/check.sh`, 2 valid fixtures, and 8 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON guardrail reports, not arbitrary free-form Markdown.
- recommended_changes: Use the JSON contract whenever a PreToolUse guardrail report must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: katas-pretooluse-guardrails
- scope_allowed: `skills/katas-pretooluse-guardrails/**`, `docs/audits/skills/katas-pretooluse-guardrails-review.md`, and the `katas-pretooluse-guardrails` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/katas-pretooluse-guardrails/scripts/check.sh`: `katas-pretooluse-guardrails check passed: valid=2 invalid=8`.
- `python3 -B scripts/validate-skill-dod.py --skill katas-pretooluse-guardrails`: `skill=katas-pretooluse-guardrails dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-pretooluse-guardrails`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `bash scripts/adapt.sh all` plus adapter diff check: `adapter freshness OK`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=103 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Markdown-only PreToolUse guardrail reports require human review against the same deterministic JSON contract.
