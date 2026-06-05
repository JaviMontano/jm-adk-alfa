---
name: prompt-engineering-audit
type: variation
audience: reviewer
description: "Audit an existing prompt for quality, safety, and effectiveness."
---
# Prompt Audit Checklist

Review the prompt against these criteria:

## Structure
- [ ] Has clear role definition
- [ ] Context is relevant and complete
- [ ] Task is specific and unambiguous
- [ ] Output format is explicitly specified

## Safety
- [ ] Resistant to injection ("ignore previous instructions")
- [ ] Handles adversarial input gracefully
- [ ] No leaked system prompt content
- [ ] Refusal patterns for out-of-scope requests

## Quality
- [ ] Tested with at least three deterministic inputs
- [ ] Consistent output format across runs
- [ ] Accuracy >= 90% on test cases
- [ ] Token-efficient (prompt:output ratio < 3:1)

## Deterministic Evidence
- [ ] Source facts are path-backed or marked as gaps
- [ ] Hidden reasoning is not requested or exposed
- [ ] Output contract and refusal policy are explicit
