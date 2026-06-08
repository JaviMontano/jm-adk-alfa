---
name: prompting-and-meta-prompting
version: 1.0.0
description: "Transform intentions into durable prompts, meta-prompts, acceptance criteria, and eval-ready prompt systems."
owner: "JM Labs"
triggers:
  - prompting
  - meta-prompting
  - prompt-optimizer
  - system-prompt
  - prompt-design
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Prompting And Meta Prompting

## When To Use

- User wants a prompt, system prompt, meta-prompt, reusable instruction, or prompt evaluation.
- A repeated workflow should become a skill, command, checklist, or eval.
- A weak prompt needs objective, context, constraints, output shape, and anti-drift rules.

## When Not To Use

- The user needs direct execution and the prompt is not the deliverable.
- The request depends on recent facts that have not been verified.
- The prompt would ask for secrets or bypass safety controls.

## Inputs

- Objective and audience.
- Runtime/model target if known.
- Constraints, allowed tools, privacy boundaries, and definition of done.
- Examples or counterexamples when available.

## Outputs

- Optimized prompt or meta-prompt.
- Acceptance criteria and output shape.
- Eval cases when behavior changes.
- Safety notes and assumptions.

## Workflow

1. Discover: extract goal, context, constraints, missing data, and done criteria.
2. Analyze: select prompt pattern and failure modes.
3. Execute: produce prompt with role, situation, task, sequence, constraints, and output contract.
4. Validate: check ambiguity, safety, evidence, and eval coverage.

## Deterministic Assets

- Use `assets/prompting-and-meta-prompting-contract.json` when the output must be machine-checkable.
- Use `assets/prompt-component-policy.json` to require objective, audience, context, constraints, sequence, output contract, anti-drift rules, and missing-data handling.
- Use `assets/meta-prompt-policy.json` when the deliverable reviews or improves future prompts.
- Use `assets/acceptance-criteria-policy.json` and `assets/eval-case-policy.json` to make quality gates verifiable.
- Use `assets/safety-anti-drift-policy.json` to reject credential capture, hidden chain-of-thought requests, unsafe automation, and unverifiable outputs.

## Offline Validation

When a JSON prompt-system report is produced, validate it with:

```bash
bash skills/prompting-and-meta-prompting/scripts/check.sh
```

The validator checks the required prompt contract, meta-prompt review dimensions, verifiable acceptance criteria, edge-case eval coverage, safety boundaries, and Guardian decision consistency.

## Safety Limits

- Do not expose hidden chain-of-thought.
- Do not optimize prompts for credential capture or unsafe automation.
- Mark missing facts as `Dato requerido` or validation pending.

## Success Criteria

- Prompt is executable in one pass when inputs are present.
- Output shape is explicit.
- Anti-drift and safety constraints are included.
- Evals cover happy path, minimal input, conflicting requirements, and false positives.

## Fallback

If the target runtime is unknown, produce a Markdown-first prompt with portable placeholders.

## Examples

- Convert a vague request into a SPEC prompt.
- Create a meta-prompt that reviews future prompts for evidence, constraints, and acceptance criteria.
