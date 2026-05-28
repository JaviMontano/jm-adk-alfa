---
name: competitor-teardown
description: >
  Triggers on "competitor teardown", "competitive analysis", "analizar competencia",
  "competitor comparison". Detailed competitor product/service analysis with feature
  comparison matrix, pricing analysis, positioning map, SWOT per competitor, and
  differentiation opportunities. Output: branded HTML competitive report. [EXPLICIT]
argument-hint: "your product/service name + list of competitors to analyze"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# competitor-teardown

## TL;DR

Produces a structured competitive intelligence report analyzing named competitors against the user's product or service. Generates a feature comparison matrix, pricing tier analysis, positioning narrative, per-competitor SWOT, and actionable differentiation recommendations. Output is a branded HTML report using JM Labs dark theme, ready for stakeholder presentation or strategic planning sessions.

## When to Activate

- User names specific competitors and asks for comparison or analysis.
- User requests a competitive landscape review for a product, service, or market segment.
- User asks for feature-by-feature competitor comparison or pricing benchmarks.
- User mentions "competitor teardown", "competitive analysis", "analizar competencia", or "competitor comparison".
- Do NOT activate for broad market sizing (use `market-intelligence`), internal product strategy (use `product-strategy`), or vendor evaluation for procurement (use `vendor-evaluation`).

## Analysis Framework

### Phase 1: Competitor Profiling

For each named competitor, build a structured profile:

| Dimension | Data Points |
|-----------|-------------|
| **Identity** | Company name, founding year, HQ location, employee count estimate, funding status |
| **Product** | Core offering, product lines, target customer segment, delivery model (SaaS, services, hybrid) |
| **Market position** | Estimated market share, growth trajectory (expanding/stable/declining), geographic reach |
| **Pricing** | Published pricing tiers, freemium availability, enterprise pricing model, discounting patterns |
| **Technology** | Tech stack (if public), integrations, API availability, mobile support |
| **Reputation** | G2/Capterra rating range, notable client logos, public case studies, known complaints |

Evidence tagging: every data point marked `[EXPLICIT]` if from user input, `[INFERRED]` if derived from public knowledge, `[OPEN]` if unverifiable and requiring user validation.

### Phase 2: Feature Comparison Matrix

Build a comprehensive feature matrix as an HTML table:

- **Rows**: features/capabilities relevant to the competitive space.
- **Columns**: user's product + each competitor.
- **Cell values**: supported (checkmark), partial (tilde), not supported (dash), unknown (question mark).
- **Priority column**: user rates each feature as MUST-HAVE, NICE-TO-HAVE, or DIFFERENTIATOR.
- **Source column**: where the information was obtained or inferred.

Group features into logical categories (e.g., Core Functionality, Integrations, Support & SLA, Pricing & Billing, Security & Compliance).

### Phase 3: Positioning Analysis

Construct a 2x2 positioning narrative (not a visual chart, described textually for reproducibility):

- **Default axes**: Price (low to high) vs Feature Breadth (narrow to broad).
- **Alternative axes**: user can specify (e.g., Enterprise Focus vs SMB Focus, Technical Depth vs Ease of Use).
- **Quadrant descriptions**: name each quadrant and place competitors with reasoning.
- **Movement vectors**: note if any competitor is shifting position (launching enterprise tier, going downmarket, etc.).

### Phase 4: SWOT per Competitor

For each competitor, produce a focused SWOT:

