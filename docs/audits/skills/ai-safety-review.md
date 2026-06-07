# ai-safety Review

## SpokeReport - Ledger Auditor
- status: pass [CÓDIGO]
- findings:
  - Ledger row existed for `ai-safety` with status `pending` before hardening. [CÓDIGO]
  - Review doc did not exist before this pass. [CÓDIGO]
- coverage_gaps:
  - No DoD evidence was recorded for this skill before the current branch. [CÓDIGO]
- recommended_changes:
  - Close only the `ai-safety` ledger row after local validation evidence is available. [CONFIG]
- risk: marking `dod-complete` without validation would break the one-skill hardening contract. [CONFIG]

## SpokeReport - Determinism Auditor
- status: warn [CÓDIGO]
- findings:
  - Initial DoD failed because `assets/` was missing, examples retained scaffold text, and `evals/evals.json` did not expose a `cases` list. [CÓDIGO]
  - SKILL, README, agents, prompts, knowledge, templates, examples, and evals were generic scaffold content. [CÓDIGO]
  - No offline validator existed for risk taxonomy, control coverage, jailbreak tests, evaluation metrics, escalation, or evidence ids. [CÓDIGO]
- coverage_gaps:
  - Live model safety performance remains outside the offline report validator. [CÓDIGO]
- recommended_changes:
  - Add deterministic assets and local validator for AI safety reports. [CONFIG]
  - Require every risk to map to controls and critical risks to avoid allow-only action. [CONFIG]
- risk: safety plans can look complete while omitting over-refusal metrics, escalation, or jailbreak tests. [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass [CÓDIGO]
- findings:
  - Added 10 deterministic eval cases covering support assistant safety, medical triage, jailbreak suites, unknown risk domains, uncovered risks, critical allow actions, missing metrics, false-positive prompts, and script validation. [CÓDIGO]
- coverage_gaps:
  - The evals validate packet behavior and activation boundaries, not live red-team exhaustiveness. [CÓDIGO]
- recommended_changes:
  - Keep risk taxonomy, control coverage, jailbreak coverage, evaluation metrics, and escalation checks mandatory. [CONFIG]
- risk: generic safety wording can overlap with non-AI policy writing unless AI guardrail scope remains explicit. [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass [CÓDIGO]
- findings:
  - Added `scripts/validate_ai_safety_report.py`, `scripts/check.sh`, 2 valid fixtures, and 7 invalid fixtures. [CÓDIGO]
  - Validator enforces schema, evidence ids, system metadata, risk domains, severities, controls, critical-risk action policy, jailbreak tests, required metrics, escalation policy, validation checks, and risks list. [CÓDIGO]
- coverage_gaps:
  - The script validates deterministic safety report packets, not production model telemetry. [CÓDIGO]
- recommended_changes:
  - Treat production safety metrics as evidence inputs to the packet when available. [CONFIG]
- risk: safety performance can drift after deployment, so monitoring remains required outside this DoD packet. [INFERENCIA]

## HardeningBrief
- skill: ai-safety [CONFIG]
- scope_allowed:
  - `skills/ai-safety/**` [CONFIG]
  - `docs/audits/skills/ai-safety-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `ai-safety` only after local evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, eval cases, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not claim live model certification from offline fixtures. [CONFIG]
  - Do not mark `dod-complete` before evidence, review doc, and validations pass. [CONFIG]
- validation_plan:
  - `bash skills/ai-safety/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-safety` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill ai-safety` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/ai-safety/scripts/check.sh` passed with 2 valid fixtures accepted and 7 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-safety` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill ai-safety` passed with `skill=ai-safety dod=pass errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/count-components.py --check-docs` passed with `skills=600`, `agents=261`, `commands=267`, `prompts=256`, `components=1384`. [CÓDIGO]
- `bash scripts/check-repo-boundaries.sh` passed with `Repo boundaries OK`. [CÓDIGO]
- `python3 -B scripts/qa/run-adversarial-tests.py` passed with `summary: passed=11 failed=0 total=11`. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=89 warnings=0 errors=0`. [CÓDIGO]
- `bash scripts/doc-factory/check.sh` passed with `OK: doc-factory deterministic smoke check passed`. [CÓDIGO]
- `git diff --check` passed with no output. [CÓDIGO]

## Guardian Decision
- pass for local skill-level and repository-level validation; proceed to PR creation and Quality Gates. [CÓDIGO]
