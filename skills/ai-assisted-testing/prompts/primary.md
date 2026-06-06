---
name: ai-assisted-testing-primary
type: execution
version: 2.0.0
description: "Execute the AI Assisted Testing workflow with triad orchestration."
triad:
  lead: "ai-assisted-testing-lead"
  support: "ai-assisted-testing-support"
  guardian: "ai-assisted-testing-guardian"
---

# AI Assisted Testing — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{target}}` | Code, API, workflow, or module to test | Yes | User/workspace |
| `{{evidence}}` | Requirements, code, examples, defects, coverage | Yes | User/workspace |
| `{{constraints}}` | Safety, runtime, language, framework limits | No | User/workspace |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. Load assets and knowledge.
2. Inventory evidence and current test/coverage state.
3. Generate candidate tests with target, rationale, oracle, and evidence.
4. Bound fuzzing and mutation testing.
5. Separate proposed/generated/executed status.
6. Validate JSON plan with `scripts/check.sh` when present.

## Output

- Test plan with evidence-backed candidate tests.
- Coverage, fuzzing, mutation, and regression sections.
- Validation status and residual risks.
