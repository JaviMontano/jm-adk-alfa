---
name: plugin-builder
argument-hint: "plugin-name" [EXPLICIT]
description: 
  Builds complete Claude Code plugins from scratch — scaffolds plugin.json, CLAUDE.md, commands/, agents/,
  skills/, hooks/, scripts/, settings.json. Activates when the user says "create a plugin", "scaffold a plugin",
  "build a new plugin", "initialize plugin structure", or "set up a plugin project". Also triggers on mentions
  of plugin creation, plugin scaffolding, or Claude Code extension packaging. Use this skill even if the user
  only names the plugin — it interviews for missing details. [EXPLICIT]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
version: 1.0.0
---

# Plugin Builder — Claude Code Plugin Scaffolding

Creates production-ready Claude Code plugins following the official plugin specification. [EXPLICIT]

## Plugin Directory Structure (mandatory)

```
{plugin-name}/
├── .claude-plugin/
│   └── plugin.json              ← Manifest (only file here)
├── commands/                     ← User-invocable skills (/plugin:command)
│   └── {verb}-{context}.md      ← Verb-first naming
├── agents/                       ← Custom agent definitions
│   └── {role-name}.md           ← Role-based naming
├── skills/                       ← Agent skills (model-invoked)
│   └── {skill-name}/
│       └── SKILL.md             ← Frontmatter + instructions
├── hooks/
│   └── hooks.json               ← Event handlers
├── scripts/                      ← Shell scripts for hooks
├── settings.json                 ← Default settings (e.g., default agent)
├── CLAUDE.md                     ← Orchestration guide
└── README.md                     ← User documentation
```

## plugin.json Schema

```json
{
  "name": "{kebab-case-name}",
  "version": "1.0.0",
  "description": "{1-2 sentence purpose}",
  "author": {
    "name": "{Author Name}",
    "url": "{homepage}"
  },
  "homepage": "{url}",
  "repository": "{git-url}",
  "license": "SEE LICENSE IN LICENSE",
  "keywords": ["{keyword1}", "{keyword2}"]
}
```

**Critical**: `name` field = command prefix. Users type `/name:command`. Keep it SHORT.

## Command File Template (.md)

```yaml
---
description: "{What it does — shown in /help}"
user-invocable: true
---

# {TITLE}

{System prompt for this command. This is what Claude reads when the user invokes it.}

## ROLE
{Who Claude becomes}

## PROTOCOL
{Step-by-step instructions}

## OUTPUT CONFIGURATION
- Language: {target language}
- Format: {markdown/html/etc}

## CONSTRAINTS
{What NOT to do}
```

## Agent File Template (.md)

```yaml
---
name: plugin-builder
description: "{Role and when activated}"
co-authored-by: {Author} (with Claude Code)
---

# {Role Title}

{You are a... + responsibilities + skills assigned}
```

## Skill File Template (SKILL.md)

```yaml
---
name: plugin-builder
author: {Team/Author}
description: >
  {When to use this skill — trigger phrases and keywords}
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

# {Skill Title}

{Purpose statement}

## Guiding Principle
> *{Philosophy in 1-3 sentences}*

## Procedure
{Step-by-step methodology}

## Quality Criteria
{Acceptance criteria}

## Anti-Patterns
{What NOT to do}
```

## hooks.json Template

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {"type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/startup.sh", "timeout": 10}
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh", "timeout": 15}
        ]
      }
    ]
  }
}
```

## Alias Command Template (for shortcuts)

```yaml
---
description: "Alias → {target-command}. Use /{plugin}:{target-command} instead."
user-invocable: true
---

# Redirect: {alias} → {target-command}

Activate `{target-command}` skill with all arguments passed through: $ARGUMENTS [EXPLICIT]
```

## Packaging as .skill file

Each skill can be packaged as a ZIP with extension `.skill`: [EXPLICIT]
```
sofka-{name}.skill (ZIP containing):
  sofka-{name}/
    SKILL.md
    references/
      body-of-knowledge.md
      state-of-the-art.md
      knowledge-graph.mmd
    prompts/
      metaprompts.md
      use-case-prompts.md
    examples/
      sample-output.md
      sample-output.html
```

## Packaging as .plugin file

The entire plugin can be packaged as a ZIP with extension `.plugin`: [EXPLICIT]
```
{name}.plugin (ZIP containing):
  {name}/
    plugin.json
    settings.json
    CLAUDE.md
    README.md
    agents/*.md
    commands/*.md
    hooks/hooks.json
    scripts/*.sh
```

## Procedure

1. **Ask**: Plugin name, purpose, author, initial commands/agents/skills
2. **Scaffold**: Create directory structure with all templates
3. **Generate**: plugin.json, settings.json, CLAUDE.md, README.md
4. **Create commands**: Verb-first naming, with aliases for each
5. **Create agents**: Role-based, with skills assigned
6. **Create skills**: MOAT structure (references + prompts + examples)
7. **Create hooks**: If automation needed
8. **Verify**: Check all frontmatter valid, all cross-refs correct
9. **Test**: Suggest `claude --plugin-dir ./{name}` to verify

## Usage

Example invocations: [EXPLICIT]

- "/plugin-builder" — Run the full plugin builder workflow
- "plugin builder on this project" — Apply to current context


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
