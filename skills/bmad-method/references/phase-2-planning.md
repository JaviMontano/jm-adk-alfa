# Phase 2 — Planning: Deep Reference Guide

## Table of Contents
- [Purpose of Phase 2](#purpose-of-phase-2)
- [PRD Structure and Writing Guide](#prd-structure-and-writing-guide)
- [Writing Measurable Requirements](#writing-measurable-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [User Persona Creation](#user-persona-creation)
- [Success Metrics — SMART Framework](#success-metrics--smart-framework)
- [UX Spec Creation](#ux-spec-creation)
- [Wireframe Conventions (Text-Based)](#wireframe-conventions-text-based)
- [Scope Management](#scope-management)
- [Handoff to Phase 3](#handoff-to-phase-3)

---

## Purpose of Phase 2

Phase 2 transforms the product brief into a complete specification set: PRD, personas, UX spec. These artifacts must be precise enough for an architect to design a system and a developer to estimate work — without requiring further stakeholder interviews.

**Primary agent**: Product Manager (PM) — requirement writer, scope guardian.

**Inputs**: Product Brief from Phase 1 (or stakeholder input for abbreviated flows).

**Outputs**: PRD, User Personas, UX Specification (optional: wireframes, user flow diagrams).

### PRD Quality Score Rubric

Rate each PRD section 1-5. **Minimum passing score: 3 on every section, average >= 3.5 overall.**

| Section | 1 (Fail) | 3 (Acceptable) | 5 (Excellent) |
|---------|----------|-----------------|---------------|
| Problem Statement | Vague or missing | Specific problem for a named audience | Quantified problem with evidence tags and urgency |
| Functional Requirements | Missing IDs or untestable | All FRs have IDs, priorities, basic AC | Every FR has ID, MoSCoW, source ref, and testable AC |
| Non-Functional Requirements | Aspirational ("fast") | Quantitative targets present | Targets with measurement method and consequence |
| Personas | Demographics only | Behavioral with goals and frustrations | 2+ scenarios per persona, mapped to FRs |
| Success Metrics | "Improve UX" | SMART metrics with targets | SMART with baselines, measurement method, and owner |
| Scope Boundaries | Not documented | IN/OUT sections present | 3+ out-of-scope items with disposition (Phase N / Never) |
| Open Questions | Missing | List exists | Each question has an owner and target resolution date |

---

## PRD Structure and Writing Guide

The Product Requirements Document is the most information-dense artifact in the BMAD chain. It bridges the problem space (Phase 1) and solution space (Phase 3).

### Required Sections

```markdown
# PRD: [Product Name]

## 1. Introduction
Brief context: what is being built and why.
Reference the product brief for background.

## 2. User Personas
Summary of each persona (full details in separate persona files).
Link to persona docs.

## 3. Functional Requirements
Numbered requirements in FR format (see below).
Grouped by feature area or user journey.

## 4. Non-Functional Requirements
Performance, security, accessibility, scalability targets.
Each with quantitative threshold.

## 5. User Stories (Summary)
High-level user stories derived from FRs.
Detailed stories are created in Phase 3.

## 6. UX Requirements
Key interaction patterns, navigation model, responsive behavior.
Reference the UX spec for detailed guidance.

## 7. Success Metrics
SMART metrics with baselines and targets.

## 8. Scope
### In Scope
### Out of Scope
### Future Considerations

## 9. Dependencies and Assumptions
External systems, third-party services, team availability.

## 10. Open Questions
Inherited from brief + newly discovered during planning.
```

### Writing Principles

1. **Declarative, not imperative**: Describe WHAT the system must do, not HOW.
2. **One requirement per statement**: Never combine two behaviors in a single FR.
3. **Testable**: Every requirement must be verifiable by a human or automated test.
4. **Traceable**: Every FR must trace back to a brief section or stakeholder request.
5. **Prioritized**: Use MoSCoW (Must/Should/Could/Won't) on every FR.

---

## Writing Measurable Requirements

### Functional Requirement Format

Each FR follows a strict format:

```
FR-[AREA]-[NUMBER]: [Requirement Statement]
Priority: Must | Should | Could | Won't
Source: [Brief section or stakeholder reference]
Acceptance: [How to verify this is met]
```

**Example**:
```
FR-AUTH-001: The system shall allow users to register with email and password.
Priority: Must
Source: Brief Section 2 — Target Users
Acceptance: User can create account, receive confirmation email, and log in.

FR-AUTH-002: The system shall enforce password complexity (min 8 chars, 1 uppercase, 1 number).
Priority: Must
Source: NFR-SEC-001
Acceptance: Passwords failing complexity rules are rejected with specific error messages.

FR-SRCH-001: The system shall return search results within 2 seconds for queries up to 100 characters.
Priority: Must
Source: Brief Section 4 — Success Metrics
Acceptance: 95th percentile response time under 2 seconds measured over 1000 test queries.
```

### ID Convention

- `FR` = Functional Requirement
- Area code: 3-4 letter abbreviation (AUTH, SRCH, DASH, NOTIF, PAY, etc.)
- Number: 3-digit zero-padded sequential (001, 002, 003)
- IDs are immutable once assigned — never reuse a retired ID

### Common FR Mistakes

| Mistake | Bad Example | Good Example | Detection |
|---------|------------|-------------|-----------|
| Vague verb | "The system should handle payments" | "The system shall process credit card payments via Stripe API" | Search for "handle", "manage", "support" without specifics |
| Combined requirements | "Users can search and filter results" | Two separate FRs: one for search, one for filtering | FR contains "and" joining two behaviors |
| Implementation detail | "Use React to render the dashboard" | "The dashboard shall display 5 KPI widgets on load" | FR names a specific library or framework |
| Untestable | "The system should be user-friendly" | "A new user shall complete onboarding in under 3 minutes" | No numeric threshold or observable outcome |
| Missing error path | "Users can upload files" | "Users can upload files up to 10MB; files exceeding limit produce error E-UPLOAD-001" | FR only describes happy path |
| Implicit requirement | No FR exists for logout | FR-AUTH-010: "The system shall allow users to terminate their session" | Compare user journeys against FR list |

**[R4]** Every FR must use "shall" (mandatory) or "may" (optional). Do not use "should" — it is ambiguous.

### Common NFR Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| No measurement method | "System must be fast" | "API p95 < 200ms, measured by APM tool in production" |
| Unrealistic target without baseline | "99.999% uptime" for MVP | Set targets proportional to infrastructure: 99.9% for single-region |
| Missing consequence | "Coverage must be 80%" | Add: "PRs with coverage below 80% must not be merged" |
| Forgetting operability | No monitoring NFR | Add NFR-OPS category: logging, alerting, health checks |

---

## Non-Functional Requirements

NFRs define system qualities. Each must have a quantitative target — subjective qualities like "fast" or "secure" are not NFRs.

### NFR Categories and Examples

```
NFR-PERF-001: API response time shall be under 200ms at p95 for authenticated endpoints.
NFR-PERF-002: Page load time shall be under 3 seconds on 3G connections.

NFR-SEC-001: All user passwords shall be hashed with bcrypt (cost factor >= 12).
NFR-SEC-002: Session tokens shall expire after 24 hours of inactivity.

NFR-ACC-001: The application shall meet WCAG 2.1 Level AA compliance.
NFR-ACC-002: All interactive elements shall be keyboard-navigable.

NFR-SCALE-001: The system shall support 10,000 concurrent users without degradation.
NFR-SCALE-002: Database queries shall not exceed 100ms for datasets up to 1M rows.

NFR-REL-001: System uptime shall be 99.9% measured monthly.
NFR-REL-002: Recovery time objective (RTO) shall be under 1 hour.

NFR-MAINT-001: Code coverage shall remain above 80% for core modules.
NFR-MAINT-002: All public APIs shall have OpenAPI 3.0 documentation.
```

### NFR Specification Template

```
NFR-[CATEGORY]-[NUMBER]: [Requirement Statement]
Target: [Quantitative threshold]
Measurement: [How it will be measured]
Consequence: [What happens if not met]
```

---

## User Persona Creation

Personas are behavioral archetypes — not demographic profiles. Each persona represents a distinct set of goals, frustrations, and usage patterns.

### Persona Template

```markdown
# Persona: [Name]

## Role
[Job title or user category]

## Goals
- [Primary goal — what they are trying to achieve]
- [Secondary goal]
- [Tertiary goal]

## Frustrations
- [Current pain point 1]
- [Current pain point 2]

## Behavior Patterns
- [How they currently solve the problem]
- [Tools they use]
- [Frequency of interaction]

## Technical Proficiency
[Novice / Intermediate / Advanced]

## Key Scenarios
1. [Scenario that exercises this persona's primary goal]
2. [Scenario that exercises an edge case]

## Quotes (Synthesized)
> "I just want to [goal] without having to [frustration]."
```

### Persona Quality Criteria

- Each persona has at least 2 distinct goals not shared by other personas
- Frustrations are specific, not generic ("too slow" is bad; "waiting 30 seconds for report generation" is good)
- At least 2 key scenarios per persona
- Personas map to FRs: every FR should serve at least one persona

---

## Success Metrics — SMART Framework

Every success metric must pass the SMART test:

| Dimension | Question | Example |
|-----------|----------|---------|
| **S**pecific | What exactly are we measuring? | "Checkout completion rate" |
| **M**easurable | Can we assign a number? | "From 62% to 80%" |
| **A**chievable | Is the target realistic? | "18% increase aligns with competitor benchmarks" |
| **R**elevant | Does it connect to business value? | "Directly impacts revenue per session" |
| **T**ime-bound | When do we expect to hit the target? | "Within 3 months of launch" |

### Metric Template

```
Metric: [Name]
Baseline: [Current value or "unknown — measure pre-launch"]
Target: [Numeric target]
Method: [Analytics tool, survey, manual measurement]
Timeline: [When the target should be achieved]
Owner: [Who monitors this metric]
```

### Common Metric Categories

- **Adoption**: Registration rate, activation rate, daily active users
- **Engagement**: Session duration, feature usage frequency, return rate
- **Performance**: Task completion time, error rate, support ticket volume
- **Business**: Revenue per user, cost savings, churn rate

---

## UX Spec Creation

The UX spec translates requirements into interaction design guidance. It sits between the PRD (what) and the implementation (how).

### UX Spec Sections

```markdown
# UX Specification: [Product Name]

## 1. Navigation Model
Primary navigation structure, hierarchy depth, breadcrumb behavior.

## 2. Page Inventory
List of all pages/views with purpose and primary actions.

## 3. Interaction Patterns
Form behavior, validation timing, loading states, error handling.

## 4. Responsive Strategy
Breakpoints, layout shifts, mobile-specific interactions.

## 5. Accessibility Requirements
Focus management, screen reader considerations, color contrast.

## 6. Component Library Reference
Design system components to use (if applicable).

## 7. User Flows
Step-by-step flows for primary scenarios (text or diagram).
```

---

## Wireframe Conventions (Text-Based)

In AI-driven workflows, wireframes are often text-based. Use ASCII or markdown to represent layout.

### Layout Notation

```
┌─────────────────────────────────────────┐
│  HEADER: Logo | Nav: Home | Docs | API  │
├────────────┬────────────────────────────┤
│  SIDEBAR   │  MAIN CONTENT             │
│            │                            │
│  - Item 1  │  [Search Bar............]  │
│  - Item 2  │                            │
│  - Item 3  │  Card Grid (3 columns):   │
│            │  [Card] [Card] [Card]      │
│            │  [Card] [Card] [Card]      │
├────────────┴────────────────────────────┤
│  FOOTER: Copyright | Privacy | Terms    │
└─────────────────────────────────────────┘
```

### Component Notation

| Symbol | Meaning |
|--------|---------|
| `[Button Label]` | Clickable button |
| `[Input........]` | Text input field |
| `(o) Option` | Radio button |
| `[x] Checked` | Checkbox (selected) |
| `[ ] Unchecked` | Checkbox (unselected) |
| `[v Dropdown ]` | Select dropdown |
| `--- divider ---` | Visual separator |
| `{Modal Title}` | Modal/dialog |
| `>> Link Text` | Navigation link |

### Annotating Wireframes

Add numbered annotations below the wireframe:

```
1. Search bar auto-completes after 3 characters (FR-SRCH-002)
2. Card grid is responsive: 3 cols desktop, 2 cols tablet, 1 col mobile
3. Sidebar collapses to hamburger menu below 768px
```

---

## Scope Management

### In-Scope Documentation

List every feature area with its FR range:

```
In Scope:
- User Authentication (FR-AUTH-001 through FR-AUTH-012)
- Product Search (FR-SRCH-001 through FR-SRCH-008)
- Shopping Cart (FR-CART-001 through FR-CART-006)
```

### Out-of-Scope Documentation

Every out-of-scope item needs a reason and a disposition:

```
Out of Scope:
- Social login (Google, GitHub) — Phase 2 consideration, not MVP
- Multi-currency support — Requires payment provider upgrade, deferred to Q3
- Admin analytics dashboard — Will use third-party tool initially (Mixpanel)
- Native mobile app — Web-first strategy; mobile assessed post-launch
```

### Scope Change Protocol

When scope must change during Phase 2:
1. Document the change request with rationale
2. Assess impact on timeline, resources, and dependent FRs
3. Update the PRD with the change and a `[SCOPE-CHANGE]` tag
4. Re-validate success metrics against new scope
5. Notify the architect (Phase 3) if the change affects system boundaries

---

## Handoff to Phase 3

Phase 2 is complete when the PRD passes the following gate:

| Criterion | Verification |
|-----------|-------------|
| All FRs have unique IDs, priorities, and acceptance criteria | Spot-check the first 10 FRs in document order |
| NFRs have quantitative targets | Every NFR has a number |
| At least 2 personas exist | Each with goals, frustrations, scenarios |
| Success metrics pass SMART test | Review each metric against 5 dimensions |
| Scope boundaries are explicit | In-scope and out-of-scope both populated |
| Open questions from Phase 1 are resolved or explicitly deferred | Cross-check brief's open questions |
| UX spec covers primary user flows | At least the top 3 scenarios are documented |

**Handoff artifacts**:
- `prd.md` — committed to project `docs/` directory
- `personas/` — one file per persona
- `ux-spec.md` — interaction design guidance
- Updated `product-brief.md` — with resolved open questions

**Receiving agent**: Architect (Arch) for Phase 3 solutioning.

**Handoff protocol**: PM summarizes the PRD in 5 bullet points, flags the highest-risk FRs, and identifies the top NFR constraint that will shape the architecture.

### Scope Lock Criteria

**[R5]** Scope locks when ALL of the following are true:
1. PRD quality score averages >= 3.5 with no section below 3
2. All Phase 1 open questions are resolved or explicitly deferred with rationale
3. At least 2 personas exist with mapped FRs
4. Stakeholder has reviewed IN/OUT scope sections

After scope lock, any change requires the Scope Change Protocol (Section above) and must be tagged `[SCOPE-CHANGE]` with a re-validation of success metrics.

---

## Assumptions

- Product brief from Phase 1 (or equivalent input) exists and has been reviewed
- The PM agent has domain understanding sufficient to write testable requirements
- Stakeholders are available for scope review before Phase 3 handoff

## Limits

- Phase 2 does NOT produce architecture decisions — those are Phase 3 artifacts
- Phase 2 does NOT produce individual story files — those are created in Phase 3
- Phase 2 does NOT prescribe technology choices (the PRD is technology-agnostic)

## Edge Cases

- **PRD for an API-only product with no UI**: Skip the UX Spec. Wireframes are not applicable. Replace UX requirements with API developer experience requirements (documentation, SDK, error messages).
- **Multiple products sharing a PRD**: Split into separate PRDs. Each product must have its own FR namespace to avoid ID collisions.
- **Inherited PRD from a non-BMAD process**: Convert to BMAD format, score with the rubric, and remediate sections scoring below 3 before proceeding.

## Acceptance Criteria

- [ ] PRD quality score averages >= 3.5 with no section below 3
- [ ] All FRs follow the `FR-[AREA]-[NNN]` format with MoSCoW priority
- [ ] All NFRs have quantitative targets and measurement methods
- [ ] At least 2 personas exist with behavioral detail (not demographics)
- [ ] Scope lock criteria are met before handoff to Phase 3

See also: `references/phase-1-analysis.md`, `references/phase-3-solutioning.md`, `references/schemas.md`, `references/artifact-flow-chain.md`
