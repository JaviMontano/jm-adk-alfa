---
name: step-creator
argument-hint: "step-name [workflow-name]"
description: 
  Generates individual workflow steps with all 12 mandatory fields as an internal helper.
  Invoked by workflow-creator and skill-spec-creator when they need to "create a step",
  "generate workflow steps", "build step definitions", "produce step specs",
  or "expand a workflow into detailed steps".
user-invocable: false
model: opus
context: fork
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Step Creator (Internal Helper)

Generate workflow steps with all 12 mandatory fields. Invoked by `workflow-creator` and `skill-spec-creator`, not directly by users.

## Assumptions

- **Assumes**: Called within the context of a parent workflow — step has access to workflow objective and surrounding steps
- **Limit**: Steps are linear (no branching) — alternative paths go in `recoveryAction` and `handoffIfNeeded`

## Input

Receives from calling skill:
- `stepNumber`: Position in workflow
- `title`: Short name (2-5 words)
- `workflowContext`: Parent workflow's objective and existing steps

## Output: 12 Fields

```yaml
- stepNumber: {N}
  title: "{2-5 words}"
  desc: "{1-2 sentences — what this step does and what it produces}"
  whyThisMatters: "{Business/technical rationale — NOT a restatement of title}"
  inputNeeded: "{Specific data with types: 'userMessage: string, agentId: string'}"
  actionInstruction: "{Concrete: 'Call security.sanitize(input), destructure {safe, cleaned, reason}'}"
  promptToUse: "{Full LLM prompt with {{placeholders}}, or 'null (mechanical step)'}"
  expectedOutput: "{What success produces: '{safe: true, cleaned: string}' or 'validated schema file at /output/schema.json'}"
  validationRule: "{Testable: 'result.safe === true OR reason logged to audit trail'}"
  failureSignal: "{Observable: 'sanitize() throws InvalidInputError', 'HTTP 500', 'timeout > 30s'}"
  recoveryAction: "{Concrete fallback: 'Strip to plaintext, retry — if still fails, reject with error message to user'}"
  handoffIfNeeded: "{agent-id for delegation, or 'null'}"
```

## Quality Bar (per field)

| Field | GOOD | BAD | Why It Matters |
|---|---|---|---|
| `whyThisMatters` | "Without input validation, injection attacks propagate to all downstream agents via shared memory" | "This step validates input" | Justifies the step's existence — helps decide if it's really needed |
| `actionInstruction` | "Call `loader.loadAgent(agentId)`, destructure response, verify `fields.length === 21`" | "Load the agent" | Enables implementation without interpretation |
| `validationRule` | "`response.fields.length === 21 AND fields.every(f => f.content.length > 0)`" | "Check it works" | Enables automated verification |
| `failureSignal` | "`loadAgent` throws `AgentNotFoundError` OR `fields.length < 21` (missing: `${21 - fields.length}` fields)" | "It fails" | Enables specific error handling |
| `recoveryAction` | "Load default agent template from `templates/default-agent.md`, log warning listing missing fields, continue with defaults" | "Try again" | Provides concrete alternative path |
| `promptToUse` | "Analyze {{input}} for compliance with {{standard}}.\nReturn: `{compliant: bool, issues: [{field, reason, severity}]}`" | "Check compliance" | Enables reproducible LLM steps |

## Edge Cases

- **Mechanical step** (no LLM): Set `promptToUse: "null (mechanical step)"` — still fill all other 11 fields
- **Step that always succeeds**: Still define `failureSignal` (infrastructure failures: timeout, out of memory, network error)
- **Step with multiple possible handoffs**: List the decision logic: "If severity=critical -> `security-agent`; if severity=medium -> `review-agent`; else continue"

---
**Author:** Javier Montaño | **Last updated:** 2026-03-18

## Usage

Example invocations:

- "/step-creator" — Run the full step creator workflow
- "step creator on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]
