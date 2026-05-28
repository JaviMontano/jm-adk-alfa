---
name: value-proposition
description: >
  Triggers on "value proposition", "propuesta de valor", "value prop canvas", "messaging framework".
  Designs a value proposition canvas mapping customer jobs, pains, and gains to product features, pain relievers, and gain creators. Builds a messaging hierarchy from tagline to full narrative. Output: canvas + messaging doc. [EXPLICIT]
argument-hint: "product/service name + target customer segment + competitive context"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Value Proposition Canvas Design

## TL;DR

Produces a complete value proposition canvas with customer profile (jobs, pains, gains) mapped to a value map (features, pain relievers, gain creators). Builds a messaging hierarchy from tagline through elevator pitch to full narrative. Validates fit between what the customer needs and what the product delivers. Final output is the canvas document plus a messaging framework ready for marketing and sales use.

## When to Activate

- User mentions "value proposition", "propuesta de valor", "value prop canvas", or "messaging framework"
- Input contains a product or service needing positioning against customer needs
- Request involves defining why customers should choose this product over alternatives
- User asks for taglines, elevator pitches, or messaging hierarchies

Do NOT activate for full competitive analysis (competitive-positioning), pricing strategy (pricing-strategy), or brand identity work (brand-voice). Those are separate skills.

## 1. Customer Profile

Build the right side of the canvas — deep understanding of the target customer.

### Customer Jobs

Identify 5-8 jobs the target customer is trying to get done:

| # | Job                          | Type            | Importance (H/M/L) | Tag        |
|---|------------------------------|-----------------|---------------------|------------|
| J1| Reduce monthly reporting time| Functional      | H                   | [EXPLICIT] |
| J2| Look competent to leadership | Social          | M                   | [INFERRED] |
| J3| Feel confident in decisions  | Emotional       | H                   | [INFERRED] |
| J4| ...                          | ...             | ...                 | ...        |

Job types:
- **Functional**: tasks they are trying to perform or complete
- **Social**: how they want to be perceived by others
- **Emotional**: how they want to feel
- **Supporting**: jobs in the context of purchasing or consuming (comparing, deciding, installing)

### Customer Pains

Identify 5-8 pains related to the jobs above:

| # | Pain                             | Severity (H/M/L) | Frequency    | Tag        |
|---|----------------------------------|-------------------|--------------|------------|
| P1| Manual data aggregation takes 8h | H                 | Monthly      | [EXPLICIT] |
| P2| Errors in reports damage credibility | H              | Occasional   | [INFERRED] |
| P3| ...                              | ...               | ...          | ...        |

Classify pains as: undesired outcomes, obstacles, or risks.

### Customer Gains

Identify 5-8 gains the customer desires:

| # | Gain                             | Type              | Relevance (H/M/L) | Tag        |
|---|----------------------------------|-------------------|--------------------|------------|
| G1| Reports generated in under 1h   | Expected          | H                  | [EXPLICIT] |
| G2| Real-time dashboards impress execs | Unexpected      | H                  | [INFERRED] |
| G3| ...                              | ...               | ...                | ...        |

Gain types: required (must-have), expected (standard), desired (above expectation), unexpected (delight).

## 2. Value Map

Build the left side of the canvas — what the product actually delivers.

### Products and Services

List the core offerings that create value:

| # | Product/Service/Feature        | Maps to Jobs       | Tag        |
|---|--------------------------------|---------------------|------------|
| F1| Automated data pipeline        | J1, J3              | [EXPLICIT] |
| F2| One-click report generation    | J1, J2              | [EXPLICIT] |
| F3| ...                            | ...                 | ...        |

### Pain Relievers

How the product specifically alleviates customer pains:

| # | Pain Reliever                       | Addresses Pain | Intensity (H/M/L) | Tag        |
|---|-------------------------------------|----------------|--------------------|------------|
| PR1| Eliminates manual data aggregation | P1             | H                  | [EXPLICIT] |
| PR2| Built-in validation catches errors | P2             | H                  | [EXPLICIT] |
| PR3| ...                                | ...            | ...                | ...        |

### Gain Creators

How the product generates customer gains:

| # | Gain Creator                        | Enables Gain   | Impact (H/M/L) | Tag        |
|---|-------------------------------------|----------------|-----------------|------------|
| GC1| Sub-60-minute report generation   | G1             | H               | [EXPLICIT] |
| GC2| Live dashboard with exec-ready visuals | G2         | H               | [EXPLICIT] |
| GC3| ...                               | ...            | ...             | ...        |

## 3. Fit Assessment

Evaluate the alignment between Customer Profile and Value Map:

| Fit Type       | Definition                                    | Status       |
|----------------|-----------------------------------------------|--------------|
| Problem-Solution Fit | Pain relievers address top pains        | Strong/Weak  |
| Product-Market Fit   | Gain creators match desired gains       | Strong/Weak  |
| Coverage gaps        | Jobs/pains/gains with no product match  | List gaps    |
| Over-engineering     | Features that match no real job/pain    | List excess  |

Flag any coverage gaps as strategic risks and over-engineered features as candidates for deprioritization.

## 4. Messaging Hierarchy

Build the messaging stack from shortest to longest:

### Tagline (5-8 words)
A memorable, single-phrase distillation of the core value proposition.
- Must pass the "billboard test" — understandable in 3 seconds
- Should evoke the primary gain, not describe the product
- Generate 3 options and recommend one with reasoning

