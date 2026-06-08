# Example Output

## Evidence Summary

- Subject: Project Atlas frontend.
- Scope: frontend.
- Evidence: coverage summary, complexity report, jscpd report, Lighthouse export, bundle report, and Firestore usage snapshot.
- Exclusions: generated clients and `node_modules`.

## Metric Scorecard

| Metric | Status | Evidence |
|---|---|---|
| coverage | warn | Branch coverage is 76, below the 80 pass threshold. |
| complexity | fail | Max cyclomatic complexity is 23, above the fail threshold. |
| duplication | pass | Duplication is 3.2 percent, below 5 percent. |
| lighthouse | warn | Performance is 84, below the 90 pass threshold. |
| bundle_size | fail | Initial gzip bundle is 310KB, above 300KB fail threshold. |
| firestore_io | warn | Daily reads are above 50000. |

Quality score: 53.33.

## Gate Matrix

Each metric has a CI or dashboard gate with an explicit threshold and failure action.

## Trend Assessment

Trend window: 3 snapshots. No three-snapshot trend evidence was provided, so trend status is warn.

## Priority Actions

1. Reduce max cyclomatic complexity below 15.
2. Reduce initial bundle below 250KB gzipped.
3. Raise branch coverage to at least 80 percent.

## Guardian Decision

Decision: `warn`.

Reason: The report is valid, but multiple metrics are below pass thresholds.
