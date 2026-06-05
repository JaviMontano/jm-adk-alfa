# Benchmark Report: example-skill

**Compared:** `skills/example-skill-before` vs `skills/example-skill-after`
**Mode:** version comparison
**Net Assessment:** IMPROVED

## Summary

| Metric | State A | State B | Delta |
|---|---:|---:|---:|
| Average score | 7.1 | 8.3 | +1.2 |
| Gate pass count | 8/13 | 13/13 | +5 |
| Dimensions improved | - | 8 | - |
| Dimensions regressed | - | 0 | - |
| Gate regressions | - | 0 | - |

## Inventory

| Metric | State A | State B | Delta |
|---|---:|---:|---:|
| Files | 15 | 28 | +13 |
| Lines | 420 | 690 | +270 |
| Evals | 7 | 10 | +3 |
| Assets | 0 | 4 | +4 |
| Scripts | 0 | 2 | +2 |

## Dimension-by-Dimension

| Dimension | A | B | Delta | Direction | Evidence |
|---|---:|---:|---:|---|---|
| Foundation | 7 | 8 | +1 | Better | [CÓDIGO] Activation and assumptions became explicit. |
| Truthfulness | 7 | 8 | +1 | Better | [CÓDIGO] Missing catalog context is now marked open. |
| Quality | 7 | 8 | +1 | Better | [CÓDIGO] Output contract and validation gate were added. |
| Density | 8 | 8 | 0 | Same | [INFERENCIA] Added detail replaced scaffold filler. |
| Simplicity | 8 | 8 | 0 | Same | [CÓDIGO] The process remains one linear scoring flow. |
| Clarity | 7 | 9 | +2 | Better | [CÓDIGO] Labels and report sections are exact. |
| Precision | 7 | 9 | +2 | Better | [CÓDIGO] Numeric deltas and policy-backed labels were added. |
| Depth | 6 | 8 | +2 | Better | [CÓDIGO] Missing baseline and transformed cases were added. |
| Coherence | 7 | 9 | +2 | Better | [CÓDIGO] Agents, prompts, evals, assets, and scripts align. |
| Value | 7 | 8 | +1 | Better | [CÓDIGO] Script checks make the report reproducible. |

## Gate Changes

| Gate | A | B | Change | Evidence |
|---|---|---|---|---|
| assets_manifest | FAIL | PASS | Fixed | [CÓDIGO] `assets/manifest.json` was added. |
| eval_cases | FAIL | PASS | Fixed | [CÓDIGO] Evals now use `cases`. |
| examples_specific | FAIL | PASS | Fixed | [CÓDIGO] Scaffold examples were replaced. |
| agent_prompt_alignment | FAIL | PASS | Fixed | [CÓDIGO] Read-only agent tools now match the skill. |
| template_offline | FAIL | PASS | Fixed | [CÓDIGO] Live font dependency was removed. |

## Regressions

| Dimension or Gate | Change | Cause | Severity | Trade-off |
|---|---|---|---|---|
| none | 0 | [CÓDIGO] No lower score or gate regression observed. | none | false |

## Top Improvements

| Dimension or Gate | Change | Driver | Genuine |
|---|---|---|---|
| clarity | +2 | [CÓDIGO] Report sections and labels became explicit. | true |
| precision | +2 | [CÓDIGO] Numeric delta and assessment policy were added. | true |
| depth | +2 | [CÓDIGO] Missing baseline and transformed-state handling were added. | true |

## Trade-Offs

| Dimension | Change | Driver | Accepted |
|---|---|---|---|
| density | 0 | [INFERENCIA] Extra contract detail replaced scaffold filler. | true |

## Recommendation

[CONFIG] Merge after Quality Gates pass because no regressions remain and all
previous gate gaps were fixed.

## Caveats

- [INFERENCIA] Structural benchmarking does not prove runtime behavior.
- [CONFIG] Use evals or task-level test transcripts to compare behavior beyond
  skill structure.
