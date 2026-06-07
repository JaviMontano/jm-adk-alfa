# AI Documentation Body of Knowledge

## Canon

Source-backed documentation starts from evidence, not from desired prose.
The skill treats code, API specs, configs, tests, existing docs, and user input
as source types with explicit evidence ids.

## Documentation Targets

| Target | Purpose | Required Evidence |
|--------|---------|-------------------|
| README | developer onboarding and project overview | code, tests, existing docs, config |
| API_REFERENCE | endpoint and schema documentation | API spec, handlers, tests |
| RUNBOOK | operational procedures | config, deploy scripts, alerts, tests |
| ARCHITECTURE_NOTE | structural decisions and boundaries | code layout, ADRs, configs |
| QUICKSTART | first successful local run | README, package config, test command |
| CHANGELOG_DRAFT | release summary | commits, diff summary, user request |

## Determinism Rules

- Unknown source behavior becomes a gap.
- Every generated section must cite evidence ids.
- Blocking gaps force `validation.status` to `block`.
- Output paths must be safe relative paths.
- External documentation generators are optional aids, not required validation.
