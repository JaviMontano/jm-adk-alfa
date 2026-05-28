---
name: client-dossier
description: >
  Triggers on "build dossier on", "client profile", "prospect research", "research company X",
  "build profile on X person", "dossier for sales call", "quién es X empresa".
  Produces a branded HTML dossier: company DNA, key contacts, pain points, entry strategy.
argument-hint: "company-name or person-name"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
version: 1.0.0
---

# Client Dossier — Intelligence Brief for High-Stakes Meetings

> TL;DR: Transform public signals about a prospect into a battle-ready dossier — company DNA,
> key contacts, pain hypotheses, and a personalized approach strategy. Output: branded HTML
> dossier (JM Labs dark style) + optional markdown summary.

**Principio Rector:** Prepare like a detective, enter like a consultant. Every fact verified,
every hypothesis labeled. A dossier is not an encyclopedia — it is a decision support tool.

---

## When to Activate

**Activate when:**
- User says "build dossier on [company/person]", "research [company X]", "client profile for [name]"
- User says "quién es [empresa]", "investiga a [empresa]", "perfil de prospecto para [nombre]"
- User says "dossier for sales call", "prep for meeting with [company]", "who is [person] at [company]"
- A sales or BD context is active and a company or executive name is the primary input [INFERRED]
- User provides a company name and asks for entry strategy, pain points, or stakeholder map [INFERRED]
- User has a discovery call in <48h and needs preparation material [INFERRED]

**Do NOT activate when:**
- User is asking for general market research without a named target (use market-intelligence instead)
- The request is about internal team members or employees (use stakeholder-mapping instead)
- The request is about a private individual in a non-business context (privacy concern — decline)
- User wants a competitive landscape across multiple players (use competitive-intelligence instead)
- Input is too vague: "research my industry" — no named target present, clarify first
- User needs legal/financial due diligence for M&A (requires specialized legal tools, not this skill)

---

## S1: Dossier Types

Three dossier modes, each with a distinct research agenda. Infer the mode from phrasing.
If ambiguous, ask: "Is this a company dossier, an executive profile, or a partnership evaluation?"

**Company Dossier** [EXPLICIT]
Full organizational profile. Used before a first meeting, RFP response, or partnership pitch.
Covers founding story, ownership, revenue signals, headcount trajectory, tech stack, recent
strategic moves, and cultural tone. Most common mode. Output: all 6 sections (S2–S5 + HTML).

**Executive / Public Figure Dossier** [EXPLICIT]
Profile of a named decision-maker. Used to personalize outreach, prepare for a call, or
understand a gatekeeper. Covers career arc, public positions, speaking topics, known priorities,
management style signals, and mutual connections.
Strict scope: public professional information only. No personal life, no private data inference.
Do not include home addresses, personal social media, family data, or non-professional history.

**Partnership Target Dossier** [INFERRED]
Hybrid of company + lead contact. Used when evaluating a channel partner, reseller, or
co-builder. Emphasizes business model alignment, revenue complementarity, integration potential,
and historical partnership behavior: who they partner with, on what terms, and how long those
partnerships last.

**Minimum viable input per mode:**

| Mode | Required | Useful extras |
|---|---|---|
| Company | Company name | Website, LinkedIn URL, industry |
| Executive | Full name + company | LinkedIn URL, role title |
| Partnership | Company name + relationship type | Customer segment, known tech stack |

**Dossier depth options:**

| Mode | Time | Scope | Use case |
|---|---|---|---|
| Flash (30 min) | Fast | Company DNA + 1 contact | Inbound call in <1h |
| Standard (2h) | Medium | Full S2–S5, 2–3 contacts | Tomorrow's discovery call |
| Deep (5h+) | Slow | Full + org chart + competitive context | Strategic account, large deal |

---

## S2: Company DNA Framework

