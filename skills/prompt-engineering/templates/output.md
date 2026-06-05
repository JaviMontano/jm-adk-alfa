# Prompt Engineering Output

## Decision

- Decision: write_packet / ask / handoff / decline
- Pattern:
- Target model:
- Source boundary:
- Downstream handoff:

## Sources

| Source | Status | Evidence |
|---|---|---|
| task context | provided / missing |  |
| source material | inspected / missing |  |
| pattern matrix | applied | `assets/pattern-decision-matrix.json` |

## Pattern Selection

| Candidate | Fit | Risks | Decision |
|---|---|---|---|
|  |  |  |  |

## Instruction Package

```text
Role:
Context:
Task:
Constraints:
Output Contract:
Examples:
Guardrails:
```

## Test Matrix

| ID | Type | Input | Expected Checks |
|---|---|---|---|
| PE-001 | happy_path |  |  |
| PE-002 | edge_case |  |  |
| PE-003 | adversarial |  |  |

## Validation

- `assets/prompt-engineering-checklist.md` applied:
- `scripts/validate_prompt_packet.py` pass/fail:
- Injection resistance:
- Format compliance:
- Coverage gaps:

## Risks and Limits

- Source gaps:
- Model-specific uncertainty:
- Downstream assumptions:
