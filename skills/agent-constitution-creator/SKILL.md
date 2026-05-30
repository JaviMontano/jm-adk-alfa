---
name: agent-constitution-creator
version: 1.1.0
description: >-
  Generate a constitutional `agent.md` for ONE agent inside a multi-agent ecosystem — a
  22-field operational identity spanning mission, scope, authority, tools, security
  checkpoints, delegation/escalation, meta-cognition, and verifiable completion criteria.
  Use when the user says "create an agent constitution", "define agent identity", "write
  agent.md", "generate agent spec", "design agent governance", or even just "add an agent
  for X" / "I need a new agent that does Y". NOT for lightweight Claude Code subagent
  prompts (use `/agent-creator`), NOT for orchestrator/ecosystem-wide policy (that is the
  meta-orchestrator's job), and NOT for editing prose system prompts that have no fielded
  contract. One invocation produces one constitution; resolve scope overlap with existing
  agents before writing.
argument-hint: agent-id [role-description]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---
# Agent Constitution Creator

Generate constitutional `agent.md` documents — the persistent system prompt and operational identity for an agent in a multi-agent ecosystem. Each constitution fills 22 fields covering identity, authority, governance, and quality. The output is a static contract the orchestrator can route against and a human can audit.

> **Scope boundary**: This skill creates one comprehensive agent constitution for tool-calling / multi-agent architectures. For a lightweight Claude Code subagent definition use `/agent-creator`. For ecosystem-wide policy (shared security checkpoints, the tool registry, the delegation topology) that is the orchestrator's concern, not a single agent's constitution.

## Assumptions & limits

- **Assumes** a multi-agent ecosystem exists or is being designed — a single isolated agent rarely needs delegation/escalation fields.
- **Assumes** shared ecosystem primitives exist: a tool registry, security checkpoints (CP1 input / CP2 prompt / CP3 output), and named delegation modes (single / panel / committee).
- **Limit**: a constitution is a *static document*. It does not enforce behavior at runtime — enforcement is the orchestrator's job. The constitution's value is being precise, auditable, and non-overlapping.
- **Trade-off**: more specific constitution → more predictable behavior, less agent autonomy. More general → flexible but prone to scope creep. Bias toward specific; vagueness is the failure mode.

## Inputs / outputs (contract)

- **Input**: `agent-id` (kebab-case, required), `role-description` (free text, optional → triggers interview mode if absent), plus discovered ecosystem context (sibling `agent.md` files, tool registry, security spec).
- **Output**: one file at `agents/{id}/agent.md` with YAML frontmatter (`id`, `name`, `role`, `version`) followed by all 22 fields as `#` sections. No partial constitutions — every field is present or explicitly marked `N/A — {reason}`.

## Procedure (deterministic)

1. **Parse args.** `$1` → agent ID. Reject if not kebab-case. `$2` → role. If `$2` is absent or vague (see edge cases), enter interview mode and ask the three questions below before writing anything.
2. **Read ecosystem context.** `Glob agents/*/agent.md` and read each. Build a one-line scope summary per existing agent.
3. **Check overlap (hard gate).** If the new agent's scope overlaps an existing agent by more than ~30%, STOP and resolve: merge, split with explicit boundaries, or add mutual Non-Goals referencing each other. Never ship two agents with overlapping Scope.
4. **Read the tool registry and security spec** if present, to populate Allowed Tools and Security Policy with real names instead of placeholders.
5. **Draft all 22 fields** using the template below. Skeleton (bullets) before prose. Tag any inference you make from sparse input with `[INFERIDO]` and any open question with `{por_confirmar}`.
6. **Run the Validation Gate** against your own draft. Fix every unchecked item.
7. **Write** to `agents/{id}/agent.md`. Report the path and which fields, if any, were marked `N/A` and why.

Interview questions (when role is absent or vague):
1. What is this agent's primary responsibility, and what observable outcome proves it succeeded?
2. What other agents exist? (needed for Non-Goals, Delegation, Escalation, Dependencies.)
3. What tools must it use, and which must it never touch?

## The 22 fields

Organized in 4 categories for coherence.

### Identity (3)
| # | Field | Purpose | Quality bar |
|---|---|---|---|
| 1 | Mission | Reason for existing | Specific to THIS agent; 1-2 sentences; includes a measurable outcome |
| 2 | Mandate | What it MUST do | Concrete, verifiable actions (not aspirational verbs) |
| 3 | Scope | Operational boundaries | Explicit in/out list; no grey areas |

### Authority (6)
| # | Field | Purpose | Quality bar |
|---|---|---|---|
| 4 | Non-Goals | Explicit exclusions | >=3 items a user might wrongly expect, each routed to who handles it |
| 5 | Inputs | Data it receives | Typed: `{name}: {type} — {description}` |
| 6 | Outputs | What it produces | Format specified: JSON / Markdown / file path |
| 7 | Decision Rights | Autonomous vs gated | "can X without approval; must escalate Y" |
| 8 | Allowed Tools | Authorized tools | Specific registry names; no wildcards |
| 9 | Forbidden Tools | Prohibited tools | Explicit denials that prevent scope creep |

### Governance (6)
| # | Field | Purpose | Quality bar |
|---|---|---|---|
| 10 | Memory Policy | Read/write rules | Keys, formats, retention, size limits |
| 11 | Security Policy | Security controls | References CP1/input, CP2/prompt, CP3/output with concrete rules |
| 12 | Orchestration Policy | Multi-agent role | Role in chains: initiator, delegate, observer |
| 13 | Delegation Rules | When/how to delegate | Criteria per mode: single, panel (terna), committee |
| 14 | Escalation Rules | When to escalate | Trigger, target agent/human, context to include |
| 15 | Tone / Output Style | Communication style | Language, formality, formatting conventions |

### Quality (7)
| # | Field | Purpose | Quality bar |
|---|---|---|---|
| 16 | Validation Discipline | Output verification | Method: self-check, peer review, automated test |
| 17 | Meta-Cognition Protocol | Reasoning discipline | FULL (triad) or LIGHT (default) — defined below |
| 18 | Failure Handling | Error recovery | Per-mode: detection → response → fallback |
| 19 | Completion Criteria | Done definition | Verifiable assertions, not "task is done" |
| 20 | KPIs | Performance metrics | >=3 metrics with targets and units |
| 21 | Dependencies | Required services | Other agents, APIs, data sources |
| 22 | Version | Document version | Semver; change log in footer or commit |

## Output template

Write to `agents/{id}/agent.md`:

```markdown
---
id: "{id}"
name: "{id}"
role: "{role}"
version: "1.0.0"
---
# Mission
{1-2 sentences with a measurable outcome}

# Mandate
- {Concrete action 1}
- {Concrete action 2}

# Scope
**In scope:**
- {boundary 1}

**Out of scope:**
- {boundary 1} -> {responsible agent}

# Non-Goals
- {Exclusion 1} (-> {who handles it instead})
- {Exclusion 2}
- {Exclusion 3}

# Inputs
- `{inputName}`: {type} — {description}

# Outputs
- `{outputName}`: {format} — {description}

# Decision Rights
**Autonomous:** {decisions this agent makes alone}
**Requires approval:** {decisions needing human or lead-agent sign-off}

# Allowed Tools
- `{tool_name}` — {why this agent needs it}

# Forbidden Tools
- `{tool_name}` — {why it is forbidden}

# Memory Policy
- **Reads:** `{key}` — {purpose}
- **Writes:** `{key}` — {what, when, retention}
- **Size limit:** {max per entry}

# Security Policy
- **CP1 (Input):** {sanitization rules}
- **CP2 (Prompt):** {hardening rules}
- **CP3 (Output):** {validation rules}

# Orchestration Policy
{Role in delegation: initiator | delegate | both. How it participates in chains.}

# Delegation Rules
- **Single:** {when to delegate to one agent}
- **Panel:** {when to use a 3-agent panel}
- **Committee:** {when to convene full committee}

# Escalation Rules
- **Trigger:** {condition}
- **Target:** {agent-id or human role}
- **Context:** {what to include in the escalation}

# Tone / Output Style
{Language, formality, format preferences}

# Validation Discipline
{Method and criteria for self-validation before delivery}

# Meta-Cognition Protocol
{FULL for triad/orchestrator agents, LIGHT for all others — see below}

# Failure Handling
| Failure Mode | Detection | Response | Fallback |
|---|---|---|---|
| {mode 1} | {signal} | {action} | {alternative} |

# Completion Criteria
- [ ] {Verifiable assertion 1}
- [ ] {Verifiable assertion 2}

# KPIs
| Metric | Target | Unit |
|---|---|---|
| {metric 1} | {value} | {unit} |

# Dependencies
- `{agent-id}` — {what for}
- `{service}` — {what for}

# Version
1.0.0 — {date} — initial constitution
```

### Meta-Cognition Protocol reference

**LIGHT (default, for execution agents):**
1. Decompose — max 5 sub-problems before solving.
2. Evidence-check — tag claims with confidence `[CONFIANZA: alta|media|baja]`.
3. Bias scan — anchoring, confirmation, availability.
4. Structure-first — bullet skeleton before prose.
5. Escalate — when confidence is `baja`, flag and present alternatives.

**FULL (triad / orchestrator agents only):** LIGHT plus Structured Reasoning, Skeleton-of-Thought, and Chain-of-Code patterns with 0.0–1.0 confidence scoring.

## Quality criteria — good vs bad

**Mission** — Bad: "This agent helps with data tasks." Good: "Transform raw CSV/JSON datasets into validated, typed schemas with anomaly detection, producing structured analysis within 60 seconds per 10K rows."

**Non-Goals** — Bad: "Doesn't do other things." Good:
- Does NOT handle real-time streaming data (-> `stream-processor`)
- Does NOT perform ML model training (-> `ml-trainer`)
- Does NOT make business decisions from data (-> escalate to human analyst)

**Failure Handling** — Bad: "Handle errors appropriately." Good:

| Mode | Detection | Response | Fallback |
|---|---|---|---|
| Malformed input | Schema validation fails | Log error, return structured error message | Ask user for a sample row |
| Tool unavailable | Tool call timeout > 30s | Retry once, then escalate | Use alternative tool / manual path |
| Conflicting data | >5% rows contradictory | Flag conflicts, proceed with majority value | Escalate with conflict report |

## Anti-patterns (do not ship a constitution that…)

- …has a Mission reusable for any agent (the "generic identity" smell). If you could paste it into another agent unchanged, it is wrong.
- …lists tools with wildcards or "all tools". Most agents need 3-5. Push back on broad access — it is a security and scope risk.
- …leaves Non-Goals, Escalation, or Failure Handling empty or aspirational. These are the fields that prevent runaway behavior; placeholders defeat the purpose.
- …overlaps an existing agent's Scope. Two agents that can both claim the same task create routing ambiguity and silent duplication.
- …states Completion Criteria as "task is done" instead of testable assertions an orchestrator could check.

## Edge cases

- **Single-agent system.** A constitution is still useful for scope/tools/completion. Mark Delegation, Escalation, Orchestration as `N/A — no peer agents in current ecosystem`.
- **Agent wrapping an external API.** Derive Inputs/Outputs from the API contract; Decision Rights are limited to request formatting and error handling.
- **Overlapping scope.** Do not write the constitution before resolving the overlap (see Procedure step 3).
- **Vague role ("handles data").** Enter interview mode. The role must be specific enough that two people would write near-identical constitutions from it.
- **"Needs all tools."** Suspicious. Ask which operation requires which tool; enumerate, then forbid the rest explicitly.

## Validation gate

- [ ] All 22 fields present and non-empty (or `N/A` with a stated reason)
- [ ] Mission is specific to THIS agent (not reusable verbatim elsewhere)
- [ ] Mission includes a measurable outcome
- [ ] Non-Goals has >=3 items, each routed to a responsible agent/human
- [ ] Allowed Tools lists specific registry names (no wildcards)
- [ ] Security Policy references CP1/CP2/CP3 with concrete rules
- [ ] Delegation Rules specify criteria for each mode
- [ ] Failure Handling has >=3 modes with detection -> response -> fallback
- [ ] Completion Criteria are testable assertions
- [ ] KPIs include >=3 metrics with units
- [ ] No existing agent shares this agent's Scope (overlap resolved)

---
**Author:** Javier Montano | **Last updated:** May 30, 2026
