---
name: swot-analysis
description: >
  Triggers on "SWOT analysis", "SWOT for", "analisis FODA", "DAFO".
  Produces a structured SWOT analysis with evidence tagging, cross-impact matrix, strategic implications, and action priorities. Output: branded HTML SWOT matrix + action plan. [EXPLICIT]
argument-hint: "company/product/project name + context (market entry, pivot, annual review)"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# SWOT Analysis

## TL;DR

Delivers a rigorous SWOT analysis with evidence-tagged findings across Strengths, Weaknesses, Opportunities, and Threats. Goes beyond the basic quadrant by adding a cross-impact matrix, strategic implication synthesis, and prioritized action plan. Final output is a branded HTML SWOT matrix document with actionable recommendations.

## When to Activate

- User mentions "SWOT analysis", "SWOT for", "analisis FODA", or "DAFO"
- Input contains a business, product, or project that needs strategic assessment
- Request involves evaluating internal capabilities against external factors
- User asks for competitive positioning analysis with structured framework

Do NOT activate for pure competitive intelligence (competitive-positioning), risk-only assessment (risk-assessment), or market sizing (market-intelligence). Those are separate skills.

## 1. Input Gathering and Scope Definition

Before building the SWOT, establish the analysis frame:

| Parameter          | Value                | Evidence Tag |
|--------------------|----------------------|--------------|
| Subject            | Company/product/project | [EXPLICIT] |
| Analysis purpose   | Market entry, annual review, pivot, etc. | [EXPLICIT] or [INFERRED] |
| Time horizon       | 6 months, 1 year, 3 years | [EXPLICIT] or [INFERRED] |
| Competitive frame  | Direct competitors considered | [EXPLICIT] or [OPEN] |
| Data sources       | What information the user provided | [EXPLICIT] |

If the user provides minimal context, ask a maximum of 3 clarifying questions before proceeding with reasonable assumptions tagged as `[INFERRED]`.

## 2. SWOT Quadrant Analysis

### Strengths (Internal, Positive)

Identify 5-8 strengths with evidence and impact rating:

| # | Strength                | Evidence                           | Impact (H/M/L) | Tag        |
|---|-------------------------|------------------------------------|-----------------|------------|
| S1| Unique technology       | Patent portfolio, technical moat   | H               | [EXPLICIT] |
| S2| Strong brand recognition| Market share data, NPS scores      | H               | [INFERRED] |
| S3| ...                     | ...                                | ...             | ...        |

### Weaknesses (Internal, Negative)

Identify 5-8 weaknesses:

| # | Weakness                | Evidence                           | Impact (H/M/L) | Tag        |
|---|-------------------------|------------------------------------|-----------------|------------|
| W1| Limited geographic reach| Revenue concentration data         | M               | [EXPLICIT] |
| W2| Technical debt          | Deployment frequency, incident rate| H               | [INFERRED] |
| W3| ...                     | ...                                | ...             | ...        |

### Opportunities (External, Positive)

Identify 5-8 opportunities:

| # | Opportunity             | Evidence                           | Impact (H/M/L) | Tag        |
|---|-------------------------|------------------------------------|-----------------|------------|
| O1| Emerging market segment | Industry growth reports             | H               | [INFERRED] |
| O2| Regulatory tailwind     | Policy changes announced           | M               | [EXPLICIT] |
| O3| ...                     | ...                                | ...             | ...        |

### Threats (External, Negative)

Identify 5-8 threats:

| # | Threat                  | Evidence                           | Impact (H/M/L) | Tag        |
|---|-------------------------|------------------------------------|-----------------|------------|
| T1| New market entrant      | Competitor funding announcement    | H               | [EXPLICIT] |
| T2| Economic downturn risk  | Macro indicators                   | M               | [INFERRED] |
| T3| ...                     | ...                                | ...             | ...        |

## 3. Cross-Impact Matrix

Map interactions between quadrants to surface strategic themes:

| Combination | Question                                              | Strategic Theme          |
|-------------|-------------------------------------------------------|--------------------------|
| S + O       | Which strengths can best exploit which opportunities? | **Growth levers**        |
| S + T       | Which strengths can defend against which threats?     | **Defensive advantages** |
| W + O       | Which weaknesses prevent capturing opportunities?     | **Investment priorities**|
| W + T       | Which weaknesses amplify which threats?               | **Critical vulnerabilities** |

For each combination, identify the top 2-3 pairings and articulate the strategic implication in one sentence. Example:

- **S1 + O2**: Strong patent portfolio (S1) positions the company to lead in the newly regulated segment (O2) where compliance barriers favor incumbents.
- **W2 + T1**: Technical debt (W2) slows feature velocity, making the company vulnerable to the well-funded new entrant (T1) shipping faster.

## 4. Strategic Implications and Action Plan

Synthesize the cross-impact analysis into prioritized actions:

