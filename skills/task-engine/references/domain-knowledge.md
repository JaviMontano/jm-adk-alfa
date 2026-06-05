# Domain Knowledge — Task Engine

## DSVSR Heuristics

Use full DSVSR when the problem has at least two complexity signals, an explicit confidence target, or high-stakes consequences. Use fast path when the request is simple and the user did not ask for confidence calibration.

## Confidence Calibration

| Signal | Confidence impact |
|---|---|
| Direct evidence or mathematical proof | May support 0.95+ |
| Strong but incomplete evidence | Usually 0.85-0.94 |
| Inference without source documents | Usually 0.70-0.84 |
| Missing core input | Clarify instead of scoring |
| Missing expert capability | Apply confidence penalty and note expertise gap |

## Verification Checklist

- LOGIC: conclusion follows from premises.
- FACTS: factual claims have source or are tagged `[OPEN]`.
- COMPLETENESS: major dimensions are covered or named as gaps.
- BIAS: anchoring, confirmation, availability, and authority bias considered.

## Stop Conditions

Stop and disclose uncertainty when target confidence is unachievable, max reflection retries are reached, or the missing evidence cannot be retrieved in the current task.
