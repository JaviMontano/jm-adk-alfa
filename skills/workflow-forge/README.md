# Workflow Forge

Creates slash-command workflow definitions with phase maps, named agent
handoffs, verification checkpoints, and deterministic validation.

## Triggers

- workflow-forge
- create a workflow
- forge a slash command
- turn this process into phases
- define an agent workflow

## Allowed Tools

- Read
- Write
- Edit
- Bash
- Glob
- Grep

## Quick Use

Use this skill when the user needs a repeatable command workflow, not a one-off
task list. Start by identifying the command, deliverable, agents, skills,
phases, checkpoints, and final verification gate.

## Deterministic Check

```bash
bash skills/workflow-forge/scripts/check.sh
```

The check compiles a valid workflow fixture, validates JSON output, and confirms
invalid fixtures fail closed.

## Output Format

Markdown workflow definition with frontmatter, phase map, checkpoints, quality
gates, failure handling, example dialogue, validation evidence, and limits.
