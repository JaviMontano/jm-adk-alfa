# Prompt Creator

Deterministic prompt artifact generator for agentic ecosystems. It creates reusable prompt files, gap packets, or redirects for adjacent skills based on the prompt type and source-agent evidence.

## Triggers

- prompt-creator
- create a prompt
- write a handoff prompt
- generate a meta prompt
- committee deliberation prompt
- validation prompt
- fallback prompt
- multi-agent prompt design

## Allowed Tools

- Read
- Grep
- Glob
- Bash
- Write
- Edit

## Quick Use

Use this skill when the deliverable is a prompt file for an existing or explicitly named agent. If the request is for a full agent constitution, route to `agent-constitution-creator`. If it is for a workflow step definition, route to `workflow-creator`.

## Minimum Inputs

- Prompt type or enough intent to classify it
- Owning agent ID
- Source agent file path or explicit statement that the source is missing
- Desired filename or scenario/topic
- Success criteria and downstream boundary

## Output Format

Return a Markdown packet with decision (`write_prompt`, `ask`, `redirect`, `decline`), generated prompt artifact or gap packet, source evidence, placeholder inventory, validation results, and next action.

## Deterministic Gate

Before marking a prompt artifact validated, apply `assets/prompt-contract-checklist.md` and run:

```bash
bash skills/prompt-creator/scripts/check.sh
python3 -B skills/prompt-creator/scripts/validate_prompt_artifact.py <prompt-file.md>
```
