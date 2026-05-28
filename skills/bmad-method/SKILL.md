---
name: bmad-method
description: >
  Teach and apply the BMAD (Breakthrough Method for Agile AI-Driven Development)
  methodology for AI-driven software development. Covers the full 4-phase lifecycle:
  Analysis, Planning, Solutioning, and Implementation with 8 specialized agent personas.
  Use when: user mentions BMAD, wants AI-driven development workflow, needs PRD or
  architecture document, wants sprint planning with AI agents, asks about documentation-first
  development, needs implementation readiness gate, wants to scaffold a project with
  agent-as-code patterns, says "new project", "set up development workflow", "create stories
  from PRD", "check implementation readiness", or "run a sprint".
license: MIT
metadata:
  version: "1.0.0"
  bmad-version: "v6-alpha"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
  - TodoWrite
context:
  - type: file
    path: references/schemas.md
version: 1.0.0
---

# BMAD Method — Breakthrough Method for Agile AI-Driven Development

## 1. What is BMAD

BMAD is a **documentation-first, agent-driven** software development framework. Each of 4 sequential phases produces artifacts that become mandatory context for the next. Code is a **downstream derivative** of specifications. [EXPLICIT]

**The 4-phase model**:
1. **Analysis** — Explore problem space, validate ideas (Mary/Analyst)
2. **Planning** — Define what to build and for whom (John/PM, Sally/UX)
3. **Solutioning** — Decide how to build it, decompose into stories (Winston/Architect, Bob/Scrum Master)
4. **Implementation** — Build it, one story at a time (Amelia/Developer, Quinn/QA)

**Quick Flow**: Barry agent bypasses phases 1-3 for changes ≤3 story points with no architectural impact.

## Scope & Limits

BMAD **is**:
- A documentation-first methodology for AI-driven development
- A phase-gated workflow with mandatory artifact handoffs
- An agent-as-code framework for persona-driven AI collaboration

BMAD **is NOT**:
- A CI/CD tool — it produces artifacts consumed by CI/CD, but does not replace Jenkins/GitHub Actions/etc.
- A project management replacement — it complements Jira/Linear, not replaces them
- A testing framework — Quinn generates tests using the project's existing test infrastructure
- A design tool — Sally produces structural UX specs, not Figma-level visual designs
- A deployment platform — architecture docs describe deployment, but BMAD does not execute it

## Decision Log

| # | Decision | Rationale | Alternatives Rejected |
|---|----------|-----------|-----------------------|
| D1 | Documentation-first over code-first | AI agents perform better with structured context than with ambiguous verbal instructions `[EVIDENCIA: references/methodology-overview.md]` | Code-first with retroactive docs — leads to specification drift |
| D2 | 4-phase sequential model | Progressive context accumulation prevents rework; each phase narrows the solution space `[EVIDENCIA: references/artifact-flow-chain.md]` | Parallel phases — causes misalignment between artifacts |
| D3 | Agent-as-code (YAML personas) | Reproducible agent behavior; version-controlled with Git `[EVIDENCIA: references/agent-as-code.md]` | Free-form prompting — inconsistent results across sessions |
| D4 | Mandatory readiness gate before Phase 4 | Implementation without validated specs produces 3-5x rework `[INFERENCIA]` | Optional gate — teams skip it under pressure, then pay later |
| D5 | HALT-sharded workflow steps | Prevents AI from reading ahead and conflating steps `[EVIDENCIA: references/schemas.md]` | Single-file workflows — AI skips steps or blends context |
| D6 | Quick Flow bypass for small changes | Full BMAD ceremony for ≤3-point changes creates overhead exceeding value `[INFERENCIA]` | Always full flow — impractical for bug fixes |
| D7 | Brownfield entry at Phase 2-3 | Existing codebases already have implicit analysis; forcing Phase 1 wastes effort `[EVIDENCIA: references/brownfield-patterns.md]` | Always start at Phase 1 — redundant for established projects |

## 2. Three Dimensions

