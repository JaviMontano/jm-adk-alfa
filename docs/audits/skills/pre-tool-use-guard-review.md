# Pre Tool Use Guard Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: The skill needed deterministic assets and script-backed evidence for destructive command blocking, write boundaries, private path protection, and exit-code-2 deny behavior.
- coverage_gaps: Without fixtures, allow/block decisions could drift into prose-only safety advice.
- recommended_changes: Keep guard decisions bound to assets, JSON fixtures, and the offline validator.
- risk: New destructive command aliases may require future policy expansion.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals cover `git reset --hard`, `git clean -fd`, private path copy, out-of-scope writes, read-only allow, missing evidence, exit-code-2 contract, and secret path blocking.
- coverage_gaps: None remaining for this DoD scope.
- recommended_changes: Preserve false-positive and degradation cases in future eval edits.
- risk: Broader shell parsing may be needed if this skill begins evaluating compound scripts.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_pre_tool_use_guard.py`, `scripts/check.sh`, 2 valid fixtures, and 3 invalid mutation fixtures.
- coverage_gaps: The validator checks guard reports; it does not execute proposed commands.
- recommended_changes: Keep the validator offline and fail-closed for unknown destructive patterns.
- risk: Command policy must evolve with repo-specific guardrails.

## HardeningBrief

- skill: pre-tool-use-guard
- scope_allowed: `skills/pre-tool-use-guard/**`, `docs/audits/skills/pre-tool-use-guard-review.md`, and the `pre-tool-use-guard` ledger row.
- required_changes: Assets, eval cases, examples, SKILL frontmatter normalization, offline validator, fixtures, review doc, ledger update, and generated index refresh.
- forbidden_changes: `post-tool-use-validator`, unrelated skills, repo validators, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, adapter freshness, index freshness, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill pre-tool-use-guard`: `skill=pre-tool-use-guard dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill pre-tool-use-guard`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash skills/pre-tool-use-guard/scripts/check.sh`: `pre-tool-use-guard check passed: valid=2 invalid=3`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=601 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=601 agents=261 commands=267 prompts=256 components=1385`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=135 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check origin/main...HEAD`: pass with no output.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, generated indexes, and passing local validation evidence.
- remaining_risks: Branch source also contains `post-tool-use-validator`, but this isolated worktree diff is scoped only to `pre-tool-use-guard`.
