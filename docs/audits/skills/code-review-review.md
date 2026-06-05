# Skill Review: code-review

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`code-review` performs deterministic, read-only review of supplied code changes,
diffs, pull requests, patches, or file excerpts. [CÓDIGO] It classifies findings
with fixed severities and categories, cites exact file/line evidence, separates
blocking and non-blocking feedback, and validates report fixtures offline.
[CONFIG]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `code-review` selected as the next pending skill after the 50-skill pause; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | complete | [CÓDIGO] DoD failed before hardening: missing assets, scaffold examples, evals without `cases`, mutation-capable tools, generic templates, remote fonts, and missing review doc. | [CÓDIGO] Missing offline validator, fixtures, asset manifest, report schema, severity taxonomy, evidence policy, source boundaries, and ledger closure. | [CONFIG] Add deterministic assets/scripts, remove write tools, replace scaffold content, add review doc, and close ledger only after validation. | [INFERENCIA] High before hardening because reviews could be generic, mutable, or uncalibrated. |
| Eval Designer | complete | [CÓDIGO] Evals were activation-style prose and did not test known defects or false positives. | [CÓDIGO] Missing clean-code, style-only, security, correctness, tests, missing-input, and conflicting-instruction cases. | [CONFIG] Add 12 `cases` with deterministic checks and fixture-backed script validation. | [INFERENCIA] Medium-high before hardening because activation could pass while review quality failed. |
| Guardian | complete | [CÓDIGO] Initial `validate-skill-dod.py --skill code-review` failed with 5 errors and ledger remained pending. | [CÓDIGO] Assets, eval cases, examples, review doc, and ledger evidence were absent. | [CONFIG] Block closure until DoD and script checks pass. | [INFERENCIA] Closure-blocking until local validation passes. |

## Hardening Brief

- [CONFIG] Add activation, taxonomy, evidence, report, and source-boundary
  assets.
- [CONFIG] Add `scripts/validate_code_review_report.py`, `scripts/check.sh`,
  valid blocking and clean fixtures, and two invalid fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  and knowledge files with code-review-specific deterministic contracts.
- [CONFIG] Remove write tools from agents and skill frontmatter.
- [CONFIG] Update ledger only after per-skill validators pass.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added read-only scope, activation routing, deterministic resources, severity/category taxonomy, output contract, decision rules, and validation commands. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, assets, scripts, and output sections. |
| `assets/` | [CÓDIGO] Added activation policy, taxonomy, evidence policy, report contract, source boundary policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline JSON report validator, check script, two valid fixtures, and two negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 12 `cases` covering defects, false positives, activation, missing context, conflicts, and invalid report rejection. |
| `examples/*` | [CÓDIGO] Added realistic PR diff input and evidence-bound output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around read-only review, evidence, false-positive calibration, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and remote-font templates with deterministic Markdown, DOCX-oriented, and offline HTML templates. |
| `knowledge/*` | [CÓDIGO] Added review dimensions, severity calibration, evidence rules, decision rules, and a code-review-specific knowledge graph. |

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, evidence tags, decision
  rules, positive-pattern requirements, and false-approval rejection; it does
  not prove that every real-world code defect will be detected without supplied
  code/diff evidence.

## Decision

[CONFIG] Improved now and ready for per-skill validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/code-review/scripts/check.sh` passed with valid
  blocking, valid clean, invalid approval-with-blocker, and invalid untagged
  fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill code-review`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill code-review`
  passed with `skill=code-review dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## PR Gate Check 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`
  passed with `skills_with_scripts=45 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/count-components.py --check-docs` passed with
  `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- [CÓDIGO] `bash scripts/check-repo-boundaries.sh` passed with
  `Repo boundaries OK`.
- [CÓDIGO] `python3 -B scripts/qa/run-adversarial-tests.py` passed with
  `passed=11 failed=0 total=11`.
- [CÓDIGO] `python3 -B scripts/validate-runtime-instructions.py` passed.
- [CÓDIGO] `python3 -B scripts/qa/run-confidence-fp-tests.py` passed.
- [CÓDIGO] `python3 -B scripts/post_annotations.py --validate-only references/schemas/annotations.example.json`
  passed with `VALID: 2 annotation(s) conform to annotations.schema.json`.
- [CÓDIGO] `bash scripts/doc-factory/check.sh` passed.
- [CÓDIGO] `python3 -B scripts/diagnose-user-context.py --dry-run` reported
  `USER_CONTEXT_STATUS: ready`.
- [CÓDIGO] `python3 -B scripts/diagnose-personal-skills.py --dry-run`
  reported `PERSONAL_SKILLS_STATUS: empty`.
- [CÓDIGO] `python3 -B scripts/sync-personal-skills.py --dry-run --target /tmp/alfa-personal-skills-target`
  reported `files=0`.
- [CÓDIGO] `bash scripts/adapt.sh all` regenerated adapters for `600` skills.
- [CÓDIGO] `bash scripts/generate-pristino-index.sh` regenerated
  `PRISTINO-INDEX.md` with `Agents: 261 | Skills: 600 | Commands: 267 |
  Prompts: 256 | Components: 1384`.
- [CÓDIGO] `git diff --check` passed with no whitespace findings.
- [CÓDIGO] `shellcheck skills/code-review/scripts/check.sh` was skipped because
  `shellcheck` is not installed in the local environment.

## Release Packet

- [CONFIG] Active skill: `code-review`.
- [CONFIG] Branch: `codex/harden-code-review-dod-20260605`.
- [CÓDIGO] Ledger after local hardening: `51 dod-complete / 534 pending`.
- [CONFIG] Decision: open a ready PR after staged diff and cached whitespace
  checks pass.
