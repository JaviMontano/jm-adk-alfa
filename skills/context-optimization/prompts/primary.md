# Context Optimization Primary Prompt

## Objective

Build a deterministic context optimization report for the active task. The report must reduce context load without losing required evidence, handoff state, or active-skill focus.

## Required Inputs

- Active task and active skill or workflow.
- Available context budget and current utilization estimate.
- Candidate resources with relevance scores from 0.0 to 1.0.
- Required evidence, handoff, or session-state obligations.
- Allowed persistence target, if session state may be written.

## Process

1. Inventory candidate resources and classify each one as L1, L2, L3, or prune.
2. Permit at most one L3 resource unless the task explicitly names a second active focus.
3. Reject L3 loading when relevance is below `0.70`.
4. Propose pruning only when risk is `low`; convert higher-risk pruning to a missing-context warning.
5. Estimate naive tokens, optimized tokens, utilization percentage, and improvement percentage.
6. Persist only summarized session state when persistence is explicitly authorized.
7. Validate the machine-readable report against `assets/optimization-report-contract.json` and `scripts/check.sh`.

## Output

Return Markdown plus, when requested, JSON matching the optimization report contract. Include loading strategy, pruning actions, session-state updates, metrics, validation evidence, and residual risks.
