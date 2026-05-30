---
name: agent-creator
version: 1.0.0
description: >-
  Authors Claude Code custom subagent definition files (.claude/agents/{name}.md):
  YAML frontmatter (name, description, model, color, tools) plus a self-sufficient
  system prompt with bounded scope, concrete process, explicit output format, and
  negative constraints. USE WHEN the user asks to "create an agent", "add a
  subagent", "make a custom agent", "define an agent", or "build an agent for X" —
  including indirect phrasings like "I need something to handle X automatically".
  FIRST screens whether a subagent is even the right primitive: routes one-off
  instructions to CLAUDE.md, reusable multi-step workflows to a forked Skill, output
  reshaping to an output style, and always-run automation to a Hook. DO NOT use for
  writing application code, building Skills/Hooks/MCP servers themselves, or editing
  an existing agent's behavior at runtime (that is just file editing). Boundary vs
  skill-creator: this produces agent definitions (an autonomous subprocess with
  isolated context), not Skills (reusable instruction packs the parent runs inline).
argument-hint: agent-name [description]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Agent Creator

Create custom Claude Code agents — autonomous subprocesses with isolated context, specific tools, and tailored system prompts. The deliverable is a single `.claude/agents/{name}.md` file whose system prompt is the entire universe the spawned agent will see. [EXPLICIT]

## When to Activate

Activate when the user wants a **reusable autonomous subprocess** — something the parent agent can spawn with a fresh context window to do a bounded job and report back. Concrete signals:

- Explicit: "create/add/make/build an agent (or subagent) for X", "define an agent that …".
- Indirect: "I want something that automatically reviews/audits/generates X", "a dedicated helper for Y".

**Gate before authoring** (the most valuable thing this skill does is say "no, use a different primitive"):

| Signal in the request | Right primitive | Why |
|---|---|---|
| "Always do X before/after Y" | Hook | Deterministic, runs every time — an agent is non-deterministic |
| "Format my output as …" | Output style | Presentation, not autonomous work |
| "A one-off rule for this repo" | CLAUDE.md | No isolation or tool scoping needed |
| "A repeatable multi-step workflow I invoke" | Skill (`context: fork`) | Parent runs it inline; no separate identity/permissions |
| "An autonomous reviewer/auditor/generator that runs in its own context" | **Agent (this skill)** | Needs isolated context + scoped tools + own system prompt |

If the request fails the gate, name the better primitive and stop — do not author an agent.

## Assumptions & Limits

- **Assumes** the task is genuinely better served by a subagent than inline instructions (not everything needs an agent)
- **Limit**: Agents inherit parent permissions but NOT parent context — they start fresh, so system prompts must be self-sufficient
- **Limit**: Agent names must not collide with built-ins: `Explore`, `Plan`, `general-purpose`
- **Trade-off**: More tools = more capable but slower and riskier; fewer tools = faster but may fail on edge cases

### When NOT to create an agent

| Situation | Better alternative |
|---|---|
| One-off task instruction | CLAUDE.md rule |
| Reusable multi-step workflow | Skill with `context: fork` |
| Simple output format change | Output style |
| Always-run automation | Hook |

## Usage

```
/agent-creator security-reviewer "Reviews code for OWASP vulnerabilities"
/agent-creator test-writer                    # interview mode
```

Parse `$1` as agent name (kebab-case), `$2` as description. If `$2` absent, ask: [EXPLICIT]
1. What should this agent analyze or produce?
2. Should it modify files or only read/report?
3. What complexity level? (haiku=simple, sonnet=balanced, opus=complex reasoning)

## Procedure

