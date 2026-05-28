---
name: executive-summary
description: >
  Triggers on "executive summary", "resumen ejecutivo", "write executive brief", "summarize for C-level".
  Distills complex information into 1-page executive summaries with key metrics, decision points,
  and recommended actions. Output: formatted executive summary in markdown or HTML. [EXPLICIT]
argument-hint: "Source material (document, report, or context) and target audience"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# executive-summary

> **TL;DR** — Transforms complex, multi-page content into crisp one-page executive summaries that surface decisions, metrics, and actions for time-constrained senior leaders.

---

## When to Activate

Invoke this skill when any of these conditions are met:

| Signal | Examples |
|--------|----------|
| Summarization request | "Write an executive summary of this report", "Resumen ejecutivo" |
| C-level preparation | "Summarize this for the board", "Brief the CEO on project status" |
| Decision framing | "Distill the options into a one-pager for the leadership team" |
| Document condensation | "Turn this 40-page analysis into something a VP will read" |

Do **not** activate for meeting minutes (use `meeting-notes`), sprint reports (use `sprint-report`), or detailed technical documentation where brevity would compromise safety-critical information.

---

## 1. Source Material Analysis

Before writing, analyze the input material:

- **Source type** — full report, presentation deck, meeting transcript, data dump, or verbal briefing from the user.
- **Length and density** — estimate the compression ratio needed to reach one page (roughly 400-600 words).
- **Audience** — CEO, board, investors, department heads, or cross-functional leadership. Each audience has different priorities.
- **Decision context** — is this informational ("here is what happened"), decisional ("choose option A or B"), or action-oriented ("approve this plan")?
- **Sensitivity level** — confidential, internal, or shareable. Affects language and detail granularity.

If the source material is ambiguous or incomplete, state assumptions with `[INFERRED]` tags and flag gaps with `[OPEN]`.

---

## 2. Executive Summary Framework

The skill uses the BLUF (Bottom Line Up Front) structure optimized for executive attention patterns:

### 2.1 Opening Statement (2-3 sentences)
The single most important takeaway. Answers the question: "If the reader stops here, what must they know?" This is the BLUF — state the conclusion, recommendation, or status first.

### 2.2 Context Block (3-4 sentences)
Minimal background needed to understand the opening statement. Assume the reader has strategic context but not operational detail. Reference time period, scope, and triggering event.

### 2.3 Key Metrics Table
Maximum 5-7 metrics in a compact table. Each metric includes: Metric Name, Current Value, Target/Benchmark, Status (on-track, at-risk, off-track). Only include metrics that directly support the narrative.

### 2.4 Decision Points or Findings (3-5 bullets)
If decisional: frame each option with pros, cons, and recommendation. Bold the recommended option.
If informational: list the top findings in order of strategic importance.
If action-oriented: list the requested approvals or actions.

### 2.5 Risks and Concerns (2-3 bullets)
Only the risks that would change the executive's decision or escalate their attention. Each risk includes probability indicator and mitigation status.

### 2.6 Recommended Actions (2-4 bullets)
Concrete, time-bound next steps with assigned owners. Framed as requests: "Approve X by date Y" or "Direct team Z to begin phase 2."

### 2.7 Appendix Pointer
Single line referencing the full source document for readers who want depth. Format: "Full analysis: [document name], [page count] pages, [date]."

---

## 3. Writing Principles

These principles govern the output quality:

- **One page maximum** — 400-600 words. If printed, it fits on a single A4/Letter page with standard margins.
- **No jargon without context** — define acronyms on first use or avoid them entirely.
- **Active voice** — "Revenue declined 12%" not "A 12% decline in revenue was observed."
- **Quantify everything** — replace qualitative assessments with numbers. "Significantly delayed" becomes "17 days behind schedule."
- **Decision-ready** — every summary should answer: "What do I need to know?" and "What do I need to do?"
- **Evidence-tagged** — all claims carry `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` tags.

---

## 4. Output Formatting

- **Markdown mode** (default): clean headers, a single compact table, bullet lists, and bold emphasis for key figures and recommendations.
- **HTML mode**: self-contained single-page HTML with inline CSS. Executive-friendly typography (serif headers, generous whitespace, status color indicators). Print-optimized with `@media print` rules.
- **Slide mode**: when the user says "for a slide" or "presentation format", produce content structured for a single presentation slide — title, 3-4 bullets, one key metric callout.
- Footer: `Executive Summary | {source document} | {date} | Generated by executive-summary skill`.

