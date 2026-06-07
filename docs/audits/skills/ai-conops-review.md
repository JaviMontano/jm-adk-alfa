# ai-conops Review

## SpokeReport - Ledger Auditor
- status: pass
- findings:
  - Ledger row existed for `ai-conops` with status `pending` before hardening. [CÓDIGO]
  - Review doc did not exist before this pass. [CÓDIGO]
- coverage_gaps:
  - No DoD evidence was recorded for this skill before the current branch. [CÓDIGO]
- recommended_changes:
  - Close only the `ai-conops` ledger row after local validation evidence is available. [CONFIG]
- risk: marking `dod-complete` without validation would break the one-skill hardening contract. [CONFIG]

## SpokeReport - Determinism Auditor
- status: warn
- findings:
  - Initial DoD failed because `assets/` was missing, examples retained scaffold text, and `evals/evals.json` did not expose a `cases` list. [CÓDIGO]
  - The core `SKILL.md` had strong CONOPS domain content and references, but no machine-checkable output contract. [CÓDIGO]
  - README, agents, prompts, templates, knowledge graph, examples, and evals were generic enough to allow narrative-only outputs. [CÓDIGO]
  - The HTML template used a remote font dependency; it was replaced with a local, deterministic template. [CÓDIGO]
- coverage_gaps:
  - No offline validator existed for stakeholder coverage, autonomy level, value quadrant, metric pillars, operational modes, assumptions, or validation checks. [CÓDIGO]
- recommended_changes:
  - Add deterministic assets and a local validator for AI CONOPS packets. [CONFIG]
  - Require stakeholders, Level 1-5 interaction design, business value quadrant, three-pillar metrics, degraded/recovery modes, and explicit assumptions. [CONFIG]
- risk: CONOPS output can look executive-ready while omitting the operational controls needed for architecture readiness. [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass
- findings:
  - Added 10 deterministic eval cases covering claims copilot, shared-control fraud triage, executive scope, missing stakeholders, invalid autonomy, metric pillar gaps, value/effort conflicts, missing degraded mode, false-positive activation, and script validation. [CÓDIGO]
- coverage_gaps:
  - Financial modeling remains outside the CONOPS packet contract. [CÓDIGO]
- recommended_changes:
  - Keep value assessment directional and route detailed financial modeling to a dedicated skill. [CONFIG]
- risk: broad AI strategy requests can over-activate unless the user asks for operational concept, stakeholders, autonomy, value, metrics, or modes. [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass
- findings:
  - Added `scripts/validate_ai_conops_report.py`, `scripts/check.sh`, 2 valid fixtures, and 7 invalid fixtures. [CÓDIGO]
  - Validator enforces schema, evidence ids, stakeholder minimum, interaction level bounds, high-stakes controls, value quadrant consistency, metric pillar coverage, required operational modes, explicit assumptions, and validation checks. [CÓDIGO]
- coverage_gaps:
  - The script validates CONOPS packets; it does not validate downstream architecture implementation. [CÓDIGO]
- recommended_changes:
  - Treat architecture design choices as downstream outputs unless they are required to justify operational safety controls. [CONFIG]
- risk: CONOPS can prematurely select implementation patterns when the operational concept is still incomplete. [INFERENCIA]

## HardeningBrief
- skill: ai-conops
- scope_allowed:
  - `skills/ai-conops/**` [CONFIG]
  - `docs/audits/skills/ai-conops-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `ai-conops` only after local evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, eval cases, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not mark `dod-complete` before local validation evidence is available. [CONFIG]
  - Do not collapse open assumptions into narrative prose. [CONFIG]
- validation_plan:
  - `bash skills/ai-conops/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-conops` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill ai-conops` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/ai-conops/scripts/check.sh` passed with 2 valid fixtures accepted and 7 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-conops` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill ai-conops` passed with `skill=ai-conops dod=pass errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/count-components.py --check-docs` passed with `skills=600`, `agents=261`, `commands=267`, `prompts=256`, `components=1384`. [CÓDIGO]
- `bash scripts/check-repo-boundaries.sh` passed with `Repo boundaries OK`. [CÓDIGO]
- `python3 -B scripts/qa/run-adversarial-tests.py` passed with `summary: passed=11 failed=0 total=11`. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=84 warnings=0 errors=0`. [CÓDIGO]
- `bash scripts/doc-factory/check.sh` passed with `OK: doc-factory deterministic smoke check passed`. [CÓDIGO]
- `git diff --check` passed with no output. [CÓDIGO]

## Guardian Decision
- pass for local skill-level and repository-level validation; proceed to PR creation and Quality Gates. [CÓDIGO]
