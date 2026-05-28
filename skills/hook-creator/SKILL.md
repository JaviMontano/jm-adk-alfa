---
name: hook-creator
description: 
  This skill should be used when the user asks to "create a hook",
  "add format-on-save", "set up a file guard", "automate on tool use",
  or mentions Claude Code hooks, PreToolUse, PostToolUse, or event-driven automation. [EXPLICIT]
  It generates Claude Code hook configurations for lifecycle events including format-on-save, file guards, notifications, and quality gates. [EXPLICIT]
  Use this skill whenever the user wants deterministic automation at Claude Code lifecycle points, even if they don't explicitly ask for "hook creator". [EXPLICIT]
argument-hint: event-name [handler-type]
model: opus
context: fork
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0.0
---

# Hook Creator

Create event-driven hooks — deterministic automation that fires at Claude Code lifecycle points. Hooks are NOT LLM judgment; they're programmatic control. [EXPLICIT]

## Assumptions & Limits

- **Assumes** the behavior should be deterministic and repeatable (for LLM-based judgment, use prompt/agent hook types)
- **Limit**: Hooks run synchronously — long operations block Claude. Keep commands under 10s (configurable via `timeout`)
- **Limit**: Exit code 2 (block) only works on PreToolUse, UserPromptSubmit, TeammateIdle, TaskCompleted
- **Trade-off**: Command hooks are fast but brittle (shell parsing); prompt hooks are flexible but add latency (~2s per evaluation)

### When NOT to create a hook

| Situation | Better alternative |
|---|---|
| Complex multi-file analysis | Agent (subagent) |
| User-invoked workflow | Skill |
| Always-on response style | Output style |
| Project-specific rules | CLAUDE.md |

## Usage

```
/hook-creator PostToolUse command    # auto-format on file save
/hook-creator PreToolUse             # interview mode — determine handler type
```

Parse `$1` as event name, `$2` as handler type (default: `command`). If missing, interview: [EXPLICIT]
1. What should happen automatically? (action description)
2. When? (before/after tool use, session start, on stop, etc.)
3. Should it block the action or just react? (blocking = exit 2)

## Before Creating

1. **Read existing hooks**: `Read .claude/settings.json` -> check `hooks` key. Also `Read ~/.claude/settings.json`
2. **Verify event name** against the supported list below
3. **Check for conflicts**: Multiple hooks on same event+matcher can interact unexpectedly

## Event Reference (16 events)

| Event | When | Can Block? | Matcher On | Stdin Fields |
|---|---|---|---|---|
| `PreToolUse` | Before tool executes | Yes | Tool name | tool_name, tool_input |
| `PostToolUse` | After tool succeeds | No | Tool name | tool_name, tool_input, tool_output |
| `PostToolUseFailure` | After tool fails | No | Tool name | tool_name, tool_input, error |
| `UserPromptSubmit` | Before processing user input | Yes | -- | user_prompt |
| `Stop` | Claude finishes responding | No | -- | stop_hook_active |
| `SessionStart` | Session begins/resumes | No | Source | source |
| `SessionEnd` | Session terminates | No | -- | -- |
| `Notification` | Notification sent | No | Type | type, message |
| `SubagentStart` | Subagent spawned | No | -- | agent_name |
| `SubagentStop` | Subagent finished | No | -- | agent_name |
| `PreCompact` | Before context compaction | No | -- | -- |
| `TeammateIdle` | Teammate going idle | Yes | -- | teammate_name |
| `TaskCompleted` | Task marked done | Yes | -- | task_id, task_description |
| `ConfigChange` | Config file changes | No | Source type | config_path |
| `WorktreeCreate` | Worktree created | No | -- | worktree_path |
| `WorktreeRemove` | Worktree removed | No | -- | worktree_path |

SessionStart source values: `startup`, `resume`, `clear`, `compact` [EXPLICIT]
Notification type values: `permission_prompt`, `idle_prompt` [EXPLICIT]

## Handler Types

### Command (fast, deterministic)
```json
{
  "type": "command",
  "command": "npx prettier --write $CLAUDE_TOOL_ARG_file_path",
  "matcher": "Edit|Write",
  "timeout": 10000
}
```
**Stdin**: JSON with event data. **Exit 0**: proceed (stdout -> context). **Exit 2**: block (stderr -> Claude). **Other**: proceed (stderr -> log).

