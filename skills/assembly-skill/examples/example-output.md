# Example Output

```markdown
# Assembly Report

**Target Skill:** `skills/output-contract-enforcer`
**Mode:** standard
**Result:** CERTIFIED
**Duration Source:** [EXPLICIT] operator-supplied elapsed bucket

## Phase Evidence

| Phase | Source | Status | Evidence |
|---|---|---|---|
| Phase A | x-ray-skill | pass | [EXPLICIT] scorecard average 6.2 and gate 10/13 |
| Gate A | mode-policy | pass | [EXPLICIT] standard selected because score >= 5 and score < 7 |
| Phase B | surgeon-skill | pass | [EXPLICIT] Gate B approved before edits |
| Gate B | user approval | pass | [EXPLICIT] user approved asset/eval/script fixes |
| Phase C | certify-skill | pass | [EXPLICIT] post-intervention score 8.3 and gate 13/13 |

## Before -> After

| Dimension | Before | After | Delta |
|---|---:|---:|---:|
| Average | 6.2 | 8.3 | +2.1 |
| Gate | 10/13 | 13/13 | +3 |

## Interventions Applied

- [EXPLICIT] Added missing asset manifest.
- [EXPLICIT] Converted evals to cases with deterministic checks.

## Certification

- **Verdict:** CERTIFIED
- **Formula Source:** [EXPLICIT] certify-skill gate 13/13 and score >= 8.

## Files Modified

| File | Action | Evidence |
|---|---|---|
| `skills/output-contract-enforcer/evals/evals.json` | edited | [EXPLICIT] cases contract added |
| `skills/output-contract-enforcer/assets/manifest.json` | added | [EXPLICIT] asset map created |

## Next Steps

- [EXPLICIT] Open one PR for `output-contract-enforcer` only.
```