| Priority | Action                           | Addresses        | Owner (suggested) | Timeline   | Effort |
|----------|----------------------------------|-------------------|--------------------|------------|--------|
| P1       | Accelerate patent licensing      | S1+O2, S1+T1     | Product/Legal      | Q1-Q2      | High   |
| P2       | Technical debt reduction sprint  | W2+T1, W2+O1     | Engineering        | Q1         | High   |
| P3       | Geographic expansion pilot       | W1+O1             | Sales/Ops          | Q2-Q3      | Medium |
| P4       | ...                              | ...               | ...                | ...        | ...    |

Rules for prioritization:
- Actions addressing Critical Vulnerabilities (W+T) get highest urgency
- Actions leveraging Growth Levers (S+O) get highest impact rating
- Each action must trace back to specific SWOT item codes (S1, W2, etc.)
- Maximum 8 priority actions to maintain focus

## Trade-off Matrix

| Decision                     | Option A                  | Option B                  | Recommendation             |
|------------------------------|---------------------------|---------------------------|----------------------------|
| Analysis depth               | Broad survey (20+ items)  | Focused (5-8 per quadrant)| Focused — depth beats volume |
| Evidence standard            | Only hard data             | Include informed inference | Include inference with tags |
| Cross-impact scope           | All combinations           | Top 3 per combination     | Top 3 — actionable focus   |
| Action plan granularity      | Detailed project plans     | Strategic directions       | Strategic — leave execution to owners |
| Output format                | Markdown tables            | Branded HTML               | HTML for stakeholder sharing |

## Assumptions and Limits

- Analysis quality is directly proportional to the context the user provides [EXPLICIT]
- External factors (O and T) are based on general industry knowledge unless user provides specific market data [INFERRED]
- Competitive intelligence is inferred from public information, not proprietary databases [INFERRED]
- Cross-impact matrix uses qualitative judgment, not quantitative modeling [EXPLICIT]
- Does not replace a full market research engagement or financial due diligence [EXPLICIT]
- Time horizon defaults to 12 months if not specified by the user [INFERRED]

## Edge Cases

1. **Startup with no history** — Strengths shift to founding team capabilities, technology uniqueness, and early traction metrics. Weaknesses focus on resource constraints and market validation gaps. Tag most items as `[INFERRED]` or `[OPEN]`.
2. **Personal SWOT (career assessment)** — Adapt quadrants: Strengths = skills and reputation, Weaknesses = skill gaps and constraints, Opportunities = market trends and network, Threats = industry disruption and competition. Adjust language from corporate to personal.
3. **Multi-product company** — Clarify whether the SWOT is at the corporate level or product level. If corporate, aggregate. If product, isolate. Flag shared vs. product-specific factors.
4. **Highly regulated industry** — Add a regulatory sub-layer to both Opportunities and Threats. Flag compliance-driven strengths and regulatory-risk weaknesses separately.
5. **SWOT update (not greenfield)** — Ask for the previous SWOT. Highlight what changed, what persists, and what is new. Frame the narrative as evolution, not repetition.

## Good vs Bad Example

### Good
```
Subject: Acme SaaS Platform — Annual Strategic Review
Time Horizon: 12 months

S3: Engineering talent density — 40% of team holds advanced degrees,
    attrition rate 8% vs industry 15%. Impact: H. [EXPLICIT]
W2: No mobile app — 35% of user sessions are mobile web with 2.1x
    higher bounce rate. Impact: H. [EXPLICIT]
O1: Enterprise segment growing 28% YoY in target vertical. Impact: H. [INFERRED]
T2: Key competitor raised Series C ($45M) with mobile-first positioning. Impact: H. [EXPLICIT]

Cross-impact: W2+T2 is a Critical Vulnerability — no mobile app + mobile-first
competitor = accelerating market share risk. Priority action: fast-follow
mobile MVP in Q1.
```

### Bad
```
Strengths: Good team, nice product
Weaknesses: Could be better
Opportunities: Market is growing
Threats: Competition
(No evidence, no impact ratings, no codes, no cross-impact, no action plan)
```

## Validation Gate

Before delivering the SWOT analysis, confirm every item:

- [ ] Analysis scope defined: subject, purpose, time horizon, competitive frame
- [ ] Each quadrant contains 5-8 items with evidence and impact ratings
- [ ] Every item tagged with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`
- [ ] Cross-impact matrix completed for all 4 combinations (S+O, S+T, W+O, W+T)
- [ ] Top 2-3 strategic pairings identified per combination with one-sentence implications
- [ ] Prioritized action plan with 4-8 actions traced to SWOT item codes
- [ ] Actions include suggested owner, timeline, and effort level
- [ ] Critical Vulnerabilities (W+T) flagged with highest urgency
- [ ] Output formatted as branded HTML SWOT matrix + action plan document
- [ ] Trade-offs and assumptions explicitly documented

## Reference Files

| File | Purpose |
|------|---------|
| `references/swot-methodology.md` | SWOT framework theory, common pitfalls, and cross-impact analysis guide |
| `references/evidence-tagging.md` | Evidence classification rules and confidence calibration standards |
| `references/html-swot-template.md` | Branded HTML template for the SWOT matrix output |
