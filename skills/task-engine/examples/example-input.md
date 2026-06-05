# Example Input

Use DSVSR to decide whether we should rebuild the checkout flow around a new payment provider.

Context:

- The current checkout has intermittent payment failures.
- The new provider promises better fraud tooling.
- We have no provider API docs attached yet.
- Target confidence: 0.95.

Definition of done:

- Decompose into sub-problems.
- Score each sub-problem.
- Verify logic, facts, completeness, and bias.
- Compute global confidence.
- Name weakest assumptions before recommending next steps.
