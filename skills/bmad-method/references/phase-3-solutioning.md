# Phase 3 — Solutioning: Deep Reference Guide

## Table of Contents
- [Purpose of Phase 3](#purpose-of-phase-3)
- [Architecture Document Creation](#architecture-document-creation)
- [C4 Model](#c4-model)
- [Architecture Decision Records](#architecture-decision-records)
- [Technology Selection Criteria](#technology-selection-criteria)
- [Epic Decomposition](#epic-decomposition)
- [Story Writing — INVEST Format](#story-writing--invest-format)
- [Acceptance Criteria](#acceptance-criteria)
- [Story Estimation](#story-estimation)
- [Dependency Mapping](#dependency-mapping)
- [Implementation Readiness Gate](#implementation-readiness-gate)
- [Handoff to Phase 4](#handoff-to-phase-4)

---

## Purpose of Phase 3

Phase 3 transforms the PRD into an implementable blueprint: architecture, technology decisions, epics, and stories. This is the bridge between "what to build" and "how to build it." Every decision made here must be justified and documented.

**Primary agents**: Architect (Arch) for system design; Product Manager (PM) for story decomposition.

**Inputs**: PRD, Personas, UX Spec from Phase 2.

**Outputs**: Architecture Document, ADRs, Epic breakdown, Story files, Dependency map.

---

## Architecture Document Creation

The architecture document describes the system's structure, component responsibilities, communication patterns, and key technical decisions.

### Required Sections

```markdown
# Architecture: [Project Name]

## 1. System Overview
One-paragraph description of the system's purpose and boundaries.

## 2. Architecture Style
Monolith | Modular monolith | Microservices | Serverless | Hybrid.
Justification for the chosen style.

## 3. C4 Diagrams
Context, Container, and Component diagrams (text or visual).

## 4. Data Model
Entity-relationship overview. Key entities, their relationships, and storage locations.

## 5. API Design
REST / GraphQL / gRPC. Endpoint inventory for external-facing APIs.

## 6. Infrastructure
Hosting, CI/CD pipeline, environments (dev/staging/prod).

## 7. Security Architecture
Authentication method, authorization model, data encryption, secrets management.

## 8. Key ADRs
Summaries of critical architecture decisions. Full ADRs in separate files.

## 9. NFR Mapping
How each NFR from the PRD is addressed architecturally.

## 10. Risks and Mitigations
Technical risks identified during design, with mitigation strategies.
```

---

## C4 Model

C4 provides four levels of zoom for describing software architecture. In BMAD, Levels 1-3 are standard; Level 4 is optional.

### Level 1 — Context Diagram

Shows the system as a single box and its relationships with users and external systems.

```
[User] --> [Our System] --> [Payment Gateway]
                       --> [Email Service]
                       --> [Analytics Platform]
```

**Purpose**: Establish system boundaries. Who uses it, what does it integrate with.

**Text format**:
```
System: TaskFlow (project management application)
Users:
  - Project Manager — creates and assigns tasks
  - Developer — updates task status and logs time
  - Stakeholder — views dashboards and reports
External Systems:
  - GitHub API — pulls commit data for task linking
  - Slack — sends notifications for task updates
  - AWS S3 — stores file attachments
```

### Level 2 — Container Diagram

Breaks the system into deployable containers: web app, API, database, queue, etc.

```
[Browser SPA] --HTTPS--> [API Server] --SQL--> [PostgreSQL]
                                      --AMQP--> [RabbitMQ] --> [Worker]
                                      --S3--> [File Storage]
```

**Each container specifies**: Technology, responsibility, communication protocol.

### Level 3 — Component Diagram

Breaks a container into logical components (modules, services, controllers).

```
API Server Components:
  - AuthController — handles login, registration, token refresh
  - TaskService — CRUD operations on tasks, assignment logic
  - NotificationService — dispatches to Slack and email
  - ReportingEngine — generates dashboards and CSV exports
  - Middleware: RateLimit, Auth, Logging
```

### Level 4 — Code Diagram (Optional)

Class-level or function-level diagrams. Only create these for complex or risky components. In BMAD, this level is typically deferred to Phase 4 implementation.

---

## Architecture Decision Records

ADRs document WHY a technical decision was made. They are immutable once accepted — supersede rather than edit.

### ADR Format

```markdown
# ADR-[NUMBER]: [Title]

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
What situation or problem prompted this decision?

## Decision
What was decided and why?

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Option A | ... | ... |
| Option B | ... | ... |

## Consequences
What are the positive, negative, and neutral outcomes of this decision?
```

### When to Write an ADR

- Choosing between competing technologies (e.g., PostgreSQL vs MongoDB)
- Selecting an architectural pattern (e.g., event-driven vs request-response)
- Deviating from a team convention
- Making a decision that is expensive to reverse
- Any decision that a future developer would ask "why?" about

### ADR Example

```markdown
# ADR-003: Use PostgreSQL over MongoDB for primary data store

## Status
Accepted

## Context
The application has complex relational data (users, projects, tasks, assignments)
with many-to-many relationships and the need for transactional consistency.

## Decision
Use PostgreSQL 16 as the primary database.

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| MongoDB | Flexible schema, easy horizontal scaling | Weak joins, no native transactions across collections |
| PostgreSQL | Strong relational support, JSONB for flexibility, mature ecosystem | Vertical scaling limits, more rigid schema |

## Consequences
- Positive: Strong data integrity, mature ORM support, JSONB for semi-structured data
- Negative: Requires schema migrations for model changes
- Neutral: Team already has PostgreSQL experience
```

---

## Architecture Review Checklist

Before the architecture document exits Phase 3, verify against this checklist:

| # | Check | Pass Criteria |
|---|-------|--------------|
| 1 | Every PRD FR maps to at least one component | Cross-reference FR list against component responsibilities |
| 2 | Every NFR has an architectural response | NFR-PERF -> caching layer, NFR-SEC -> auth service, etc. |
| 3 | No orphan components | Every component serves at least one FR |
| 4 | Communication paths are explicit | Every arrow in C4 diagrams has a protocol (REST, gRPC, AMQP) |
| 5 | Data model covers all entities referenced in FRs | Spot-check the first 5 FRs in document order for entity coverage |
| 6 | Security boundaries are drawn | Auth/authz is not an afterthought — it has a component |
| 7 | Failure modes are documented | What happens when each external dependency is unavailable? |
| 8 | ADRs exist for every non-obvious choice | If a future developer would ask "why?", an ADR must exist |

## Technology Selection Criteria

Use a weighted decision matrix when choosing between technologies:

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Team expertise | 3 | 8 (24) | 5 (15) | 7 (21) |
| Community/ecosystem | 2 | 9 (18) | 7 (14) | 6 (12) |
| Performance fit | 3 | 7 (21) | 9 (27) | 6 (18) |
| Maintenance cost | 2 | 6 (12) | 5 (10) | 8 (16) |
| License compatibility | 1 | 10 (10) | 10 (10) | 8 (8) |
| **Total** | | **85** | **76** | **75** |

Score each option 1-10 per criterion. Multiply by weight. Document the matrix in an ADR.

---

## Epic Decomposition

Epics are derived from functional requirement groups in the PRD.

### Decomposition Process

1. Group FRs by feature area (the area code in FR IDs)
2. Each group becomes an epic candidate
3. Validate that each epic is deliverable within 2-4 sprints
4. If too large, split into sub-epics
5. Define epic dependencies

### Epic Format

```markdown
# Epic: [EPIC-ID] [Title]

## Description
What this epic delivers and why it matters.

## FR Coverage
- FR-AUTH-001 through FR-AUTH-012

## Dependencies
- Requires EPIC-INFRA to be complete (database provisioned)

## Estimated Size
8-12 stories, approximately 3 sprints

## Acceptance Criteria
- All covered FRs pass acceptance testing
- NFRs within this domain are met
```

---

## Story Writing — INVEST Format

Every story must satisfy the INVEST criteria:

| Letter | Criterion | Test |
|--------|-----------|------|
| **I** | Independent | Can be implemented without requiring another incomplete story |
| **N** | Negotiable | Details can be adjusted during sprint planning |
| **V** | Valuable | Delivers user or business value |
| **E** | Estimable | Team can size it with reasonable confidence |
| **S** | Small | Completable within a single sprint |
| **T** | Testable | Has clear acceptance criteria |

### Story File Format

```yaml
---
id: STORY-AUTH-001
title: User Registration with Email
epic: EPIC-AUTH
priority: must
points: 5
status: draft
---
```

```markdown
## User Story
As a new user, I want to register with my email and password
so that I can access the application.

## Acceptance Criteria
- Given I am on the registration page
  When I enter a valid email and compliant password
  Then my account is created and I receive a confirmation email

- Given I am on the registration page
  When I enter an email already associated with an account
  Then I see an error message "Email already registered"

- Given I am on the registration page
  When I enter a password that fails complexity rules
  Then I see specific guidance on what is missing

## Technical Notes
- Use bcrypt with cost factor 12 for password hashing (NFR-SEC-001)
- Confirmation email sent via SendGrid integration
- Rate limit registration endpoint to 5 attempts per IP per hour

## Dependencies
- STORY-INFRA-002 (database schema migration)
- STORY-INFRA-003 (email service integration)

## FR Traceability
- FR-AUTH-001, FR-AUTH-002
```

---

## Acceptance Criteria

Use Given/When/Then (Gherkin) format for all acceptance criteria:

```
Given [precondition or context]
When [action performed by user or system]
Then [expected observable outcome]
```

### Rules for Good Acceptance Criteria

1. **One behavior per criterion** — do not combine multiple outcomes
2. **Observable outcomes** — the result must be visible to user or measurable by test
3. **Cover the happy path AND error paths** — at minimum: success, validation error, system error
4. **No implementation details** — describe WHAT happens, not HOW
5. **Reference NFRs where applicable** — "Then results appear within 2 seconds (NFR-PERF-001)"

### Anti-Patterns

- "Then it works correctly" — not testable
- "Then the data is saved to PostgreSQL" — implementation detail
- Only happy-path criteria — must include at least one error scenario

---

## Story Estimation

BMAD uses Fibonacci points (1, 2, 3, 5, 8, 13) for relative sizing.

| Points | Meaning | Example |
|--------|---------|---------|
| 1 | Trivial — config change, copy update | Update error message text |
| 2 | Small — straightforward implementation | Add input validation to a form |
| 3 | Medium — clear scope, some complexity | CRUD endpoint with validation |
| 5 | Large — multiple components, integration | User registration with email flow |
| 8 | Very large — significant complexity | Search with autocomplete and filtering |
| 13 | Epic-level — should be split | Full authentication system |

**Rules**:
- **[R6]** Stories estimated at 13 must be split before sprint planning — no exceptions
- The team's velocity is measured in total points completed per sprint
- Points measure complexity, not time — a 5-point story is not "5 days"

### Story Splitting Heuristics

When a story is too large (8+ points), split using one of these strategies:

| Strategy | When to Use | Example |
|----------|------------|---------|
| **By workflow step** | Story covers multiple user actions | "User registration" -> "Registration form" + "Email confirmation" |
| **By data variation** | Story handles multiple input types | "Import data" -> "Import CSV" + "Import JSON" |
| **By happy/error path** | Error handling is complex | "Process payment" -> "Successful payment" + "Payment failure handling" |
| **By interface** | Story touches UI + API + DB | "Add filtering" -> "Filter API endpoint" + "Filter UI component" |
| **By CRUD operation** | Full CRUD is too large | "Manage tasks" -> "Create task" + "Read/list tasks" + "Update task" + "Delete task" |

**[R7]** After splitting, each resulting story must independently satisfy INVEST criteria. If a split story is not independently valuable, merge it back and try a different split strategy.

### Estimation Calibration Guidance

| Signal | Action |
|--------|--------|
| Team consistently finishes stories faster than estimated | Re-calibrate: your reference story may be too generous. Pick a new 3-point reference. |
| Team consistently overruns estimates | Check for hidden dependencies or unclear acceptance criteria before re-estimating. |
| Wide variance between estimators (>3 points apart) | The story is ambiguous. Clarify scope before re-estimating. |
| First sprint (no historical data) | Use the team's best guess. Expect 30-50% variance. Calibrate after Sprint 1. |

---

## Dependency Mapping

Document dependencies between stories and between epics.

### Dependency Notation

```
STORY-AUTH-001 → STORY-INFRA-002 (blocked-by)
STORY-AUTH-003 → STORY-AUTH-001 (depends-on)
EPIC-SEARCH → EPIC-INFRA (requires)
```

### Dependency Matrix (for complex projects)

```
              | INFRA-001 | INFRA-002 | AUTH-001 | AUTH-002 | SRCH-001 |
INFRA-001     |     -     |           |          |          |          |
INFRA-002     |     X     |     -     |          |          |          |
AUTH-001      |           |     X     |    -     |          |          |
AUTH-002      |           |           |    X     |    -     |          |
SRCH-001      |     X     |     X     |          |          |    -     |
```

`X` = depends on column story. Read: "SRCH-001 depends on INFRA-001 and INFRA-002."

---

## Implementation Readiness Gate

The gate between Phase 3 and Phase 4 is the most rigorous in BMAD. It has 13 checks:

| # | Check | Criterion |
|---|-------|-----------|
| 1 | Architecture documented | Architecture.md exists with all required sections |
| 2 | ADRs written | At least 1 ADR exists; all major decisions recorded |
| 3 | C4 Level 1-2 complete | Context and Container diagrams present |
| 4 | Data model defined | Entity-relationship diagram or description exists |
| 5 | API surface defined | Endpoint inventory for external APIs |
| 6 | Epics decomposed | All FRs mapped to epics |
| 7 | Stories written | All epics have stories; each story has acceptance criteria |
| 8 | Stories estimated | All stories have Fibonacci point estimates |
| 9 | Dependencies mapped | Story and epic dependencies documented |
| 10 | NFRs addressed | Every NFR has an architectural response |
| 11 | Security reviewed | Authentication, authorization, data protection documented |
| 12 | project-context.md complete | Tech stack, conventions, constraints documented |
| 13 | No 13-point stories | All stories are 8 points or fewer |

**Failure protocol**: If any check fails, the gate blocks Phase 4 entry. The responsible agent (Architect or PM) must remediate before re-attempting the gate.

---

## Handoff to Phase 4

**Handoff artifacts**:
- `architecture.md` — system design document
- `adrs/` — directory of architecture decision records
- `epics/` — epic descriptions with FR mappings
- `stories/` — individual story files with acceptance criteria
- `project-context.md` — technical constraints and conventions
- Updated PRD with any Phase 3 amendments

**Receiving agent**: Developer (Dev) for Phase 4 implementation.

**Handoff protocol**: Architect presents the architecture in a 5-minute summary, identifies the critical path (longest dependency chain), and flags the highest-risk technical decision. PM identifies the first sprint's story candidates based on dependencies and priority.

---

## Assumptions

- PRD, personas, and UX spec from Phase 2 are complete and scope-locked
- The architect has access to the team's technology expertise profile for tech selection weighting
- Story estimation is relative to a calibrated reference story (if no reference exists, Sprint 1 serves as calibration)

## Limits

- Phase 3 does NOT produce working code — that is Phase 4
- Phase 3 does NOT finalize sprint assignments — sprint planning happens at the start of Phase 4
- ADRs document decisions, not options analysis — the decision must already be made

## Edge Cases

- **Architecture requires a technology the team has zero experience with**: Add a spike story (time-boxed to 1 day) as the first story in Sprint 1. The spike validates feasibility before committing.
- **Circular dependency between stories**: This indicates a story decomposition error. Merge the circular stories into one, then re-split using a different heuristic.
- **Gate fails on Step 8 (API Contracts) for an event-driven system**: Adapt Step 8 to validate event schemas instead of REST endpoints. Document this adaptation in the gate report.

## Acceptance Criteria

- [ ] Architecture review checklist passes (8/8 checks)
- [ ] All stories are 8 points or fewer (no 13-point stories)
- [ ] Implementation readiness gate produces PASS or CONDITIONAL PASS
- [ ] Dependency graph is acyclic
- [ ] Every FR in the PRD traces to at least one story

See also: `references/phase-2-planning.md`, `references/phase-4-implementation.md`, `references/implementation-readiness-gate.md`, `references/artifact-flow-chain.md`
