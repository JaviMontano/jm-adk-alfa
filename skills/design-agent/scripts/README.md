# Design Agent Scripts

## `validate_design_agent_spec.py`

Validates a frozen JSON agent design spec against local assets:

- required and supported frontmatter fields;
- forbidden plugin subagent fields;
- tools/disallowedTools exclusivity;
- skill assignment and execution flow coverage;
- operating principle specificity;
- deterministic maxTurns calculation;
- evidence tags and exact dates.

## `check.sh`

Runs offline fixtures. It accepts valid specs and rejects specs with forbidden hooks, tools/disallowedTools conflicts, invalid maxTurns, missing flow coverage, generic principles, or invalid agent names.
