---
name: functional-spec
description: Functional specifications. MVP modules, 8+ use cases, business rules, acceptance criteria. Firestore data models. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [analysis, spec, use-cases, acceptance-criteria]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# functional-spec {Analysis} (v1.0)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
Functional specifications. MVP modules, 8+ use cases, business rules, acceptance criteria. Firestore data models. [EXPLICIT]
**When to use:** During analysis mode (MAO DNA). Before architecture or development begins.
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). [EXPLICIT]
2. **Law of Completeness:** No analysis deliverable ships without covering all required sections. [EXPLICIT]
3. **Law of Firebase Lens:** All assessments evaluated through Firebase/Google/Hostinger feasibility. [EXPLICIT]
## Core Process
### Phase 1: Gather
1. Collect inputs (documents, code, conversations, existing systems). [EXPLICIT]
2. Parse for requirements, constraints, and context. [EXPLICIT]
3. Load reusable assets from `assets/`: `functional-spec-template.md`, `use-case-schema.json`, `business-rule-taxonomy.json`, `acceptance-criteria-patterns.json`, and `firestore-model-template.json`. [EXPLICIT]
### Phase 2: Analyze
1. Apply domain-specific analysis methodology. [EXPLICIT]
2. Tag all findings with evidence tags. [EXPLICIT]
3. Score/evaluate using the skill's specific metrics. [EXPLICIT]
4. When inputs are structured, compile a deterministic functional spec with `scripts/compile-functional-spec.py --spec <spec.json>`. [EXPLICIT]
### Phase 3: Document
1. Produce the analysis deliverable in markdown. [EXPLICIT]
2. Include evidence tag summary (% by tag type). [EXPLICIT]
3. If >30% [ASSUMPTION], add WARNING banner. [EXPLICIT]
4. Include MVP modules, at least 8 use cases, business rules, acceptance criteria, Firestore model notes, open questions, and out-of-scope boundaries. [EXPLICIT]
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
- [ ] `assets/manifest.json` declares every reusable functional spec asset
- [ ] `scripts/compile-functional-spec.py` rejects specs with fewer than 8 use cases or missing acceptance criteria
- [ ] Business rules are typed and traceable to use cases
- [ ] Firestore data models include collections, required fields, and ownership/PII notes
## 5. Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner.
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation).

## Usage

Example invocations:

- "/functional-spec" — Run the full functional spec workflow
- "functional spec on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/compile-functional-spec.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill functional-spec`
- Default behavior: render Markdown to stdout; write files only when `--output` is explicit.
- Safety boundary: incomplete specs fail nonzero instead of producing partial requirements.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/functional-spec-template.md` defines the required section order.
- `assets/use-case-schema.json` defines minimum use case fields.
- `assets/business-rule-taxonomy.json` defines rule types.
- `assets/acceptance-criteria-patterns.json` defines Given/When/Then and checklist patterns.
- `assets/firestore-model-template.json` defines collection metadata required by this skill.


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
