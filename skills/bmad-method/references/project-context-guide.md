# Project Context Guide

## Table of Contents
- [Purpose](#purpose)
- [Required Sections](#required-sections)
- [Writing Each Section Effectively](#writing-each-section-effectively)
- [When to Update project-context.md](#when-to-update-project-contextmd)
- [Manual Creation vs Auto-Generation](#manual-creation-vs-auto-generation)
- [Brownfield Project Scanning](#brownfield-project-scanning)
- [Relationship to Other Artifacts](#relationship-to-other-artifacts)
- [Quality Checklist](#quality-checklist)

---

## Purpose

`project-context.md` is the project constitution for AI agents. It provides the stable, project-wide constraints that every agent and every workflow must respect. Without it, AI agents operate in a vacuum — making assumptions about technology choices, coding conventions, and project boundaries that may conflict with reality.

**Key insight**: AI agents produce better output when they know what NOT to do. project-context.md is as much about constraints and prohibitions as it is about preferences.

**Location**: Root of the project repository (alongside `package.json`, `Cargo.toml`, etc.) or in the `docs/` directory.

**Consumers**: Every BMAD agent reads this file before performing any work. It is the first file loaded into context for Phase 3 and Phase 4 operations.

---

## Required Sections

Every `project-context.md` must include these sections. Optional sections are marked.

```markdown
# Project Context: [Project Name]

## 1. Vision
## 2. Tech Stack
## 3. Constraints
## 4. Conventions
## 5. Team (optional)
## 6. Links (optional)
## 7. Exclusion Zones
## 8. Environment
```

---

## Writing Each Section Effectively

### 1. Vision

A 2-4 sentence summary of what this project is and why it exists. This grounds every agent decision in the project's purpose.

**Bad**:
```
## Vision
A web application.
```

**Good**:
```
## Vision
TaskFlow is an open-source project management tool designed for small engineering
teams (3-10 people) who find Jira too complex and Trello too simple. It emphasizes
keyboard-driven workflows, real-time collaboration, and developer-friendly integrations
(GitHub, GitLab, CI/CD pipelines). The MVP targets solo developers and pairs; team
features follow in Phase 2.
```

**Rules**:
- Include the target audience
- Include the differentiator (why THIS product, not an existing one)
- Include the current scope/phase
- Do not include marketing language or aspirational statements

### 2. Tech Stack

Enumerate every technology decision that agents must respect. Be specific about versions.

```markdown
## Tech Stack

### Frontend
- Framework: React 18 with TypeScript 5.3
- State management: Zustand 4.x
- Styling: Tailwind CSS 3.4 (no CSS modules, no styled-components)
- Build: Vite 5.x
- Testing: Vitest + React Testing Library

### Backend
- Runtime: Node.js 20 LTS
- Framework: Fastify 4.x (NOT Express — this is a deliberate choice, see ADR-001)
- ORM: Drizzle ORM (NOT Prisma, NOT TypeORM)
- Database: PostgreSQL 16
- Authentication: Lucia Auth v3

### Infrastructure
- Hosting: Railway (production), local Docker (development)
- CI/CD: GitHub Actions
- Monitoring: None yet (Phase 2)

### Shared
- Monorepo: Turborepo
- Package manager: pnpm 8.x (NOT npm, NOT yarn)
- Linting: ESLint flat config + Prettier
```

**Rules**:
- Specify versions (major at minimum, minor when it matters)
- Call out explicit NOTs when there are common alternatives the agent might assume
- Reference ADRs for non-obvious choices
- Include dev tooling, not just production tech

### 3. Constraints

Hard limits that cannot be violated. These override agent judgment.

```markdown
## Constraints

### Technical
- No server-side rendering (SSR) — SPA only for MVP
- All API responses must be under 200ms at p95 (NFR-PERF-001)
- Maximum bundle size: 500KB gzipped for initial load
- No runtime dependencies over 100KB unpacked

### Business
- Open source: MIT license. All dependencies must be MIT/Apache/BSD compatible
- No paid services in MVP (use open-source alternatives)
- Must support latest 2 versions of Chrome, Firefox, Safari, Edge

### Data
- All user data stored in PostgreSQL (no client-side storage of sensitive data)
- PII must be encrypted at rest
- Session tokens expire after 24 hours

### Process
- All code must have tests before merge
- No direct commits to main — PRs only
- Every PR must reference a story ID
```

**Rules**:
- Constraints are non-negotiable — if an agent cannot comply, it must raise the constraint as a blocker rather than violate it
- Group by category (technical, business, data, process)
- Be specific: "no large dependencies" is vague; "no dependencies over 100KB" is a constraint

### 4. Conventions

Project-specific patterns that agents should follow. These are preferences, not hard constraints — but agents should follow them unless there is an explicit reason to deviate.

```markdown
## Conventions

### Code Style
- File naming: kebab-case for files, PascalCase for React components
- Exports: Named exports only (no default exports) — enforced by ESLint
- Functions: Prefer arrow functions; use `function` keyword only for hoisted declarations
- Error handling: Always use custom error classes extending BaseError

### Directory Structure
```
src/
  features/           ← Feature-based organization
    auth/
      components/
      hooks/
      services/
      auth.test.ts
    tasks/
      ...
  shared/             ← Cross-feature utilities
    components/
    hooks/
    utils/
  infrastructure/     ← Database, external services
```

### API Design
- RESTful endpoints: plural nouns (e.g., /api/tasks, not /api/task)
- Versioning: URL-based (/api/v1/tasks)
- Error responses: { error: { code: string, message: string, details?: object } }
- Pagination: cursor-based with `?cursor=xxx&limit=20`

### Git
- Branch naming: type/STORY-ID-short-description
- Commit messages: [STORY-ID] description
- Squash merge to main
```

**Rules**:
- Conventions are prescriptive (do THIS), not descriptive (we tend to do this)
- Include code examples where patterns are non-obvious
- Reference directory structure — agents need this to know where to put files

### 5. Team (Optional)

Who works on this project and their roles. Useful for agents that need to route decisions.

```markdown
## Team

- **Lead Developer**: Handles architecture decisions and code review
- **AI Agents**: BMAD agent suite (Analyst, PM, Architect, Developer, Barry)
- **Stakeholder**: Reviews product brief and PRD before Phase 3
```

### 6. Links (Optional)

Key URLs that agents might need.

```markdown
## Links

- Repository: https://github.com/org/taskflow
- Production: https://taskflow.app
- Staging: https://staging.taskflow.app
- Design system: https://ui.taskflow.app
- API documentation: /docs/api.md
```

### 7. Exclusion Zones

Files and directories that AI agents must NEVER modify. This is a safety mechanism.

```markdown
## Exclusion Zones

The following paths must not be modified by any agent:
- `.env*` — Environment files with secrets
- `migrations/` — Database migrations (created only through ORM CLI)
- `scripts/deploy.sh` — Deployment script managed by ops team
- `LICENSE` — Legal document
- `.github/workflows/` — CI/CD pipelines (modified only through dedicated PRs)
```

**Rules**:
- Exclusion zones are absolute — no agent may modify these files regardless of instructions
- Include the reason for exclusion
- This list should be short (5-10 items) — if everything is excluded, the project-context is too restrictive

### 8. Environment

Development environment setup that agents need to know about.

```markdown
## Environment

### Local Development
- Run `pnpm install` to install dependencies
- Run `pnpm dev` to start the development server (port 3000)
- Run `pnpm test` to run the test suite
- Database: PostgreSQL via Docker (`docker compose up db`)

### Environment Variables
Required variables (see .env.example):
- DATABASE_URL — PostgreSQL connection string
- SESSION_SECRET — Lucia auth session secret
- GITHUB_CLIENT_ID — GitHub OAuth app ID (for integrations)

### Ports
- 3000: Frontend dev server
- 3001: API server
- 5432: PostgreSQL
```

---

## When to Update project-context.md

| Trigger | What to Update |
|---------|---------------|
| New technology added to the stack | Tech Stack section |
| ADR accepted that changes conventions | Conventions section, reference the ADR |
| New exclusion zone identified | Exclusion Zones section |
| Team composition changes | Team section |
| New environment variable added | Environment section |
| Constraint discovered during implementation | Constraints section |
| Phase transition (e.g., MVP to Phase 2) | Vision section (scope update) |

### Staleness Detection Rules

**[R14]** project-context.md is stale when ANY of these are true:

| Signal | Detection Method | Maximum Staleness |
|--------|-----------------|-------------------|
| Tech stack version mismatch | Compare `Tech Stack` section against `package.json`/lock files | 0 days — must be updated in the same PR that changes dependencies |
| Missing new environment variable | Compare `Environment` section against `.env.example` | 1 sprint |
| ADR accepted but not reflected in Conventions | Cross-check ADR dates against last `Conventions` update | 1 sprint |
| Phase transition occurred | Compare `Vision` current phase against actual project state | 0 days — update at phase boundary |
| New exclusion zone identified but not documented | Team member reports a file that must not be modified | 1 day |

### Mandatory Review Cadence

**[R15]** project-context.md must be reviewed:
- At every phase transition (Phase 1->2, 2->3, 3->4)
- At every sprint boundary during Phase 4
- Whenever an ADR is accepted
- Whenever a new team member joins (onboarding validation)

### Section-Level Validation

When reviewing project-context.md, validate each section independently:

| Section | Validation Method |
|---------|------------------|
| Vision | Does it match current product scope? Is the phase correct? |
| Tech Stack | Run `diff` against dependency manifests. Versions must match. |
| Constraints | Are all constraints still relevant? Any new ones discovered? |
| Conventions | Do the first 3 source files in stable path order follow the stated conventions? |
| Exclusion Zones | Are all listed paths still valid? Any new paths needed? |
| Environment | Can a new developer set up the environment from this section alone? |

**Rules**:
- **[R16]** Update BEFORE the change takes effect, not after
- Every update must be a dedicated commit with a clear message
- Major changes must be reviewed by the team (or the architect agent)
- Never remove history — if a constraint is relaxed, note that it was changed and why

---

## Manual Creation vs Auto-Generation

### Manual Creation (Recommended for Greenfield)

For new projects, write project-context.md by hand during Phase 3 (Solutioning). The architect agent should draft it as part of the architecture workflow, then the developer refines it.

**Workflow**:
1. Architect creates initial draft from architecture document and ADRs
2. Developer reviews and adds conventions, exclusion zones, environment details
3. Both agree on the final version before Phase 4 begins

### Auto-Generation (Recommended for Brownfield)

For existing projects, scan the codebase to generate a starting point:

```
Scan targets:
- package.json / Cargo.toml / requirements.txt → Tech Stack
- .eslintrc / .prettierrc / tsconfig.json → Conventions
- .gitignore / .dockerignore → hints for Exclusion Zones
- docker-compose.yml → Environment
- README.md → Vision, Links
- Directory structure → Conventions (directory layout)
```

Auto-generated context requires human review — the scanner captures what IS, not what SHOULD BE.

---

## Brownfield Project Scanning

When joining an existing project that lacks project-context.md:

### Scanning Protocol

1. **Inventory the tech stack**: Read dependency manifests, Dockerfiles, CI configs
2. **Identify patterns**: Analyze 10 representative source files for naming conventions, directory structure, import patterns
3. **Find constraints**: Look for linting rules, CI gates, security configurations
4. **Detect exclusion zones**: Files with restricted permissions, deployment scripts, generated code
5. **Document gaps**: Note where the project lacks consistency (mixed conventions, missing tests)

### Brownfield Template

```markdown
# Project Context: [Project Name] (Brownfield Scan)

## Scan Date
[Date of scan]

## Confidence Levels
- Tech Stack: HIGH (read from manifests)
- Conventions: MEDIUM (inferred from code patterns, may have exceptions)
- Constraints: LOW (no explicit documentation found, inferred from CI/linting)

## Discovered Tech Stack
[Auto-populated from scan]

## Inferred Conventions
[Patterns observed in code, flagged for human review]

## Suggested Constraints
[Derived from CI/CD config and linting rules]

## NEEDS HUMAN REVIEW
- [ ] Confirm inferred conventions are intentional, not accidental
- [ ] Add exclusion zones
- [ ] Write or verify the Vision section
- [ ] Add any undocumented constraints
```

---

## Relationship to Other Artifacts

```
product-brief.md ──→ prd.md ──→ architecture.md ──→ project-context.md
                                                           │
                                                           ▼
                                                    story files, code
```

- **product-brief.md**: Provides the Vision section's foundation
- **prd.md**: NFRs feed into Constraints; FRs inform Conventions
- **architecture.md**: Technology decisions become the Tech Stack; ADRs become Conventions
- **story files**: Reference project-context.md for implementation guidance
- **code**: Must comply with everything in project-context.md

**project-context.md is NOT**:
- A substitute for the PRD (it does not contain requirements)
- A substitute for the architecture doc (it does not explain WHY decisions were made)
- A README (it is for AI agents, not human onboarding — though humans benefit too)

---

## Quality Checklist

```markdown
## project-context.md Quality Review

### Completeness
- [ ] Vision section is present and specific
- [ ] Tech Stack lists all major technologies with versions
- [ ] Constraints include at least one item per category (technical, business, data)
- [ ] Conventions include directory structure
- [ ] Exclusion Zones list at least .env files

### Precision
- [ ] Tech Stack specifies versions (not just "React" but "React 18")
- [ ] Constraints are quantitative where possible ("200ms" not "fast")
- [ ] Conventions include code examples for non-obvious patterns

### Consistency
- [ ] Tech Stack matches actual dependencies in package.json / equivalent
- [ ] Conventions match actual linting rules
- [ ] No contradictions between sections

### Usability
- [ ] An agent reading only this file could set up a development environment
- [ ] An agent reading only this file would know where to put a new feature file
- [ ] An agent reading only this file would know which libraries to use and which to avoid
```

---

## Assumptions

- The project uses Git (or compatible VCS) for version control
- At least one person on the team is responsible for maintaining project-context.md accuracy
- AI agents read project-context.md before performing any Phase 3 or Phase 4 work

## Limits

- project-context.md is NOT a substitute for the PRD (it does not contain requirements)
- project-context.md is NOT a substitute for the architecture doc (it does not explain WHY decisions were made)
- project-context.md must stay under 2K tokens — if it exceeds this, move details to linked documents

## Edge Cases

- **Monorepo with multiple projects**: Each project gets its own project-context.md. Shared conventions go in a root-level `organization-context.md`. See `references/enterprise-governance.md`.
- **project-context.md and architecture.md contradict each other**: project-context.md wins for stack/conventions. Architecture doc wins for design rationale. Resolve the contradiction immediately — do not leave both in conflict.
- **Auto-generated project-context.md has low confidence sections**: Mark low-confidence sections with `[INFERRED — NEEDS REVIEW]` and schedule human review within 1 sprint.

## Acceptance Criteria

- [ ] All required sections (Vision, Tech Stack, Constraints, Conventions, Exclusion Zones, Environment) are populated
- [ ] Tech Stack versions match actual dependency manifests (spot-check 3 dependencies)
- [ ] Staleness detection passes — no section exceeds its maximum staleness threshold
- [ ] File stays under 2K tokens

See also: `references/methodology-overview.md`, `references/brownfield-patterns.md`, `references/schemas.md`, `references/progressive-context.md`
