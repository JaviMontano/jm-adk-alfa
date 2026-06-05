# Skill Review: prompt-forge

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`prompt-forge` creates, reviews, evolves, repairs, and ports system prompts. For Alfa, the skill must produce deterministic Playbook packets with source boundaries, output contracts, rubric scorecards, platform-portability notes, adversarial tests, and script-backed validation.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | One active Phase 1 skill selected after `prompt-engineering`; branch created from `origin/main`. | None. | Keep branch and PR scoped to `prompt-forge`. | Low if scope remains isolated. |
| Determinism Auditor | complete | DoD failed before changes due missing assets, scaffold examples, root-list evals, missing references, remote font dependency, hidden-reasoning risk, and uncontrolled current-platform claims. | Missing source-boundary policy, no-invention rules, offline asset contract, and deterministic validator. | Add assets, source policy, offline templates, missing references, and fixture-backed validation. | High before hardening. |
| Eval Designer | complete | Evals covered only generic activation. | Missing create, review, evolve, repair, port, prompt-creator routing, false positives, minimal input, and adversarial source-boundary coverage. | Convert evals to DoD `cases` with expected activation, behavior, include/exclude checks, and expected checks. | High before hardening because weak evals could pass broad validation. |
| Script Engineer | complete | No script existed to validate Playbook or forge packets. | None after script addition. | Add `validate_forge_packet.py`, fixtures, and `check.sh`. | Low after fixture validation. |
| Guardian | complete | Ledger was pending and review doc absent; per-skill DoD failed with 5 errors before hardening. | Full PR gates still required before merge. | Block ledger closure until assets, evals, examples, review doc, script checks, and DoD pass. | Low after per-skill validation, pending PR gates. |

## Hardening Brief

- Replace scaffold README, examples, templates, agents, prompts, and knowledge with prompt-forge-specific deterministic contracts.
- Add `assets/prompt-forge-checklist.md`, `assets/playbook-contract.json`, and `assets/platform-portability-matrix.json`.
- Add missing reference files for design principles, rubric, Playbook template, platform guides, and context engineering.
- Add `scripts/validate_forge_packet.py`, deterministic fixtures, and `scripts/check.sh`.
- Convert evals to DoD `cases` covering create, review, evolve, repair, port, prompt-creator routing, false positives, ambiguous input, and adversarial source-boundary conflict.
- Remove remote Google Fonts dependency from HTML template and make platform-current claims source-boundary guarded.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | Added activation rules, deterministic contract, source boundaries, no-invention policy, hidden-reasoning privacy, assets, and scripts. |
| `README.md` | Replaced scaffold text with triggers, required inputs, output packet, and deterministic gate commands. |
| `assets/` | Added checklist, Playbook contract, platform matrix, README, and manifest. |
| `references/` | Added missing prompt-forge references so SKILL links resolve locally. |
| `scripts/` | Added forge packet validator, fixture-backed check, and script README. |
| `evals/evals.json` | Replaced root-list evals with DoD cases and required expected checks. |
| `examples/*` | Added realistic source-grounded billing assistant input and validated output example. |
| `agents/*` and `prompts/*` | Specialized responsibilities around mode selection, source boundaries, rubric checks, porting, and validation. |
| `templates/*` | Replaced generic output structure and removed remote font dependency from HTML. |
| `knowledge/*` | Added Playbook, source boundary, rubric, portability, and forge packet concepts. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/prompt-forge/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill prompt-forge
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill prompt-forge
python3 -B scripts/validate-skills.py --strict
```

Results:

- `OK: prompt-forge forge packet validator passed`
- `skill=prompt-forge dod=pass errors=0`
- `skills_with_scripts=1 warnings=0 errors=0`
- `skills=585 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
python3 -B scripts/validate-mcp-config.py
python3 -B scripts/check-devkit-readiness.py
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
git diff --check
```

Results:

- `skills=585 warnings=0 errors=0`
- `skills=585 agents=260 commands=267 prompts=256 components=1368`
- `mcp config: passed`
- `devkit readiness: passed`
- `Repo boundaries OK`
- `summary: passed=11 failed=0 total=11`
- `skills_with_scripts=25 warnings=0 errors=0`
- `OK: doc-factory deterministic smoke check passed`
- `git diff --check` produced no output

## Decision

Improved now and ready for PR.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
