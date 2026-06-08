---
name: quality-engineering
version: 1.0.0
argument-hint: "project-or-system-name"
description:
  Designs strategic quality engineering frameworks covering test strategy, automation architecture, quality gates,
  metrics, and shift-left practices. Activates when the user says "design test strategy", "plan quality gates",
  "set up test automation", "assess quality maturity", or "define quality metrics". Also triggers on mentions of
  test pyramid, shift-left, CI/CD quality, automation architecture, or quality engineering. Use this skill even if
  the user only asks about test coverage because it assesses the full quality posture. [EXPLICIT]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Quality Engineering

Strategic quality engineering framework. Designs the system — QA teams execute it. For architects, engineering leads, and quality strategists who define *how* quality works. [EXPLICIT]

Use this skill to produce an evidence-backed framework for a project, product, service, or platform. The output is strategy: maturity assessment, test architecture, quality gates, metrics, roadmap, and priority actions. It does not write test suites or CI pipelines directly.

## Deterministic Contract

Load these files only when the request needs the corresponding detail:

- `assets/quality-framework-contract.json`: required report fields and decisions.
- `assets/maturity-model.json`: score bands and canonical six dimensions.
- `assets/test-strategy-policy.json`: architecture-to-test-shape mapping.
- `assets/gate-policy.json`: canonical quality gates, enforcement modes, timeouts, and required criteria.
- `assets/metrics-policy.json`: required leading and lagging metrics.
- `assets/action-priority-policy.json`: top action sorting rules.
- `references/quality-patterns.md`: concise reference for maturity, test shape, gates, and dashboard patterns.

When a machine-checkable handoff is requested, emit JSON that passes:

```bash
python3 -B skills/quality-engineering/scripts/validate_quality_engineering.py <report.json>
```

## Inputs

Parse the user request for:

- `subject`: project, product, service, platform, or team being assessed.
- `architecture_type`: one of `monolith`, `microservices`, `event-driven`, or `frontend`. If unknown, choose `monolith` only with an explicit assumption.
- `mode`: `executive`, `technical`, or `full`. Default `technical`.
- `evidence_sources`: local files, user-provided facts, command output, or explicitly named assumptions.
- `constraints`: regulated domain, release cadence, team size, pipeline limits, tool stack, or timebox.

## Workflow

1. Confirm the skill applies to quality strategy, quality gates, automation architecture, shift-left practice, or quality metrics.
2. Inspect local evidence when available with read-only commands such as `find . -name "*.test.*" -o -name "*.spec.*" -o -name "*test*" -type d | head -20`.
3. Score the six maturity dimensions from `assets/maturity-model.json`; every score requires evidence or an assumption.
4. Select the test strategy shape from `assets/test-strategy-policy.json`; do not invent percentages.
5. Define the five canonical gates from `assets/gate-policy.json`; each gate needs mode, timeout, criteria, and failure handling.
6. Include all metrics from `assets/metrics-policy.json`; mark metrics as unavailable only when evidence is absent.
7. Produce exactly three priority actions unless fewer than three dimensions are below target.
8. Run Guardian validation before finalizing.

## Output Requirements

Every final report includes:

- Evidence Summary
- Maturity Assessment
- Test Strategy
- Quality Gates
- Metrics Dashboard
- Roadmap
- Top Priority Actions
- Guardian Decision

For JSON reports, use schema version `1`, skill `quality-engineering`, and the canonical order defined in assets.

## Scoring Rules

- Scores are integers from 0 to 100.
- Levels derive from score bands in `assets/maturity-model.json`.
- `overall_score` is the arithmetic mean of the six dimension scores rounded to two decimals.
- `overall_level` is derived from `overall_score`.
- `target_level` must be between `overall_level` and `5`.
- Priority actions sort by largest gap to the minimum score of `target_level`, then by lower score, then by canonical dimension order.

## Guardrails

- Do not claim a gate is enforced unless evidence shows it blocks or alerts as specified.
- Do not use coverage as the only quality metric.
- Do not recommend network-only, time-dependent, or random validation as the sole gate.
- Do not mark security criteria bypassable.
- Do not call a plan complete if it lacks maturity scores, test shape, gate criteria, metrics, roadmap, priority actions, or evidence.

## Handoff

If the report is blocked by missing evidence, return `guardian.decision="warn"` or `guardian.decision="block"` with concrete missing inputs and a reduced-scope note.
