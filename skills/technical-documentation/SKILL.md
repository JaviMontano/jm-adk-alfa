---
name: technical-documentation
description: README generation, API endpoint docs from Cloud Functions, ADR templates, ops runbooks, and developer onboarding guides
version: 1.0.0
status: production
owner: Javier Montaño
tags: [documentation, readme, api-docs, adr, runbooks, onboarding]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 101 — Technical Documentation {Documentation}

## Purpose
Generate and maintain living technical documentation that accelerates developer onboarding, documents architectural decisions, provides operational runbooks, and auto-documents Cloud Functions API endpoints. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Living Docs**: Documentation that drifts from code is worse than no documentation. Docs are updated in the same PR as code changes. [EXPLICIT]
2. **Law of Audience Fit**: Each doc type serves a specific audience. README = new contributor. ADR = future architect. Runbook = on-call engineer. API docs = consumer. [EXPLICIT]
3. **Law of Automation**: Everything that can be generated from source code should be. Manual documentation is reserved for context, decisions, and intent. [EXPLICIT]

## Protocol

### Phase 1 — README.md Generation
1. Structure: Project name, description, tech stack, prerequisites, setup instructions, available scripts, deployment, contributing guidelines. [EXPLICIT]
2. Include badges: CI status, coverage, version, license. [EXPLICIT]
3. Setup instructions must be copy-paste executable — test on clean machine. [EXPLICIT]
4. Update README in same PR when setup process changes. [EXPLICIT]

### Phase 2 — API Documentation
1. Extract Cloud Functions endpoints from source: function name, HTTP method, path, request/response types. [EXPLICIT]
2. Use JSDoc/TSDoc comments on function handlers — auto-generate docs via `typedoc` or custom script. [EXPLICIT]
3. Document authentication requirements, rate limits, error codes per endpoint. [EXPLICIT]
4. Output: Markdown file or hosted docs page (e.g., Swagger UI for REST, or custom Markdown). [EXPLICIT]

### Phase 3 — ADRs, Runbooks & Onboarding
1. **ADR (Architecture Decision Record)**: Template in `docs/adr/` — `NNN-title.md` with Status, Context, Decision, Consequences. [EXPLICIT]
2. **Runbooks**: `docs/runbooks/` — step-by-step procedures for: deploy, rollback, incident response, database migration, scaling. [EXPLICIT]
3. **Onboarding guide**: `docs/onboarding.md` — Day 1 setup, codebase overview, key contacts, access requests, first PR workflow. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Project metadata + scripts | `README.md` with badges, setup, scripts |
| Cloud Functions source code | API endpoint documentation (Markdown) |
| Architectural decision | ADR document in `docs/adr/` |
| Operational procedure | Runbook in `docs/runbooks/` |
| Team onboarding needs | `docs/onboarding.md` guide |

## Quality Gates — 5 Checks

1. **README setup works on clean machine** — tested quarterly by new team member or fresh clone. [EXPLICIT]
2. **API docs match deployed functions** — generated from source, not manual. [EXPLICIT]
3. **ADR exists for every major decision** — framework choice, database schema, auth strategy. [EXPLICIT]
4. **Runbook exists for every ops procedure** — deploy, rollback, incident, migration. [EXPLICIT]
5. **Docs updated in same PR as code changes** — enforced by PR checklist. [EXPLICIT]

## Edge Cases

- **Private endpoints**: Document internally only. Do not expose in public API docs.
- **Deprecated APIs**: Mark with `@deprecated` tag. Include removal timeline and migration path.
- **Multi-language teams**: Keep primary docs in English. Add translated summaries if needed.
- **Rapid iteration phases**: Minimum viable docs (README + API) during MVP. Full docs before v1.0.

## Self-Correction Triggers

- New developer cannot set up project from README alone → update README immediately.
- API consumer reports undocumented endpoint → add to API docs, add generation check.
- Incident response delayed by missing runbook → create runbook post-mortem.
- ADR missing for major decision → retroactively document with rationale and context.

## Usage

Example invocations:

- "/technical-documentation" — Run the full technical documentation workflow
- "technical documentation on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