| Dimension | What | Start here |
|-----------|------|------------|
| **DECLARE** | Set up BMAD: install, configure, define agents, create workflows | Section 4 |
| **USE** | Operate BMAD: run workflows, produce artifacts, manage gates | Section 5-7 |
| **APPLY** | Apply BMAD in real projects: greenfield, brownfield, enterprise | Section 8 |

Reference Index: Section 10. [EXPLICIT]

## 3. Quick Start

### Entry Point A — New Project (Full Flow)
```
1. Run: python scripts/init_project.py <project-name> --greenfield
2. Activate Mary (Analyst) → produce product-brief.md
3. Follow phase-by-phase workflow in workflows/full-flow/
```

### Entry Point B — Specific Phase
```
1. Identify your current phase (1-4)
2. Read the corresponding prompt: prompts/phase-N-to-M-handoff.md
3. Activate the phase agent and produce the required artifact
```

### Entry Point C — Quick Fix / Small Feature
```
1. Activate Barry (Quick Flow) agent
2. Follow workflows/quick-flow/ (triage → implement → verify)
3. No PRD/architecture needed — story-level documentation only
```

## 4. DECLARE — Setting Up BMAD

### 4.1 Project Initialization

Run the init script to scaffold a BMAD project: [EXPLICIT]
```bash
python scripts/init_project.py <project-name> [--greenfield|--brownfield]
```

This creates: [EXPLICIT]
```
<project-name>/
├── .bmad/
│   ├── project-context.md    # Project constitution (from template)
│   ├── agents/               # Custom agent definitions
│   └── config.yaml           # BMAD configuration
├── planning_artifacts/       # PRD, UX spec, product brief
├── architecture/             # Architecture docs, ADRs
├── epics/                    # Epic definitions
├── stories/                  # User stories
├── sprints/                  # Sprint status and plans
└── project-knowledge/        # Codebase documentation (brownfield)
```

### 4.2 Project Context (Constitution)

The `project-context.md` file is your project's constitution. Every workflow loads it automatically. Create from template: [EXPLICIT]
- Template: `templates/project-context.md.tmpl`
- Guide: `references/project-context-guide.md`

Key sections: Vision, Tech Stack, Constraints, Conventions, Team, Links. [EXPLICIT]

### 4.3 Agent Definition

Agents are defined as YAML files with persona, menu, and prompts. To create a custom agent: [EXPLICIT]
```bash
python scripts/scaffold_agent.py <agent-name> --role "<role description>"
```

Agent YAML structure — see `references/agent-as-code.md`: [EXPLICIT]
```yaml
metadata:
  id: agent-code
  name: Display Name
  icon: emoji
persona:
  role: Professional title
  identity: Background and personality
  communication_style: How the agent speaks
  principles: [Core beliefs]
menu:
  - trigger: "XX"
    description: Workflow name
    workflow: path/to/workflow
```

### 4.4 Workflow Configuration

Workflows are sharded into step files for sequential execution. To scaffold a new workflow: [EXPLICIT]
```bash
python scripts/scaffold_workflow.py <workflow-name> --steps 5
```

This creates `step-01-init.md` through `step-05-name.md` with HALT commands preventing AI read-ahead. See `references/schemas.md` for the step file schema. [EXPLICIT]

## 5. USE — Operating BMAD Phase by Phase

### 5.1 Phase 1: Analysis

**Agent**: Mary (Analyst) — `agents/mary-analyst.md` | **Goal**: Explore problem space before committing to planning.

| Workflow | Output | Required |
|----------|--------|----------|
| Brainstorming | brainstorming-report.md | Optional |
| Research (domain/market/technical) | Research findings | Optional |
| Create Product Brief | product-brief.md | **Yes** |

**Procedure**:
1. Read `references/phase-1-analysis.md` for detailed guidance
2. Activate Mary agent persona
3. Conduct brainstorming if problem space is unclear
4. Perform domain/market research as needed
5. Produce `product-brief.md` in `planning_artifacts/`
6. Validate: brief covers problem, audience, goals, success metrics