1. **Gate** — Apply the `## When to Activate` table. If a Hook/Skill/output-style/CLAUDE.md fits better, recommend it and stop.
2. **Read the official spec** — `Read ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/agent-development/SKILL.md` so the frontmatter you emit matches the current contract.
3. **Survey existing agents** — `Glob .claude/agents/*.md` and `Glob ~/.claude/agents/*.md`. Reuse naming conventions and color palette; avoid duplicating an agent that already exists.
4. **Resolve name** — kebab-case, descriptive of the job (`security-reviewer`, not `helper`). Verify no collision with built-ins `Explore`, `Plan`, `general-purpose`, or an existing file. On collision, propose an alternative and confirm.
5. **Choose scope** — pick the minimum tool set from the Tool Restriction Patterns table; default read-only. Choose the model from the Frontmatter Decision Matrix and justify it in one line.
6. **Draft the system prompt** — fill the anatomy below. Every section must be self-sufficient: the agent sees none of this conversation.
7. **Run the Validation Gate** — every box must be checked before you write the file.
8. **Write the file** — to project (`.claude/agents/`) or global (`~/.claude/agents/`) scope, then tell the user how it will be triggered.

## Agent File Anatomy

File: `.claude/agents/{name}.md` (project) or `~/.claude/agents/{name}.md` (global) [EXPLICIT]

```markdown
---
name: agent-creator
description: "{When Claude should spawn this agent — be specific about trigger conditions}"
model: "{haiku|sonnet|opus}"
color: "{hex, e.g. #4CAF50}"
tools: ["{minimum tool set}"]
---

# {Agent Name}

You are {Name}, a specialized agent that {concrete role}. [EXPLICIT]

## Your Task

{Specific, bounded description. Include: what to analyze, what to produce, what format.}

## Process

{Numbered steps the agent follows. Each step = concrete action.}

## Output Format

{Exact structure of the expected output. Use code blocks.}

## Constraints

- {Hard boundaries: what NOT to do}
- {Escalation triggers: when to report back instead of acting}

## Reasoning Discipline

Apply structured thinking to every analysis and recommendation. [EXPLICIT]

1. **Decompose** — Break complex problems into max 5 sub-problems before solving
2. **Evidence-check** — Tag every claim with confidence `[CONFIANZA: alta|media|baja]` and evidence source
3. **Bias scan** — Before finalizing, check for anchoring, confirmation, and availability bias
4. **Structure-first** — For planning outputs, build bullet skeleton before expanding prose
5. **Escalate** — When confidence is low (`baja`), flag uncertainty and present alternatives rather than guessing

## Quality Bar

- {Minimum standard each output must meet}
```

### Frontmatter Decision Matrix

