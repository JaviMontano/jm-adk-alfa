---
name: workflow-creator
description: 
  Generates complete workflow definitions with steps, DoD, RACI, KPIs, and failure handling for agentic ecosystems. [EXPLICIT]
  Use when the user asks to "create a workflow", "define workflow steps", "build a workflow YAML",
  "generate a workflow spec", or mentions workflow definition, step-by-step procedure, or RACI matrix. [EXPLICIT]
argument-hint: workflow-id [owning-skill-id]
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Workflow Creator

Generate complete workflow definitions — sequential step-by-step operational procedures for agent skills. Each workflow has 17 fields including steps (12 fields each), RACI, KPIs, and failure routes. [EXPLICIT]

## Assumptions & Limits

- **Assumes** workflows belong to a skill within an agent ecosystem (standalone workflows → consider a simpler checklist or runbook)
- **Limit**: Linear execution only — no branching/conditionals in the step sequence (use failureHandling/fallbackRoute for alternative paths)
- **Limit**: Each step assumes the previous completed successfully (guard with preconditions and validationRules)
- **Trade-off**: More steps = better traceability and debugging; fewer steps = easier maintenance. Sweet spot: 3-7 steps.

## Usage

```
/workflow-creator user-onboarding customer-management
/workflow-creator incident-response                     # interview for context
```

Parse `$1` as workflow ID (kebab-case), `$2` as owning skill. If `$2` absent, ask. [EXPLICIT]

## Before Generating

1. **Read skill spec**: If `$2` provided, find and read the skill.yaml for context, inputs/outputs, and tools
2. **Read step spec**: `Read references/step-spec.md` if available
3. **Check existing workflows**: Avoid duplicating workflows within the same skill

## Output: 17-Field Workflow

```yaml
- id: "{id}"
  title: "{Human-readable title}"
  objective: "{Measurable outcome — not 'handle X' but 'process X producing Y within Z'}"
  trigger: "{Specific event, condition, or command — not 'when needed'}"
  preconditions:
    - "{Checkable condition BEFORE starting — not aspirational}"
  inputs:
    - name: "{name}"
      type: "{type}"
      required: true
      description: "{what and why}"
  steps:
    - stepNumber: 1
      title: "{2-5 words}"
      desc: "{1-2 sentences}"
      whyThisMatters: "{Why skipping this would break the workflow}"
      inputNeeded: "{Specific data with types}"
      actionInstruction: "{Concrete: 'Call api.validate(input), check status === 200'}"
      promptToUse: "{Full LLM prompt text, or 'null (mechanical step)'}"
      expectedOutput: "{What success produces — format and content}"
      validationRule: "{Testable: 'response.status === 200 AND body.id exists'}"
      failureSignal: "{Observable: 'HTTP 500', 'field X null', 'timeout > 30s'}"
      recoveryAction: "{Concrete: 'Load from cache, log warning, continue with defaults'}"
      handoffIfNeeded: "{agent-id or null}"
  mainOutput: "{Primary deliverable with format}"
  secondaryOutputs:
    - "{logs, metrics, notifications, state changes}"
  DoD:
    - "{Verifiable: 'Response sent AND log entry created AND memory updated'}"
  qaChecklist:
    - "{Specific check: 'Output schema validates against spec v2.1'}"
  raci:
    responsible: "{agent that does the work}"
    accountable: "{agent that owns the outcome}"
    consulted: "{agent that provides input — or 'none'}"
    informed: "{agent notified — or 'none'}"
  kpis:
    - metric: "{name}"
      target: "{value}"
      unit: "{seconds|percentage|count|ratio}"
      measurement: "{how to measure}"
  cadence: "{on-demand | hourly | daily | per-event | per-request}"
  errorHandling: "{Unrecoverable error strategy: log + escalate + graceful degradation}"
  fallbackRoute: "{Alternative workflow ID or 'direct-response'}"
  escalationRoute: "{agent-id or human role to escalate to}"
```

## Step Quality Standards

The 12 fields per step are the atomic unit of traceability. Each must meet this bar: [EXPLICIT]

| Field | GOOD (specific, testable) | BAD (vague, untestable) |
|---|---|---|
| `whyThisMatters` | "Without sanitization, injection attacks propagate to downstream agents" | "This step cleans the input" |
| `actionInstruction` | "Call `security.sanitize(input)` — returns `{safe, cleaned, reason}`" | "Sanitize the input" |
| `validationRule` | "`result.safe === true` OR `result.reason` logged and workflow continues" | "Input is clean" |
| `failureSignal` | "`sanitize()` throws `InvalidInputError` OR returns `{safe: false}` with reason matching `/injection/i`" | "It fails" |
| `recoveryAction` | "Log warning with `reason`, strip input to plaintext, retry sanitization — if still unsafe, reject with user-facing error" | "Try again" |
| `promptToUse` | "Analyze the following text for {{domain}} compliance:\n```\n{{input}}\n```\nReturn: {compliant: bool, issues: string[], severity: 'low'\|'medium'\|'high'}" | "Check the text" |

## Design Decisions

### How many steps?

| Steps | Indicates | Action |
|---|---|---|
| 1-2 | Too coarse — likely a single operation, not a workflow | Decompose or merge into parent workflow |
| 3-5 | Ideal for most workflows | Proceed |
| 6-7 | Complex but manageable | Ensure each step is truly distinct |
| 8+ | Over-decomposed | Merge related steps or split into sub-workflows |

### DoD vs QA Checklist

| DoD | QA Checklist |
|---|---|
| "Is it done?" | "Is it done well?" |
| Binary pass/fail | Graduated quality |
| Blocks completion | Flags for improvement |

## Edge Cases

- **Step depends on external service**: Add explicit timeout in `actionInstruction` and timeout-specific `failureSignal`
- **Step has conditional logic**: Keep the step linear; put the condition in `validationRule` and branches in `recoveryAction`/`handoffIfNeeded`
- **Workflow spans multiple agents**: Each agent's portion is a separate workflow; connect via `handoffIfNeeded` and `interoperabilityContract` in skill.yaml
- **No meaningful KPIs**: At minimum measure: execution time, success rate, error rate

## Validation Gate

- [ ] All 17 top-level fields present
- [ ] `objective` is measurable (includes expected outcome)
- [ ] `trigger` is a specific event/condition (not "when needed")
- [ ] `preconditions` are checkable before workflow starts
- [ ] 3-7 steps, each with all 12 fields non-empty
- [ ] No step's `whyThisMatters` is a restatement of its `title`
- [ ] `DoD` items are verifiable assertions
- [ ] `raci` names actual agents from ecosystem
- [ ] `kpis` include units of measurement
- [ ] `fallbackRoute` names a concrete alternative
- [ ] `escalationRoute` names a specific target

---
**Author:** Javier Montano | **Last updated:** 2026-03-12