- **Strengths**: 3-5 genuine competitive advantages with evidence tags.
- **Weaknesses**: 3-5 exploitable gaps or limitations.
- **Opportunities**: market shifts that could benefit them.
- **Threats**: factors that could weaken their position (including the user's own product).

Close each SWOT with an **"Attack Vector"** paragraph: the single most effective way to compete against this specific player.

## Differentiation Synthesis

After individual analysis, synthesize cross-cutting findings:

1. **Uncontested space**: features or positioning no competitor owns.
2. **Table-stakes gaps**: capabilities the user lacks that all competitors offer.
3. **Perception gaps**: areas where competitors are perceived stronger but may not actually be.
4. **Pricing opportunity**: underserved price points or packaging models.
5. **Recommended actions**: prioritized list of 3-5 strategic moves, each with effort estimate (Low/Medium/High) and impact estimate (Low/Medium/High).

## Report Structure (HTML Output)

The branded HTML report contains:

1. **Executive Summary**: 3-paragraph overview of competitive landscape and key findings.
2. **Competitor Profiles**: one section per competitor with profile card.
3. **Feature Matrix**: interactive-feeling table (CSS hover highlights, sticky headers).
4. **Positioning Map**: textual description with competitor placement rationale.
5. **SWOT Cards**: grid layout, one card per competitor, color-coded quadrants.
6. **Differentiation Roadmap**: prioritized action items with effort/impact badges.
7. **Methodology Note**: evidence tagging legend, data freshness disclaimer.

Brand styling: JM Labs dark theme (`#0a0a0a`, `#e94560`, `#1a1a2e`), Inter font stack, print stylesheet included.

## Trade-off Matrix

| Decision | Option A | Option B | Default |
|----------|----------|----------|---------|
| Competitor count | 2-3 deep dives | 5-8 surface scans | 3-5 balanced depth |
| Data sourcing | User-provided only | User + public knowledge | User + public knowledge |
| SWOT format | Bullet lists | Narrative paragraphs | Bullet lists (scannable) |
| Positioning axes | Standard (price/features) | Custom user-defined | Standard, custom on request |
| Output format | HTML report | Markdown summary | HTML report (presentation-ready) |
| Evidence rigor | All claims tagged | Key claims only | All claims tagged (credibility) |

## Assumptions & Limits

- **Assumption**: user has basic familiarity with named competitors; this skill synthesizes and structures, not discovers from scratch. [INFERRED]
- **Assumption**: analysis is based on publicly available information and user-provided intelligence, not proprietary data. [EXPLICIT]
- **Assumption**: the user's own product/service capabilities are provided or known from context. [EXPLICIT]
- **Limit**: no live web scraping or API calls to competitor sites; analysis uses provided data and training knowledge.
- **Limit**: pricing data may be outdated; all figures include freshness disclaimer.
- **Limit**: no visual chart generation (scatter plots, radar charts); positioning is described textually.
- **Limit**: maximum 8 competitors per report for depth quality.

## Edge Cases

1. **Single competitor**: user names only one competitor. Produce full teardown of that one player with extended SWOT and attack vector, skip positioning map (needs 2+ points).
2. **Competitor is a giant** (e.g., Google, Microsoft): focus analysis on the specific competing product/feature, not the entire company. Flag resource asymmetry explicitly.
3. **No pricing data available**: competitor has opaque enterprise pricing. Mark as `[OPEN]`, note "Contact for quote" model, compare on value dimensions instead.
4. **User IS the new entrant**: user has no existing product yet. Frame analysis as market entry opportunity assessment, focus on gaps and positioning whitespace.
5. **Rapidly changing market**: competitor just launched/pivoted/was acquired. Add prominent "Market Event" callout box with date and implications.

## Good vs Bad Example

### Good

```
Input: "Teardown of Notion vs Coda vs Airtable for our project management tool
        targeting Latin American SMBs. We're cheaper ($5/user) and have
        WhatsApp integration they don't."

Output: Branded HTML report with:
- 3 competitor profiles with evidence-tagged data points
- Feature matrix: 25+ features across 5 categories
- Each feature marked with support level and source
- User's WhatsApp integration highlighted as differentiator
- SWOT per competitor with LatAm-specific observations
- Positioning: user placed in "affordable + regional fit" quadrant
- Action items: "Double down on WhatsApp workflows" [High Impact, Low Effort]
- All pricing marked [INFERRED - verify current rates]
```

### Bad

```
Output that:
- Copies marketing language from competitor websites verbatim
- Presents opinions as facts without evidence tags
- Ignores the LatAm SMB context entirely
- Produces a generic SWOT with platitudes ("strong brand")
- Recommends "be better at everything" without prioritization
- Omits the user's own product from the comparison matrix
- Uses a plain text dump instead of structured HTML report
```

## Validation Gate

Before delivering the competitive report, verify:

- [ ] Every factual claim carries an evidence tag: `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- [ ] Feature matrix includes the user's own product as the first column.
- [ ] SWOT produced for each named competitor (not a generic combined SWOT).
- [ ] Each SWOT contains an "Attack Vector" recommendation.
- [ ] Differentiation synthesis identifies at least one uncontested space.
- [ ] Pricing data includes freshness disclaimer and verification recommendation.
- [ ] HTML output uses JM Labs brand colors and is self-contained (no external deps).
- [ ] Print stylesheet included for stakeholder distribution.
- [ ] Executive summary is 3 paragraphs or fewer, not a wall of text.
- [ ] Recommended actions include effort and impact estimates.
- [ ] No proprietary competitor data presented as public (ethical boundary).
- [ ] Report handles the actual competitor count provided (not padded with extras).

## Reference Files

| File | Purpose |
|------|---------|
| `references/analysis-frameworks.md` | SWOT, Porter's Five Forces, positioning map templates |
| `references/brand-tokens.md` | JM Labs color palette, typography, card layout patterns |
| `references/evidence-tagging.md` | Tag definitions and usage guidelines for claims |
| `references/report-structure.md` | HTML skeleton for competitive intelligence reports |
