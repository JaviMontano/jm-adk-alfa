# Example Output

## Evidence Summary

- Plugin: `jm-example`. [EXPLICIT]
- Evaluated dimensions: 6 of 7. [EXPLICIT]
- Reduced scope: `content` was not evaluated because the content audit was not
  run. [EXPLICIT]

## Scorecard

| Dimension | Status | Score | Findings (C/W/I) |
|-----------|--------|-------|------------------|
| Structure Conformance | pass | 10 | 0 / 0 / 2 |
| Manifest Quality | warn | 6 | 0 / 1 / 0 |
| Component Standards | pass | 10 | 0 / 0 / 1 |
| Hook Safety | fail | 2 | 1 / 0 / 0 |
| Reference Integrity | pass | 10 | 0 / 0 / 0 |
| Security Posture | warn | 6 | 0 / 2 / 0 |
| Content Quality | na | - | not evaluated |

## Grade

- Total score: `44/60`. [EXPLICIT]
- Percentage: `73.33%`. [EXPLICIT]
- Grade: `C`. [EXPLICIT]

## Top 3 Priority Actions

1. Hook Safety: fix the critical hook failure; expected improvement `+8`.
   [EXPLICIT]
2. Security Posture: resolve warning findings; expected improvement `+4`.
   [EXPLICIT]
3. Manifest Quality: resolve manifest warning; expected improvement `+4`.
   [EXPLICIT]

## Guardian Decision

- Status: warn. [EXPLICIT]
- Reason: grade is C and one dimension was not evaluated. [EXPLICIT]
