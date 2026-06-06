---
name: continuous-learning-primary
type: execution
version: 2.0.0
description: "Execute the Continuous Learning workflow with triad orchestration."
triad:
  lead: "continuous-learning-lead"
  support: "continuous-learning-support"
  guardian: "continuous-learning-guardian"
---

# Continuous Learning — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{source_event}}` | Debate, discovery, decision, or incident to learn from | Yes | User/session |
| `{{existing_insights}}` | Relevant entries from `insights/` | Yes | Workspace |
| `{{recurrence_evidence}}` | Prior occurrences of the ambiguity class | No | User/workspace |
| `{{output_format}}` | md or JSON learning report | No | Auto |

## Execution

1. Confirm the source event is learnable and has enough evidence.
2. Search existing insights before creating a new entry.
3. Extract direct answer, question refinements, and coverage gaps.
4. Produce insight candidates with domain, pattern, rationale, triggers, anchor, status, and evidence.
5. Block duplicate active insights; refine or supersede instead.
6. Propose amendments only when recurrence count is at least 3.
7. Validate JSON reports with `scripts/check.sh`.

## Output

- Continuous learning report in `{{output_format}}`
- Evidence tags on every claim
- Update plan for insights and optional ADR amendment
- Guardian decision
