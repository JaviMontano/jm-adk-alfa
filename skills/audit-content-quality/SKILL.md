---
name: audit-content-quality
version: 1.0.1
author: JM Labs (Javier Montaño)
description: >
  Audits SKILL.md content quality with a deterministic 6-dimension rubric,
  per-skill scorecards, plugin averages, bottom-skill priorities, systematic
  gap detection, and machine-readable report validation. [EXPLICIT]
  Trigger: audit content quality, score skills, check skill quality, content
  rubric, weakest skills, plugin quality score. [EXPLICIT]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Audit Content Quality

Audits `SKILL.md` files in a plugin or skill directory using a deterministic
6-dimension structural rubric. The output is a scorecard report that is
actionable, reproducible, and validated against local assets. [EXPLICIT]

## Deterministic Assets

Use these local files before producing or reviewing a content quality audit:

| Path | Use |
|---|---|
| `assets/activation-policy.json` | Activation, false-positive, and clarification rules |
| `assets/scoring-rubric.json` | Canonical dimensions, score bounds, grade thresholds, bottom count, and priorities |
| `assets/report-contract.json` | Required JSON report sections and fields |
| `assets/evidence-policy.json` | Evidence tag and rationale requirements |
| `references/content-quality-rubric.md` | Human-readable mirror of the rubric |
| `scripts/validate_content_quality_report.py` | Offline JSON report validator |
| `scripts/check.sh` | Deterministic positive and negative fixture check |

The validator reads only local JSON files. It does not call the network,
current time, random sources, model providers, or MCP tools. [EXPLICIT]

## When To Activate

Activate when the user asks to audit, score, rank, compare, or improve
`SKILL.md` content quality for a plugin, skill directory, or explicit set of
skill files. [EXPLICIT]

Do not activate for generic code review, security review, factuality review,
website/article copy quality, design critique, grammar-only review, or content
work that is not about `SKILL.md` skill contracts. [EXPLICIT]

If no plugin root, skill directory, or `SKILL.md` file is supplied, ask for the
target path instead of inventing a scope. [EXPLICIT]

## Input Contract

Accept:

- a plugin root containing one or more `SKILL.md` files;
- a list of skill directories or `SKILL.md` paths;
- optional scoring constraints, such as "only rank the bottom 3".

If zero `SKILL.md` files are found, report `blocked` with the searched path and
do not produce fake scorecards. [EXPLICIT]

## Scoring Rubric

Score each skill on these six dimensions from `0` to `10`, using
`assets/scoring-rubric.json` as the source of truth:

1. `completeness`
2. `description_quality`
3. `procedure_clarity`
4. `quality_criteria`
5. `anti_patterns`
6. `edge_cases`

The total score is the sum of the six dimensions, max `60`.
`percentage = total_score / 60 * 100`. Grades are:

| Grade | Percentage |
|---|---:|
| A | 90-100 |
| B | 80-89.999 |
| C | 70-79.999 |
| D | 60-69.999 |
| F | 0-59.999 |

Any dimension average below `6.0` is a systematic gap. [EXPLICIT]

## Procedure

1. Confirm activation using `assets/activation-policy.json`.
2. Discover all target `SKILL.md` files with `Glob` or an explicit input list.
3. Parse each file for frontmatter, description, allowed tools, procedure,
   quality criteria, anti-patterns, edge cases, examples, and references.
4. Score all six dimensions using the local rubric and write one rationale per
   dimension with `[CODE]`, `[CONFIG]`, `[DOC]`, or `[INFERENCE]` evidence tags.
5. Compute `total_score`, `percentage`, `grade`, and `lowest_dimension` for
   every skill.
6. Compute plugin average score, average percentage, and summary grade.
7. Sort bottom skills by `total_score` ascending, then skill name ascending;
   report up to `3` items with priority from `assets/scoring-rubric.json`.
8. Compute systematic gaps for dimension averages below `6.0`.
9. Report coverage: discovered skills, scored skills, and skipped skills.
10. Validate JSON reports with `scripts/validate_content_quality_report.py`
    when a machine-readable artifact is produced.

## Output Contract

Markdown output must include these sections:

1. `Summary`
2. `Scorecards`
3. `Bottom Skills`
4. `Systematic Gaps`
5. `Coverage`
6. `Warnings`

JSON output must match `assets/report-contract.json`. [EXPLICIT]

Every scorecard must include:

- skill name and path;
- six dimension scores;
- six dimension rationales;
- total score, percentage, grade, lowest dimension, and recommendation.

## Local Validation

Run the skill check:

```bash
bash skills/audit-content-quality/scripts/check.sh
```

Validate a JSON report:

```bash
python3 -B skills/audit-content-quality/scripts/validate_content_quality_report.py \
  --contract skills/audit-content-quality/assets/report-contract.json \
  --rubric skills/audit-content-quality/assets/scoring-rubric.json \
  --evidence-policy skills/audit-content-quality/assets/evidence-policy.json \
  --report <content-quality-report.json>
```

## Quality Gate

- Every discovered `SKILL.md` is scored or listed under `coverage.skipped_skills`.
- Scores use the exact six dimensions and `0-10` bounds.
- Totals, percentages, grades, averages, and bottom skills are formula-derived.
- Every dimension score has a rationale with an accepted evidence tag.
- Bottom skills include specific recommendations and priorities.
- Systematic gaps are reported only when dimension averages fall below `6.0`.
- No remote assets, wall-clock dates, or mutation tools are required.

## Assumptions & Limits

- Read-only. This skill never modifies target `SKILL.md` files. [EXPLICIT]
- The rubric is structural, not a truth validator; factual correctness of a
  skill's domain claims requires a separate audit. [EXPLICIT]
- Single-skill targets are valid; bottom analysis reports only that one skill.
  [EXPLICIT]
- For unconventional skills, score the observable contract and explain fit
  concerns in the rationale instead of silently skipping the skill. [EXPLICIT]
