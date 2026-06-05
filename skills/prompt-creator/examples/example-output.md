# Example Output

## Decision

- [CÓDIGO] Decision: `write_prompt`.
- [CÓDIGO] Prompt type: `handoff_prompt`.
- [CÓDIGO] Target path: `agents/customer-onboarding/prompts/handoff.md`.
- [CONFIG] Next action: write the prompt artifact and validate it with `scripts/validate_prompt_artifact.py`.

## Prompt Artifact

```markdown
---
type: "handoff_prompt"
owningAgent: "customer-onboarding"
sourceAgentMd: "agents/customer-onboarding/agent.md"
version: "1.0.0"
createdBy: "prompt-creator"
validationStatus: "validated"
---

# Customer Onboarding Handoff Prompt

## Purpose
Transfer a bounded onboarding task from {{source_agent_id}} to {{target_agent_id}}.

## Inputs
- {{task_id}}
- {{state_summary}}
- {{completed_steps}}
- {{decision_needed}}

## Context to Pass
- Current state: {{state_summary}}
- Completed steps: {{completed_steps}}
- Pending decision: {{decision_needed}}

## Context to Omit
- Hidden reasoning
- Irrelevant chat history
- Failed attempts without reusable evidence

## Procedure
1. Confirm the target agent owns the next action.
2. Send only the bounded context.
3. Ask for acknowledgement before execution.

## Output Contract
Return task id, target agent id, accepted context, omitted context, and next action.

## Success Criteria
- Target agent confirms enough context to proceed.
- No hidden reasoning is transferred.

## Validation Gate
- Required frontmatter is present.
- Pass and omit lists are both non-empty.

## Failure Handling
If target ownership is unclear, return `ask` with the missing ownership fact.

## Downstream Boundary
This prompt transfers context only; it does not perform the customer onboarding task.
```

## Sources

- [CÓDIGO] `agents/customer-onboarding/agent.md` inspected.
- [CÓDIGO] Existing prompt paths checked.
- [CONFIG] `assets/prompt-contract-checklist.md` applied.

## Validation

- [CÓDIGO] `scripts/validate_prompt_artifact.py` accepts the artifact shape.
- [CONFIG] Placeholders are descriptive snake_case.
- [CONFIG] Downstream task is not executed.
