# Auto Prompt Matching - Body of Knowledge

## Canon

Prompt matching is a routing decision. It must be deterministic, auditable, and reversible because it decides which downstream workflow receives the user's request. The route is valid only when the selected skill or prompt exists in inspected sources.

## Routing Inputs

| Input | Use |
|---|---|
| Explicit prefix or command | Highest-priority evidence when it maps to an existing skill/prompt |
| User request terms | Normalized intent tokens and quoted exact terms |
| Artifact type | Narrows candidates such as HTML, XLSX, DOCX, PDF, PR, dashboard, or prompt |
| Brand/context | Narrows candidates when source metadata supports that scope |
| Source indexes | `PRISTINO-INDEX.md`, `.agent/skills_index.json`, prompt metadata, and `skills/*/SKILL.md` |

## Scoring Rules

- Exact explicit prefix to existing skill/prompt wins unless the target is missing or deprecated.
- Exact trigger match outranks fuzzy purpose match.
- A narrow skill beats a broad skill when both cover the request.
- Penalize candidates whose scope explicitly excludes the request.
- Use alphabetical slug only as the final tie-breaker for reproducibility.
- Do not route when evidence is missing, contradictory, or below threshold; ask one narrow clarification.

## Confidence Bands

| Band | Meaning | Action |
|---|---|---|
| `route` | Strong source-backed match with no unresolved tie | Select route and provide next action |
| `ask` | Multiple plausible candidates or missing key intent | Ask one targeted clarification |
| `decline` | No indexed capability or unsafe/unsupported request | Decline or hand off to discovery |

## Failure Modes

- Inventing a skill because its name sounds plausible.
- Treating memory of a plugin as evidence when the current repo/index does not list it.
- Picking the broadest skill even when a narrow skill exists.
- Returning only a confidence number without score components.
- Hiding `coverage_gap` when an index cannot be read.
- Executing the routed task instead of returning the route.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Source-backed candidates | 100% | Every candidate exists in inspected sources |
| Score transparency | 100% | Each route lists score components and tie-breaks |
| False-positive rejection | 100% | Unsupported/weather/generic requests do not activate |
| Coverage gap visibility | 100% | Missing or stale indexes are reported |
| Downstream separation | 100% | Routing output does not execute the selected skill |

## References

- `PRISTINO-INDEX.md`
- `.agent/skills_index.json`
- `skills/*/SKILL.md`
- `prompts/**/*.md`
- `assets/routing-checklist.md`
