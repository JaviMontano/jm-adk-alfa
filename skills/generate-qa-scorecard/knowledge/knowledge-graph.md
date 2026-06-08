# Generate QA Scorecard - Knowledge Graph

## Core Concepts

- [[evidence-source]] provides findings and evaluation scope.
- [[quality-dimension]] maps findings to one of 7 canonical dimensions.
- [[status-rule]] maps severity counts to pass, warn, fail, or na.
- [[score-math]] calculates total score, evaluated max, percentage, and grade.
- [[priority-action]] ranks remediation by status, impact, and finding counts.
- [[reduced-scope-note]] discloses unevaluated dimensions.
- [[guardian-decision]] blocks inconsistent scorecards.

## Flow

- [[evidence-source]] -> [[quality-dimension]]
- [[quality-dimension]] -> [[status-rule]]
- [[status-rule]] -> [[score-math]]
- [[status-rule]] -> [[priority-action]]
- [[quality-dimension]] -> [[reduced-scope-note]]
- [[score-math]] -> [[guardian-decision]]
- [[priority-action]] -> [[guardian-decision]]
