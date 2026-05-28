---
name: client-prospecting
description: >
  Triggers on "find prospects", "prospecting", "lead list", "ICP definition",
  "target accounts", "who should I contact", "prospectar clientes", "lista de prospectos".
  Systematic prospect identification and qualification: ICP definition, lead lists,
  scoring model, and prioritization. Output: qualified lead list + approach brief.
  Argument: business context (what you sell + to whom) + geography/sector filters.
argument-hint: "your-offering [industry] [geography] [size-range] [list-size: 10|25|50]"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
version: 1.0.0
---

# Client Prospecting — Systematic Lead Identification and Qualification

> TL;DR: Define the ICP, identify lead sources, score by fit, and deliver a prioritized list of qualified prospects with an approach brief for each.

**Principio Rector:** A short list of right-fit targets beats a long list of wrong ones. Quality over quantity, always.

---

## When to Activate

**Activate when:**
- User says "find prospects", "prospecting", "lead list", "ICP definition"
- User says "target accounts", "who should I contact", "who are my best customers"
- User is entering a new market and needs to identify early targets [INFERRED]
- User has a product/service and needs to build a pipeline from scratch [EXPLICIT]
- User wants to define or refine their Ideal Customer Profile [EXPLICIT]

**Do NOT activate when:**
- User has a named target and needs a deep profile (use client-dossier skill)
- User wants to write outreach messages (use b2b-outreach skill)
- User needs market size data (use market-intelligence skill)
- User's list is already built and needs only scoring (apply S3 only)

---

## S1 — ICP Definition Workshop

The Ideal Customer Profile is the foundation. A weak ICP produces a weak list. [EXPLICIT]

### 1a. Firmographic Dimensions

Define the organizational characteristics of your best-fit customer: [EXPLICIT]

| Dimension | Questions | Example Answer |
|-----------|----------|----------------|
| Industry | Which verticals do you serve best? | Fintech, SaaS, logistics |
| Company size | Headcount range? | 50-500 employees |
| Revenue range | ARR or annual revenue? | $5M-$50M |
| Geography | Where do they operate? | LatAm, US Hispanic market |
| Business model | B2B, B2C, B2B2C? | B2B SaaS |
| Growth stage | Pre-seed to Series C? Bootstrapped? | Series A-B |
| Ownership | VC-backed, PE, public, family? | VC-backed preferred |

### 1b. Technographic Dimensions

Define the technology signals that indicate fit: [INFERRED]

- **Stack compatibility:** Do they use tech you integrate with?
- **Maturity level:** Are they using spreadsheets (early buyer) or mature tooling (late buyer)?
- **Cloud provider:** AWS / GCP / Azure — matters for infrastructure products
- **Key platforms:** Salesforce users, HubSpot users, SAP users — defines ecosystem fit
- **Budget signals:** BuiltWith premium tools = company willing to pay for solutions

### 1c. Behavioral / Intent Signals

Real-time signals that indicate a company is likely in-market: [INFERRED]

| Signal | Meaning | Source |
|-------|---------|--------|
| Job postings for your use case | Budget allocated, pain active | LinkedIn, Indeed |
| Recent funding (Series A/B) | Budget available, growth phase | Crunchbase, TechCrunch |
| New executive hire in relevant function | New agenda, vendor re-evaluation | LinkedIn |
| Conference attendance in your space | Actively exploring solutions | Event websites |
| Competitor customer (churned or public) | Aware of the category, in evaluation mode | G2, Capterra |
| Content engagement with your topic | Top-of-funnel interest signal | LinkedIn, Google |

### 1d. Negative ICP (Disqualifiers)

Define who NOT to pursue. This is as important as the positive ICP: [EXPLICIT]

- Companies smaller than [X] employees (too small to afford / get ROI)
- Industries with regulatory barriers to your solution
- Companies using [competitor/incompatible stack] with long contracts
- Geographies where you have no legal entity or support capacity
- Startups pre-revenue (no budget, wrong stage)

