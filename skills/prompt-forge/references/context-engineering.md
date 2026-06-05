# Prompt Forge Context Engineering

## Layers

- Hot context: system prompt, current user turn, output contract.
- Warm context: user-supplied files, style guides, policy snippets.
- Cold context: retrieved data or tool outputs supplied at runtime.

## Rules

- Keep stable behavior in the Playbook.
- Keep long-lived facts in knowledge surfaces when the target platform supports them.
- Mark missing context as a coverage gap instead of inventing it.
- Define how retrieved snippets must be cited or rejected.
