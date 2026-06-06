<!--
generated-by: scripts/scaffold-skill.py
generated-for: guardrails-management
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Guardrails Management

Detect, confirm, store, list, remove, and enforce user-declared working rules as
deterministic JSON guardrails.

## Triggers

- guardrails-management
- guardrail
- guideline
- constraint
- from now on
- always use
- never use
- prefer
- avoid

## Allowed Tools

- Read
- Write
- Edit
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the user declares a durable working rule or asks to inspect,
change, remove, or enforce saved rules.

Never persist a new rule from implication alone. Create a proposal, classify it,
check duplicates/conflicts, ask for explicit confirmation, then write only the
target JSON file if confirmed.

## Output Format

Markdown or JSON with:

- Operation and source utterance
- Proposed or affected rule entry
- Classification and target file
- Duplicate/conflict review
- Confirmation state
- Persistence action
- Validation evidence
- Risks and assumptions

JSON operation packets can be validated offline with:

```bash
bash skills/guardrails-management/scripts/check.sh
```
