---
name: input-analysis
description: Parse project inputs (RFPs, briefs, emails). Detect contradictions, gaps, ambiguities. Score completeness 0-100. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [analysis, input, requirements, completeness]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# input-analysis {Analysis} (v1.0)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
Parse project inputs (RFPs, briefs, emails). Detect contradictions, gaps, ambiguities. Score completeness 0-100. [EXPLICIT]
**When to use:** During analysis mode (MAO DNA). Before architecture or development begins.
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). [EXPLICIT]
2. **Law of Completeness:** No analysis deliverable ships without covering all required sections. [EXPLICIT]
3. **Law of Firebase Lens:** All assessments evaluated through Firebase/Google/Hostinger feasibility. [EXPLICIT]
## Core Process
### Phase 1: Gather
1. Collect inputs (documents, code, conversations, existing systems). [EXPLICIT]
2. Parse for requirements, constraints, and context. [EXPLICIT]
### Phase 2: Analyze
1. Apply domain-specific analysis methodology. [EXPLICIT]
2. Tag all findings with evidence tags. [EXPLICIT]
3. Score/evaluate using the skill's specific metrics. [EXPLICIT]
### Phase 3: Document
1. Produce the analysis deliverable in markdown. [EXPLICIT]
2. Include evidence tag summary (% by tag type). [EXPLICIT]
3. If >30% [ASSUMPTION], add WARNING banner. [EXPLICIT]

## Deterministic Assets

Use `assets/manifest.json` as the offline contract index. The assets define evidence tags, finding taxonomy, completeness scoring, assumption warning rules, and the JSON report contract. If a structured report is produced, validate it with `bash skills/input-analysis/scripts/check.sh` before acceptance.
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Project context | Text/Files | Yes | What to analyze |
| Output | Type | Description |
|--------|------|-------------|
| Analysis deliverable | Markdown | Evidence-tagged findings |
## Validation Gate
- [ ] All findings have evidence tags
- [ ] Firebase feasibility assessed
- [ ] Deliverable follows R-008 output standards
- [ ] No implementation details (phase separation)
- [ ] Actionable recommendations included
- [ ] JSON reports pass `scripts/check.sh` against `assets/`
## 5. Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner.
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation).

## Usage

Example invocations:

- "/input-analysis" — Run the full input analysis workflow
- "input analysis on this project" — Apply to current context


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
