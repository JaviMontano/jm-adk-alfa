# Example Output

# QA Report: acme-validator

**Reference Date**: 2026-06-06
**Plugin**: plugins/acme-validator
**Source Coverage**: partial [EXPLICIT]

## TL;DR

acme-validator has 1 critical and 1 warning across completed source runs. [EXPLICIT]
Structure passed with no findings. [EXPLICIT]
Priority: remove and rotate the hardcoded token in `hooks/post-install.sh:7`. [EXPLICIT]

## Summary Statistics

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| WARNING | 1 |
| INFO | 0 |

## Findings

| ID | Severity | Category | Component | Description | Recommendation |
|----|----------|----------|-----------|-------------|----------------|
| F-001 | CRITICAL | Security | hooks/post-install.sh:7 | Hardcoded token was reported by audit-security. [EXPLICIT] | Remove token, rotate credential, and load from environment. |
| F-002 | WARNING | Manifest | plugin.json | Missing description was reported by validate-manifest. [EXPLICIT] | Add a concise plugin description. |

## Recommendations

1. Remove and rotate the hardcoded token because credential exposure is the highest-impact finding. [EXPLICIT]
2. Add the missing plugin description because it affects discoverability and manifest quality. [EXPLICIT]

## Validation

- Summary counts match the findings table. [INFERRED]
- Content quality source is disclosed as missing, not silently omitted. [EXPLICIT]

## Risks

- The report does not verify whether upstream findings are correct; it aggregates supplied source runs. [SUPUESTO]