### Prompt (LLM judgment, single-turn)
```json
{
  "type": "prompt",
  "prompt": "Evaluate if the task is truly complete. Check all requirements are met.",
  "matcher": null
}
```
Returns `{"ok": true/false, "reason": "..."}`. Uses Haiku by default. Good for subjective quality checks. [EXPLICIT]

### Agent (multi-turn verification)
```json
{
  "type": "agent",
  "prompt": "Read the changed files and verify they pass the test suite. Run tests if needed.",
  "timeout": 60000
}
```
Full subagent with tool access. 60s default timeout, max 50 tool turns. Use when verification needs codebase state. [EXPLICIT]

### HTTP (webhook)
```json
{
  "type": "http",
  "url": "https://hooks.example.com/events",
  "headers": { "Authorization": "Bearer ${API_TOKEN}" },
  "allowedEnvVars": ["API_TOKEN"]
}
```
POST event data to endpoint. Cannot be added via `/hooks` menu — requires direct JSON editing. [EXPLICIT]

## Matcher Patterns

Matchers are **regex** applied to the event's matcher field: [EXPLICIT]

| Pattern | Matches | Use Case |
|---|---|---|
| `Edit\|Write` | Edit OR Write | Format-on-save |
| `Bash` | Only Bash | Command auditing |
| `mcp__.*` | Any MCP tool | MCP monitoring |
| `Edit` | Exactly Edit | Targeted formatting |
| `startup` | Session start (not resume) | First-run setup |
| `compact` | After compaction | Re-inject critical context |

## Configuration Scopes

| Scope | File | Shared? | Precedence |
|---|---|---|---|
| Personal | `~/.claude/settings.json` | No | All projects |
| Project shared | `.claude/settings.json` | Yes (git) | This project |
| Project local | `.claude/settings.local.json` | No | This project |
| Plugin | `hooks/hooks.json` | With plugin | Plugin scope |
| Skill/Agent | Frontmatter `hooks:` | With skill | Skill scope |

## Battle-Tested Patterns

### Auto-format on save
```json
{ "PostToolUse": [{ "type": "command", "command": "npx prettier --write $CLAUDE_TOOL_ARG_file_path", "matcher": "Edit|Write" }] }
```

### Block edits to lock files
```json
{ "PreToolUse": [{ "type": "command", "command": "echo $CLAUDE_TOOL_INPUT | jq -r '.file_path' | grep -qE '(package-lock|yarn\\.lock|\\.lock)' && (echo 'Lock files are auto-generated' >&2; exit 2) || exit 0", "matcher": "Edit|Write" }] }
```

### macOS notification on idle
```json
{ "Notification": [{ "type": "command", "command": "osascript -e 'display notification \"Claude needs attention\" with title \"Claude Code\"'", "matcher": "permission_prompt|idle_prompt" }] }
```

### Re-inject context after compaction
```json
{ "SessionStart": [{ "type": "command", "command": "cat .claude/critical-context.md", "matcher": "compact" }] }
```

### Quality gate before task completion
```json
{ "TaskCompleted": [{ "type": "prompt", "prompt": "Verify all acceptance criteria are met. Check that tests pass and no regressions were introduced." }] }
```

## Gotchas & Debugging

| Problem | Cause | Fix |
|---|---|---|
| Stop hook infinite loop | Hook triggers Claude, which triggers Stop again | Check `stop_hook_active` field — if true, exit 0 immediately |
| JSON parse error in stdout | Shell profile `echo` statements pollute output | Guard with `if [[ $- == *i* ]]` |
| Hook doesn't fire | Wrong event name or matcher miss | Debug with `claude --debug` or Ctrl+O verbose mode |
| Hook blocks unexpectedly | Exit code 2 from unexpected path | Test command standalone: `echo '{}' \| your-command` |
| Timeout kills hook | Operation too slow | Increase `timeout` or make command async |

## Validation Gate

- [ ] Event name is one of the 16 supported events
- [ ] Handler type is valid (command, prompt, agent, http)
- [ ] If blocking (exit 2): event supports blocking (PreToolUse, UserPromptSubmit, TeammateIdle, TaskCompleted)
- [ ] Matcher regex is valid (test with `echo "ToolName" | grep -qE 'pattern'`)
- [ ] Command handles JSON stdin correctly (not expecting positional args)
- [ ] No infinite loop risk in Stop hooks (checks stop_hook_active)
- [ ] Timeout appropriate for operation complexity
- [ ] Saved to correct scope file
- [ ] Tested standalone before deployment: `echo '{"tool_name":"Edit"}' | your-command`

---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
