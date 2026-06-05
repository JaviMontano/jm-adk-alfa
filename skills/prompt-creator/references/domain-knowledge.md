# Domain Knowledge - prompt creator

## Overview

This reference provides foundational knowledge for deterministic prompt artifact generation. [EXPLICIT]

## Key Concepts

| Concept | Definition | Relevance |
|---------|-----------|-----------|
| Prompt artifact | Reusable markdown prompt file with frontmatter, sections, placeholders, and validation gate | Direct output of the skill [EXPLICIT] |
| Prompt type matrix | Canonical list of generated and redirected prompt types | Prevents arbitrary prompt categories [EXPLICIT] |
| Source agent | Agent file or explicit user-provided source that grounds the prompt | Prevents invented identity and authority [EXPLICIT] |
| Evidence taxonomy | [CÓDIGO]/[CONFIG]/[INFERENCIA]/[SUPUESTO] classification | Required for review and validation claims [EXPLICIT] |

## Best Practices

1. Always gather source agent evidence before writing. [EXPLICIT]
2. Return `ask` or `coverage_gap` when a required source is missing. [EXPLICIT]
3. Use descriptive snake_case placeholders. [EXPLICIT]
4. Separate generated prompt content from validation evidence. [EXPLICIT]
5. Validate generated artifacts with `scripts/validate_prompt_artifact.py` when available. [EXPLICIT]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|-------------|-------------|-------------------|
| Invented agent identity | Prompt grants authority that does not exist | Require source file or gap packet |
| Generic placeholders | Orchestrator cannot bind values reliably | Use descriptive snake_case placeholders |
| Context explosion | Handoffs leak hidden reasoning or irrelevant history | Split pass vs omit sections |
| Committee convergence | Agents lose independent judgment | Require independent first-pass evaluation |
| Severity-free validation | Feedback cannot be triaged | Use critical/major/minor levels |

## Integration Points

- This skill may be invoked by orchestrator skills in the pipeline. [EXPLICIT]
- Prompt artifacts may be consumed by downstream agents or workflow definitions. [EXPLICIT]
- Script validation provides deterministic regression coverage. [EXPLICIT]
