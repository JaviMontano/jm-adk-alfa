# Skill Review: auto-prompt-matching

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

The skill routes user input to the best available skill or prompt. For Alfa, that routing must be deterministic because it decides which downstream workflow receives user context.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | One active skill selected from the Phase 1 queue. | None. | Keep this PR scoped to `auto-prompt-matching`. | Low if scope remains isolated. |
| Determinism Auditor | complete | Scaffold examples, generic README/body, no assets, root-list evals, no scoring/tie-break contract. | No skill-specific script existed. | Add routing checklist, source-backed scoring, no-invention rule, and downstream separation. | High before hardening because routing could invent capabilities. |
| Eval Designer | complete | Evals only tested activation and did not cover false positives, missing indexes, ambiguity, or tie-breaks. | None. | Convert to `cases` with routing, ask, decline, false-positive, and DoD scenarios. | Medium if evals remain broad. |
| Script Engineer | complete | No deterministic script is required for this text-routing skill in this PR. | Automated routing script can be a future separate PR. | Cover `deterministic_scripts` through eval metadata and repo-wide script gates. | Low. |
| Guardian | complete | DoD requires assets, non-generic examples, `cases`, review doc, ledger row, and validation evidence. | None after changes. | Block unless per-skill DoD and repo gates pass. | Low after validation. |

## Hardening Brief

- Replace fuzzy matching prose with deterministic routing policy.
- Add source-backed candidate rules, confidence bands, and tie-break order.
- Add `assets/routing-checklist.md`, asset manifest, and output template sections.
- Replace scaffold examples with a real XLSX routing scenario.
- Convert evals to DoD `cases` with at least eight cases and expected checks.
- Update agents, prompts, knowledge, and knowledge graph to enforce routing-only behavior.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | Added source order, scoring/tie-break policy, no-invention rule, confidence bands, and asset reference. |
| `README.md` | Added triggers, minimum inputs, output contract, and non-invention rule. |
| `assets/` | Added README, manifest, and reusable routing checklist. |
| `evals/evals.json` | Replaced root-list activation tests with 9 DoD `cases`. |
| `examples/*` | Added realistic deterministic XLSX routing example and evidence-tagged output. |
| `templates/output.md` | Replaced placeholders with routing decision, source, score, tie-break, validation, and risk sections. |
| `agents/*` and `prompts/*` | Specialized roles and execution prompts around source-backed routing and downstream separation. |
| `knowledge/*` | Replaced generic knowledge with routing rules and graph concepts. |

## No-Regression Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skill-dod.py --skill auto-prompt-matching
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
git diff --check
```

Results:

- `skill=auto-prompt-matching dod=pass errors=0`
- `skills=585 warnings=0 errors=0`
- `skills=585 agents=260 commands=267 prompts=256 components=1368`
- `Repo boundaries OK`
- `summary: passed=11 failed=0 total=11`
- `skills_with_scripts=22 warnings=0 errors=0`
- `OK: doc-factory deterministic smoke check passed`
- `git diff --check` produced no output

## Decision

Improved now and ready for PR after local validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status is `dod-complete` with decision `completed-auto-prompt-matching-dod`.
