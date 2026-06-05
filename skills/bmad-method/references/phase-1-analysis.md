# Phase 1 — Analysis: Deep Reference Guide

## Table of Contents
- [Purpose of Phase 1](#purpose-of-phase-1)
- [When to Run Analysis vs Skip](#when-to-run-analysis-vs-skip)
- [Brainstorming Techniques](#brainstorming-techniques)
- [Research Methods](#research-methods)
- [Product Brief Format](#product-brief-format)
- [Evidence Tagging](#evidence-tagging)
- [Common Mistakes](#common-mistakes)
- [Handoff Criteria to Phase 2](#handoff-criteria-to-phase-2)

---

## Purpose of Phase 1

Phase 1 transforms a vague idea into a validated product brief. The goal is not to plan the solution — it is to understand the problem deeply enough that a plan can be written without backtracking.

**Primary agent**: Analyst (Ana) — domain researcher, brainstormer, brief author.

**Inputs**: Raw idea, stakeholder conversations, market signals, existing documentation.

**Outputs**: Product Brief (the single artifact that gates entry to Phase 2).

**[R1] Time-box**: Phase 1 must complete within **2 sprints maximum** (4 weeks). If analysis cannot converge in that window, the scope is too broad — split into sub-problems and run Phase 1 on each independently.

| Project Size | Phase 1 Time-box | Research Depth |
|-------------|-----------------|----------------|
| MVP / internal tool | 1-2 days | Abbreviated: 1 research method minimum |
| Standard product feature | 3-5 days | Standard: 2 research methods minimum |
| New product / regulatory | 1-2 sprints | Full: 3+ research methods, stakeholder validation |

Phase 1 answers three questions:
1. What problem exists and for whom?
2. Is the problem worth solving (market, strategic, or technical justification)?
3. What are the boundaries of the solution space?

---

## When to Run Analysis vs Skip

Not every project needs a full Phase 1 cycle. Use this decision matrix:

| Signal | Action |
|--------|--------|
| Greenfield product, no prior research | Full Phase 1 |
| Existing product, new major feature | Abbreviated Phase 1 — focus on gap analysis |
| Bug fix or minor enhancement | Skip to Phase 4 via Quick Flow (Barry) |
| Proof of concept / spike | Abbreviated Phase 1 — focus on technical feasibility |
| Migration or rewrite with known scope | Skip brainstorming, run research only |
| Regulatory or compliance project | Full Phase 1 with heavy domain research |

**[R2] Skip criteria for Quick Flow escalation**: If the scope is under 3 story points, involves no new domain concepts, and touches fewer than 3 files, the Barry agent must handle it directly via Quick Flow without Phase 1. See `references/quick-flow.md`.

**[R3] Minimum Viable Brief Checklist** (for abbreviated Phase 1):
- [ ] Problem statement with at least one evidence tag
- [ ] One primary user segment identified with behavioral detail
- [ ] 2-3 success metrics (baselines may be "unknown")
- [ ] At least 2 out-of-scope items listed
- [ ] One explored alternative documented

If all 5 items are met, the abbreviated brief is sufficient for Phase 2 entry.

---

## Brainstorming Techniques

### SCAMPER

SCAMPER is a structured ideation checklist. Apply each lens to the problem space:

| Letter | Lens | Example Question |
|--------|------|-----------------|
| **S** | Substitute | What component could be replaced with something simpler? |
| **C** | Combine | Can two user workflows merge into one? |
| **A** | Adapt | What existing solution from another domain applies here? |
| **M** | Modify | What if we exaggerated or minimized a feature? |
| **P** | Put to other use | Can this tool serve a secondary audience? |
| **E** | Eliminate | What would happen if we removed this feature entirely? |
| **R** | Reverse | What if the user flow ran in the opposite direction? |

**Usage in BMAD**: Run SCAMPER after the initial problem statement is drafted. Document at least 3 SCAMPER-derived insights in the brief's "Explored Alternatives" section.

### Mind Mapping

Start with the core problem as the center node. Branch into:
- **Users** — Who is affected? Segment by role, frequency, expertise.
- **Pain points** — What specifically hurts? Quantify where possible.
- **Constraints** — Technical, legal, budgetary, time.
- **Opportunities** — What becomes possible if solved?

In text-based environments, represent mind maps as indented lists:

```
Problem: Slow onboarding for new developers
  Users
    Junior developers (0-2 years)
    Contractors (short-term engagement)
    Open source contributors
  Pain Points
    Environment setup takes 2+ days [DATA]
    No single source of truth for conventions [INFERENCE]
    Tribal knowledge locked in Slack threads [DATA]
  Constraints
    Must support Mac and Linux
    Budget: $0 tooling cost (open source only)
  Opportunities
    Reduce onboarding from 5 days to 4 hours
    Improve contributor retention by 30%
```

### How Might We (HMW)

Convert problem statements into opportunity questions:
- Problem: "Users abandon checkout when shipping is unclear."
- HMW: "How might we make shipping costs transparent before the cart page?"

Generate 5-10 HMW questions per major pain point. Prioritize by impact and feasibility. The top 3 HMW questions feed directly into the brief's scope section.

---

## Research Methods

### Domain Research

Understand the problem domain before proposing solutions.

- Interview stakeholders (or synthesize from provided transcripts)
- Map existing workflows end-to-end
- Identify domain vocabulary and create a glossary
- Document regulatory or compliance constraints
- Tag all findings: `[DATA]` for verified facts, `[INFERENCE]` for conclusions drawn

### Market Research

Position the product within the competitive landscape.

- Identify 3-5 direct competitors and 2-3 adjacent solutions
- Create a feature comparison matrix
- Identify differentiators and table-stakes features
- Assess market timing and trends
- Document market size estimates with source attribution

### Technical Research

Assess feasibility and technical constraints.

- Inventory existing systems, APIs, and data sources
- Identify integration points and their maturity
- Evaluate technology constraints (languages, platforms, cloud providers)
- Assess team capabilities and skill gaps
- Prototype critical unknowns (spike investigations)
- Document all findings with evidence tags

### Competitive Analysis

Go deeper than feature comparison:

- User experience teardown of top 2 competitors
- Pricing model analysis
- Review aggregation (app stores, G2, Reddit)
- Identify competitor weaknesses the product can exploit
- Document switching costs and lock-in risks

---

## Product Brief Format

The product brief is the single output artifact of Phase 1. It must be comprehensive enough to write a PRD from, but concise enough to read in 10 minutes.

### Required Sections

```markdown
# Product Brief: [Product Name]

## 1. Problem Statement
What problem exists, for whom, and why it matters now.
Tag severity: Critical / High / Medium / Low.

## 2. Target Users
Primary and secondary user segments with behavioral descriptions.
Not demographics — behaviors, goals, and frustrations.

## 3. Proposed Solution (High-Level)
One paragraph describing the solution concept.
No technical details — this is the "elevator pitch."

## 4. Success Metrics
3-5 measurable outcomes. Each metric must have:
- Current baseline (or "unknown — measure in Phase 2")
- Target value
- Measurement method

## 5. Scope Boundaries
What is explicitly IN scope and OUT of scope.
Out-of-scope items should note "Phase N" or "Never."

## 6. Key Risks
Top 3-5 risks with likelihood, impact, and mitigation strategy.

## 7. Research Summary
Condensed findings from domain, market, technical, and competitive research.
Every claim tagged with evidence type.

## 8. Explored Alternatives
At least 2 alternative approaches considered and why they were not chosen.

## 9. Open Questions
Unresolved items that Phase 2 must address.
```

### Quality Criteria

A brief is ready for Phase 2 when:
- [ ] Problem statement is specific enough to derive requirements from
- [ ] At least one user segment is described with behavioral detail
- [ ] Success metrics have baselines or explicit "unknown" markers
- [ ] Scope boundaries explicitly list at least 3 out-of-scope items
- [ ] All factual claims carry evidence tags
- [ ] Open questions list is present (even if empty)
- [ ] At least 2 alternatives were explored

---

## Evidence Tagging

Every claim in Phase 1 artifacts must carry an evidence tag. This is not optional — it prevents hallucinated requirements from propagating through the artifact chain.

| Tag | Meaning | Example |
|-----|---------|---------|
| `[DATA]` | Verified from a primary source | "Average checkout time is 4.2 minutes [DATA]" |
| `[INFERENCE]` | Logical conclusion from data | "Users likely abandon due to surprise shipping costs [INFERENCE]" |
| `[ASSUMPTION]` | Unverified belief requiring validation | "Mobile users prefer single-page checkout [ASSUMPTION]" |

**Rules**:
- `[DATA]` claims must cite the source (interview, analytics, documentation)
- `[INFERENCE]` must reference the data it derives from
- `[ASSUMPTION]` items automatically generate Open Questions for Phase 2
- Downstream artifacts inherit and refine these tags — they do not drop them

---

## Common Mistakes

### 1. Solutioning During Analysis
Jumping to architecture or technology choices before the problem is understood. Phase 1 must stay in problem space, not solution space.

### 2. Skipping Research for "Obvious" Problems
Even well-understood problems benefit from structured research. Obvious solutions often miss edge cases that research reveals.

### 3. Vague Success Metrics
"Improve user experience" is not a metric. "Reduce task completion time from 12 minutes to under 5 minutes" is.

### 4. No Out-of-Scope Documentation
Without explicit out-of-scope items, scope creep begins in Phase 2. Force yourself to list at least 3 things the product will NOT do.

### 5. Single-Perspective Analysis
Only talking to developers, only reading competitor websites, only analyzing data. Use at least 2 research methods to triangulate findings.

### 6. Untagged Claims
Statements without evidence tags become unverifiable requirements downstream. Tag everything — even when it feels obvious.

### 7. Treating the Brief as a Formality
The brief is the foundation for every downstream artifact. A weak brief creates weak PRDs, vague stories, and rework in Phase 4.

---

## Handoff Criteria to Phase 2

Phase 1 is complete when the product brief passes the following gate:

| Criterion | Verification |
|-----------|-------------|
| Problem is specific and scoped | Analyst reviews with stakeholder |
| At least 1 user segment defined | Behavioral description present, not just demographics |
| Success metrics are measurable | Each metric has target value and measurement method |
| Scope boundaries are explicit | IN and OUT of scope sections populated |
| Research is documented | At least 2 research methods used, findings tagged |
| Risks are identified | Top 3-5 risks with mitigation strategies |
| Open questions are captured | List exists in brief, even if empty |
| Evidence tags are applied | Spot-check: >80% of claims are tagged |

**Handoff artifact**: The completed `product-brief.md` file, committed to the project's `docs/` directory.

**Receiving agent**: Product Manager (PM) for Phase 2 planning.

**Handoff protocol**: Analyst summarizes the brief in 3 sentences and flags the top 3 open questions that Phase 2 must resolve first.

---

## Assumptions

- The team has access to at least one source of user/stakeholder input (interviews, transcripts, analytics, or domain documentation)
- The Analyst agent has user-supplied reference material or explicit approval to perform domain research
- Phase 1 output will be consumed by a PM agent or human product manager in Phase 2

## Limits

- Phase 1 does NOT produce architecture decisions, technology selections, or implementation plans
- Phase 1 does NOT produce user stories — those are Phase 3 artifacts
- Competitive pricing analysis is out of scope for Phase 1 (use FTE-month estimates only)

## Edge Cases

- **Idea is too vague to even brainstorm**: Run a time-boxed (2-hour) divergent brainstorm session using SCAMPER before attempting the brief. If still unclear after 2 hours, escalate to stakeholders for clarification.
- **Multiple competing problems identified**: Create separate briefs for each problem. The PM in Phase 2 decides which to pursue or whether to combine.
- **No access to users or stakeholders**: Mark all claims as `[ASSUMPTION]` and ensure Phase 2 resolves them before the PRD is finalized.

## Acceptance Criteria

- [ ] Product brief exists with all 9 required sections populated
- [ ] >80% of factual claims carry evidence tags (spot-check the first 10 factual claims in document order)
- [ ] Phase 1 completed within the time-box for the project size category
- [ ] Handoff summary delivered to Phase 2 receiving agent

See also: `references/methodology-overview.md`, `references/phase-2-planning.md`, `references/quick-flow.md`, `references/artifact-flow-chain.md`
