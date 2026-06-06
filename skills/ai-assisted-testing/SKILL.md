---
name: ai-assisted-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  AI-generated test cases, fuzzing, mutation testing, coverage optimization. [EXPLICIT]
  Trigger: "ai assisted testing"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Ai Assisted Testing
> "Method over hacks."
## TL;DR
AI-generated test cases, fuzzing, mutation testing, coverage optimization. [EXPLICIT]

Use deterministic assets in `assets/` for test taxonomy, evidence, fuzzing, mutation, coverage, and report shape. When producing a JSON assisted testing plan, validate it offline with `bash skills/ai-assisted-testing/scripts/check.sh`. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather context and requirements
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
### Step 3: Execute
- Implement with evidence tags
### Step 4: Validate
- Verify quality criteria met
## Quality Criteria
- [ ] Every generated test has target, rationale, oracle, and evidence.
- [ ] Fuzzing proposals are bounded by domain, seed, iterations, timeout, and safety scope.
- [ ] Mutation testing includes baseline, operators, kill criteria, and surviving-mutant handling.
- [ ] Coverage plan names target files/modules and thresholds.
- [ ] Execution status distinguishes `proposed`, `generated`, and `executed`.
- [ ] JSON plan passes `scripts/check.sh` when produced.

## Usage

Example invocations:

- "/ai-assisted-testing" — Run the full ai assisted testing workflow
- "ai assisted testing on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
