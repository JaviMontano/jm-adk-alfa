---
name: benchmark-skill
version: 1.0.1
description: Compares two skill states or one skill against a benchmark standard using a deterministic rubric, inventory deltas, gate changes, regression detection, trade-off analysis, and net assessment. Use when the user asks to compare skill versions, benchmark a skill, measure skill improvement, diff skill states, prove before/after quality, or evaluate a skill against a quality standard.
argument-hint: "state-a state-b | state --against-standard"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
model: opus
context: fork
---

# Skill Benchmark

Benchmark skill quality with reproducible evidence. The skill compares two
states of a skill, or one skill against a fixed standard, and produces a report
with inventory deltas, 10-dimension scores, 13 gate checks, regressions,
trade-offs, top improvements, and a net assessment. [EXPLICIT]

## Deterministic Assets

Use local assets before writing the report. [EXPLICIT]

| Path | Use |
|---|---|
| `assets/benchmark-rubric.json` | 10 scoring dimensions, score bounds, evidence requirements, and variance policy |
| `assets/gate-policy.json` | 13 deterministic quality gates and pass/fail fields |
| `assets/net-assessment-policy.json` | IMPROVED, LATERAL, REGRESSED, TRANSFORMED, IDENTICAL, and GAP-TO-STANDARD rules |
| `assets/report-contract.json` | Required benchmark report sections and blocked vague phrases |
| `scripts/validate_benchmark_report.py` | Offline validator for JSON benchmark report fixtures |
| `scripts/check.sh` | Deterministic positive and negative fixture checks |

The script reads only explicit local JSON files. It does not call APIs, MCP
tools, model providers, the network, system time, random sources, or mutate the
skills being compared. [EXPLICIT]

## When To Activate

Activate only when the user asks for a benchmark, comparison, before/after
proof, gap-to-standard report, or regression analysis of a skill. [EXPLICIT]

| User intent | Activate? | Reason |
|---|---:|---|
| "Compare this skill before and after hardening" | Yes | Version benchmark |
| "Benchmark prompt-forge against the standard" | Yes | Gap-to-standard |
| "Did this skill improve after the PR?" | Yes | Requires delta and regression detection |
| "Certify this skill as ready to ship" | No | Use certification/gate skills |
| "Find issues in this skill" | No | Use audit/x-ray skills |
| "Compare two vendor tools" | No | Not a skill-state benchmark |

If either state path is missing, or a state lacks `SKILL.md`, stop and ask for a
valid baseline rather than fabricating scores. [EXPLICIT]

## Input Modes

| Mode | Required Input | Output |
|---|---|---|
| Version comparison | State A path and State B path, each with `SKILL.md` | Delta report with net assessment |
| Same-skill commits | Two extracted directories or explicit git refs supplied by the user | Delta report with commit references |
| Against standard | One skill path plus `--against-standard` | Gap-to-standard report; regressions are not applicable |
| Different skills | Two skill paths and user confirmation that they are comparable | Parallel scorecards plus stronger/weaker assessment |

## Benchmark Process

1. Confirm activation and input mode. [EXPLICIT]
2. Verify every real state has `SKILL.md`; if not, stop and ask. [EXPLICIT]
3. Inventory each state: files, lines, `SKILL.md` lines, references, eval cases,
   agents, scripts, assets, examples, and templates. [EXPLICIT]
4. Score both states using `assets/benchmark-rubric.json`. Reuse the exact State
   A score for unchanged evidence; do not rescore unchanged sections. [EXPLICIT]
5. Run the 13 gates from `assets/gate-policy.json` on both states. [EXPLICIT]
6. Calculate deltas and classify regressions, improvements, trade-offs, and net
   assessment using `assets/net-assessment-policy.json`. [EXPLICIT]
7. Produce the report using `assets/report-contract.json` and
   `templates/output.md`. [EXPLICIT]
8. If the report is represented as JSON, run
   `scripts/validate_benchmark_report.py` before finalizing. [EXPLICIT]

## Report Contract

Every benchmark report must include: [EXPLICIT]

1. Compared states and input mode.
2. Inventory table with State A, State B or Standard, and delta.
3. 10-dimension scorecard with scores, deltas, direction, and evidence.
4. 13 gate check table with pass/fail and changes.
5. Regressions table, even when empty.
6. Top improvements table for dimensions improved by 2+ points.
7. Trade-off analysis when a dimension drops but another rises from the same
   change.
8. Net assessment that follows the policy exactly.
9. Recommendation with the next action.
10. Caveats for transformed states, missing baselines, or against-standard mode.

## Net Assessment Rules

Use these labels only when the data supports them: [EXPLICIT]

| Label | Required Evidence |
|---|---|
| `IMPROVED` | Average score increases by at least 0.5, no gate regression, no 2+ point rubric regression, and at least two dimensions improve |
| `LATERAL` | Average changes by less than 0.5 and trade-offs balance without net gate change |
| `REGRESSED` | Average decreases by at least 0.5, any gate regression, or at least two dimensions regress by 2+ points |
| `TRANSFORMED` | Structure changed so direct delta comparison is misleading |
| `IDENTICAL` | Inventory, scores, and gates show no meaningful change |
| `GAP-TO-STANDARD` | Against-standard mode; all deltas represent gaps rather than regressions |

## Validation Gate

- [ ] All real states have `SKILL.md`.
- [ ] Inventory includes file, line, eval, asset, agent, script, and template
  counts.
- [ ] All 10 rubric dimensions have numeric scores from 1-10 and evidence.
- [ ] Every score delta equals `score_b - score_a`.
- [ ] All 13 gates have State A and State B or Standard outcomes.
- [ ] All regressions and gate regressions are listed with severity and cause.
- [ ] Net assessment matches `assets/net-assessment-policy.json`.
- [ ] Against-standard mode does not report regressions.
- [ ] Transformed mode avoids misleading direct "improved/regressed" claims.
- [ ] The report includes evidence tags and avoids vague phrases such as
  "looks better", "good job", or "probably improved".

## Failure Modes

| Failure | Signal | Recovery |
|---|---|---|
| Missing baseline | State A path absent or not provided | Ask for baseline path, extracted commit, or `--against-standard` |
| Missing `SKILL.md` | Path exists but no skill root | Stop and ask for a valid skill directory |
| Identical states | Inventory, scores, and gates unchanged | Report `IDENTICAL`; verify paths are distinct |
| Incomparable rewrite | Structural shift makes direct deltas misleading | Use `TRANSFORMED` and parallel scorecards |
| Score conflict | Same unchanged evidence gets different score | Reuse State A score and note the anchoring correction |

## Reference Files

| File | Content | Load When |
|---|---|---|
| `references/comparison-framework.md` | Scoring consistency, delta classification, trade-off analysis, and transformed-state guidance | Always for human scoring calibration |
| `assets/benchmark-rubric.json` | Machine-readable dimensions and score/evidence rules | Always |
| `assets/gate-policy.json` | 13 deterministic gates | Always |
| `assets/net-assessment-policy.json` | Classification rules | Always |
| `assets/report-contract.json` | Required report sections and blocked phrases | Always |
| `scripts/check.sh` | Fixture-backed validator smoke test | When scripts can be run |

---
**Author:** Javier Montano | **Last updated:** 2026-06-05