### 1e. ICP Summary Template

```
ICP Name:          [Descriptive name, e.g., "Series A Fintech in LatAm"]
Industry:          [Sector(s)]
Headcount:         [Range] employees
Revenue:           [Range] ARR/annual
Geography:         [Country/region]
Growth stage:      [Seed / A / B / Enterprise / etc.]
Tech stack signal: [Must-have indicator]
Behavioral signal: [Top 1-2 intent signals to prioritize]
Negative filter:   [Disqualifier(s)]
Estimated TAM:     [Number of companies fitting this profile] [INFERRED]
```

---

## S2 — Lead Source Strategy

Identify where to find prospects matching the ICP. [EXPLICIT]

### 2a. Digital Signal Sources

| Source | What to Find | How |
|-------|------------|-----|
| LinkedIn Sales Navigator | Title + industry + headcount + geography | Boolean search, saved searches |
| LinkedIn Company Search | Headcount filters, industry, recent activity | Free tier (limited) |
| Crunchbase / CB Insights | Funding rounds, investor portfolio, industry | Filter by stage + sector + geography |
| AngelList / Wellfound | Startups, tech-first companies, founding team | Category + funding filter |
| G2 / Capterra | Companies using competitor tools | Category page, review filters |
| BuiltWith / Wappalyzer | Companies using specific tech stack | Technology adoption lists |
| Apollo.io | Email + firmographic data | ICP filter + export |

### 2b. Trigger Event Feeds

Monitor for in-market signals continuously: [INFERRED]

| Feed | Trigger Type | Cadence |
|-----|------------|--------|
| TechCrunch / VentureBeat | Funding announcements | Daily |
| LinkedIn notifications | Job postings in your pain category | Weekly |
| Google Alerts "[competitor] review" | Competitor dissatisfaction signals | Daily |
| Industry association member lists | Verified sector companies | Monthly |
| Conference attendee lists | Self-selected in-market buyers | Per event |
| Press release monitoring | Product launches, expansions | Weekly |

### 2c. Network-Based Sources

| Source | How to Activate |
|-------|----------------|
| Customer referrals | Ask top 3 customers: "Who else in your network has this problem?" |
| Partner co-prospecting | Joint prospecting with complementary vendors |
| Alumni networks | LinkedIn alumni filter — ex-colleagues who moved to ICP companies |
| Investor portfolio | Ask VC connections for warm intros to their portcos |
| Trade association directories | Member company lists (often public) |

### 2d. Geographic Focus — LatAm Context

For prospects in Latin America, specific sources: [EXPLICIT]

- **Colombia:** Cámara de Comercio de Bogotá business registry, Colombia Startup directory
- **Mexico:** Secretaría de Economía, Mexico Startup Ecosystem report
- **Brazil:** Crunchbase BR, ABStartups, Distrito database
- **Latam regional:** LAVCA (Latin American Venture Capital Association) portfolio
- **Miami corridor:** Brickell tech scene, Endeavor Miami, eMerge Americas network

---

## S3 — Scoring Model

Apply a consistent scoring framework to prioritize the list. [EXPLICIT]

### BANT + Fit Composite Score

Score each prospect on two dimensions: BANT qualification and ICP fit.

**BANT Score (0-40 points):**

| Dimension | 0 pts | 5 pts | 10 pts |
|-----------|-------|-------|--------|
| **B**udget | No signal | Indirect signal (funding, team size) | Direct signal (published spend, purchase intent) |
| **A**uthority | Unknown | Influencer identified | Decision maker identified |
| **N**eed | No signal | Inferred pain | Explicit pain confirmed |
| **T**iming | No signal | 6-12 months window | Active evaluation or urgent trigger |

