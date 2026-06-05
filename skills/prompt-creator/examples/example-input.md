# Example Input

Create a deterministic handoff prompt for the `customer-onboarding` agent.

Sources available:

- `agents/customer-onboarding/agent.md`
- Existing prompts: none under `agents/customer-onboarding/prompts/`

Requirements:

- Source agent: `sales-intake`
- Target agent: `customer-onboarding`
- The handoff must pass task state, completed steps, and pending decision.
- The handoff must omit hidden reasoning, irrelevant chat history, and failed attempts without reusable evidence.
- The prompt must not execute the onboarding task.
