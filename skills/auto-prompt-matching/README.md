# Auto Prompt Matching

Deterministic routing workflow for selecting the best skill or prompt for a user request from the current Alfa indexes.

## Triggers

- auto-prompt-matching
- auto prompt matching
- route this prompt
- match user intent
- which skill should handle
- prompt routing

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the assistant must choose a skill or prompt before executing work. The deliverable is a routing decision with evidence, not the downstream task output.

## Minimum Inputs

- Raw user request
- Any explicit prefix, command, plugin, brand, or repository context
- Desired artifact type or action when present
- Available indexes or skill/prompt files

## Output Format

Markdown routing packet with selected route, confidence band, candidate table, evidence sources, rejected alternatives, coverage gaps, and next action.

## Non-Invention Rule

Only route to skills/prompts discovered in `PRISTINO-INDEX.md`, `.agent/skills_index.json`, prompt metadata, or the `skills/` tree. If evidence is missing, mark `coverage_gap` and ask or hand off.
