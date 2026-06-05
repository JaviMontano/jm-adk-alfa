# Skill Review: funnel-analytics

Date: 2026-06-05
Reviewer: Codex
Status: reviewed and improved
Severity: P1

## Intended Purpose

The skill promises conversion funnel tracking, drop-off analysis, and optimization strategy. For Alfa, that requires a deterministic measurement contract: source evidence, step definitions, denominators, identity/session handling, data-quality gaps, segment limits, and experiment-ready recommendations.

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | Scaffold-level discover/analyze/execute/validate steps did not define funnel events, denominators, source status, or no-invention rules. |
| `README.md` | Scaffold text and no minimum input contract. |
| `knowledge/body-of-knowledge.md` | Generic standards language instead of funnel measurement contracts. |
| `templates/output.md` | Generic summary/evidence/result placeholders rather than a funnel report structure. |
| `evals/evals.json` | Root list of activation cases, not DoD `cases` with edge coverage. |
| `examples/*` | Generic sample input/output, not a realistic funnel scenario. |
| `agents/*` and `prompts/*` | Generic roles and confidence language instead of event, denominator, data-quality, and privacy review gates. |
| `assets/` | Missing required DoD assets. |

## User Impact

A user could receive plausible conversion advice even when event definitions, denominators, identity stitching, bot filters, or segment windows were not verified. That risks optimizing an unmeasured step or presenting causal claims from observational counts.

## Improvement Applied

| File | Change |
|---|---|
| `skills/funnel-analytics/SKILL.md` | Added funnel objective, step mapping, formula, evidence, no-invention, privacy, segment, and validation contracts. |
| `skills/funnel-analytics/README.md` | Added triggers, minimum inputs, output contract, and `not verified` rule. |
| `skills/funnel-analytics/knowledge/body-of-knowledge.md` | Replaced generic standards with measurement contracts and failure modes. |
| `skills/funnel-analytics/templates/output.md` | Replaced placeholders with funnel definition, formula, drop-off, segment, instrumentation, backlog, validation, and risks sections. |
| `skills/funnel-analytics/evals/evals.json` | Added 11 DoD `cases` covering verified funnels, missing instrumentation, denominator mismatch, identity stitching, segment mix, small samples, privacy, scripts, and false positives. |
| `skills/funnel-analytics/examples/*` | Added realistic SaaS activation input and evidence-tagged output. |
| `skills/funnel-analytics/prompts/*` | Specialized execution, quick, deep, and meta prompts around measurement-first analysis. |
| `skills/funnel-analytics/agents/*` | Specialized lead, support, specialist, and guardian roles around evidence, denominators, data quality, privacy, and causal limits. |
| `skills/funnel-analytics/knowledge/knowledge-graph.*` | Replaced scaffold graph with funnel-analysis concepts and gates. |
| `skills/funnel-analytics/assets/*` | Added README, manifest, and reusable deliverable checklist. |

## No-Regression Check

Run:

```bash
python3 -B scripts/validate-skill-dod.py --skill funnel-analytics
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
git diff --check
```

Expected:

- Per-skill DoD returns `dod=pass errors=0`.
- Strict skill validation returns zero warnings and zero errors.
- Component count, repo boundaries, QA adversarial tests, script-backed checks, and whitespace checks pass.

## Decision

Improved now and ready for ledger closure.

## Ledger Completion 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill funnel-analytics` returned `skill=funnel-analytics dod=pass errors=0`.
- [CÓDIGO] Added `assets/README.md`, `assets/manifest.json`, and `assets/deliverable-checklist.md` to satisfy the Alfa DoD asset contract.
- [CÓDIGO] `skills/funnel-analytics/evals/evals.json` now uses the `cases` contract and includes `assets`, `deterministic_scripts`, and `quality_criteria` in `expected_checks` coverage.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` returned `skills=585 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/count-components.py --check-docs` returned `skills=585`, `agents=260`, `commands=267`, `prompts=256`, and `components=1368`.
- [CÓDIGO] `bash scripts/check-repo-boundaries.sh` returned `Repo boundaries OK`.
- [CÓDIGO] `python3 -B scripts/qa/run-adversarial-tests.py` returned `summary: passed=11 failed=0 total=11`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` returned `skills_with_scripts=22 warnings=0 errors=0`.
- [CONFIG] Ledger status should be `dod-complete` with decision `completed-funnel-analytics-dod` after validation passes.
