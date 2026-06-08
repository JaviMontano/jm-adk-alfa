# Quality Metrics Body of Knowledge

## Canon

Quality metrics convert engineering quality into deterministic thresholds. A valid scorecard includes coverage, complexity, duplication, Lighthouse, bundle size, and Firestore I/O unless reduced scope is explicit.

## Metric Rules

| Metric | Pass rule |
|---|---|
| coverage | Lines, branches, functions, and statements are all at least 80 percent. |
| complexity | Maximum cyclomatic complexity is at most 15. |
| duplication | Duplicated code is below 5 percent. |
| lighthouse | Performance, Accessibility, Best Practices, and SEO meet their score thresholds. |
| bundle_size | Initial gzipped bundle is at most 250KB. |
| firestore_io | Daily read budget and spike multiplier stay below warning thresholds. |

## Evidence Requirements

- Every metric requires source evidence or reduced-scope reason.
- Every metric has a gate with a threshold and on-failure action.
- Coverage alone never proves quality completeness.
- Trend regression requires three consecutive snapshots.
