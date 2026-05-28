---
name: spec-agent-command
author: JM Labs (Javier Montaño)
description: 
  Generate production-ready agent .md and command .md files from designs. Enforces plugin subagent constraints and alias linkage. [EXPLICIT]
  Trigger: spec agent, spec command, generate agent file, write command file, create agent specification. [EXPLICIT]
argument-hint: "agent-design-path"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
version: 1.0.0
---

# Spec Agent Command

> "An agent without a clear role is a meeting without an agenda -- everyone is busy, nothing gets done."

Generates production-ready agent markdown files and command markdown files (canonical + alias pairs) from design documents. Enforces plugin subagent constraints: no `hooks`, `mcpServers`, or `permissionMode` in agent frontmatter. Validates kebab-case naming and cross-reference integrity. [EXPLICIT]

---

## Procedure

### Step 1 -- Read Agent and Command Designs

- Read the design file at the path provided via `argument-hint`. `[Read]`
- Extract for each agent: name, description, role, tools, skills assigned, execution flows, operating principles.
- Extract for each command: name, description, skill it invokes, argument-hint, aliases.
- If the design references skills not yet defined, flag them as `WARNING: Unresolved skill reference`.

### Step 2 -- Generate Agent .md File

Compose the agent file with these sections:

1. **Frontmatter** (YAML):
   - `name`: kebab-case agent identifier. [EXPLICIT]
   - `description`: 1-2 sentence role description. [EXPLICIT]
   - `tools`: list of tools the agent uses. [EXPLICIT]
   - `model`: typically `inherit`. [EXPLICIT]
   - MUST NOT contain: `hooks`, `mcpServers`, `permissionMode` (plugin subagent constraint). [EXPLICIT]

2. **Title** -- H1 with the agent name in title case. [EXPLICIT]

3. **Role** -- 2-4 sentences defining what the agent does, which movement it owns, and its relationship to other agents. [EXPLICIT]

4. **Responsibilities** -- Numbered list of high-level duties. [EXPLICIT]

5. **Skills Assigned** -- Table with columns: `#`, `Skill`, `Trigger`. [EXPLICIT]

6. **Execution Flows** -- One subsection per command/workflow showing the skill execution sequence as an indented flow diagram. [EXPLICIT]

7. **Operating Principles** -- Numbered list of behavioral rules (5-8 items). Include safety, idempotency, and cross-reference rules. [EXPLICIT]

### Step 3 -- Enforce Subagent Constraints

- Scan the generated agent frontmatter for forbidden fields: `hooks`, `mcpServers`, `permissionMode`.
- If any are present, remove them and add an INFO note explaining the constraint.
- Verify the `tools` list only contains valid tool names (Read, Write, Edit, Glob, Grep, Bash, etc.).

### Step 4 -- Generate Command .md Files (Canonical)

For each canonical command:

1. **Frontmatter** (YAML):
   - `description`: 1 sentence describing what the command does. [EXPLICIT]
   - `user-invocable`: `true`. [EXPLICIT]
   - `argument-hint`: from design (use `<>` for required, `[]` for optional). [EXPLICIT]

2. **Body**:
   - **Usage** section with the command syntax. [EXPLICIT]
   - **Execution Flow** describing which skill(s) are invoked and in what order. [EXPLICIT]
   - **Output** describing what the user receives. [EXPLICIT]

### Step 5 -- Generate Alias Command .md Files

For each alias:

1. **Frontmatter** (YAML):
   - `alias-of`: the canonical command name (without plugin prefix). [EXPLICIT]
   - `description`: same as canonical. [EXPLICIT]
   - `user-invocable`: `true`. [EXPLICIT]

2. **Body**: Single line stating this is an alias. Example: `Alias for [canonical-name]. See commands/{canonical-name}.md.`

### Step 6 -- Validate Naming