Systematic extraction of organizational identity signals. Work through each dimension.
Tag every claim with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`. [EXPLICIT]

**Founding & Ownership**
- Year founded, founding team background (operators vs. investors vs. technologists) [EXPLICIT]
- Current ownership: bootstrapped, VC-backed (series + lead investor), PE-owned, public [EXPLICIT]
- Acquisition history: have they been acquired or acquired others? Signals strategic ambition [EXPLICIT]
- Ownership concentration: founder-led vs. institutional vs. family-controlled [INFERRED]

**Revenue & Growth Signals**
- Public revenue if available; otherwise triangulate from funding rounds + headcount trend [INFERRED]
- Growth stage: pre-PMF, scaling, mature/optimizing, declining/pivoting [INFERRED]
- Geographic footprint: single market, regional, global — matters for solution scope [EXPLICIT]
- Hiring velocity: net new roles in last 90 days signals investment in capability [INFERRED]

**Headcount & Team Composition**
- Total headcount from LinkedIn (snapshot, not exact); engineering % vs. sales % vs. ops % [INFERRED]
- Departures / executive churn: LinkedIn tenure data, Glassdoor reviews as qualitative signal [INFERRED]
- Key department gaps: 5 open data engineer roles → they have an infrastructure problem [INFERRED]
- Note: headcount from LinkedIn can be ±15-20% of actual; label as `[est.]` [EXPLICIT]

**Tech Stack Signals**
- Job posting language: "must know Kubernetes", "experience with Salesforce", "dbt + Snowflake"
- BuiltWith / Wappalyzer (if web-facing product) for frontend/marketing stack [INFERRED]
- GitHub org activity: open-source repos, language distribution, commit frequency [EXPLICIT]
- Integration partners mentioned on their website or in press releases [EXPLICIT]

**Recent News & Strategic Moves (last 90 days)**
- Funding announcements, acquisitions, product launches [EXPLICIT]
- Leadership changes (new CTO/CPO = new agenda, new vendor evaluation cycle) [INFERRED]
- Customer wins / case studies published = proof of strategic direction [EXPLICIT]
- Conference appearances and speaking slots = what narrative they are pushing publicly [INFERRED]
- Regulatory or legal events (SEC filings if public, lawsuit mentions) [EXPLICIT]

**Cultural & Operational Tone**
- Mission language on careers page: "move fast", "customer obsessed", "enterprise-grade" [INFERRED]
- Glassdoor themes: execution culture vs. churn risk; note review recency [INFERRED]
- Social media tone: thought leadership vs. pure broadcast vs. community-engaged [INFERRED]

**Financial Signals Table:**

| Signal | What It Indicates |
|---|---|
| Recent funding round | Available budget, growth phase, investor expectations |
| High job posting volume | Investment areas, team priorities, active pain points |
| Contract announcements | Revenue tiers, deal size norms |
| Downsizing / layoffs | Budget pressure, cost-saving motive, churn risk |
| Awards / rankings | Brand health, employer strength, strategic priorities |
| Re-posted same role 3× | Retention problem or unrealistic hiring bar |

> [OPEN] Revenue figures for private companies are estimates. Flag all inferred revenue
> with `[est. — not verified]` in every output. Never present as confirmed facts.

---

## S3: Key Contacts Map

Build a stakeholder map of the target organization focused on the deal or engagement type.
Produce a Contact Card (see template below) for each named person. [EXPLICIT]

**Decision Maker Identification by Deal Type**

| Deal Type | Decision Maker | Influencer | Gatekeeper |
|---|---|---|---|
| Technology / SaaS | CTO, VP Engineering | Engineering Manager | EA, Procurement |
| Consulting / services | CEO, COO | CFO | EA, Legal |
| Training / enablement | CHRO, VP L&D | Department Head | Training Coordinator |
| Data / analytics | CDO, VP Data | Data Lead | Procurement |
| Marketing tech | CMO, VP Marketing | Demand Gen Lead | Marketing Ops |
| Digital transformation | CIO / CDO + C-suite sponsor | COO | PMO, Legal |

**Contact Research Protocol** (execute in this order):
1. LinkedIn search: "[Company] [Title]" — note tenure, previous companies, education [EXPLICIT]
2. Company website team/about page — often lists leadership with bios [EXPLICIT]
3. Search "[Name] [Company] interview" or "[Name] [Company] podcast" for public positions [EXPLICIT]
4. Twitter/X profile for thought leadership signals and engagement patterns [EXPLICIT]
5. Note mutual connections — warm intro is always the highest-value outreach path [INFERRED]

**Email Pattern Inference** (validate before use — never assume confirmed):
- `firstname@company.com` — common at startups and SMB
- `firstname.lastname@company.com` — most common at mid-market and enterprise
- `flastname@company.com` — common in finance and professional services
- `f.lastname@company.com` — frequent in European companies
Use Hunter.io pattern matching (if user has access) or validate via email verification tool.
Label all email patterns as `[INFERRED — not verified]` in output. [EXPLICIT]

**Contact Card Template (produce one per person):**
```
Name:              [Full Name]                          [EXPLICIT]
Title:             [Current Title]                      [EXPLICIT]
Tenure:            [X years at company]                 [EXPLICIT]
Prior companies:   [2–3 most relevant past employers]   [EXPLICIT]
Background:        [2-sentence career arc]              [EXPLICIT]
Public positions:  [Key theme they discuss publicly]    [EXPLICIT]
Best channel:      [LinkedIn / email / warm intro via X][INFERRED]
Likely priority:   [What they care about professionally][INFERRED]
Potential concern: [What might make them say no]        [INFERRED]
Email pattern:     [pattern@company.com — confidence: H/M/L] [INFERRED]
Mutual connection: [Name + relationship if applicable]  [EXPLICIT / OPEN]
```

**Org Chart Reconstruction** [INFERRED]
- Map reporting lines from LinkedIn titles and tenure signals
- Identify recently promoted people (likely championing new initiatives)
- Flag who joined from a competitor (may bring vendor preferences with them)
- Note who is actively hiring under them (signals budget ownership)

> [EXPLICIT] Only use publicly available professional information. Do not infer personal
> details, home addresses, or non-professional social media content.

---

## S4: Pain Point Hypothesis

Construct a hypothesis of what is hurting the target organization right now.
This drives message-market fit for the outreach or pitch. Produce 3–5 hypotheses. [EXPLICIT]

**Signal-to-Pain Mapping:**

| Signal Observed | Derived Pain Hypothesis |
|---|---|
| 15+ open engineering roles | Scaling pains, team capacity issues, delivery bottleneck |
| 3 CTOs in 24 months | Tech strategy instability, culture/direction tension |
| No data/analytics roles | Low data maturity, spreadsheet-heavy operations |
| Series B raised 12 months ago | Board pressure for growth metrics and unit economics |
| Recent compliance-related press | Regulatory risk, need for audit/governance tooling |
| Legacy tech stack in job postings | Migration need, tech debt, developer experience friction |
| Rapid expansion to new markets | Localization needs, operational complexity, compliance gaps |
| Re-posting the same role 3× | Retention problem or misaligned expectations |
| Competitor launched a feature they lack | Product gap, pressure to close the gap fast |
| Customer forum / G2 complaints visible | Support overload, churn risk, UX debt |

**Pain Point Hypothesis Format (produce per hypothesis):**
```
Hypothesis:    [Company X] likely struggles with [SPECIFIC PAIN]         [INFERRED]
Evidence:      [Signal 1: source] + [Signal 2: source]
Urgency:       [Why this pain is acute NOW vs. chronic background noise]  [INFERRED]
Our hook:      [How our offering maps to this specific pain]              [INFERRED]
Confidence:    High / Medium / Low
Validation Q:  [The one question to ask on the call to confirm or refute]
```

**Pain Categories Checklist:**
- [ ] Revenue growth blocked (can't acquire, expand, or retain customers)
- [ ] Operational efficiency (manual work, slow processes, high headcount for low output)
- [ ] Technical debt (legacy stack slowing product velocity)
- [ ] Talent (can't hire, retain, or upskill fast enough)
- [ ] Compliance / risk (regulatory pressure, security gaps, audit failures)
- [ ] Data visibility (can't measure what matters, decisions made on gut)
- [ ] Customer experience (churn, NPS decline, support volume growing)

> [EXPLICIT] Pain hypotheses are hypotheses. They must be validated in the discovery call.
> Do not present them as confirmed facts in the dossier or in outreach messages.

---

## S5: Approach Strategy

Synthesize dossier findings into a concrete outreach and engagement plan. [INFERRED]

**Best Entry Angle Selection:**

| Context | Recommended Angle |
|---|---|
| Recent funding round | Congrats + growth/scale challenge framing, budget window open |
| New executive hire | Fresh start, new vendor evaluation cycle, open to change |
| Recent product launch | Integration opportunity, complementary capability |
| Cost pressure signal | ROI-first framing, fast time-to-value, efficiency story |
| Competitor win in their space | Urgency angle, competitive pressure, fear of falling behind |
| Award / milestone | Validation: "how do you maintain this standard at scale?" |
| Pain signal from job postings | Precision hook: "we saw your [X] postings, we solve that" |

**Personalization Layers (stack all four for highest conversion):**
1. **Company layer** — Reference specific company news, milestone, or challenge [EXPLICIT]
2. **Role layer** — Speak to their specific responsibilities and KPIs [INFERRED]
3. **Person layer** — Reference their public content, career moves, or interests [EXPLICIT]
4. **Timing layer** — Connect to a trigger event (funding, launch, Q1 planning cycle) [INFERRED]

**Channel Sequence Recommendation:**
1. LinkedIn connection request (no note, or short note referencing shared context)
2. LinkedIn message after connection (1 paragraph, specific hook, one clear ask)
3. Email follow-up 5 days later (reference the LinkedIn outreach, add new value element)
4. Warm intro via mutual connection if one exists (highest conversion, always preferred)

**Objection Pre-empts:**

| Common Objection | Pre-empt in the Message |
|---|---|
| "We already have a solution" | Acknowledge + differentiate on one specific dimension |
| "Not the right time / budget frozen" | Ask for a 15-min discovery, not a commitment |
| "Send me more info" | Offer a 1-pager tailored to their use case, not a generic deck |
| "We handle this internally" | Validate their approach, offer a benchmark/audit angle |
| "We're in evaluation mode already" | Ask to be included, offer a specific POV or framework |

**Opening Message Draft Formula:**
```
[Trigger event / personalization hook] + [specific pain we solve] +
[1 reference to a peer / analogous company] + [metric or outcome] + [single soft ask]
```

Example:
> "Saw your team posted 6 data engineer roles this quarter — teams scaling data infra
> at your stage usually hit the orchestration wall 60 days after the dbt rollout.
> We helped [Peer Company] cut pipeline failures by 70% in that window.
> Worth a 20-minute call to see if the pattern fits?"

---

## S6: HTML Dossier Output Template

Generate a branded, self-contained HTML dossier. Load full template from `references/html-template.md`. [EXPLICIT]

**Brand tokens**: `--navy: #122562` · `--gold: #FFD700` · `--blue: #137DC5` · dark bg `#0d0d0d` · Poppins headings + Inter body.