---

## Trade-off Matrix

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| Clarity | HIGHEST | Ambiguity is the enemy of executive communication |
| Brevity | HIGH | One page is a hard constraint, not a suggestion |
| Accuracy | HIGH | Misrepresented data destroys trust instantly |
| Completeness | MEDIUM | Deliberately sacrificed for brevity; point to the full document |
| Visual polish | MEDIUM | Clean formatting aids scanning but substance wins |

---

## Assumptions & Limits

1. The skill summarizes content the user provides — it does not generate original analysis or fabricate data. [EXPLICIT]
2. Metrics are reproduced from source material. If no metrics exist, the skill highlights their absence. [EXPLICIT]
3. Recommended actions reflect the source material's conclusions. If the source has no recommendations, the skill flags this as an `[OPEN]` item. [EXPLICIT]
4. The skill assumes the audience is English-speaking C-level leadership unless told otherwise. [INFERRED]
5. For Spanish-language output ("resumen ejecutivo"), the skill produces the summary in Spanish while maintaining the same structural framework. [EXPLICIT]
6. Compression necessarily loses nuance — the appendix pointer is mandatory to preserve access to detail. [EXPLICIT]

---

## Edge Cases

1. **Source material is already short (under 500 words)** — do not artificially pad. Restructure into the BLUF framework, add metrics table if data supports it, and note that the source was already concise.
2. **Contradictory information in source** — do not silently resolve contradictions. Surface them in the Risks section: "Source data contains conflicting figures for Q2 revenue (p.12 vs p.34). Clarification required before board presentation." Tag as `[OPEN]`.
3. **Highly technical source for non-technical audience** — strip all technical detail. Replace implementation specifics with business impact statements. "Migrated to microservices architecture" becomes "Completed infrastructure modernization, reducing deployment time by 60%."
4. **Multiple source documents** — synthesize across sources into a single coherent summary. Note source documents in the appendix pointer. Flag any inter-document inconsistencies.

---

## Good vs Bad Example

**Good output** (excerpt):
```
## Executive Summary: Project Atlas Q1 Status

Project Atlas is on track to deliver Phase 1 by June 2026, with 73%
of milestone deliverables completed. Budget utilization is at 68%
against a 75% plan, indicating a favorable variance. One critical
risk requires board attention: the vendor contract for the data
platform expires April 30 with no renewal signed. [EXPLICIT]

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Milestone completion | 73% | 75% | On track |
| Budget utilization | 68% | 75% | Favorable |
| Team attrition | 2 of 14 | 0 | At risk |
| Customer pilot signups | 12 | 10 | Ahead |

**Recommended Actions:**
1. **Approve vendor contract renewal** by April 15 to avoid
   platform access disruption. Owner: VP Engineering. [EXPLICIT]
2. Backfill two departed engineers by Sprint 8. Owner: HR. [EXPLICIT]
```

**Bad output** (excerpt):
```
## Summary
The project is going well overall. We have done a lot of work and
things are mostly on schedule. There are some risks but the team is
handling them. We recommend continuing as planned.
```

The good example leads with the bottom line, provides a scannable metrics table with status indicators, and closes with specific, time-bound actions and owners. The bad example is vague, unquantified, and gives no actionable information.

---

## Validation Gate

Before delivering the executive summary, confirm every item:

- [ ] Summary fits within one page (400-600 words maximum)
- [ ] Opens with a BLUF statement (conclusion or recommendation first)
- [ ] Context block provides minimal necessary background without operational detail
- [ ] Key metrics table contains 3-7 metrics with current value, target, and status
- [ ] Decision points or findings are ordered by strategic importance
- [ ] Risks section includes only escalation-worthy items with probability indicators
- [ ] Recommended actions are concrete, time-bound, and have assigned owners
- [ ] Appendix pointer references the full source document
- [ ] All claims carry evidence tags (EXPLICIT, INFERRED, OPEN)
- [ ] Language uses active voice, avoids jargon, and quantifies assessments
- [ ] Output format matches user request (markdown, HTML, or slide)
- [ ] Output file written to disk at confirmed path

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/bluf-template.md` | BLUF framework template with section prompts |
| `references/body-of-knowledge.md` | Executive communication best practices and BLUF methodology |
| `references/html-template.html` | Print-optimized HTML template for executive summaries |
| `evals/evals.json` | Evaluation scenarios for summary quality, compression ratio, and accuracy |
