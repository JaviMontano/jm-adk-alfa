# Skill Review: quality-gatekeeper

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`quality-gatekeeper` validates JM-ADK deliverables at G0-G3 gates using
deterministic criteria, evidence tags, sequential gate order, score-history
entry contracts, remediation, and fail-closed missing-evidence handling.
[CÓDIGO] The hardened skill must block rubber-stamped passes, out-of-sequence
gate approvals, missing evidence, and unverified score-history claims.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `quality-gatekeeper` selected as the next Phase 2 quality skill after `constitution-compliance`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed for missing `assets/`, scaffold examples, root-array evals, no scripts, Google Fonts, prompt drift, and unresolved `.specify/score-history` contract. | [CÓDIGO] No deterministic validator for G0-G3 criteria, missing evidence, gate order, or score-history entry shape. | [CONFIG] Add assets, offline validator, fixtures, eval cases, offline templates, and read-only agents. | [INFERENCIA] High before hardening because the skill could sound authoritative without proving gate status. |
| Eval Designer | complete | [CÓDIGO] Evals were 7 prose activation checks and did not test gate logic, blocking, evidence, sequencing, score-history, or report structure. | [CÓDIGO] Missing G0/G1/G2/G3 pass/block cases, assumption warning, and false-positive routing. | [CONFIG] Convert evals to 10 `cases` with expected outputs, forbidden outputs, required checks, and fixture references. | [INFERENCIA] High before hardening because rubber-stamped gate approvals were unblocked. |
| Guardian | complete | [CÓDIGO] The skill itself says no evidence means no pass, but lacked review doc, ledger closure, executable eval evidence, and score-history schema. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, scripts, evals, examples, review doc, DoD, and full gates pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add deterministic assets for G0-G3 criteria, evidence policy,
  report contract, activation policy, and score-history schema.
- [CONFIG] Add `scripts/validate_gate_report.py`, `scripts/check.sh`, and
  pass/block/false-pass fixtures.
- [CONFIG] Replace scaffold README, examples, evals, prompts, agents,
  knowledge, and templates with gate-specific contracts.
- [CONFIG] Remove live web dependencies from templates.
- [CONFIG] Narrow default agents to read-only evidence collection and reporting.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation boundaries, required inputs, gate process, criteria summary, report contract, validation gate, severity policy, and edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation guidance, deterministic resources, and local checks. |
| `assets/` | [CÓDIGO] Added manifest, G0-G3 criteria, report contract, evidence policy, score-history schema, activation policy, and README. |
| `scripts/` | [CÓDIGO] Added offline report validator, `check.sh`, valid pass fixture, valid blocked fixture, and invalid false-pass fixture. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 10 DoD `cases` covering G0-G3 pass/block, missing evidence, out-of-sequence G3, assumption warning, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic G3 release gate input and blocked gate report output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles and prompts around gate scope, evidence, sequential order, and Guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and live-font templates with offline Markdown, HTML, and DOCX-oriented gate report templates. |
| `knowledge/*` | [CÓDIGO] Added canon, operating rules, anti-patterns, and a gate-specific knowledge graph. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/quality-gatekeeper/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill quality-gatekeeper
python3 -B scripts/validate-skill-dod.py --skill quality-gatekeeper
```

Results:

- [CÓDIGO] `OK: quality-gatekeeper reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=quality-gatekeeper dod=pass errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
python3 -B scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 -B scripts/validate-runtime-instructions.py
bash scripts/adapt.sh all
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/qa/run-confidence-fp-tests.py
python3 -B scripts/post_annotations.py --validate-only references/schemas/annotations.example.json
python3 -B scripts/diagnose-user-context.py --dry-run
python3 -B scripts/diagnose-personal-skills.py --dry-run
python3 -B scripts/sync-personal-skills.py --dry-run --target /tmp/alfa-personal-skills-target
bash scripts/generate-pristino-index.sh
git diff --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills_with_scripts=40 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `ADAPTER-COMPLETE: antigravity (600 skills indexed)`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `USER_CONTEXT_STATUS: ready`
- [CÓDIGO] `PERSONAL_SKILLS_STATUS: empty`
- [CÓDIGO] `Generated: PRISTINO-INDEX.md`
- [CÓDIGO] `shellcheck` was not installed in this environment, so shell lint was
  skipped.

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, criterion coverage,
  evidence-tag presence, blocking policy, assumption warning behavior, and
  score-history entry shape; it does not prove the underlying project is ready
  beyond supplied evidence.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/quality-gatekeeper/scripts/check.sh` passed with
  deterministic pass, blocked, and invalid fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill quality-gatekeeper` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill quality-gatekeeper` passed with `dod=pass errors=0`.
