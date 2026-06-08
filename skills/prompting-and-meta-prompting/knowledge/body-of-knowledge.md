# Prompting And Meta Prompting Body of Knowledge

## Canon

A durable prompt system is a contract, not a clever paragraph. It names the objective, audience, available context, task sequence, constraints, output schema, anti-drift rules, missing-data behavior, acceptance criteria, eval cases, and Guardian decision logic.

## Prompt Components

- **Objective:** one concrete outcome. If the objective is plural, split or rank it.
- **Audience/runtime:** who consumes the output and where the prompt runs.
- **Context boundary:** what evidence the model may use and what must be marked missing.
- **Task sequence:** observable steps, not hidden chain-of-thought.
- **Output contract:** sections, fields, allowed decisions, and failure states.
- **Anti-drift:** explicit bans for summaries that replace findings, invented evidence, secret capture, hidden chain-of-thought, and unsafe automation.
- **Missing-data handling:** ask, mark `Dato requerido`, or defer validation; never fill gaps silently.

## Meta-Prompt Components

A meta-prompt evaluates future prompts against objective alignment, context sufficiency, output-contract completeness, safety boundaries, acceptance criteria, eval coverage, and evidence policy. It should not optimize for persuasion alone; it must reject prompts that cannot be verified.

## Quality Signals

| Signal | Target |
|---|---|
| Objective alignment | Prompt task and output contract serve the same outcome |
| Output verifiability | Required sections and fields are explicit |
| Acceptance criteria | Each criterion has an id and `verifiable=true` |
| Eval coverage | Happy path, minimal input, conflict, and false positive cases exist |
| Safety boundary | Secrets, hidden chain-of-thought, and unsafe automation are blocked |
| Drift resistance | Missing facts are marked instead of invented |

## Anti-Patterns

- Prompt only says "be helpful" or "be concise" without a task sequence or output contract.
- Meta-prompt grades style but ignores evidence, safety, eval coverage, or missing-data handling.
- Acceptance criteria are subjective, such as "sounds good", instead of verifiable.
- Evals only test happy path and explicit trigger.
- Prompt asks for hidden reasoning, credentials, or unverified claims.