**Sections in the HTML output**: Header (company name + date + confidential badge) → TL;DR executive brief (3 bullets) → Company DNA (10-field data grid) → Key Contacts (2 contact cards) → Pain Hypotheses (3 items with confidence badges) → Approach Strategy (4-step numbered list) → Footer (JM Labs attribution).

**Delivery rules** [EXPLICIT]:
- Replace every `[placeholder]` with researched data
- Label inferred fields with `[est.]` inline
- Do not deliver with unfilled placeholders
- Mark `[INFERRED]` on estimated revenue / headcount / tech stack when source is indirect

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|---|---|---|---|
| Depth vs. speed | Full 6-section dossier (2-3h) | Quick 2-section brief (30min) | Full for strategic accounts; brief for same-day inbound |
| Public vs. inferred data | Only confirmed facts | Include reasoned inferences | Include inferences, tag clearly with [INFERRED] |
| HTML vs. markdown output | Branded HTML dossier | Plain markdown summary | HTML for client-facing; markdown for internal notes |
| Company vs. person focus | Company-first, then people | Person-first, then company | Company-first unless user specifies a named target |
| One contact vs. full map | Single decision-maker | Full stakeholder map | Full map for deals >$50K; single for fast outreach |
| Hypothesis depth | 1 primary pain | 3–5 ranked hypotheses | 3–5 always; more hypotheses = better discovery call prep |

