---
name: prompt-creator
description:  [EXPLICIT]
  Generates structured prompts for 9 prompt types in agentic ecosystems — meta, handoff, deliberation, [EXPLICIT]
  synthesis, validation, and fallback. Activates when the user says "create a prompt", "write a handoff prompt", [EXPLICIT]
  "generate a meta prompt", "build a committee deliberation prompt", or "make a fallback prompt". Also triggers [EXPLICIT]
  on mentions of prompt types, agent prompts, or multi-agent prompt design. Use this skill even if the user [EXPLICIT]
  only names the agent — it interviews for prompt type and context. [EXPLICIT]
argument-hint: prompt-type owning-agent-id [EXPLICIT]
model: opus [EXPLICIT]
context: fork [EXPLICIT]
allowed-tools: Read, Write, Edit, Glob, Grep [EXPLICIT]
---

# Prompt Creator

Generate structured prompt files for multi-agent ecosystems. Covers 9 prompt types from system prompts to committee deliberation to fallback recovery. [EXPLICIT]

## Assumptions & Limits

- **Assumes** an agentic ecosystem with defined agents (prompts reference agent constitutions)
- **Limit**: Prompts are templates, not runtime — placeholders (`{{var}}`) are filled by the orchestrator
- **Limit**: Committee prompts (deliberation/synthesis) require ≥3 agents to be meaningful
- **Trade-off**: More detailed prompts = more predictable agent behavior but less adaptability. For creative tasks, keep prompts loose.

## Usage

```
/prompt-creator meta_prompt data-analyst
/prompt-creator handoff_prompt customer-onboarding
/prompt-creator committee_deliberation                # interview mode
```

Parse `$1` as prompt type, `$2` as owning agent ID. If missing, ask. [EXPLICIT]

## Before Generating

1. **Read the agent**: `Read agents/$2/agent.md` — ground prompt in agent identity, tone, and constraints
2. **Check existing prompts**: `Glob agents/$2/prompts/*.md` — avoid duplicates
3. **Read prompt spec**: `Read references/prompt-types-spec.md` if available

## The 9 Types

| # | Type | File Pattern | Purpose | Complexity |
|---|---|---|---|---|
| 1 | `agent_system_prompt` | `agent.md` | Full constitution | → Use `/agent-constitution-creator` |
| 2 | `meta_prompt` | `prompts/meta-{topic}.md` | Behavioral instruction for ONE aspect | Low |
| 3 | `system_user_pair` | `prompts/pair-{scenario}.md` | Reusable system+user template | Low |
| 4 | `workflow_step_prompt` | Inline in skill.yaml | Step-level LLM instruction | → Use `/workflow-creator` |
| 5 | `handoff_prompt` | `prompts/handoff.md` | Task transfer protocol | Medium |
| 6 | `committee_deliberation` | `prompts/deliberation.md` | Independent multi-agent evaluation | High |
| 7 | `committee_synthesis` | `prompts/synthesis.md` | Merge multiple agent responses | High |
| 8 | `validation_prompt` | `prompts/validation.md` | Quality validation of outputs | Medium |
| 9 | `fallback_prompt` | `prompts/fallback.md` | Recovery when primary fails | Medium |

Types 1 and 4 redirect to specialized skills — this skill handles types 2, 3, 5-9. [EXPLICIT]

## Output Format

Write to `agents/{agentId}/prompts/{filename}.md`: [EXPLICIT]

```markdown
---
type: "{promptType}"
owningAgent: "{agentId}"
sourceAgentMd: "agents/{agentId}/agent.md"
version: "1.0.0"
---

# {Title}

{Content per type-specific rules below}
```

## Type-Specific Rules

### meta_prompt — Behavioral aspect instruction
- **Focus**: Exactly ONE aspect: reasoning OR formatting OR restrictions OR style
- **Structure**: Preamble (agent identity) → Framework (the rules) → Constraints (boundaries)
- **Anti-pattern**: Combining reasoning + formatting in one meta_prompt → split into two

```markdown
# Reasoning Meta-Prompt

You are {{agent.name}}. Your role: {{agent.role}}. [EXPLICIT]

## Framework
1. {Step 1 of reasoning process}
2. {Step 2}

## Constraints
- {Hard limit 1}
- {Hard limit 2}
```

### system_user_pair — Reusable scenario template
- **Must have**: `## System` and `## User` sections
- **System**: Sets context, constraints, output format
- **User**: Scenario template with `{{placeholders}}`
- **Design rule**: Each pair handles ONE scenario (not a Swiss Army knife)

### handoff_prompt — Task transfer protocol
- **Must specify**:
  - Context to PASS: task state, progress, relevant data
  - Context to OMIT: internal reasoning, failed attempts, irrelevant history
  - Target agent: explicit ID
  - Success criteria: how target agent knows it's done
- **Anti-pattern**: Passing the entire conversation (context explosion)

### committee_deliberation — Independent evaluation
- **Must require**: Agent gives INDEPENDENT opinion FIRST, before seeing others
- **Must include**: Scoring rubric with weighted dimensions
- **Must specify**: Output format for structured comparison
- **Key insight**: The value of committees comes from independent evaluation — if agents see each other's work first, they converge prematurely

### committee_synthesis — Multi-response merger
- **Must define**: Redundancy removal strategy, conflict resolution method, confidence weighting
- **Merge strategies**:
  - Majority vote (for binary decisions)
  - Weighted average (for numeric assessments)
  - Reasoned selection (for qualitative choices — requires justification)

### validation_prompt — Quality checker
- **Must define**: Pass/fail criteria with severity levels (critical/major/minor)
- **Must produce**: Actionable feedback (not "this could be better" but "section 3 missing required field X")
- **Must reference**: The DoD/qaChecklist from the originating workflow

### fallback_prompt — Recovery playbook
- **Must define**: Trigger conditions (when does fallback activate?)
- **Must specify**: Preservation priorities (what to save vs sacrifice)
- **Must include**: User communication template (how to explain the degradation)
- **Must have**: Escalation path if fallback also fails

## Example: Good vs Bad

**Bad handoff_prompt:**
```
Hand off the task to the next agent. [EXPLICIT]
```

**Good handoff_prompt:**
```markdown
## Handoff Protocol: {{source_agent}} → {{target_agent}}

### Context to Pass
- Task ID: {{task_id}}
- Current state: {{state_summary}}
- Completed steps: {{completed_steps}}
- Pending decision: {{decision_needed}}

### Context to Omit
- Internal reasoning chains
- Failed approaches and why they failed
- Intermediate calculations

### Success Criteria
The handoff is complete when {{target_agent}} confirms: [EXPLICIT]
- [ ] Context received and understood
- [ ] Can proceed without clarification
- [ ] Estimated completion: {{time_estimate}}
```

## Validation Gate

- [ ] YAML frontmatter has type, owningAgent, sourceAgentMd, version
- [ ] Type is one of the 9 defined types (or redirects to appropriate skill)
- [ ] Agent.md was read and prompt references agent identity
- [ ] Type-specific rules followed (see table above)
- [ ] No empty sections
- [ ] All `{{placeholders}}` are named descriptively (not `{{x}}`)
- [ ] Committee prompts require independent evaluation before comparison
- [ ] Handoff prompts specify both what to pass AND what to omit
- [ ] Validation prompts include severity levels
- [ ] Fallback prompts include escalation path

---
**Author:** Javier Montaño | **Last updated:** March 12, 2026

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
