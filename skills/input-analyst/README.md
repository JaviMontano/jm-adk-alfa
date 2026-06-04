# Input Analyst

Pre-processing layer that analyzes raw user input — detecting surface errors, performing root-cause analysis (5 Whys), impact tracing (7 So-Whats), and intent gap analysis — then reformulates into a precise, actionable prompt.

## Triggers

- input-analyst

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when raw input is vague, typo-heavy, emotionally loaded,
under-scoped, or likely to route downstream work incorrectly.

For a deterministic offline artifact:

```bash
python3 skills/input-analyst/scripts/compile-input-analysis.py \
  --input skills/input-analyst/scripts/fixtures/input-analysis-input.json \
  --output /tmp/input-analysis.md
```

## Output Format

Markdown or JSON with surface errors, 5 Whys, 7 So-Whats, intent gaps,
ambiguity register, actionability score, clarified prompt, routing hints,
privacy flags, and confidence.
