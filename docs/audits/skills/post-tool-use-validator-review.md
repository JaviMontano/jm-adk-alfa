# Post Tool Use Validator Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: The skill needed deterministic assets and script-backed evidence for command status matching, evidence tags, quality gates, secret output blocking, and scope compliance.
- coverage_gaps: Without fixtures, post-tool validation could accept unsupported success claims after failed commands.
- recommended_changes: Keep validation bound to JSON reports, offline fixtures, and explicit next actions.
- risk: Secret detection policy may need future expansion for new token formats.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals cover pass-with-evidence, failed-command false pass, missing evidence, unmasked secret output, scope violations, quality gate failure, warning state, and blocked next action.
- coverage_gaps: None remaining for this DoD scope.
- recommended_changes: Preserve false-positive and degradation cases in future eval edits.
- risk: Compound tool outputs may need richer path summaries later.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_post_tool_use_report.py`, `scripts/check.sh`, 1 valid fixture, and 3 invalid mutation fixtures.
- coverage_gaps: The validator checks post-tool reports; it does not rerun the original command.
- recommended_changes: Treat non-zero exit/pass mismatches as fail-closed.
- risk: Output redaction rules should evolve with repo-specific secret patterns.

## HardeningBrief

- skill: post-tool-use-validator
- scope_allowed: `skills/post-tool-use-validator/**`, `docs/audits/skills/post-tool-use-validator-review.md`, and the `post-tool-use-validator` ledger row.
- required_changes: Assets, eval cases, examples, SKILL frontmatter normalization, offline validator, fixtures, review doc, ledger update, and generated index refresh.
- forbidden_changes: `pre-tool-use-guard`, `validate-hooks`, unrelated skills, repo validators, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, adapter freshness, index freshness, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill post-tool-use-validator`: `skill=post-tool-use-validator dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill post-tool-use-validator`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash skills/post-tool-use-validator/scripts/check.sh`: `post-tool-use-validator check passed: valid=1 invalid=3`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=601 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=601 agents=261 commands=267 prompts=256 components=1385`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=136 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check origin/main...HEAD`: pass with no output.
- `git diff --check`: pass with no output.
- CI remediation: initial PR Quality Gates failed tracked secret pattern scan on the invalid secret fixture; the fixture now uses `UNMASKED_SAMPLE_TOKEN` plus `output_contains_secret: true` to keep deterministic negative coverage without matching tracked secret patterns.
- Python mirror of CI tracked secret pattern scan: `No tracked secret patterns detected`.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, generated indexes, and passing local validation evidence.
- remaining_risks: Source branch also contains other runtime guard changes, but this isolated worktree diff is scoped only to `post-tool-use-validator`.
