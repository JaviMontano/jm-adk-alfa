---
name: agent-creator
description:  [EXPLICIT]
  This skill should be used when the user asks to "create an agent", [EXPLICIT]
  "add a subagent", "make a custom agent", "define agent definition", [EXPLICIT]
  or "build an agent for X". Creates Claude Code custom agent definitions [EXPLICIT]
  with system prompts, tool restrictions, model selection, and reasoning [EXPLICIT]
  discipline. Use this skill whenever someone needs a new autonomous [EXPLICIT]
  subprocess for their project, even if they just say "I need something [EXPLICIT]
  to handle X automatically". [EXPLICIT]
argument-hint: agent-name [description] [EXPLICIT]
model: opus [EXPLICIT]
context: fork [EXPLICIT]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep [EXPLICIT]
version: 1.0.0
---

# Agent Creator

Create custom Claude Code agents — autonomous subprocesses with isolated context, specific tools, and tailored system prompts. [EXPLICIT]

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

## Before Creating

1. **Read official spec**: `Read ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/agent-development/SKILL.md`
2. **Check existing**: `Glob .claude/agents/*.md` and `Glob ~/.claude/agents/*.md`
3. **Verify no name collision** with built-in agents

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

## Edge Cases

- **Agent needs project-specific context**: Use `!command` in the skill that spawns it to inject dynamic state
- **Agent spawns too often**: Narrow the description trigger conditions; add "Only spawn when X AND Y"
- **Agent output too verbose**: Add token/line limits in system prompt ("Max 50 lines")
- **Multiple agents for related tasks**: Create an agent "team" with clear ownership boundaries per file/module

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