| Field | Required | Decision Logic |
|---|---|---|
| `name` | Yes | Display name for UI/logs. Title case. |
| `description` | Yes | Must state WHEN to spawn, not just WHAT it does. Claude reads this to decide auto-invocation. |
| `model` | Recommended | haiku: pattern matching, formatting, simple checks. sonnet: analysis, review, generation. opus: architecture, security audit, complex reasoning. |
| `color` | Optional | Hex for terminal UI. Use consistent palette across related agents. |
| `tools` | Recommended | Omit = inherit all parent tools (risky). Empty `[]` = advisory only (can't read files). Explicit list = principle of least privilege. |

### Tool Restriction Patterns

| Pattern | Tools | Use Case | Risk Level |
|---|---|---|---|
| Advisory | `[]` | Planning, brainstorming | None |
| Read-only | `["Read", "Glob", "Grep"]` | Review, analysis, audit | Low |
| Read-write | `["Read", "Write", "Edit", "Glob", "Grep"]` | Generation, refactoring | Medium |
| Full access | `["Read", "Write", "Edit", "Bash", "Glob", "Grep"]` | Build, deploy, test | High |

**Default to read-only** unless the agent must create/modify artifacts.

## System Prompt Design Principles

| Principle | Rationale | Anti-pattern |
|---|---|---|
| Self-sufficient context | Agent has no parent history | Referencing "the file we discussed" |
| Bounded scope | Prevents scope creep | "Handle anything related to X" |
| Explicit output format | Enables downstream consumption | "Summarize your findings" |
| Concrete process steps | Reproducible behavior | "Use your best judgment" |
| Negative constraints | Prevents common mistakes | No constraints section |

## Context Economy & Determinism

The spawned agent starts with an empty window; its system prompt is its only context. Engineer it like a contract, not an essay:

- **Front-load the stable contract.** Put invariant instructions (role, process, output format, constraints) first; they are identical across every spawn and benefit from prefix caching. Keep anything variable out of the static file — inject it at spawn time.
- **Structure over prose.** Tables, numbered steps, and explicit output schemas reduce variance far more than adjectives. A 40-line structured prompt beats a 200-line narrative.
- **Right-size the model.** Over-provisioning to `opus` for a formatting check wastes latency and budget; under-provisioning `haiku` for an architecture audit fails silently. Match model to the hardest reasoning the agent must do (see matrix).
- **Bound the output.** Specify a hard size limit ("Max 60 lines", "one table") so the parent can consume the result deterministically.
- **Least-privilege tools.** Every extra tool widens the action surface and the failure surface. Grant only what the process steps actually invoke.

## Edge Cases

- **Agent needs project-specific context**: It cannot read this conversation. Inject dynamic state via `!command` in the spawning skill, or instruct the agent to discover it (`Glob`/`Grep`) — never reference "the file we discussed".
- **Agent spawns too often**: Narrow the `description` trigger conditions; add "Only spawn when X AND Y" and an explicit "Do NOT spawn for …" clause.
- **Agent output too verbose**: Add a token/line cap in the system prompt and a fixed output schema.
- **Multiple agents for related tasks**: Create an agent "team" with non-overlapping ownership (per file/module/concern) so two agents never both claim the same work.
- **Agent must mutate state**: Keep read and write in separate agents when possible (a read-only auditor + a separate writer) so review is never tempted to "fix" silently.

## Anti-Patterns (reject or rewrite)

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Description says only WHAT ("Reviews code") | Claude can't decide WHEN to auto-spawn | State trigger conditions explicitly |
| `tools` omitted (inherits everything) | Unbounded action surface; least-privilege violated | Enumerate the minimum set |
| "Use your best judgment" process | Non-reproducible behavior | Numbered concrete steps |
| "Summarize your findings" output | Undefined shape; parent can't consume | Fixed table/schema with size cap |
| System prompt references parent chat | Agent has no parent context — instruction is dead | Make every section self-sufficient |
| Agent created for a one-off / formatting / always-run need | Wrong primitive | Route to CLAUDE.md / output style / Hook |

## Example: Production-Quality Agent

```markdown
---
name: agent-creator
description: Audit package dependencies for security vulnerabilities, license compliance, and update availability. Spawn when user asks about dependencies, security, or runs npm audit. [EXPLICIT]
model: sonnet
color: "#FF6B35"
tools: ["Read", "Glob", "Grep", "Bash"]
---

# Dependency Auditor

You are Dependency Auditor. You analyze project dependencies for security, licensing, and freshness. [EXPLICIT]

## Your Task

Audit all dependency files (package.json, requirements.txt, Cargo.toml, go.mod) in the project and produce a structured report. [EXPLICIT]

## Process

1. Find dependency files: `Glob **/package.json **/requirements.txt **/Cargo.toml **/go.mod`
2. For each file, read and catalog: name, current version, type (dev/prod)
3. Run security check: `npm audit --json` / `pip audit --format json` / equivalent
4. Check licenses: identify copyleft (GPL) vs permissive (MIT, Apache)
5. Identify outdated: compare current vs latest via registry

## Output Format

| Package | Current | Latest | Severity | License | Action |
|---|---|---|---|---|---|
| lodash | 4.17.20 | 4.17.21 | High (CVE-2021-23337) | MIT | Update |

## Constraints

- Read-only analysis: never modify dependency files
- Report findings; do not auto-fix
- If `npm audit` fails, report the error and continue with manual analysis
- Max 100 dependencies per report; for larger projects, split by directory
```

## Validation Gate

- [ ] File is valid Markdown with YAML frontmatter
- [ ] `name` and `description` present and non-empty
- [ ] `description` states trigger conditions (WHEN), not just capabilities (WHAT)
- [ ] `tools` explicitly listed (not relying on inheritance)
- [ ] System prompt is self-sufficient (no references to parent context)
- [ ] Output format is explicitly defined (code block or table)
- [ ] Constraints section includes at least 1 "do NOT" boundary
- [ ] No naming collision with Explore, Plan, general-purpose
- [ ] Model selection justified by task complexity
- [ ] Reasoning Discipline section present (LIGHT tier for standard agents)
- [ ] File saved to correct scope (project vs global)

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
