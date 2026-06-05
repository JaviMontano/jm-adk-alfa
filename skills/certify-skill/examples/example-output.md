# Certification Report: example-onboarding

| Field | Value |
|---|---|
| Certification | CONDITIONAL |
| Overall Score | 8.0/10 |
| Structural | 8/9 pass |
| Content | 18/18 pass |
| Systemic | PASS |
| MOAT | SKIPPED |

## Rubric Scores

| # | Criterion | Score | Evidence |
|---:|---|---:|---|
| 1 | Foundation | 8 | [DOC] Rules include rationale. |
| 2 | Truthfulness | 8 | [CODE] Claims cite files or are tagged. |
| 3 | Quality | 8 | [CODE] Headings and references are consistent. |
| 4 | Density | 8 | [CODE] No duplicated reference paragraphs found. |
| 5 | Simplicity | 8 | [DOC] Instructions are direct and bounded. |
| 6 | Clarity | 8 | [DOC] Terms are defined before use. |
| 7 | Precision | 8 | [DOC] Thresholds are numeric. |
| 8 | Depth | 8 | [DOC] Edge cases and failure modes exist. |
| 9 | Coherence | 8 | [CODE] Key terms match across files. |
| 10 | Value | 8 | [DOC] Each section supports certification decisions. |
| | Average | 8.0 | [CONFIG] Formula-derived. |

## Structural Checks

| Check | Result | Evidence |
|---|---|---|
| S1-S5 | PASS | [CODE] SKILL.md exists, frontmatter parses, and description is valid. |
| S6 | FAIL | [CODE] `references/patterns.md` is referenced but missing. |
| S7-S9 | PASS | [CODE] No orphan files, eval JSON parses, and no stale singular paths remain. |

## Blockers

| Issue | Fix Required | Estimated Effort |
|---|---|---|
| [CODE] Missing referenced file. | Create `references/patterns.md` or remove the reference. | 30 minutes |

## Recommendation

[CONFIG] Fix 1 blocker, then re-certify. Do not mark CERTIFIED until S6 passes.
