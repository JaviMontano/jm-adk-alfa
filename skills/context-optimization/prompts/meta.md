# Context Optimization Meta Prompt

Decide whether `context-optimization` should activate and which deterministic controls are required before optimizing context.

## Activation Check

- Activate when the user asks to optimize context usage, manage a context window, configure progressive loading, prune loaded resources, preserve session state, or reduce token load for a multi-skill workflow.
- Do not activate for ordinary summarization, generic editing, or unrelated performance tuning.
- Require an active task, at least one candidate resource, and either a stated budget or an explicit budget estimate.
- Prefer a narrower domain skill when the request is only about that domain and has no context-window concern.

## Safety Check

- Block if optimization requires deleting evidence needed for validation.
- Warn if session state is requested but no approved persistence target is provided.
- Require `low` prune risk for destructive removal recommendations.
- Require local/offline validation for any machine-readable report.
