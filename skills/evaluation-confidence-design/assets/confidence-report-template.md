# Evaluation Confidence Design Report: {evaluator}

## Summary

- Labeled set: `{totalExamples}` examples.
- Stratification: `{stratificationField}` with `{strataNames}`.
- Calibration method: `{calibrationMethod}`.
- Decision threshold: `{threshold}` on `{thresholdOn}`.
- Disabled categories: `{disabledCategories}`.

## Sampling

{samplingMarkdown}

## Calibration Map

{calibrationMarkdown}

## Category Criteria

{categoryMarkdown}

## Metrics

- Aggregate accuracy is secondary: `{reportAggregateAccuracy}`.
- Report by stratum: `{reportByStratum}`.
- Report FP by category: `{reportFpByCategory}`.

## Validation

- Threshold uses calibrated confidence, not raw model confidence.
- Labeled set is present and stratified.
- Each category has positive and negative examples by severity.
- FP rate is reported per category.
- High-FP categories can be disabled temporarily.

## Risks

{risksMarkdown}
