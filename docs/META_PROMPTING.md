# Meta Prompting

## Purpose

Meta-prompts improve prompts, evaluate prompt quality, or generate prompt systems. They are useful when a workflow repeats or needs consistent output across runtimes.

## Minimum Output

- Optimized prompt.
- Inputs and defaults.
- Anti-drift boundaries.
- Output contract.
- Acceptance criteria.
- Eval cases.
- Runtime notes.

## Safety

- Do not optimize prompts that request secrets, credential capture, unsafe automation, or unsupported runtime claims.
- Prefer placeholders over sensitive values.
- Keep provider-specific claims marked as validation pending unless verified.

## Promotion Rule

Manual flow first. If the same prompt pattern repeats three or more times with stable inputs and outputs, consider promoting it to a skill, command, or checklist.
