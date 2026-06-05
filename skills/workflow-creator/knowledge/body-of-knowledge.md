# Workflow Creator Body Of Knowledge

## Canon

Workflow Creator turns an agentic procedure into a deterministic workflow
definition. The canonical output is a 17-field workflow object with 3-7 ordered
steps. Each step has 12 traceability fields so another agent can execute,
validate, recover, and hand off without guessing.

## Deterministic Contract

- A workflow is valid only when every top-level field in
  `assets/workflow-definition-contract.json` is present.
- Step numbers are sequential and each step has an observable
  `validationRule`, `failureSignal`, and `recoveryAction`.
- RACI values must name concrete agents or human roles.
- KPIs require target, unit, and measurement method.
- Missing catalog context is marked `[OPEN]`; it is never invented.
- Network lookup is off by default and requires explicit user request.

## Quality Metrics

| Metric | Target | How To Measure |
|---|---:|---|
| Top-level field completeness | 100% | Validator confirms all 17 fields |
| Step field completeness | 100% | Validator confirms all 12 fields per step |
| Step count | 3-7 | Validator counts `steps` |
| RACI concreteness | 100% | No anonymous roles from blocked phrase list |
| KPI measurability | 100% | All KPIs have target, allowed unit, and measurement |
| Local validation | Pass | `bash skills/workflow-creator/scripts/check.sh` |

## Anti-Patterns

| Anti-pattern | Failure | Correction |
|---|---|---|
| One-step workflow | No handoff or verification boundary | Split into prepare, execute, verify |
| Vague trigger | Cannot know when to start | Name command, event, request, or condition |
| Anonymous RACI | Accountability cannot be audited | Name agent ID or human role |
| Generic recovery | Cannot fail closed | Use stop, retry, rerun, ask, fallback, escalate, patch, or log |
| Hidden branch | Linear workflow becomes ambiguous | Move alternatives to fallback or sub-workflow |
