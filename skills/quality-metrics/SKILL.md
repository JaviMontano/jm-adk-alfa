---
name: quality-metrics
description: Code coverage, cyclomatic complexity, duplication, Lighthouse scores, bundle size, and Firestore read/write tracking
version: 1.0.0
status: production
owner: Javier Montaño
tags: [testing, metrics, coverage, complexity, lighthouse, bundle-size, firestore]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Quality Metrics

Code coverage, cyclomatic complexity, duplication, Lighthouse scores, bundle size, and Firestore read/write tracking.

Use this skill to define, collect, and enforce quantitative quality thresholds across an application or repository. Every metric has a numeric target, evidence source, CI gate, and deterministic status.

## Deterministic Contract

Load these files only when needed:

- `assets/quality-metrics-contract.json`: required report fields and Guardian decisions.
- `assets/metrics-thresholds.json`: canonical metric order, thresholds, warn bands, and score points.
- `assets/gate-policy.json`: required gate fields and enforcement policy.
- `assets/trend-policy.json`: deterministic trend window and regression rules.
- `assets/action-priority-policy.json`: top action sorting rules.
- `assets/evidence-policy.json`: accepted evidence types and blocked claims.

When a machine-checkable handoff is required, emit JSON that passes:

```bash
python3 -B skills/quality-metrics/scripts/validate_quality_metrics.py <report.json>
```

## Inputs

Parse the request for:

- `subject`: repository, app, product, package, or service being measured.
- `scope`: `repo`, `package`, `route`, `frontend`, `backend`, or `firebase`.
- `evidence_sources`: local reports, command output, user facts, CI artifacts, or assumptions.
- `trend_window`: sprint or snapshot count. Default is `3` because regressions require three consecutive snapshots.

## Workflow

1. Confirm the request is about quality metrics, coverage, complexity, duplication, Lighthouse, bundle size, Firestore reads/writes, or quality thresholds.
2. Gather local evidence with read-only inspection when available. Examples: coverage summary, ESLint complexity output, jscpd report, Lighthouse JSON, bundle report, or Firestore usage snapshot.
3. Evaluate the six canonical metrics in this order: `coverage`, `complexity`, `duplication`, `lighthouse`, `bundle_size`, `firestore_io`.
4. Derive metric status from `assets/metrics-thresholds.json`. Do not invent thresholds.
5. Define one enforcement gate per canonical metric. Each gate has `enforced`, `tool`, `threshold`, and `on_failure`.
6. Compute `quality_score`: `pass=10`, `warn=6`, `fail=2`; `na` is excluded from the denominator.
7. Sort priority actions by severity, then expected improvement, then canonical metric order.
8. Run Guardian validation before final output.

## Output Requirements

Every final report includes:

- Evidence Summary
- Metric Scorecard
- Gate Matrix
- Trend Assessment
- Priority Actions
- Guardian Decision

For JSON reports, use schema version `1`, skill `quality-metrics`, and the canonical metric order defined in assets.

## Guardrails

- Do not treat a metric as passing without evidence.
- Do not call a metric enforced unless a gate blocks or alerts as declared.
- Do not use network-only Lighthouse or Firestore checks as the only evidence unless the user explicitly provided exported results.
- Do not mark generated code or third-party dependencies as measured scope unless they are explicitly included.
- Do not call quality complete if any canonical metric is missing without a reduced-scope reason.

## Handoff

If evidence is missing, return `guardian.decision="warn"` or `guardian.decision="block"` with concrete missing inputs and reduced-scope notes.