---

## Assumptions & Limits

- [EXPLICIT] All research is based on publicly available information only. No paid databases,
  no data brokers, no private data inference beyond professional context.
- [INFERRED] Revenue and headcount figures for private companies are estimates. Every such
  figure is labeled `[est. — not verified]` in the output.
- [EXPLICIT] Email patterns are hypotheses, not confirmed addresses. User must validate before use.
- [OPEN] Tech stack inferences from job postings may lag reality by 6–12 months. Directional only.
- [EXPLICIT] This skill does not profile private individuals outside a professional or public-figure
  context. If a request concerns a private person, decline and explain the privacy concern.
- [INFERRED] Pain hypotheses are probabilistic. The validation question in each hypothesis is
  mandatory — do not treat as confirmed until the discovery call verifies it.
- [EXPLICIT] Dossier freshness degrades fast — refresh if >30 days old before any meeting.

---

## Edge Cases

**EC-1: Company with no digital footprint**
Very small or recently founded company has minimal LinkedIn presence, no press, minimal web.
Action: Build a lightweight dossier from whatever is available. Flag the confidence score as
low. Use industry + company size + founding year to construct pain hypotheses from first
principles (e.g., "at 20 employees in SaaS, the most common pain at 18 months is [X]").

**EC-2: Executive with a common name / ambiguous identity**
"John Smith at Acme" — multiple LinkedIn matches, ambiguous results.
Action: Ask user for LinkedIn URL or full title before proceeding. Do not produce a dossier on
the wrong person. Verify company + current title before writing any Contact Card.

