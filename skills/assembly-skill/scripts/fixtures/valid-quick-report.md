# Assembly Report

**Target Skill:** `sample-skill`
**Mode:** quick
**Result:** DIAGNOSTIC
**Duration Source:** [EXPLICIT] operator-supplied elapsed bucket

## Phase Evidence

| Phase | Source | Status | Evidence |
|---|---|---|---|
| Phase A | x-ray-skill | pass | [EXPLICIT] scorecard average 8.6 and gate 13/13 |
| Gate A | mode-policy | pass | [EXPLICIT] quick selected because score >= 8 and gate passed |
| Phase D | assembly report | pass | [EXPLICIT] diagnostic-only report emitted |

## Before -> After

| Dimension | Before | After | Delta |
|---|---:|---:|---:|
| Average | 8.6 | 8.6 | 0 |
| Gate | 13/13 | 13/13 | 0 |

## Interventions Applied

- [EXPLICIT] No interventions applied.

## Certification

- **Verdict:** DIAGNOSTIC
- **Formula Source:** [EXPLICIT] quick mode does not certify or modify files.

## Files Modified

| File | Action | Evidence |
|---|---|---|
| No files modified | none | [EXPLICIT] quick mode is read-only |

## Next Steps

- [EXPLICIT] No PR is required unless the user requests changes.
