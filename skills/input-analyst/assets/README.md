# Input Analyst Assets

These assets define the stable offline contract for compiling an input analysis.
They are loaded by `scripts/compile-input-analysis.py` and are intentionally
local-only.

## Files

- `input-analysis-schema.json`: required input fields and output sections.
- `surface-patterns.json`: deterministic typo, punctuation, language, and
  privacy signal patterns.
- `intent-gap-taxonomy.json`: supported gap types, signals, and priorities.
- `quality-calibration.json`: actionability, confidence, and quality thresholds.
- `input-analysis-template.md`: canonical Markdown report skeleton.
- `source-map.md`: local references used by the skill.