**Failure Recovery**:
- **Mary cannot validate assumptions** (no data available): Document as `[ASSUMPTION]` with Low confidence, proceed with explicit risk acknowledgment in brief. Flag to John/PM that these assumptions must be validated before PRD is finalized.
- **Brainstorming yields no viable direction**: Narrow the problem scope — split into sub-problems and research each independently. If still blocked, escalate to user for additional domain context.

**Transition**: Use `prompts/phase-1-to-2-handoff.md` to hand off to Phase 2.

### 5.2 Phase 2: Planning

**Agents**: John (PM) + Sally (UX) — `agents/john-pm.md`, `agents/sally-ux.md`
**Goal**: Define what to build and for whom.

**Workflows**:
| Workflow | Output | Required |
|----------|--------|----------|
| Create PRD | PRD.md | Yes |
| Create UX Design | ux-spec.md | Yes (if UI) |

**Procedure**:
1. Read `references/phase-2-planning.md`
2. Load `product-brief.md` as input context
3. As John/PM: Create PRD using `templates/prd.md.tmpl`
   - Define functional requirements (FRs) and non-functional requirements (NFRs)
   - Set success metrics (measurable, SMART)
   - Map user personas and journeys
4. As Sally/UX: Create UX spec with user flows, wireframes, design constraints
5. Validate: PRD covers all brief requirements, UX aligns with PRD

**Failure Recovery**:
- **PRD requirements conflict with brief**: Surface conflicts to user with specific brief sections vs. PRD sections. User must resolve before proceeding.
- **UX spec cannot satisfy all PRD requirements**: Document which FRs are UX-constrained, propose trade-offs to John/PM. Never silently drop requirements.

**Transition**: Use `prompts/phase-2-to-3-handoff.md`.

### 5.3 Phase 3: Solutioning

**Agents**: Winston (Architect) + Bob (Scrum Master) — `agents/winston-architect.md`, `agents/bob-scrum-master.md`
**Goal**: Decide how to build it and break work into implementable stories.