**EC-3: Company in a language other than English**
Target is a Latin American or European company with minimal English-language presence.
Action: Research in the native language. Produce the dossier in the language the user requests.
Use `[data-l="es"]` / `[data-l="en"]` HTML markup throughout the output.

**EC-4: User wants a dossier on a competitor (not a prospect)**
Intent is competitive intelligence, not a sales dossier.
Action: Redirect to the competitive-intelligence skill. The dossier framework is optimized for
outreach and entry strategy, not competitive positioning — wrong tool for this use case.

**EC-5: Publicly traded company with overwhelming data volume**
10-K, earnings calls, IR page, analyst coverage — information overload.
Action: Prioritize recency (last 12 months) and strategic relevance (what affects this deal).
Summarize, do not dump. The dossier is a decision tool, not an archive. Cite specific
sections for the user to read if they want more depth.

---

## Good vs. Bad Example

**BAD — Generic, no action value:**
> "Acme Corp is a technology company with around 500 employees. They seem to be growing
> and might be interested in our services. Their CEO is John Doe."

**GOOD — Specific, hypothesis-driven, actionable:**
> "Acme Corp (Series B, $42M raised Jan 2024 [EXPLICIT], 340 → 480 employees in 12 months
> [INFERRED via LinkedIn]) is scaling engineering faster than their data infrastructure
> can support. Evidence: 6 open data engineer roles in Q1 [EXPLICIT], all requiring dbt +
> Snowflake, none requiring Airflow — the orchestration gap [INFERRED]. Decision-maker:
> Maria Gómez, VP Engineering (joined 8 months ago from Stripe [EXPLICIT], previously built
> a data platform team from scratch [EXPLICIT via LinkedIn bio]). Hook: 'We saw your data
> engineer postings — teams at your stage typically hit the orchestration wall 60 days after
> the dbt rollout. We solved this for [Peer Company] and cut pipeline failures by 70%.
> Worth a 20-min call?' [INFERRED pain + EXPLICIT peer reference]."

The good version has: named signals with evidence tags, a specific gap, a named contact with
career context, a peer reference, a metric, and a specific one-ask close. Every element traces
to a real signal source.

---

## Validation Gate

Before delivering any dossier output, verify all of the following:

- [ ] Company name correctly spelled and verified — not a homonym or alias
- [ ] All revenue / headcount figures labeled `[est.]` if not from a public source
- [ ] At least 2 specific signals support the primary pain hypothesis
- [ ] Every named contact drawn from public professional sources only
- [ ] Email patterns labeled as `[INFERRED — not verified]`, not as confirmed addresses
- [ ] Tech stack claims trace to at least one concrete signal (job posting, website, press)
- [ ] Approach strategy includes a specific personalization hook, not a generic opener
- [ ] HTML output uses JM Labs brand tokens (navy `#122562`, gold `#FFD700`, blue `#137DC5`)
- [ ] Bilingual `[data-l]` attributes present on all user-facing strings in HTML output
- [ ] All `[placeholder]` tokens in HTML have been replaced with real researched data

---

## Reference Files

| File | Purpose |
|---|---|
| `knowledge/body-of-knowledge.md` | Sales intelligence and OSINT methodology |
| `knowledge/knowledge-graph.md` | Entity relationships for prospect research |
| `evals/` | Scored dossier examples for quality calibration |

---

## Related Skills

- `market-intelligence` — Broader market/sector context before the dossier
- `b2b-outreach` — Convert dossier findings into outreach sequences
- `client-prospecting` — Identify who to build dossiers for
- `competitive-intelligence` — Competitor profiles (different framework from prospect dossiers)
- `executive-pitch` — Use dossier findings to prepare a pitch narrative
- `stakeholder-mapping` — Internal org mapping when target is an existing client
