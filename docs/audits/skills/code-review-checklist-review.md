# Skill Review: code-review-checklist

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`code-review-checklist` applies a deterministic, read-only checklist for
supplied PR diffs, changed files, dependency updates, Firestore rules, Firebase
code, TypeScript code, and frontend changes. [CÓDIGO] It covers security,
Firebase/performance, TypeScript/code quality, exact evidence, merge decision
rules, and offline checklist report validation. [CONFIG]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `code-review-checklist` selected after `code-review`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] DoD failed before hardening: missing assets, scaffold README/examples/templates/knowledge, evals without `cases`, mutation-capable tools, remote fonts, implicit date placeholders, and missing review doc. | [CÓDIGO] Missing offline validator, fixtures, report schema, checklist taxonomy, evidence policy, source boundaries, and ledger closure. | [CONFIG] Add deterministic assets/scripts, remove write tools, replace scaffold content, add review doc, and close ledger only after validation. | [INFERENCIA] High before hardening because outputs could be generic, mutable, and unauditable. |
| Eval Designer | complete | [CÓDIGO] Evals were activation-style prose and did not test security, Firebase, performance, type safety, false positives, or report contracts. | [CÓDIGO] Missing clean-code, safe React, batched Firestore, dependency-only, missing-context, hotfix, and invalid-report cases. | [CONFIG] Add 14 `cases` plus validator fixtures for blocking, clean, invalid approval, and invalid evidence. | [INFERENCIA] Medium-high before hardening because activation could pass while checklist gates failed. |
| Guardian | complete | [CÓDIGO] Initial `validate-skill-dod.py --skill code-review-checklist` failed with 5 errors and ledger remained pending. | [CÓDIGO] Assets, eval cases, examples, review doc, and ledger evidence were absent. | [CONFIG] Block closure until DoD and script checks pass. | [INFERENCIA] Closure-blocking until local validation passes. |

## Hardening Brief

- [CONFIG] Add activation, checklist taxonomy, evidence, report, and
  source-boundary assets.
- [CONFIG] Add `scripts/validate_code_review_checklist_report.py`,
  `scripts/check.sh`, two valid fixtures, and two negative fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  and knowledge files with checklist-specific deterministic contracts.
- [CONFIG] Remove `Write` and `Edit` tools from skill and agents.
- [CONFIG] Update ledger only after per-skill validators pass.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added read-only posture, activation routing, deterministic resources, fixed checklist IDs, validation gate, decision rules, and anti-patterns. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, assets, scripts, and output sections. |
| `assets/` | [CÓDIGO] Added activation policy, checklist taxonomy, evidence policy, report contract, source boundary policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline checklist validator, check script, two valid fixtures, and two negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 14 `cases` covering security, Firebase, performance, types, false positives, missing context, and hotfix mode. |
| `examples/*` | [CÓDIGO] Added realistic Firebase/TypeScript checklist input and evidence-bound output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles around checklist execution, false-positive calibration, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and remote-font templates with deterministic Markdown, DOCX-oriented, and offline HTML templates. |
| `knowledge/*` | [CÓDIGO] Added checklist domains, evidence rules, decision rules, and a checklist-specific knowledge graph. |

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, evidence tags, checklist
  IDs, source fields, decision rules, and invalid approval rejection; it does
  not prove runtime behavior outside supplied code, tests, rules, audit output,
  or CI evidence.

## Decision

[CONFIG] Improved now and ready for per-skill validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/code-review-checklist/scripts/check.sh` passed with
  valid blocking, valid clean, invalid approval-with-blocker, and invalid
  untagged-check fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill code-review-checklist`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill code-review-checklist`
  passed with `skill=code-review-checklist dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## PR Gate Check 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`
  passed with `skills_with_scripts=46 warnings=0 errors=0`.
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
- [CÓDIGO] `shellcheck skills/code-review-checklist/scripts/check.sh` was
  skipped because `shellcheck` is not installed in the local environment.

## Release Packet

- [CONFIG] Active skill: `code-review-checklist`.
- [CONFIG] Branch: `codex/harden-code-review-checklist-dod-20260605`.
- [CÓDIGO] Ledger after local hardening: `52 dod-complete / 533 pending`.
- [CONFIG] Decision: open a ready PR after staged diff and cached whitespace
  checks pass.
