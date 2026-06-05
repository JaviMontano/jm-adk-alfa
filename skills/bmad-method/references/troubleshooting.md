# BMAD Troubleshooting — Diagnostic Guide

## Table of Contents
- [How to Use This Guide](#how-to-use-this-guide)
- [Phase 1 Issues (Analysis)](#phase-1-issues-analysis)
- [Phase 2 Issues (Planning)](#phase-2-issues-planning)
- [Phase 3 Issues (Solutioning)](#phase-3-issues-solutioning)
- [Phase 4 Issues (Implementation)](#phase-4-issues-implementation)
- [Quick Flow Issues](#quick-flow-issues)
- [Cross-Phase Issues](#cross-phase-issues)
- [Context and Agent Issues](#context-and-agent-issues)
- [Brownfield Adoption Issues](#brownfield-adoption-issues)
- [Diagnostic Questions Flowchart](#diagnostic-questions-flowchart)

---

## How to Use This Guide

Each entry follows the format: **Symptom** (what you observe), **Diagnosis** (root cause), **Fix** (concrete action), **Agent** (who owns the fix), **Reference** (where to find details).

Start with the phase where the problem manifests. If the symptom spans phases, check [Cross-Phase Issues](#cross-phase-issues).

---

## Phase 1 Issues (Analysis)

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 1.1 | Product brief is vague — no measurable success criteria | Mary accepted stakeholder input verbatim without validation | Rerun brainstorming workflow. Add SMART criteria: each metric must have a number, a baseline, and a deadline. | Mary (Analyst) | `references/phase-1-analysis.md` |
| 1.2 | Brief contains solution assumptions ("we will use React") | Analysis conflated problem definition with solutioning | Strip all technology references from the brief. Technology decisions belong in Phase 3 only. | Mary (Analyst) | `references/methodology-overview.md#core-principles` |
| 1.3 | Phase 1 stalls — analyst keeps researching without converging | No exit criteria defined for the analysis phase | Time-box analysis to 2 sessions max. The brief is a hypothesis, not a thesis. If 3+ open questions remain after 2 sessions, document them as risks and proceed to Phase 2. | Mary (Analyst) | `references/phase-1-analysis.md` |
| 1.4 | Multiple contradictory product directions in the brief | Stakeholder alignment was not achieved before analysis | HALT. Escalate to the user. Present the contradictions as a numbered list with trade-offs. The user must choose one direction before Phase 2 can start. | Orchestrator | `references/methodology-overview.md` |

---

## Phase 2 Issues (Planning)

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 2.1 | PRD has 50+ functional requirements for an MVP | Scope was not bounded; every stakeholder wish became an FR | Apply MoSCoW. An MVP PRD must have no more than 15 Must-have FRs. Move the rest to Should/Could/Won't. If you cannot prioritize, the brief's scope boundaries are insufficient — return to Phase 1. | John (PM) | `references/phase-2-planning.md` |
| 2.2 | FRs are not testable ("the system should be user-friendly") | Requirements were written as goals, not behaviors | Rewrite every FR in the format: "The system SHALL [verb] [object] when [condition]." If you cannot write a test for it, it is not an FR — it is a goal and belongs in the brief. | John (PM) | `references/schemas.md` |
| 2.3 | UX spec contradicts PRD requirements | Sally (UX) worked from the brief instead of the PRD | UX spec must be derived from the PRD, not the brief. Reload the PRD as primary input. Cross-reference every UX flow to its FR-IDs. | Sally (UX) | `references/artifact-flow-chain.md` |
| 2.4 | Personas are fictional archetypes with no grounding | No user research or data informed persona creation | Personas must cite evidence: interview quotes, analytics data, or explicit `[ASSUMPTION]` tags. Remove any persona trait that has no source. | Sally (UX) | `references/phase-2-planning.md` |
| 2.5 | PRD keeps changing after Phase 2 "completes" | No formal scope-change protocol enforced | Every post-Phase-2 PRD change must follow the impact analysis protocol: create an impact analysis record, trace downstream effects, update traceability matrix. Tag changes with `[SCOPE-CHANGE]`. | John (PM) | `references/artifact-flow-chain.md#impact-analysis` |

---

## Phase 3 Issues (Solutioning)

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 3.1 | Architecture document does not reference the PRD | Architect designed from memory or preferences, not requirements | Rebuild the architecture with the PRD loaded. Every component must trace to at least one FR. Run `validate_prd.py` to verify cross-references. | Winston (Architect) | `references/phase-3-solutioning.md` |
| 3.2 | Stories are epics in disguise (8+ story points each) | Decomposition stopped too early | Apply the INVEST criteria. No story may exceed 5 points. If the story cannot be split, it has hidden complexity — document it and split along boundaries (API, data, UI). | Bob (Scrum Master) | `references/implementation-readiness-gate.md#step-3` |
| 3.3 | Gate fails repeatedly on the same step | Systemic gap in Phase 3 process for that domain | After 3 failures on the same step: (1) create a team training story, (2) add a pre-gate checklist item for that specific area, (3) review if the gate step criteria are appropriate for this project type. | Gate Reviewer | `references/implementation-readiness-gate.md#gate-metrics-history` |
| 3.4 | Circular dependencies between stories | Story decomposition was function-based instead of slice-based | Redesign stories as vertical slices (each story delivers end-to-end value through one narrow path). Remove the circular link. Run `check_artifact_flow.py` to validate the DAG. | Bob (Scrum Master) | `references/implementation-readiness-gate.md#step-5` |
| 3.5 | No ADRs exist but multiple technology decisions were made | Architect made decisions informally without documenting rationale | Retroactively create an ADR for every technology choice in the architecture doc. Each ADR must include: context, decision, alternatives considered, consequences. | Winston (Architect) | `references/schemas.md#4-architecture-document-frontmatter` |
| 3.6 | Gate passes but implementation immediately hits issues | Gate evaluated artifact completeness but not technical correctness | The gate validates documentation, not feasibility. Create a spike story (time-boxed to 4 hours) for any architecture component the team has not built before. Run the spike before the first sprint. | Winston (Architect) | `references/implementation-readiness-gate.md#limits` |

---

## Phase 4 Issues (Implementation)

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 4.1 | Velocity drops >30% for 2 consecutive sprints | Misestimation, hidden dependencies, or architecture mismatch | Run root-cause analysis: (a) check carry-over ratio, (b) count blockers, (c) compare estimates to actuals. If estimates are consistently 2x off, re-calibrate the entire backlog. | Bob (Scrum Master) | `references/phase-4-implementation.md#velocity-anomaly-detection` |
| 4.2 | Sprint has >25% of points blocked simultaneously | Dependency mapping failure in Phase 3 | Immediately re-sequence: pull unblocked stories forward, resolve blocking stories as top priority. Update the dependency graph. Add a dependency validation step to future sprint planning. | Bob (Scrum Master) | `references/phase-4-implementation.md#handling-blockers` |
| 4.3 | AI-generated code passes tests but does not match the AC | Tests were generated from implementation, not from acceptance criteria | Delete the tests. Re-read the story's Given/When/Then. Write tests manually from the AC text. Then regenerate code to pass those tests. This is a TDD violation — the test must precede the code. | Amelia (Developer) | `references/phase-4-implementation.md#test-driven-story-development` |
| 4.4 | sprint-status.yaml is stale or never updated | Developer treats tracking as overhead instead of tool | Mandate sprint-status.yaml update as part of the Definition of Done for every story. If a story is "done" but sprint-status.yaml does not reflect it, the story is not done. Run `generate_sprint_status.py` to scaffold updates. | Amelia (Developer) | `references/phase-4-implementation.md#sprint-tracking` |
| 4.5 | Mid-sprint requirement changes derail the sprint | No scope protection during active sprints | Invoke the scope freeze protocol: new requirements enter the backlog, never the active sprint. If the change is critical, trade out a same-sized story. Document the swap in the sprint retro. | John (PM) | `references/phase-4-implementation.md#when-to-correct-course` |
| 4.6 | Completed points <40% of velocity target (sprint failure) | Sprint overcommitment or unresolved blockers | Execute sprint failure recovery: (1) stop new story starts, (2) stabilize in-progress work, (3) classify all incomplete stories, (4) carry over max 2, (5) run focused retrospective. | Bob (Scrum Master) | `references/phase-4-implementation.md` [R8] |
| 4.7 | Code does not follow project-context.md conventions | Context was not loaded or developer ignored constraints | Add a pre-commit validation step that checks for convention violations. Include project-context.md in every developer agent's `context.required_files`. | Amelia (Developer) | `references/progressive-context.md` |

---

## Quick Flow Issues

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 5.1 | Quick Flow change introduces a regression | Insufficient self-review or missing test coverage in affected area | Revert immediately. Write a proper story with comprehensive AC including the regression scenario. Do not attempt a second Quick Flow in the same area. | Barry (Quick Flow) | `references/quick-flow.md#edge-cases` |
| 5.2 | 4+ consecutive Quick Flows in the same feature area | Accumulated Quick Flows indicate emerging complexity | Stop. Review the last 3-4 changes. Write a retroactive story consolidating them. Proceed with remaining work as Phase 3-4 flow. | Barry (Quick Flow) | `references/quick-flow.md` [R10] |
| 5.3 | Quick Flow touches a file in an exclusion zone | Scope check did not verify exclusion zones | Abort Quick Flow immediately. Exclusion zones override all Quick Flow eligibility. Route to full BMAD flow with the Architect reviewing the change. | Barry (Quick Flow) | `references/quick-flow.md#edge-cases` |
| 5.4 | Quick Flow scope expands mid-implementation (>3 files) | Underestimated complexity at triage | Escalate to full BMAD. Preserve the rapid spec and work done so far — they become inputs to Phase 3. The rapid spec is not wasted. | Barry (Quick Flow) | `references/quick-flow.md#when-to-escalate-to-full-flow` |
| 5.5 | Cannot write clear acceptance criteria for a Quick Flow in 2 minutes | The change is not well-understood enough for Quick Flow | Escalate. If you cannot specify it in 2 minutes, you cannot implement it safely without a proper story. | Barry (Quick Flow) | `references/quick-flow.md#triage-criteria` |

---

## Cross-Phase Issues

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 6.1 | Artifacts contradict each other (PRD says X, architecture says Y) | Change propagation protocol was not followed after an upstream change | Run the impact analysis algorithm: (1) identify the changed artifact, (2) trace downstream dependencies, (3) update all affected artifacts, (4) re-validate the traceability matrix. The upstream artifact wins unless a formal scope change overrides it. | John (PM) or Winston (Architect) | `references/artifact-flow-chain.md#conflict-resolution` |
| 6.2 | Orphan stories exist (stories referencing removed FRs) | Backward scan was not run after PRD changes | Run `check_artifact_flow.py`. Archive all orphan stories with an explanation note. Never delete — archive. Update the traceability matrix. | Bob (Scrum Master) | `references/artifact-flow-chain.md#orphan-detection` |
| 6.3 | project-context.md is >2K tokens | Too much detail embedded instead of linked | Refactor: move detailed sections to linked documents. project-context.md retains summaries and links only. Each section must be 2-3 sentences max. | Orchestrator | `references/progressive-context.md` [R25] |
| 6.4 | New team member cannot understand the project from project-context.md alone | Missing sections or stale content | Validate against the schema: Vision, Tech Stack, Constraints, Conventions, Team, Links. Every section must be current. If a new reader cannot explain the project in 2 minutes after reading it, the document has failed its purpose. | Orchestrator | `references/project-context-guide.md` |
| 6.5 | Phase skipping — developer starts coding without passing the gate | Process discipline breakdown | The Orchestrator must verify artifact existence before routing to Phase 4. If gate-result file does not exist or shows FAIL, block Phase 4 entry. Make this a hard rule in the Orchestrator's routing logic. | Orchestrator | `references/implementation-readiness-gate.md` [R20] |
| 6.6 | Agent outputs are inconsistent across sessions | Persona definition is too vague or context loading varies | Tighten the persona's `identity` field to >=3 specific sentences. Pin `context.required_files` explicitly. Run the persona consistency test: 3 inputs, compare output structure across sessions — must be >80% similar. | Orchestrator | `references/agent-as-code.md#persona-design-principles` |

---

## Context and Agent Issues

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 7.1 | Agent produces hallucinated code patterns or libraries | Context window overloaded or critical context not loaded | Verify context loading against the phase table in `progressive-context.md`. Drop items from priority level 7 upward. Ensure project-context.md is loaded first. Never truncate artifacts mid-section. | Any agent | `references/progressive-context.md` [R27] |
| 7.2 | Agent ignores constraints from project-context.md | Constraints section is buried in the middle of a long context | Move constraints to the beginning of the context load (front-load critical information). Use the Context Priority Ranking — project-context.md must be position 1. | Any agent | `references/progressive-context.md#context-window-optimization` |
| 7.3 | Session exceeds 50 turns with degrading output quality | Conversational debris is consuming context capacity | Start a new session. Summarize the current state into project-context.md before closing. Load the updated project-context.md and current task in the new session. | Any agent | `references/progressive-context.md#avoiding-context-pollution` |
| 7.4 | Two agents produce conflicting outputs for the same task | Agent boundaries are unclear — task falls in an overlap zone | Consult the agent ownership: analysis=Mary, planning=John+Sally, solutioning=Winston+Bob, implementation=Amelia+Quinn. If overlap exists, the agent whose phase owns the artifact type is the authority. | Orchestrator | `references/agent-as-code.md` |
| 7.5 | Agent attempts work outside its phase | No `forbidden_actions` constraint defined | Add explicit `constraints.forbidden_actions` to the agent YAML. Example: Developer must not modify PRD or architecture files. Architect must not write implementation code. | Orchestrator | `references/agent-as-code.md#agent-yaml-format` |

---

## Brownfield Adoption Issues

| # | Symptom | Diagnosis | Fix | Agent | Reference |
|---|---------|-----------|-----|-------|-----------|
| 8.1 | AI agent modifies files in an exclusion zone | Exclusion zones were not defined before BMAD adoption started | Stop all AI-assisted work. Define exclusion zones immediately in project-context.md. List every file and directory that AI must not touch. Resume only after exclusion zones are confirmed. | Orchestrator | `references/brownfield-patterns.md` [R29] |
| 8.2 | Retroactive architecture document is already stale | No update protocol was established after initial creation | Add architecture doc update as a Definition of Done item for every story. Each PR that changes component behavior must update the corresponding architecture section. | Winston (Architect) | `references/brownfield-patterns.md#pitfall-3` |
| 8.3 | Team resists BMAD adoption — treats it as overhead | Big-bang adoption attempted instead of incremental | Fall back to Level 1 (stories only). Demonstrate value on one pilot feature. Show the before/after: rework rate, time-to-merge, defect count. Expand only after the pilot validates the approach. | Orchestrator | `references/brownfield-patterns.md#incremental-adoption-strategy` |
| 8.4 | Brownfield risk score is 0-4 but team attempted full adoption | Risk assessment was skipped or ignored | Re-score using the risk matrix. For scores 0-4, use Level 1 only (stories). Do not attempt architecture documentation or gate reviews until score improves through test coverage and CI pipeline additions. | Orchestrator | `references/brownfield-patterns.md` [R28] |
| 8.5 | Generated project-context.md does not match actual codebase | AI-generated documentation was not validated against code | Run the validation checklist: (1) does every listed component exist in code? (2) are tech stack versions accurate per lock files? (3) are there code components not listed? Fix every discrepancy before proceeding. | Winston (Architect) | `references/brownfield-patterns.md#validation` |

---

## Gate-Specific Troubleshooting

When the implementation readiness gate fails, use this targeted lookup to route remediation.

| Failed Step | Most Common Root Cause | Fastest Fix | Script to Run | Agent |
|-------------|----------------------|-------------|---------------|-------|
| Step 1 (PRD Completeness) | Missing out-of-scope section or vague success metrics | Add explicit out-of-scope items; convert metrics to SMART format | `validate_prd.py` | John (PM) |
| Step 2 (Architecture Alignment) | Architecture designed from preferences, not PRD FRs | Re-read PRD. Map every FR to a component. Add missing components. | `check_artifact_flow.py` | Winston (Architect) |
| Step 3 (Story Decomposition) | Stories are epics in disguise (>5 points) | Split along UI/API/data boundaries. Each slice must deliver testable value. | None — manual review | Bob (Scrum Master) |
| Step 4 (AC Quality) | Subjective language in acceptance criteria | Replace every adjective with a number. "fast" → "< 200ms p95" | None — manual review | Bob (Scrum Master) |
| Step 5 (Dependency Mapping) | Circular dependencies between stories | Redraw as vertical slices. Break the cycle by extracting shared logic into a foundation story. | `check_artifact_flow.py` | Bob (Scrum Master) |
| Step 6 (Risk Register) | No risk register exists at all | Create one. 5 risks minimum: 2 technical, 2 process, 1 timeline. Each with mitigation and owner. | None — manual creation | Winston (Architect) |
| Step 7 (NFR Coverage) | NFRs are aspirational ("should be fast") | Add specific thresholds. Every NFR must have a number and a measurement method. | `validate_prd.py` | John (PM) |
| Step 8 (API Contracts) | Only happy-path responses defined | Add error responses for every endpoint: 400, 401, 403, 404, 500. Standardize error object shape. | None — manual review | Winston (Architect) |
| Step 9 (Data Model) | Model contradicts API contracts | Align field names. Every API response field must trace to a model field. Document indexes. | None — manual review | Winston (Architect) |
| Step 10 (Security Review) | No auth strategy documented | Document: auth mechanism, token lifecycle, input validation approach, encryption strategy. | None — manual review | Winston (Architect) |
| Step 11 (Performance Targets) | No load testing approach | Define: latency targets (p50, p95, p99), throughput target, load testing tool and scenario. | None — manual creation | Winston (Architect) |
| Step 12 (Deployment Strategy) | Deployment is "implied" by existing CI | Document explicitly: environment list, CI stages, migration strategy, feature flag approach. | None — manual creation | Winston (Architect) |
| Step 13 (Rollback Plan) | No rollback triggers defined | Define: error rate threshold, latency threshold, manual trigger authority, rollback procedure. | None — manual creation | Winston (Architect) |

---

## Validation Script Reference

When diagnosing issues, these scripts provide automated checks only if they exist in the target BMAD project. Verify each path before running it; when absent, perform the corresponding manual check from this table.

| Script | Purpose | When to Run | Typical Output |
|--------|---------|-------------|----------------|
| `scripts/validate_prd.py` | Checks PRD schema compliance, FR format, NFR presence | After PRD changes, before gate | List of schema violations with field names |
| `scripts/validate_project.py` | Full project validation — artifacts, stories, context | Before gate, at sprint boundaries | Per-artifact pass/fail with details |
| `scripts/check_artifact_flow.py` | Traceability check — orphans, gaps, circular deps | After story changes, before gate | Orphan list, uncovered FRs, dependency graph issues |
| `scripts/generate_sprint_status.py` | Generates or updates sprint-status.yaml | Sprint planning, daily updates | Updated sprint-status.yaml file |
| `scripts/init_project.py` | Scaffolds initial project structure | Project start | Directory structure with template files |
| `scripts/export_project_report.py` | Generates project health report | Monthly, at retrospectives | Markdown report with metrics |

---

## Diagnostic Questions Flowchart

When a problem occurs, answer these questions in order to locate the root cause:

```
1. Is the problem in a specific artifact?
   ├── YES → Which phase produced the artifact?
   │         ├── Phase 1 → See Phase 1 Issues (1.1-1.4)
   │         ├── Phase 2 → See Phase 2 Issues (2.1-2.5)
   │         ├── Phase 3 → See Phase 3 Issues (3.1-3.6)
   │         └── Phase 4 → See Phase 4 Issues (4.1-4.7)
   └── NO → Is the problem between artifacts?
             ├── YES → See Cross-Phase Issues (6.1-6.6)
             └── NO → Is the problem with an agent?
                       ├── YES → See Context and Agent Issues (7.1-7.5)
                       └── NO → Is this a brownfield project?
                                 ├── YES → See Brownfield Issues (8.1-8.5)
                                 └── NO → Is this Quick Flow?
                                           ├── YES → See Quick Flow Issues (5.1-5.5)
                                           └── NO → Check the sprint retro for patterns
```

### Triage by Urgency

| Urgency | Criteria | Action |
|---------|----------|--------|
| **Immediate** | Sprint is blocked, gate is failing repeatedly, security vulnerability discovered | Drop everything. Fix the blocking issue. See Emergency Procedures below. |
| **This Sprint** | Rework rate >20%, velocity dropping, artifact contradictions | Schedule fix within current sprint. Create a remediation story if needed. |
| **Next Sprint** | Process inefficiency, stale artifacts, agent persona drift | Add to retro action items. Schedule fix in next sprint planning. |
| **Backlog** | Cosmetic issues, minor template improvements, nice-to-have automation | Create a chore story. Prioritize against feature work. |

### Emergency Procedures

| Emergency | Immediate Action | Follow-Up |
|-----------|-----------------|-----------|
| AI generated code that passed tests but has a security vulnerability | Revert the commit. Run security scan. Create a security-focused story with explicit security AC. | Add security check to CI pipeline. Update gate step 10 criteria. |
| Sprint is failing (<40% velocity at midpoint) | Stop new story starts. Stabilize in-progress work. | Run sprint failure recovery protocol [R8]. |
| Critical artifact is corrupted or lost | Restore from Git history (`git log --all -- path/to/file`). | Add artifact backup verification to the sprint boundary checklist. |
| Agent enters an infinite loop (keeps revising without converging) | End the session. Start fresh with narrower scope. | Tighten the agent's success criteria. Add a max-iterations constraint (3 revisions max, then HALT for human review). |
| Two agents produce contradictory outputs causing downstream confusion | HALT both agents. Identify which agent's domain owns the decision. Apply the conflict resolution protocol. | Document the conflict as CR-NNN. Add domain boundary clarification to agent YAML. |
| Gate has failed 3 times on the same step | Stop re-running the gate. Escalate to a human architecture review session. The problem is systemic, not incremental. | Create a training story. Add a pre-gate checklist for the failing area. |

---

## Assumptions

- All BMAD artifacts are version-controlled in Git and recoverable from history
- The team either has access to BMAD validation scripts or can run the corresponding manual checks from this guide
- At least one team member can interpret diagnostic output and route fixes to the correct phase

## Limits

- This guide diagnoses process and artifact problems — it does NOT diagnose code bugs or runtime errors
- This guide does NOT cover LLM-specific issues (model selection, token limits, API rate limiting)
- Fixes reference existing BMAD protocols — this guide does NOT introduce new processes

## Acceptance Criteria

- [ ] Every issue has a concrete, actionable fix (not "investigate further")
- [ ] Every fix references the responsible agent and the source reference document
- [ ] The diagnostic flowchart routes to the correct section for any given problem type
- [ ] Emergency procedures provide immediate containment actions, not just analysis steps

See also: `references/methodology-overview.md`, `references/artifact-flow-chain.md`, `references/implementation-readiness-gate.md`, `references/phase-4-implementation.md`, `references/quick-flow.md`, `references/brownfield-patterns.md`
