# Functional Toolbelt — Body of Knowledge

## Canon

The functional toolbelt is a reusable requirements-quality suite, not a single deliverable. It combines six tools: event storming, story mapping, business rule extraction, acceptance criteria, traceability matrix, and anti-pattern detection.

## Required Tool Outputs

| Tool | Required Output | Deterministic Check |
|---|---|---|
| Event storming | Events, commands, actors, aggregates, hot spots. | `event_storming` contains all five lists. |
| Story mapping | Activities, stories, releases, user value. | At least four stories across activities. |
| Business rules | Rule id, type, condition, action, linked use cases. | Every rule has non-empty use case links. |
| Acceptance criteria | Given/When/Then scenarios. | Every scenario has all five fields. |
| Traceability | Requirement to use case to flow to test to AC. | No empty coverage cells. |
| Anti-patterns | Category, severity, text, fix. | Category and severity match assets ruleset. |

## Asset Usage

- `assets/toolbelt-tools.json`: canonical six-tool registry.
- `assets/event-storming-card-template.md`: event card structure.
- `assets/story-map-lane-template.md`: story map lane structure.
- `assets/decision-table-template.md`: business rule decision table structure.
- `assets/gwt-scenario-template.md`: acceptance criteria format.
- `assets/traceability-matrix-schema.json`: traceability coverage requirements.
- `assets/anti-pattern-rules.json`: requirements-quality anti-pattern taxonomy.

## Scripted Report

Use `scripts/compile-functional-toolbelt.py --input <toolbelt.json>` when all six tool sections are available. The script rejects partial packages and traceability gaps so the toolbelt remains deterministic rather than a loose checklist.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---|
| Six-tool coverage | 100% | Input includes all required sections. |
| Traceability coverage | 100% | Requirement rows have use cases, flows, tests, and AC. |
| Rule traceability | 100% | Every business rule links use cases. |
| Anti-pattern actionability | 100% | Each finding has a concrete fix. |
