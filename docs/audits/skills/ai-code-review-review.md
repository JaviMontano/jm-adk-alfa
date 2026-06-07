# ai-code-review Review

## SpokeReport - Ledger Auditor
- status: pass
- findings:
  - Ledger row existed for `ai-code-review` with status `pending` before hardening. [CÓDIGO]
  - Review doc did not exist before this pass. [CÓDIGO]
- coverage_gaps:
  - No DoD evidence was recorded for this skill before the current branch. [CÓDIGO]
- recommended_changes:
  - Close only the `ai-code-review` ledger row after local validation evidence is available. [CONFIG]
- risk: marking `dod-complete` without evidence would break the one-skill hardening contract. [CONFIG]

## SpokeReport - Determinism Auditor
- status: warn
- findings:
  - Initial DoD failed because `assets/` was missing, examples retained scaffold text, and `evals/evals.json` did not expose a `cases` list. [CÓDIGO]
  - Existing agents, prompts, templates, and knowledge were generic and did not require file-line evidence, false-positive filtering, or no-fake-test-result controls. [CÓDIGO]
  - The HTML template referenced external Google Fonts and mixed MetodologIA branding into the JM Labs skill output. [CÓDIGO]
- coverage_gaps:
  - No machine-checkable review report contract existed. [CÓDIGO]
  - No offline validator existed for priorities, scope, evidence, confidence, or command-backed test claims. [CÓDIGO]
- recommended_changes:
  - Add deterministic assets and an offline report validator for AI-assisted code review packets. [CONFIG]
  - Require exact `file`, `line_start`, evidence id, priority, confidence, impact, and recommendation for every finding. [CONFIG]
- risk: AI-assisted review can overstate speculative issues or invent test results when no deterministic contract exists. [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass
- findings:
  - Added 10 deterministic eval cases covering PR review, clean review, security issue review, missing line evidence, fake tests, generated-file scope, low-confidence P1, false-positive weather/general AI prompts, and script validation. [CÓDIGO]
- coverage_gaps:
  - Live PR platform comments remain outside the local offline contract. [INFERENCIA]
- recommended_changes:
  - Keep platform-specific review posting separate from the machine-checkable report packet. [CONFIG]
- risk: activation can be too broad when users mention AI generally without asking for code review. [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass
- findings:
  - Added `scripts/validate_ai_code_review_report.py`, `scripts/check.sh`, 2 valid fixtures, and 7 invalid fixtures. [CÓDIGO]
  - Validator enforces schema, scope, evidence tags, file-line findings, priority thresholds, duplicate ids, false-positive degradation, and no-fake-test-result rules. [CÓDIGO]
- coverage_gaps:
  - The script validates review packets; it does not execute arbitrary project tests. [CÓDIGO]
- recommended_changes:
  - Treat project test commands as evidence inputs through `validation.commands_run`. [CONFIG]
- risk: project-specific runtime behavior remains unverified unless commands are explicitly run and captured. [INFERENCIA]

## HardeningBrief
- skill: ai-code-review
- scope_allowed:
  - `skills/ai-code-review/**` [CONFIG]
  - `docs/audits/skills/ai-code-review-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `ai-code-review` only after local evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, eval cases, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not claim tests passed or failed without command evidence. [CONFIG]
  - Do not mark `dod-complete` before local validation evidence is available. [CONFIG]
- validation_plan:
  - `bash skills/ai-code-review/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-code-review` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill ai-code-review` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/ai-code-review/scripts/check.sh` passed with 2 valid fixtures accepted and 7 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-code-review` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill ai-code-review` passed with `skill=ai-code-review dod=pass errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/count-components.py --check-docs` passed with `skills=600`, `agents=261`, `commands=267`, `prompts=256`, `components=1384`. [CÓDIGO]
- `bash scripts/check-repo-boundaries.sh` passed with `Repo boundaries OK`. [CÓDIGO]
- `python3 -B scripts/qa/run-adversarial-tests.py` passed with `summary: passed=11 failed=0 total=11`. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=83 warnings=0 errors=0`. [CÓDIGO]
- `bash scripts/doc-factory/check.sh` passed with `OK: doc-factory deterministic smoke check passed`. [CÓDIGO]
- `git diff --check` passed with no output. [CÓDIGO]

## Guardian Decision
- pass for local skill-level and repository-level validation; proceed to PR creation and Quality Gates. [CÓDIGO]