**ICP Fit Score (0-60 points):**

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Industry match | 15 pts | Exact match=15, adjacent=8, tangential=3 |
| Size match | 15 pts | Exact range=15, within 2x=8, edge case=3 |
| Tech stack signal | 10 pts | Strong signal=10, moderate=5, none=0 |
| Geography match | 10 pts | Primary market=10, secondary=5, out of scope=0 |
| Behavioral signal | 10 pts | Active trigger=10, passive signal=5, none=0 |

**Total Score Interpretation:**

| Score | Priority Tier | Action |
|-------|-------------|--------|
| 80-100 | Tier 1 — Hot | Full dossier + personalized sequence this week |
| 60-79 | Tier 2 — Warm | Semi-personalized outreach + monitoring |
| 40-59 | Tier 3 — Cool | Template outreach + trigger alert setup |
| Below 40 | Disqualified | Remove from active list; archive for 6 months |

---

## S4 — Prioritization Matrix

Map prospects on two axes to visualize prioritization. [INFERRED]

```
                HIGH FIT
                    |
     High Fit,      |     High Fit,
     Low Urgency    |     High Urgency
     (Nurture)      |     (Close Now)
                    |
LOW URGENCY --------+-------- HIGH URGENCY
                    |
     Low Fit,       |     Low Fit,
     Low Urgency    |     High Urgency
     (Archive)      |     (Evaluate fit)
                    |
                LOW FIT
```

**Urgency Indicators (moves right on the matrix):**
- Active hiring for your use-case role [EXPLICIT]
- Recent funding round (< 90 days) [EXPLICIT]
- Competitor churn signal [INFERRED]
- Exec change in buying function [EXPLICIT]
- End of fiscal year approaching [INFERRED]

**Priority Rules:**
1. Work top-right (high fit + high urgency) first — highest conversion probability [INFERRED]
2. Invest in top-left (high fit + low urgency) for pipeline building — these become top-right [INFERRED]
3. Evaluate bottom-right (low fit + high urgency) only if capacity allows — often a poor use of time [INFERRED]
4. Never work bottom-left — archive immediately [EXPLICIT]

---

## S5 — Output — Qualified List + Approach Brief

### 5a. Qualified Lead List Format

Deliver a structured table (or CSV) with scored, ranked prospects: [EXPLICIT]

```
| # | Company | Industry | Size | HQ | BANT | Fit | Total | Tier | Trigger Event | Best Contact | Channel | Priority |
|---|---------|---------|------|-----|------|-----|-------|------|--------------|-------------|---------|---------|
| 1 | Acme Corp | Fintech | 200 | Bogotá | 32 | 55 | 87 | T1 | Series B (Jan) | VP Eng | LinkedIn | This week |
| 2 | Beta SaaS | Logistics | 85 | CDMX | 25 | 48 | 73 | T2 | New CTO (Feb) | CEO | Email | Next sprint |
```

### 5b. Approach Brief (per Tier 1 prospect)

For every Tier 1 prospect, produce a one-paragraph approach brief: [EXPLICIT]

```
Company: [Name]
Score: [Total] (Tier 1)
Why now: [Trigger event — specific, dated]
Entry angle: [Personalized hook based on the trigger]
Best contact: [Name + Title + LinkedIn]
Recommended channel: [LinkedIn / Email / Warm intro via X]
Validation question: [What to ask in the first call to confirm the hypothesis]
```

### 5c. CSV Export Template

```csv
Rank,Company,Website,Industry,Headcount,HQ,BANT,Fit,Total,Tier,Trigger,Contact Name,Contact Title,LinkedIn,Email Pattern,Channel,Approach Angle,Notes
1,Acme Corp,acme.com,Fintech,200,Bogotá,32,55,87,T1,Series B Jan 2024,Maria G.,VP Eng,linkedin.com/in/...,m.garcia@acme.com [est.],LinkedIn,Series B scale angle,Warm intro via JM
```

---

## Trade-off Matrix

