# Example Input

Run a content quality audit for `skills/sample-plugin`.

Discovered files:

- `skills/sample-plugin/alpha/SKILL.md`: complete frontmatter, triggers,
  numbered tool-aware procedure, five quality criteria, four anti-patterns,
  and four edge cases.
- `skills/sample-plugin/beta/SKILL.md`: frontmatter exists, procedure has vague
  steps, quality criteria are thin, anti-patterns lack explanations, and edge
  cases have limited handling.
- `skills/sample-plugin/gamma/SKILL.md`: complete frontmatter and criteria, but
  only two anti-patterns and two edge cases.

Return per-skill scorecards, bottom skills, plugin average, systematic gaps,
coverage, and warnings.
