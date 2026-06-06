# Example Input

Run `context-optimization` for phase `implementation`.

Constraints:

- max context tokens: 24000
- target utilization: 85 percent
- naive full loading: 30000 tokens
- candidate skills: `session-protocol`, `tasklog-management`,
  `context-window-management`, `seo-technical`
- persist essential session state only if authorized

Create a loading, pruning, lazy-load, and session-state plan with metrics.