| Decision | Approach A | Approach B | Recommendation |
|---------|-----------|-----------|---------------|
| List size | 10 accounts (deep) | 100+ accounts (broad) | 10-25 Tier 1 accounts per quarter for quality motions |
| Manual vs. automated | Hand-researched | Apollo/LinkedIn export | Hybrid: automated for discovery, manual for Tier 1 scoring |
| Speed vs. accuracy | Fast list, low confidence | Slow list, high confidence | Prefer accuracy — a wrong list wastes more time than building the right one |
| ICP breadth | Narrow ICP (1 segment) | Wide ICP (3 segments) | Start narrow, expand after first 3 customers confirm the ICP |
| Geographic focus | Single market | Multi-market | Single market until first $100K ARR; expand after proof of concept |

---

## Assumptions & Limits

- Data sourced from public sources (LinkedIn, Crunchbase, press) unless user has Apollo/SalesNav [EXPLICIT]
- Headcount and revenue estimates for private companies are approximate [EXPLICIT]
- Behavioral signals (job postings) reflect stated investment, not confirmed budget [INFERRED]
- BANT scoring on early-stage prospects is inherently speculative — validate in discovery calls [EXPLICIT]
- List is a starting point — user must verify before outreach [EXPLICIT]
- Geographic data quality varies; LatAm-specific sources listed in S2d may require registration [INFERRED]

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| User has no ICP yet | Run S1 ICP Workshop fully before any list building; list without ICP = wasted effort |
| Very niche market with < 50 total companies | Build full universe list; focus on completeness over scoring |
| User wants to prospect internationally without local knowledge | Flag knowledge gaps per market; use S2d for LatAm-specific sources |
| User's product has multiple ICPs | Build separate scored lists per ICP; do not mix in one list |
| User has existing customers to exclude | Add "exclude" column to CSV; cross-reference against CRM export |

---

## Good vs Bad Example

**BAD list entry:**
> "Company: Startup X. They might be a good fit for our product."

**GOOD list entry:**
> "Company: Fintech Y (Series A, $8M, March 2024 [EXPLICIT], Bogotá, 45 employees [INFERRED via LinkedIn]). ICP fit: 82/100. Trigger: Hired VP Engineering from Nubank 6 weeks ago [EXPLICIT]. Pain hypothesis: scaling data infrastructure from startup to Series A [INFERRED — confirmed by 4 open data roles on LinkedIn]. Best contact: Diego Torres, VP Eng (joined 6 weeks ago, previously built data platform at Nubank). Channel: LinkedIn — connection request via JM Labs network. Approach angle: 'Saw you came from Nubank — you know what good data infra looks like at scale. Most Series A teams hit the wall at 50% of what Nubank needs. We help bridge that.'"

---

## Validation Gate

- [ ] ICP defined with all firmographic + technographic + behavioral dimensions
- [ ] Negative ICP (disqualifiers) explicitly listed
- [ ] At least 3 lead sources identified and searched
- [ ] BANT score calculated for each prospect (0-40)
- [ ] ICP Fit score calculated for each prospect (0-60)
- [ ] Total scores used to assign tiers (T1/T2/T3/Disqualified)
- [ ] Prioritization matrix applied — Tier 1 confirmed as high-fit AND high-urgency
- [ ] Approach brief produced for every Tier 1 prospect
- [ ] CSV output includes all required columns
- [ ] Trigger event documented (with date) for every Tier 1 prospect

---

## Reference Files

- `knowledge/body-of-knowledge.md` — Sales prospecting methodology foundations
- `knowledge/knowledge-graph.md` — ICP and market entity relationships
- `evals/` — Scored prospect list examples for calibration

---

## Related Skills

- `market-intelligence` — Sector/territory context to inform ICP definition
- `client-dossier` — Deep-dive on each Tier 1 prospect from this list
- `b2b-outreach` — Convert the qualified list into outreach sequences
- `competitive-positioning` — Refine ICP by understanding competitor customer profiles
