---
name: prompt-creator
version: 1.0.0
description: Generates deterministic prompt files for agentic ecosystems using the canonical prompt-type matrix, including meta prompts, system-user pairs, handoffs, committee deliberation, synthesis, validation, fallback, and redirects for agent constitutions and workflow steps. Use when the user asks to create a prompt, write a handoff prompt, generate a meta prompt, build a committee deliberation prompt, make a fallback prompt, or design agent prompts. If prompt type or owning agent is missing, interview for the minimum required inputs before writing. [EXPLICIT]
argument-hint: prompt-type owning-agent-id
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Prompt Creator

Generate deterministic prompt files for multi-agent ecosystems. The output is a prompt artifact plus a validation packet, not a free-form writing exercise. Covers 9 prompt types from system prompts to committee deliberation to fallback recovery. [EXPLICIT]

## When to Activate

Use this skill when the user requests one of these actions:

- create, write, generate, or improve a reusable prompt for an agent
- create a meta prompt, handoff prompt, validation prompt, fallback prompt, committee deliberation prompt, or synthesis prompt
- design a prompt contract for multi-agent routing, execution, validation, recovery, or handoff
- the user names an agent but omits prompt type; interview for prompt type, target agent, source files, and success criteria

Do not use this skill for the downstream work the prompt will perform. For full agent constitutions, route to `agent-constitution-creator`. For workflow step definitions, route to `workflow-creator`.

## Assumptions & Limits

- **Assumes** an agentic ecosystem with defined agents; generated prompts must reference real source agent files or report the gap.
- **Limit**: Prompts are templates, not runtime; placeholders (`{{var}}`) are filled by the orchestrator.
- **Limit**: Committee prompts (deliberation/synthesis) require at least 3 agents to be meaningful.
- **Trade-off**: More detailed prompts = more predictable agent behavior but less adaptability. For creative tasks, keep prompts loose.

## Usage

```
/prompt-creator meta_prompt data-analyst
/prompt-creator handoff_prompt customer-onboarding
/prompt-creator committee_deliberation                # interview mode
```

Parse `$1` as prompt type, `$2` as owning agent ID. If missing, ask. [EXPLICIT]

## Before Generating

1. **Read the agent**: `Read agents/$2/agent.md` or the user-provided source path. If absent, emit `missing_source_agent` and ask before writing.
2. **Check existing prompts**: `Glob agents/$2/prompts/*.md` to avoid duplicates and name collisions.
3. **Read prompt spec**: `Read references/prompt-types-spec.md` if available, then apply `assets/prompt-type-matrix.json`.
4. **Apply checklist**: use `assets/prompt-contract-checklist.md` before finalizing.
5. **Freeze nondeterminism**: do not invent dates, estimates, tool names, agent IDs, quality gates, or external URLs. Use user-provided values or explicit placeholders.

## Deterministic Contract

- Candidate prompt type must be one of the 9 rows in `assets/prompt-type-matrix.json`.
- The owning agent ID must come from a source file, explicit user input, or a clearly marked placeholder.
- Generated frontmatter must include `type`, `owningAgent`, `sourceAgentMd`, `version`, `createdBy`, and `validationStatus`.
- Every placeholder must be descriptive snake_case inside `{{...}}`; reject `{{x}}`, `{{var}}`, and unlabeled placeholders.
- Every generated prompt must include: purpose, inputs, procedure, output contract, validation gate, failure handling, and handoff/next-action boundary.
- If required context is missing, return a gap packet instead of filling creatively.

## Source and No-Invention Rules

- Do not invent agents, tools, commands, files, quality gates, brand constraints, or time estimates.
- Do not claim an agent constitution was read unless a path was inspected.
- Do not overwrite an existing prompt path unless the user explicitly asks for an update.
- Do not execute the prompt's downstream task.
- If external knowledge is needed, ask for it or cite the missing source as `coverage_gap`.

## Time, Network, and Randomness Policy

- Use the session date only when the user or runtime provides it; otherwise use `{{created_date}}`.
- Do not fetch remote fonts, templates, or examples for prompt generation.
- Do not use random names, randomized examples, or nondeterministic ordering; sort candidates by prompt type then slug.

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
createdBy: "prompt-creator"
validationStatus: "draft|validated"
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
- [ ] Missing agent/spec/context emits a gap packet instead of invented content
- [ ] Type-specific rules followed (see table above)
- [ ] No empty sections
- [ ] All `{{placeholders}}` are named descriptively (not `{{x}}`)
- [ ] Duplicate existing prompt path was checked
- [ ] Committee prompts require independent evaluation before comparison
- [ ] Handoff prompts specify both what to pass AND what to omit
- [ ] Validation prompts include severity levels
- [ ] Fallback prompts include escalation path
- [ ] `assets/prompt-contract-checklist.md` was applied

## Downstream Boundaries

- Prompt files may be consumed by orchestrators, agents, validators, and renderers.
- The prompt artifact must not include hidden reasoning, secrets, private user context, or unverified runtime state.
- The validation packet must list unresolved gaps so the next workflow can stop or ask before execution.

## Assets

- `assets/prompt-contract-checklist.md` defines the reusable deterministic prompt gate.
- `assets/prompt-type-matrix.json` defines type-specific required sections, redirects, and failure modes.

## Scripts

- `scripts/validate_prompt_artifact.py` validates generated prompt markdown frontmatter, required sections, placeholders, and type-specific gates.
- `scripts/check.sh` runs deterministic fixtures and must pass before ledger closure.

---
**Author:** Javier Montaño | **Last updated:** March 12, 2026

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
