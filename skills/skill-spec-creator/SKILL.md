---
name: skill-spec-creator
description:  [EXPLICIT]
  This skill should be used when the user asks to "create a skill spec", "generate a [EXPLICIT]
  skill.yaml", "define skill workflows", "design an agentic capability", or mentions [EXPLICIT]
  skill specifications, workflow decomposition, agent capabilities, or YAML skill [EXPLICIT]
  definitions. Generates complete skill.yaml specifications with workflows, security, [EXPLICIT]
  observability, and failure handling for agentic ecosystems. Use this skill whenever [EXPLICIT]
  the user needs to define a structured capability for a multi-agent system, even if [EXPLICIT]
  they don't explicitly ask for "skill-spec-creator". [EXPLICIT]
argument-hint: skill-id owning-agent-id [EXPLICIT]
model: opus [EXPLICIT]
context: fork [EXPLICIT]
allowed-tools: Read, Write, Edit, Glob, Grep [EXPLICIT]
version: 1.0.0
---
 [EXPLICIT]
# Skill Spec Creator [EXPLICIT]
 [EXPLICIT]
Generate complete `skill.yaml` definitions — capability modules for agents in multi-agent ecosystems. Each spec defines inputs/outputs, security, observability, interoperability contracts, and minimum 4 workflows with full step decomposition. [EXPLICIT]
 [EXPLICIT]
> **Scope**: This creates YAML skill specifications for agentic frameworks (custom agent ecosystems). For Claude Code SKILL.md files, use `/skill-creator-moat`. [EXPLICIT]
 [EXPLICIT]
## Assumptions & Limits [EXPLICIT]
 [EXPLICIT]
- **Assumes** an agentic ecosystem with defined agents, tools, and security checkpoints [EXPLICIT]
- **Assumes** the owning agent's `agent.md` constitution exists (reads it for grounding) [EXPLICIT]
- **Limit**: YAML specs are design artifacts — they don't execute themselves (orchestrator interprets them) [EXPLICIT]
- **Limit**: Exactly 4 workflows minimum; fewer suggests the "skill" is actually a single operation, not a capability [EXPLICIT]
- **Trade-off**: More granular steps = better traceability but more maintenance; coarser steps = easier to maintain but harder to debug [EXPLICIT]
 [EXPLICIT]
## Usage [EXPLICIT]
 [EXPLICIT]
``` [EXPLICIT]
/skill-spec-creator text-analysis data-analyst [EXPLICIT]
/skill-spec-creator customer-onboarding          # interview mode [EXPLICIT]
``` [EXPLICIT]
 [EXPLICIT]
Parse `$1` as skill ID (kebab-case), `$2` as owning agent ID. If missing, ask: [EXPLICIT]
1. What capability does this skill provide? (1-2 sentences) [EXPLICIT]
2. Which agent owns it? (must exist in `agents/`) [EXPLICIT]
3. What does the user get? (business value, not implementation detail) [EXPLICIT]
 [EXPLICIT]
## Before Generating [EXPLICIT]
 [EXPLICIT]
1. **Read the agent**: `Read agents/$2/agent.md` — ground the skill in agent's mandate, tools, security policy [EXPLICIT]
2. **Check existing skills**: `Glob agents/$2/skills/*/skill.yaml` — avoid overlap [EXPLICIT]
3. **Read specs if available**: `Read references/skill-yaml-spec.md`, `Read references/workflow-spec.md`, `Read references/step-spec.md` [EXPLICIT]
 [EXPLICIT]
## Output Structure [EXPLICIT]
 [EXPLICIT]
Write to `agents/{agentId}/skills/{skillId}/skill.yaml`: [EXPLICIT]
 [EXPLICIT]