- Check all generated file names against kebab-case pattern: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`.
- Check agent names, command names, and skill references for kebab-case compliance.
- Report `WARNING` for each violation with suggested correction.

### Step 7 -- Validate Cross-References

- Collect all skill names referenced in agent files and command execution flows.
- Verify each referenced skill exists in the design or in the plugin's existing `skills/` directory. `[Glob]`
- Collect all command names referenced in agent execution flows.
- Verify each referenced command exists in the design or in `commands/`. `[Glob]`
- Report `WARNING` for each unresolved reference.

---

## Quality Criteria

- [ ] Agent frontmatter contains no forbidden fields (`hooks`, `mcpServers`, `permissionMode`).
- [ ] Every command has a matching alias file with correct `alias-of` pointer.
- [ ] All file names are kebab-case compliant.
- [ ] All skill and command cross-references resolve to existing or designed entities.
- [ ] Agent file includes at least: role, skills table, one execution flow, and operating principles.

## Assumptions & Limits

- Requires a completed agent/command design document as input. Cannot infer agent roles or command routing from scratch -- that is `design-agent`'s job.
- The subagent constraint check (Step 3) removes forbidden fields silently with an INFO note. It does not ask for confirmation because these fields are never valid for plugin agents.
- Alias generation assumes a 1:1 mapping (one alias per canonical command). Multiple aliases for the same canonical must be specified explicitly in the design.
- Cross-reference validation (Step 7) checks existence only, not semantic correctness. A command referencing `validate-structure` will pass even if the command has nothing to do with validation.
- Cannot validate that execution flows will actually work at runtime -- only that the referenced skills and commands exist.

## Good vs Bad

**Bad agent spec:**
```
---
name: my-agent
description: Does stuff
hooks:
  PreToolUse: [...]
---
# My Agent
Handles validation.
```
Missing: forbidden `hooks` field, no tools list, no skills table, no execution flows, no operating principles. [EXPLICIT]

**Good agent spec:**
```
---
name: plugin-qa-engineer
description: >
  Orchestrates plugin quality assurance across validation, audit, and reporting. [EXPLICIT]
tools:
  - Read
  - Glob
  - Grep
  - Bash
maxTurns: 45
---
# Plugin QA Engineer
**Role**: Validates plugin quality by orchestrating 9 QA skills across 4 movements.
## Skills Assigned
| # | Skill | Movement |
|---|-------|----------|
| 1 | validate-structure | VALIDATE |
## Execution Flows
### /pqa:validate
1. Run validate-structure → 2. Run validate-manifest → ... [EXPLICIT]
## Operating Principles
1. Read first, write never. [EXPLICIT]
```
Includes: no forbidden fields, tool list, maxTurns, skills table, execution flow, operating principles. [EXPLICIT]

## Anti-Patterns

1. **Including hooks in agent frontmatter** -- Plugin subagents cannot define their own hooks. Hooks belong in `hooks/hooks.json` at the plugin level. Remove the field entirely. [EXPLICIT]
2. **Alias without canonical** -- Creating an alias command that points to a non-existent canonical command. Always generate the canonical first, then the alias. [EXPLICIT]
3. **Execution flow with unnamed skills** -- Writing flows like "run validation" instead of referencing the exact skill name (`validate-structure`). Every step in a flow must reference a concrete skill. [EXPLICIT]

## Edge Cases

1. **Agent with a single skill** -- Valid. Still generate the full agent structure including a minimal execution flow and skills table with one row. [EXPLICIT]
2. **Command with no argument-hint** -- Valid for commands that take no arguments (e.g., `/pqa:menu`). Omit `argument-hint` from frontmatter rather than setting it to empty string. [EXPLICIT]
3. **Multiple agents sharing a skill** -- Valid. The skill appears in both agents' skills tables. Note this in both agents' operating principles for clarity. [EXPLICIT]

## Usage

Example invocations:

- "/spec-agent-command" — Run the full spec agent command workflow
- "spec agent command on this project" — Apply to current context