### Elevator Pitch (30 seconds / 60-80 words)
Structured as: For [target customer] who [key job/pain], [product name] is a [category] that [primary pain reliever/gain creator]. Unlike [alternative], we [key differentiator].

### One-Paragraph Narrative (100-150 words)
Expands the elevator pitch with:
- Context: the market problem or shift driving urgency
- Solution: what the product does and why it works
- Proof: one concrete metric, testimonial, or case reference
- CTA: clear next step for the reader

### Full Narrative (300-500 words)
Complete value story including:
- Customer world before the product (empathy with current pain)
- The insight or approach that changes things
- How the product works (not features — outcomes)
- Evidence of results (metrics, social proof)
- Vision of the customer world after adoption
- Clear call to action

Each level must be independently complete — the tagline works alone, the elevator pitch works alone, etc.

## Trade-off Matrix

| Decision                     | Option A                  | Option B                  | Recommendation             |
|------------------------------|---------------------------|---------------------------|----------------------------|
| Customer segment scope       | Broad (multiple personas) | Narrow (one ideal customer)| Narrow first — expand later |
| Pain vs gain emphasis        | Lead with pain relief     | Lead with gain creation   | Lead with pain — urgency converts |
| Differentiation strategy     | Feature comparison        | Outcome comparison        | Outcomes — features commoditize |
| Messaging tone               | Bold and provocative      | Professional and measured | Match the audience; default measured |
| Proof type                   | Metrics and data          | Stories and testimonials  | Both — metrics convince, stories connect |

## Assumptions and Limits

- Customer jobs, pains, and gains are based on user-provided context; real validation requires customer interviews [EXPLICIT]
- Competitive differentiation claims are based on available information, not proprietary competitor data [INFERRED]
- Messaging effectiveness cannot be predicted without market testing; this is a hypothesis to validate [EXPLICIT]
- Canvas assumes a single primary customer segment; multi-segment products need one canvas per segment [EXPLICIT]
- Does not produce visual design assets — delivers structured text for design teams to execute [EXPLICIT]

## Edge Cases

1. **No clear competitor** — Use the status quo (manual process, spreadsheets, doing nothing) as the alternative in the elevator pitch. Position against inertia, not a named product.
2. **Platform with multiple user types** — Build separate customer profiles for each user type (buyer vs end-user vs admin). Create one value map but show which features serve which profile. Messaging hierarchy targets the buyer persona by default.
3. **Commodity market with feature parity** — Shift differentiation from features to experience, support, integration ease, or brand trust. Messaging emphasizes "how" and "why" over "what."
4. **Pre-product (idea stage)** — Canvas becomes a hypothesis document. Tag everything as `[OPEN]`. Emphasize that this is a design tool for validation, not a marketing asset yet.
5. **B2B with long sales cycle** — Add a "buying committee" layer: map jobs/pains/gains for each stakeholder in the purchasing decision (champion, economic buyer, technical evaluator, end user).

## Good vs Bad Example

### Good
```
Customer Profile: Mid-market CFOs managing 5-15 person finance teams
J1: Close monthly books within 5 business days [EXPLICIT — from 3 customer interviews]
P1: Manual reconciliation takes 40+ hours/month [EXPLICIT — user provided metric]
G1: Same-day financial visibility for board reporting [INFERRED — from role expectations]

Value Map:
F1: Automated bank reconciliation engine
PR1: Reduces reconciliation from 40h to 2h [EXPLICIT — product benchmark]
GC1: Real-time P&L dashboard with board-ready exports [EXPLICIT]

Fit: Strong problem-solution fit on P1-PR1 axis. Gap: no multi-entity
consolidation (J4 unaddressed). Flagged as roadmap priority.

Tagline: "Close the books before lunch."
Elevator: For mid-market CFOs who lose weeks to manual reconciliation,
CloseFast is an automated finance platform that cuts monthly close from
days to hours. Unlike legacy ERPs, we deploy in 48 hours with no IT dependency.
```

### Bad
```
Value prop: We are the best solution for finance teams.
Features: Fast, easy, affordable.
Tagline: The future of finance.
(No customer profile, no evidence, no fit analysis, no specificity)
```

## Validation Gate

Before delivering the canvas and messaging, confirm every item:

- [ ] Customer profile completed: 5+ jobs, 5+ pains, 5+ gains with types and ratings
- [ ] Value map completed: features, pain relievers, and gain creators with mappings
- [ ] Every item tagged with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`
- [ ] Fit assessment completed: problem-solution fit, coverage gaps, over-engineering check
- [ ] Tagline: 3 options generated with recommendation and reasoning
- [ ] Elevator pitch follows the For/Who/Product/Unlike structure
- [ ] One-paragraph narrative includes context, solution, proof, and CTA
- [ ] Full narrative (300-500 words) tells a complete customer transformation story
- [ ] Each messaging level works independently without requiring the others
- [ ] Trade-offs and assumptions explicitly documented with evidence tags

## Reference Files

| File | Purpose |
|------|---------|
| `references/canvas-methodology.md` | Value Proposition Canvas theory and completion guide |
| `references/messaging-patterns.md` | Messaging hierarchy templates and tone calibration examples |
| `references/fit-assessment.md` | Problem-solution and product-market fit evaluation criteria |
