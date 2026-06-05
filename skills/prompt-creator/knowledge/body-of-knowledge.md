# Prompt Creator - Body of Knowledge

## Canon

Prompt creation is a contract-design task. A good prompt artifact narrows agent behavior without hiding uncertainty, inventing source context, or executing the downstream task. Deterministic prompt creation requires stable prompt types, explicit source files, required sections, validated placeholders, and a visible failure path.

## Prompt Type Families

| Family | Types | Deterministic Requirement |
|---|---|---|
| Single-agent behavior | `meta_prompt`, `system_user_pair` | One behavioral aspect or one scenario only |
| Task transfer | `handoff_prompt` | Separate context to pass from context to omit |
| Committee work | `committee_deliberation`, `committee_synthesis` | Independent first pass, rubric, conflict handling, confidence weighting |
| Quality and recovery | `validation_prompt`, `fallback_prompt` | Severity levels, escalation path, user communication |
| Redirects | `agent_system_prompt`, `workflow_step_prompt` | Route to specialized skills without generating here |

## Deterministic Inputs

| Input | Use |
|---|---|
| Prompt type | Selects required sections from `assets/prompt-type-matrix.json` |
| Owning agent ID | Binds artifact to a real or explicit target |
| Source agent file | Grounds tone, constraints, authority, and limits |
| Existing prompt paths | Prevents duplicate or accidental overwrite |
| Success criteria | Defines completion and validator behavior |
| Downstream boundary | Prevents the prompt artifact from doing the task itself |

## Anti-Patterns

- Inventing an agent constitution or tool contract because it sounds plausible.
- Passing the entire conversation in a handoff prompt.
- Mixing reasoning, formatting, restrictions, and style in one meta prompt.
- Letting committee agents read one another's answers before independent evaluation.
- Returning validation feedback without severity levels or actionable locations.
- Using generic placeholders such as `{{x}}` or `{{var}}`.
- Pulling remote templates or fonts into prompt generation.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Source grounding | 100% | Prompt artifact names source agent path or gap |
| Type conformance | 100% | Required sections match type matrix |
| Placeholder quality | 100% | Descriptive snake_case placeholders only |
| No-invention compliance | 100% | No invented agents, tools, files, or dates |
| Script validator pass | 100% | `validate_prompt_artifact.py` returns pass for validated artifacts |

## References

- `assets/prompt-contract-checklist.md`
- `assets/prompt-type-matrix.json`
- `scripts/validate_prompt_artifact.py`
- `references/domain-knowledge.md`
