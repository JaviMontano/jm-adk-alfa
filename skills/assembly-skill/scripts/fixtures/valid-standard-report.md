# Assembly Report

**Target Skill:** `sample-skill`
**Mode:** standard
**Result:** CERTIFIED
**Duration Source:** [EXPLICIT] operator-supplied elapsed bucket

## Phase Evidence

| Phase | Source | Status | Evidence |
|---|---|---|---|
| Phase A | x-ray-skill | pass | [EXPLICIT] scorecard average 5.8 and gate 9/13 |
| Gate A | mode-policy | pass | [EXPLICIT] standard selected because score < 7 |
| Phase B | surgeon-skill | pass | [EXPLICIT] Gate B approved intervention plan before edits |
| Gate B | user approval | pass | [EXPLICIT] user approved 3 interventions |
| Phase C | certify-skill | pass | [EXPLICIT] post-intervention score 8.4 and gate 13/13 |

## Before -> After

| Dimension | Before | After | Delta |
|---|---:|---:|---:|
| Average | 5.8 | 8.4 | +2.6 |
| Gate | 9/13 | 13/13 | +4 |

## Interventions Applied

- [EXPLICIT] Added assets manifest.
- [EXPLICIT] Replaced scaffold evals with deterministic cases.

## Certification

- **Verdict:** CERTIFIED
- **Formula Source:** [EXPLICIT] certify-skill gate 13/13 and score >= 8.

## Files Modified

| File | Action | Evidence |
|---|---|---|
| `skills/sample-skill/SKILL.md` | edited | [EXPLICIT] frontmatter and validation gate updated |
| `skills/sample-skill/evals/evals.json` | edited | [EXPLICIT] cases contract added |

## Next Steps

- [EXPLICIT] Open one PR for `sample-skill` only.
