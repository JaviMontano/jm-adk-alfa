# Skill Review: ab-testing

Date: 2026-05-28
Reviewer: Codex
Status: reviewed and improved
Severity: P2

## Intended Purpose

The skill promised hypothesis formulation, statistical significance, sample-size calculation, and test duration.
That means it should help a user design or review an A/B test, not merely produce a generic analysis workflow.

## Current-State Gap

Before this review, the skill validated structurally but the domain contract was shallow:

| Area | Gap |
|---|---|
| `SKILL.md` | Procedure was generic and did not define hypothesis, primary metric, guardrails, MDE, power, alpha, duration, or stopping rules. |
| `knowledge/body-of-knowledge.md` | Contained placeholder "industry standards" language rather than A/B testing readiness states and validity threats. |
| `templates/output.md` | Used generic summary/evidence/result sections instead of an experiment brief. |
| `evals/evals.json` | Tested generic activation rather than experiment-design failure modes. |
| examples | Did not show a realistic A/B testing deliverable. |
| guardian | Checked generic evidence/compliance, not experiment validity. |

## User Impact

A vibe coder could ask for an A/B test and receive a plausible but under-specified answer that spends traffic without a decision rule.
The main risk is false confidence: treating a quick experiment idea as launch-ready without metric ownership, instrumentation checks, or stopping policy.

## Agent Risk

The agent could overclaim significance, invent sample-size numbers from missing inputs, ignore guardrails, or report a skill as "done" while the experiment remains invalid.

## Improvement Applied

| File | Change |
|---|---|
| `skills/ab-testing/SKILL.md` | Rewrote purpose, procedure, quality criteria, anti-patterns, related skills, and limits around A/B experiment design. |
| `skills/ab-testing/README.md` | Clarified triggers and output shape. |
| `skills/ab-testing/knowledge/body-of-knowledge.md` | Added minimum experiment contract, readiness states, validity threats, and quality metrics. |
| `skills/ab-testing/templates/output.md` | Replaced generic output with experiment brief template. |
| `skills/ab-testing/evals/evals.json` | Replaced generic evals with purpose-specific design, audit, missing-input, guardrail, false-positive, and peeking cases. |
| `skills/ab-testing/examples/*` | Added realistic input and expected output shape. |
| `skills/ab-testing/prompts/primary.md` | Aligned orchestration with experiment readiness, validity threats, and no-overclaiming rule. |
| `skills/ab-testing/agents/guardian.md` | Added experiment-specific validation gates. |

## No-Regression Check

Run:

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/qa/generate-skill-review-ledger.py --mark-reviewed ab-testing --review-doc docs/audits/skills/ab-testing-review.md --severity P2 --decision "improved" --notes "Aligned A/B testing outputs, evals, examples, and quality gates with experiment-design purpose."
```

Expected:

- Skill validation passes.
- Ledger reports 524 skills, 1 reviewed, 523 pending.

## Decision

Improved now.
Next skill in default order: `accessibility-audit`.

## Ledger Completion 2026-06-05

- [CODE] `python3 -B scripts/validate-skill-dod.py --skill ab-testing` returned `dod=pass errors=0`.
- [CODE] Added `assets/README.md`, `assets/manifest.json`, and `assets/deliverable-checklist.md` to satisfy the Alfa DoD asset contract.
- [CODE] `skills/ab-testing/evals/evals.json` now uses the `cases` contract and includes `assets`, `deterministic_scripts`, and `quality_criteria` in `expected_checks` coverage.
- [CODE] `python3 -B scripts/validate-skills.py --strict` returned `skills=585 warnings=0 errors=0` after this closure batch.
- [CONFIG] Ledger status updated to `dod-complete` with decision `completed-assets-dod`.
