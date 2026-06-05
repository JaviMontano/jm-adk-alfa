# Example Output

## Summary

| Metric | Value |
|---|---:|
| Plugin root | `skills/sample-plugin` |
| Total skills | 3 |
| Average score | 42.00 / 60 |
| Average percentage | 70.00% |
| Grade | C |
| Systematic gaps | 1 |

## Scorecards

| Skill | Completeness | Description Quality | Procedure Clarity | Quality Criteria | Anti-Patterns | Edge Cases | Total | Grade | Lowest Dimension |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| alpha | 10 | 8 | 8 | 10 | 8 | 8 | 52 / 60 | B | description_quality |
| beta | 6 | 6 | 5 | 6 | 5 | 6 | 34 / 60 | F | procedure_clarity |
| gamma | 8 | 8 | 7 | 8 | 4 | 5 | 40 / 60 | D | anti_patterns |

Rationales:

- alpha description_quality: [DOC] Description has clear purpose and trigger phrases.
- beta procedure_clarity: [DOC] Procedure has steps but limited tool-aware outputs.
- gamma anti_patterns: [DOC] Only two anti-patterns are listed.

## Bottom Skills

| Rank | Skill | Total | Grade | Priority | Recommendation |
|---:|---|---:|---|---|---|
| 1 | beta | 34 | F | P1 | Add tool-aware procedure outputs and explain at least three anti-patterns. |
| 2 | gamma | 40 | D | P2 | Add three explained anti-patterns and two edge cases with handling. |
| 3 | alpha | 52 | B | P3 | Add negative activation guidance to move Description Quality toward 10. |

## Systematic Gaps

| Dimension | Average | Priority | Recommendation |
|---|---:|---|---|
| anti_patterns | 5.67 | P2 | Add at least three anti-patterns with why-it-matters explanations to every low-scoring skill. |

## Coverage

| Discovered | Scored | Skipped |
|---:|---:|---:|
| 3 | 3 | 0 |

## Warnings

None.
