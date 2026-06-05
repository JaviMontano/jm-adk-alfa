# Routing Checklist

Use this checklist before finalizing an `auto-prompt-matching` routing decision.

## Source Checks

- Inspect explicit prefix or command first.
- Inspect `PRISTINO-INDEX.md`, `.agent/skills_index.json`, relevant `skills/*/SKILL.md`, or prompt metadata.
- Include only candidates found in inspected sources.
- Record missing or stale sources as `coverage_gap`.

## Score Components

| Component | Points |
|---|---:|
| Explicit valid prefix or command | 40 |
| Exact trigger or slug/name match | 30 |
| Purpose/description match | 25 |
| Artifact type or output format match | 20 |
| Brand/context fit | 10 |
| Narrower scope than alternatives | 10 |
| Negative scope or unsupported capability | -30 |
| Source missing or stale | -20 |

## Confidence Bands

- `route`: selected candidate has strong source-backed evidence and no unresolved tie.
- `ask`: two or more plausible candidates remain tied, or a required intent dimension is missing.
- `decline`: no candidate exists in inspected sources or the request asks for unsupported routing.

## Tie-Break Order

1. Explicit valid prefix.
2. Exact trigger.
3. Exact slug/name.
4. Stronger purpose evidence.
5. Narrower scope.
6. Fewer penalties.
7. Alphabetical slug, only if the route remains semantically equivalent.

## Final Gate

- Selected route exists in source.
- Candidate table explains rejected alternatives.
- No invented skill, prompt, plugin, or score.
- Downstream task is not executed inside the routing response.
