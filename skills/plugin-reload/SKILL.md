---
name: plugin-reload
argument-hint: "plugin-name"
description: 
  Deploys, validates, and reloads Claude Code plugins from local development.
  Activates when the user says "reload plugins", "deploy plugin", "sync plugins",
  "update local plugins", or "verify plugin structure". Also triggers on mentions of
  plugin validation, plugin deployment, or post-change verification. Use this skill even if
  the user just says something broke after editing a plugin — it diagnoses structure issues.
model: opus
context: fork
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
version: 1.0.0
---

# Plugin Reload & Deploy

> Validates plugin structure, syncs files, and reloads plugins in Claude Code.

## Protocol

### Phase 1: Validate Plugin Structure

For the target plugin directory, verify:

1. **`.claude-plugin/plugin.json`** exists and has valid JSON with `name`, `version`, `description`
2. **`commands/`** directory exists with `.md` files (each with `description:` + `user-invocable: true` frontmatter)
3. **`agents/`** directory exists with `.md` files (each with `name:` + `description:` frontmatter)
4. **`skills/`** directory exists with subdirectories containing `SKILL.md`
5. **`hooks/hooks.json`** exists and is valid JSON
6. **`CLAUDE.md`** exists as the orchestrator hub

Report counts: X commands, X agents, X skills, X hooks.

### Phase 2: Check for Common Issues

- Orphaned files (commands referencing non-existent agents/skills)
- Missing `sofka-` prefix in agent/skill names
- Stale version numbers
- Invalid hook matchers
- Broken file references in CLAUDE.md

### Phase 3: Sync to Active Location

If the plugin is under `~/skills/plugins/`, it's already in the active location.
Verify Claude Code can see it by checking:

```bash
# Plugin should be discoverable
ls ~/.claude/plugins/ 2>/dev/null
# Or check if it's in the project settings
cat .claude/settings.json 2>/dev/null | grep -i plugin
```

### Phase 4: Reload

Instruct the user to run:
```
/reload-plugins
```

This reloads all commands, agents, skills, hooks, and MCP servers without restarting Claude Code.

**If hooks changed**: Run `/hooks` to verify hook registration.
**If LSP changed**: Full restart required (`exit` + relaunch Claude Code).

### Phase 5: Verify

After reload, verify:
1. Run `/sdf:menu` — should show command palette
2. Check a few random skills are accessible: `/sdf:demo`, `/sdf:run-auto`
3. Verify hook activation: check if `.discovery/` gets created on next session

## Output

```
=== Plugin Reload Report ===
Plugin: {name} v{version}
Location: {path}
Commands: {count} ✅
Agents: {count} ✅
Skills: {count} ✅
Hooks: {count} ✅
Status: READY — run /reload-plugins to activate
```

## Edge Cases

| Scenario | Action |
|----------|--------|
| Plugin JSON invalid | Show error, suggest fix |
| Missing directories | Create them with `mkdir -p` |
| Duplicate skill names | Flag conflict and suggest rename |
| Hook script not executable | Run `chmod +x` on scripts |

## Usage

Example invocations:

- "/plugin-reload" — Run the full plugin reload workflow
- "plugin reload on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
