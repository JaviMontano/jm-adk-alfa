# Design Skill — Body of Knowledge

## Canon

`design-skill` produces a reviewable SKILL.md design specification. It validates frontmatter, procedure structure, quality criteria, anti-patterns, edge cases, tool rationale, and MOAT score before any deployable skill file is written.

## Deterministic Rules

| Rule | Requirement |
|------|-------------|
| Skill name | Kebab-case and matches intended directory slug. |
| Procedure | 5-10 ordered steps with action, input, output, and evidence tag. |
| Quality criteria | 4-6 measurable pass/fail statements. |
| Anti-patterns | 4-6 specific mistakes, not correct behaviors. |
| Edge cases | 3-5 boundary scenarios with expected behavior. |
| Tools | Least-privilege profile with rationale for every tool. |
| MOAT score | Total must be at least 75. |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Frontmatter required fields | 100 percent |
| Procedure step coverage | 5-10 structured steps |
| Tool overreach | 0 unnecessary tools |
| MOAT score | >= 75 |
| Offline validation | `scripts/check.sh` passes |