**Workflows**:
| Workflow | Output | Required |
|----------|--------|----------|
| Create Architecture | architecture.md + ADRs | Yes |
| Create Epics & Stories | epics/*.md, stories/*.md | Yes |
| Check Implementation Readiness | Gate: PASS/CONCERNS/FAIL | Yes |

**Procedure**:
1. Read `references/phase-3-solutioning.md`
2. Load PRD.md + ux-spec.md as input context
3. As Winston/Architect:
   - Create architecture using `templates/architecture-doc.md.tmpl`
   - Document ADRs (Architecture Decision Records)
   - Define component diagram, data model, API contracts, deployment strategy
4. As Bob/Scrum Master:
   - Decompose into epics using `templates/epic.md.tmpl`
   - Write stories using `templates/user-story.md.tmpl`
   - Sequence stories by dependency, estimate complexity
5. **Run Implementation Readiness Gate** (Section 7)

**Failure Recovery**:
- **Architecture cannot satisfy an NFR**: Create an ADR documenting the constraint, propose alternatives to user (e.g., relaxed SLA, different tech stack). Never silently ignore an NFR.
- **Story decomposition reveals PRD gaps**: Escalate to John/PM with specific missing requirements. Do not invent requirements — return to Phase 2 for PRD amendment.
- **Gate returns FAIL**: See Section 7 for concrete remediation steps.

**Transition**: Only proceed if gate returns PASS. Use `prompts/phase-3-to-4-handoff.md`.

### 5.4 Phase 4: Implementation

**Agents**: Amelia (Developer) + Quinn (QA) — `agents/amelia-developer.md`, `agents/quinn-qa.md`
**Goal**: Build it, one story at a time, with continuous validation.

**Workflows**:
| Workflow | Output | Required |
|----------|--------|----------|
| Sprint Planning | sprint-status.yaml | Yes |
| Create Story | story-[slug].md (detailed) | Per story |
| Dev Story | Working code + tests | Per story |
| Code Review | Approval or revision | Per story |
| Retrospective | Lessons learned | Per sprint |

**Procedure**:
1. Read `references/phase-4-implementation.md`
2. Sprint Planning:
   - Select stories for sprint from prioritized backlog
   - Create sprint-status.yaml using `scripts/generate_sprint_status.py`
   - Use `prompts/sprint-kickoff-prompt.md`
3. Per Story:
   - Load story file + architecture.md + project-context.md as context
   - As Amelia/Developer: Implement on branch, write tests, follow project conventions
   - As Quinn/QA: Review code against acceptance criteria, run tests
   - Use `templates/code-review-checklist.md.tmpl`
4. Sprint Close:
   - Update sprint-status.yaml (mark stories complete/needs-fixes)
   - Run retrospective using `prompts/retrospective-prompt.md`
   - Archive completed epics

**Failure Recovery**:
- **Story implementation reveals architectural gap**: STOP implementation. Escalate to Winston/Architect. Create an ADR for the gap, update architecture.md, then resume.
- **Tests fail acceptance criteria despite correct implementation**: Revisit acceptance criteria with Bob/SM — criteria may be ambiguous or incorrect. Amend story, not code.
- **Sprint velocity drops below 50% of planned**: Bob/SM triggers a mid-sprint review. Remove lowest-priority stories, do NOT add scope. Document in retrospective.

### 5.5 Quick Flow (Barry Agent)

**Agent**: Barry (Quick Flow Dev) — `agents/barry-quick-flow.md`
**When to use**: Bug fixes, small features in established codebases, prototypes, single-story changes.

**Procedure**:
1. Read `references/quick-flow.md`
2. Triage: Confirm scope is small enough for quick flow (no PRD/arch needed)
3. Write a lightweight tech spec (story-level)
4. Implement directly with tests
5. Self-review against `templates/code-review-checklist.md.tmpl`

## 6. USE — Artifact Flow Chain

Each phase's output becomes mandatory input for the next: [EXPLICIT]

```
product-brief.md ──→ PRD.md ──→ architecture.md ──→ epics/*.md ──→ stories/*.md ──→ Code
     (Phase 1)      (Phase 2)     (Phase 3)         (Phase 3)      (Phase 4)     (Phase 4)
```

**Rules**:
- Never skip upstream artifacts — architecture without PRD produces drift
- Cross-reference: PRD references brief, architecture references PRD, stories reference epics
- When upstream changes, downstream must be reviewed for impact

**Validate the chain**:
```bash
python scripts/check_artifact_flow.py <project-root>
```

This reports: broken references, orphaned artifacts, missing cross-links. [EXPLICIT]

See `references/artifact-flow-chain.md` for the full dependency model. [EXPLICIT]

## 7. USE — Implementation Readiness Gate

The gate is a **mandatory checkpoint** before Phase 4. It validates that planning and solutioning artifacts are complete and aligned. Run with `python scripts/validate_prd.py <project-root>`. Output: `PASS` / `CONCERNS` / `FAIL`. See `references/implementation-gate-details.md` for the 13 validation steps, gate result actions, FAIL remediation routing, and agent roster. [EXPLICIT]

## 8. APPLY — Real Project Patterns

### 8.1 Greenfield vs Brownfield

| Factor | Greenfield | Brownfield |
|--------|-----------|------------|
| Start phase | Phase 1 (Analysis) | Phase 2 or 3 (skip brief) |
| Init flag | `--greenfield` | `--brownfield` |
| Extra step | None | Run Document Project workflow first |
| project-context.md | Created from scratch | Generated from codebase scan |
| Key reference | `references/greenfield-patterns.md` | `references/brownfield-patterns.md` |

### 8.2 Enterprise Scaling

For multi-team BMAD adoption, see `references/enterprise-governance.md`: [EXPLICIT]
- Shared project-context.md across teams
- Cross-team dependency management in epics
- Compliance artifacts (audit trail via Git versioning)
- Centralized gate reviews

### 8.3 BMAD Lite (Solo/Small Scope)

For solo developers or projects ≤2 weeks, see `references/bmad-lite.md`: [EXPLICIT]
- 3-stage compressed workflow: Define → Design → Build
- 5-step gate instead of 13-step
- Solo agent model cycling through 3 perspectives
- Upgrade signals: when to switch from Lite to Full

### 8.4 Customization

See `references/customization-guide.md`: [EXPLICIT]
- Add/remove phases, create custom agents, modify gate criteria
- Integrate with external tools (Jira, Linear) via `references/integration-patterns.md`

### 8.5 Diagnostics & Quality

| Need | Tool |
|------|------|
| Lint all artifacts | `scripts/lint_artifacts.py <project-root>` |
| Diagnose project health | `scripts/diagnose_project.py <project-root>` |
| Troubleshoot a stalled workflow | `references/troubleshooting.md` |
| Resolve inter-agent conflicts | `references/conflict-resolution-protocol.md` |
| Measure BMAD effectiveness | `references/metrics-framework.md` |
| Identify anti-patterns | `references/anti-patterns-catalog.md` |

### 8.6 Operational Checklists

Standalone checklists for quick operational verification: [EXPLICIT]

| Checklist | Use when |
|-----------|----------|
| `checklists/phase-1-complete.md` | Before handing off from Mary to John |
| `checklists/phase-2-complete.md` | Before handing off from John/Sally to Winston/Bob |
| `checklists/phase-3-complete.md` | Before running the 13-step gate |
| `checklists/sprint-ready.md` | Before starting a sprint |
| `checklists/story-ready.md` | Before picking up a story for development |
| `checklists/story-done.md` | Before marking a story as complete |
| `checklists/quick-flow-triage.md` | Before starting a quick flow |

## 9. Agent Roster

11 agents across 4 phases: Mary (Analyst, Phase 1), John (PM, Phase 2), Sally (UX, Phase 2), Winston (Architect, Phase 3), Bob (Scrum Master, Phase 3-4), Amelia (Developer, Phase 4), Quinn (QA, Phase 4), Barry (Quick Flow, any phase), Orchestrator (meta-router), Gate Reviewer (impartial evaluator), Retro Facilitator. See `references/implementation-gate-details.md` for the full roster with conflict resolution rules.

## 10. Reference Index

| Need | Read |
|------|------|
| BMAD theory, principles, glossary | `references/methodology-overview.md` |
| Phase 1 deep guide | `references/phase-1-analysis.md` |
| Phase 2 deep guide | `references/phase-2-planning.md` |
| Phase 3 deep guide | `references/phase-3-solutioning.md` |
| Phase 4 deep guide | `references/phase-4-implementation.md` |
| Quick Flow guide | `references/quick-flow.md` |
| Agent YAML spec | `references/agent-as-code.md` |
| project-context.md guide | `references/project-context-guide.md` |
| Artifact dependency model | `references/artifact-flow-chain.md` |
| 13-step gate spec | `references/implementation-readiness-gate.md` |
| Context engineering | `references/progressive-context.md` |
| Existing codebase adoption | `references/brownfield-patterns.md` |
| New project patterns | `references/greenfield-patterns.md` |
| Multi-team/enterprise | `references/enterprise-governance.md` |
| Adapting BMAD | `references/customization-guide.md` |
| YAML/JSON schemas | `references/schemas.md` |
| Troubleshooting stalled workflows | `references/troubleshooting.md` |
| CI/CD, Git hooks, IDE integration | `references/integration-patterns.md` |
| KPIs and effectiveness measurement | `references/metrics-framework.md` |
| Inter-agent conflict resolution | `references/conflict-resolution-protocol.md` |
| Anti-pattern catalog (27 entries) | `references/anti-patterns-catalog.md` |
| Simplified BMAD for solo devs | `references/bmad-lite.md` |

## 11. Assumptions

- The user has Python 3.8+ available for running BMAD scripts
- The project uses Git for version control
- AI agents operate within a single-session context window (artifacts must be file-based, not memory-based)
- The user can provide domain knowledge when Mary/Analyst cannot find sufficient data
- Templates (`.tmpl` files) exist and are accessible at `templates/` relative to the skill directory
- The project has or will have a test framework — BMAD does not prescribe which one
- One user operates all agents (BMAD does not currently support multi-user concurrent agent sessions)

## Usage

Example invocations: [EXPLICIT]

- "/bmad-method" — Run the full bmad method workflow
- "bmad method on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
