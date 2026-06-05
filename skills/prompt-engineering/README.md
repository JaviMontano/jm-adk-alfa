# Prompt Engineering

Deterministic workflow for designing, auditing, and optimizing LLM instruction packages with source-grounded context, pattern selection, guardrails, and fixture-backed evaluation packets.

## Triggers

- prompt-engineering
- prompt engineering
- prompt design
- system instruction
- few-shot examples
- structured output prompt
- prompt audit
- prompt optimization
- injection-resistant prompt

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the deliverable is a prompt engineering packet: selected pattern, instruction package, guardrails, output contract, test cases, metrics, and risks. For durable prompt files, hand off to `prompt-creator`.

## Minimum Inputs

- Task the instruction package must accomplish
- Target model family or `model_unspecified`
- Source boundary and required context
- Output format or schema
- Safety and refusal boundary
- Success metrics or validation criteria

## Output Format

Markdown packet with decision, pattern selection, rejected alternatives, optimized instruction package, guardrails, output contract, test matrix, validation status, risks, and downstream handoff.

## Deterministic Gate

Validate JSON prompt engineering packets with:

```bash
bash skills/prompt-engineering/scripts/check.sh
python3 -B skills/prompt-engineering/scripts/validate_prompt_packet.py <packet.json>
```
