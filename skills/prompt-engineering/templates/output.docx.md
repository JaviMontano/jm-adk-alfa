# DOCX Output Template - Prompt Engineering

## Document Structure (for python-docx generation)

```
Title: "Prompt Library: {{project_name}}"
Subtitle: "Designed with JM Labs Prompt Engineering"

Section 1: Executive Summary
  - Task description
  - Pattern selected (with justification)
  - Key metrics (accuracy, consistency, token efficiency)

Section 2: Prompt Catalog
  For each prompt:
  - Name, version, pattern type
  - Full prompt text (in code block)
  - Test results (at least three inputs with outputs)
  - Confidence score

Section 3: Evaluation Matrix
  Table: prompt × metric × score

Section 4: Recommendations
  - Improvement opportunities
  - Model-specific adaptations
  - Guardrail enhancements

Footer: "JM Labs — {{created_date}}"
```

## Formatting Rules
- Heading 1: Arial Bold 18pt, Navy #0A122A
- Heading 2: Arial SemiBold 14pt, Gold #FFD700
- Body: Arial Regular 11pt
- Code: Monospace 10pt, gray background
- Tables: Gold header row, alternating light/dark rows
