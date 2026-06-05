# Skill Review: triad-composition

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`triad-composition` selects a deterministic Lead, Support, and Guardian from the PRISTINO composition matrix using domain classification, confidence thresholds, stable tie-breakers, execution-mode routing, and fail-explicit degraded mode. [CÓDIGO] The hardened skill must not apply defaults to missing context, must reject unrelated "triad" meanings, and must never skip Guardian in triad or committee mode.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `bmad-method`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `triad-composition`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with missing `assets/`, scaffold examples, root-list evals, missing JSON fixture contract, scaffold prompts, and remote Google Fonts in HTML. | [CÓDIGO] No asset-backed matrix, thresholds, degraded mode, packet contract, or script fixture evidence. | [CONFIG] Add assets, JSON fixture, packet validator, offline templates, and stable prompt contracts. | [INFERENCIA] Medium-high before hardening. |
| Eval Designer | complete | [CÓDIGO] Evals had 7 broad prose cases and expected minimal-input defaults. [CÓDIGO] PRISTINO matrix and confidence bands were not asserted. | [CÓDIGO] Missing exact Lead/Support/Guardian names, thresholds, tie ambiguity, false-positive jazz triad, missing context, and committee escalation. | [CONFIG] Convert evals to 10 DoD cases with exact matrix assertions and negative checks. | [INFERENCIA] High before hardening because routing regressions could still "produce output." |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`, review doc absent, examples generic, evals root array, and script JSON fixture missing. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, evals, examples, scripts, review doc, DoD, and full PR gates pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add `assets/composition-matrix.json`, `assets/classification-policy.json`, `assets/degraded-mode-policy.json`, and `assets/triad-output-contract.json`.
- [CONFIG] Add `scripts/validate_triad_packet.py`, `scripts/check.sh`, Markdown packet fixtures, and `scripts/fixtures/fixture-contract.json`.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, knowledge, and templates with triad-specific deterministic contracts.
- [CONFIG] Remove remote font dependency and uncontrolled date placeholders from templates.
- [CONFIG] Keep the external `prompts/meta/105-triad-compose.md` path mismatch as a separate follow-up because this PR is scoped to one skill.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added activation boundaries, required inputs, confidence thresholds, execution modes, matrix procedure, packet contract, validation gate, and edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with deterministic resources and local checks. |
| `assets/` | [CÓDIGO] Added matrix, classification policy, degraded-mode policy, packet contract, README, and manifest. |
| `scripts/` | [CÓDIGO] Added offline packet validator, JSON fixture contract, pass/fail Markdown fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with 10 DoD `cases` covering exact triads, thresholds, ambiguity, false positives, missing context, and committee escalation. |
| `examples/*` | [CÓDIGO] Added realistic payroll onboarding input and Requirements triad output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around classification, ambiguity review, Guardian blocking, and safe quick/deep modes. |
| `templates/*` | [CÓDIGO] Replaced scaffold templates with packet-shaped offline templates. |
| `knowledge/*` | [CÓDIGO] Added matrix fidelity, threshold, Guardian, false-positive, and anti-pattern guidance. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
python3 -m json.tool skills/triad-composition/assets/manifest.json
python3 -m json.tool skills/triad-composition/evals/evals.json
bash skills/triad-composition/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill triad-composition
python3 -B scripts/validate-skill-dod.py --skill triad-composition
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] Asset, eval, knowledge graph, and fixture JSON parsed successfully.
- [CÓDIGO] `OK: triad-composition packets validated`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=triad-composition dod=pass errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 scripts/validate-runtime-instructions.py
bash scripts/adapt.sh all
python3 scripts/qa/run-adversarial-tests.py
python3 scripts/qa/run-confidence-fp-tests.py
python3 scripts/post_annotations.py --validate-only references/schemas/annotations.example.json
bash scripts/generate-pristino-index.sh
git diff --check
git diff --cached --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills_with_scripts=35 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `shellcheck not installed; skipping shell lint`
- [CÓDIGO] `workflow-local-pass`

## Follow-Up Gap

- [CÓDIGO] `prompts/meta/105-triad-compose.md` still names `triad-compose` and references `skills/triad-compose/...`; this is outside the one-skill scope and should be fixed in a separate routing cleanup PR.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