```yaml [EXPLICIT]
id: "{id}" [EXPLICIT]
name: skill-spec-creator
purpose: "{1-2 sentences — the WHY}" [EXPLICIT]
businessValue: "{User-facing value, not implementation detail}" [EXPLICIT]
triggerTypes: ["command", "event", "schedule", "delegation"]
owningAgent: "{agentId}"

inputs:
  - name: "{inputName}"
    type: "{string|number|object|array|file}"
    required: true
    description: "{what it is and why it's needed}"
    validation: "{format/range/pattern constraint}"

outputs:
  - name: "{outputName}"
    type: "{type}"
    format: "{JSON|Markdown|HTML|file}"
    description: "{what gets produced}"

dependencies:
  - "{runtime dependency}: {version constraint}"

toolUsage:
  - tool: "{tool_name}"
    purpose: "{why this skill needs this tool}"
    # Only tools from agent's Allowed Tools list

memoryReadsWrites:
  reads:
    - key: "{memory_key}"
      purpose: "{why it reads this}"
  writes:
    - key: "{memory_key}"
      trigger: "{when it writes}"
      retention: "{how long to keep}"

securityValidations:
  - checkpoint: "CP1"
    validates: "{what gets sanitized and how}"
  - checkpoint: "CP2"
    validates: "{prompt hardening rules}"
  - checkpoint: "CP3"
    validates: "{output validation rules}"

observabilityEvents:
  - event: "{skill_id}_started"
    data: "{what gets logged}"
  - event: "{skill_id}_completed"
    data: "{result summary}"
  - event: "{skill_id}_failed"
    data: "{error details}"

failureHandling:
  - mode: "{failure type}"
    detection: "{how to detect — observable signal}"
    impact: "{what breaks if unhandled}"
    recovery: "{concrete action, not 'retry'}"
    fallback: "{alternative path}"

interoperabilityContract:
  consumes:
    - from: "{skill_id}"
      artifact: "{what it receives}"
      format: "{expected format}"
  produces:
    - artifact: "{what it outputs}"
      format: "{format}"
      consumers: ["{skill_ids that use this}"]

wowCriteria:
  - "{EXCEPTIONAL quality — aspirational, differentiating}"
safeCriteria:
  - "{MINIMUM acceptable — the floor, non-negotiable}"

workflows:
  - id: "{workflow-id}"
    title: "{title}"
    objective: "{measurable outcome}"
    trigger: "{specific event or condition}"
    preconditions: ["{checkable conditions}"]
    inputs: ["{typed inputs}"]
    steps:
      - stepNumber: 1
        title: "{2-5 words}"
        desc: "{1-2 sentences}"
        whyThisMatters: "{business/technical rationale}"
        inputNeeded: "{specific data with types}"
        actionInstruction: "{concrete: call X, query Y, write Z}"
        promptToUse: "{full prompt or 'null (mechanical step)'}"
        expectedOutput: "{what success produces}"
        validationRule: "{testable assertion}"
        failureSignal: "{observable: HTTP 500, null, timeout}"
        recoveryAction: "{concrete fallback action}"
        handoffIfNeeded: "{agent-id or null}"
    mainOutput: "{primary deliverable}"
    secondaryOutputs: ["{logs, metrics, notifications}"]
    DoD: ["{verifiable done criteria}"]
    qaChecklist: ["{quality checks}"]
    raci:
      responsible: "{agent doing the work}"
      accountable: "{agent owning outcome}"
      consulted: "{agent providing input}"
      informed: "{agent notified of result}"
    kpis:
      - metric: "{name}"
        target: "{value}"
        unit: "{unit}"
    cadence: "{on-demand | daily | per-event}"
    errorHandling: "{unrecoverable error strategy}"
    fallbackRoute: "{alternative workflow}"
    escalationRoute: "{escalation target}"
```

## Quality Differentiation

### wowCriteria vs safeCriteria

| Aspect | safeCriteria (Floor) | wowCriteria (Ceiling) |
|---|---|---|
| Purpose | Minimum to not be rejected | What makes users say "this is excellent" |
| Example | "Output has all required fields" | "Output includes insights the user didn't ask for but needs" |
| Enforcement | Automated validation | Human/expert judgment |

## Workflow Design Principles

| Principle | Rule | Rationale |
|---|---|---|
| Minimum 4 workflows | Fewer = skill is too narrow; consider merging into another skill | Ensures the capability is substantial |
| 3-7 steps per workflow | Fewer = steps too coarse to debug; more = over-decomposed | Goldilocks granularity |
| Steps in execution order | No conditional branching in linear spec | Branches go in failureHandling/fallbackRoute |
| Each step self-contained | A step should make sense without reading adjacent steps | Enables parallel review |

## Edge Cases

- **Agent has no security checkpoints**: Create simplified securityValidations with input validation and output sanity checks
- **Skill has only 2-3 workflows**: Likely too narrow — consider: is there a diagnostic workflow? A rollback workflow? An edge-case workflow?
- **Multiple agents could own this skill**: The agent with the broadest mandate over this domain owns it; others consume via interoperabilityContract
- **Circular dependencies between skills**: Break with async events (skill A emits event → skill B subscribes) rather than direct consumption

## Validation Gate

- [ ] All top-level fields present and non-empty
- [ ] `businessValue` describes USER value, not system implementation
- [ ] `toolUsage` only lists tools from agent's Allowed Tools (in agent.md)
- [ ] `securityValidations` reference specific checkpoints with rules
- [ ] `wowCriteria` ≠ `safeCriteria` (aspirational vs minimum)
- [ ] ≥4 workflows, each with 3-7 steps
- [ ] Every step has all 12 fields, none empty or placeholder
- [ ] `observabilityEvents` use snake_case naming
- [ ] `failureHandling` has ≥3 modes with detection→recovery→fallback
- [ ] `interoperabilityContract` specifies concrete formats
- [ ] `inputs` have validation constraints

version: 1.0.0
---
**Author:** Javier Montano | **Last updated:** March 18, 2026
