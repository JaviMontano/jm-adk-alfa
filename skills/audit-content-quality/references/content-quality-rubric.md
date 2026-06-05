# Content Quality Scoring Rubric

Human-readable mirror of `assets/scoring-rubric.json`. The JSON asset is the
source of truth for validators.

Each dimension is scored from `0` to `10`.

## Dimensions

| Dimension | 10 | 8 | 6 | 4 | 0 |
|---|---|---|---|---|---|
| Completeness | Frontmatter and all required body sections are present, including examples or references. | One minor field or section is thin. | Two optional fields or one major section is absent. | Multiple sections are missing. | Only frontmatter or no useful body content. |
| Description Quality | Clear purpose, trigger phrases, when-to-use, and when-not-to-use guidance. | Clear purpose and triggers but no negative guidance. | Describes what but not when to trigger. | Vague or generic description. | Missing or single-word description. |
| Procedure Clarity | Numbered steps, tool-aware actions, inputs/outputs, and branch logic. | Numbered steps with tools but some outputs are thin. | Steps exist but are not tool-aware or lack branch logic. | Prose without clear steps. | No procedure section. |
| Quality Criteria | Five or more measurable criteria with evidence markers. | Four or more criteria, mostly testable. | Three criteria, some vague. | One or two criteria, not testable. | No quality criteria section. |
| Anti-Patterns | Five or more anti-patterns with why-it-matters explanations. | Four explained anti-patterns. | Three anti-patterns, some thin. | One or two unlabeled anti-patterns. | No anti-pattern section. |
| Edge Cases | Five or more edge cases covering empty inputs, boundaries, unusual states, and error paths. | Four edge cases with good variety. | Three edge cases with limited variety. | One or two edge cases. | No edge cases section. |

## Formula

- `total_score = sum(six dimension scores)`
- `percentage = total_score / 60 * 100`
- `average_score = mean(total_score)`
- `average_percentage = mean(percentage)`
- `systematic_gap = dimension_average < 6.0`

## Grades

| Grade | Percentage |
|---|---:|
| A | 90-100 |
| B | 80-89.999 |
| C | 70-79.999 |
| D | 60-69.999 |
| F | 0-59.999 |

## Bottom Skills

Sort scorecards by `total_score` ascending, then skill name ascending. Report up
to three bottom skills. Priority is `P1` for F, `P2` for D/C, and `P3` for B/A.
