---
name: b2b-outreach
description: >
  Triggers on "outreach sequence", "cold email", "B2B outreach", "prospecting messages",
  "contact X company", "write outreach for", "sales sequence", "follow-up cadence".
  Designs B2B outreach sequences — personalized messages, follow-up cadences,
  multi-channel strategy. Output: ready-to-send scripts + CSV tracker template.
  Argument: target company/persona + product/service being sold + deal context.
argument-hint: "target-persona-or-company [product/service] [sequence-length: 3|5|7]"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
version: 1.0.0
---

# B2B Outreach — Sequences That Start Conversations

> TL;DR: Design a multi-touch B2B outreach sequence — cold intro to follow-up — with persona-specific hooks, channel strategy, and a ready-to-deploy CSV tracking template.

**Principio Rector:** Personalization at scale beats volume. One relevant message outperforms ten generic ones.

---

## When to Activate

**Activate when:**
- User says "outreach sequence", "cold email", "B2B outreach", "prospecting messages"
- User says "contact X company", "sales sequence", "follow-up cadence"
- User needs to reach a specific persona or company with a product/service offer [EXPLICIT]
- User is launching a new sales motion and needs templates [INFERRED]

**Do NOT activate when:**
- User needs a single one-off email (use a writing skill instead)
- User needs legal/compliance review of outreach (consult legal counsel)
- User is targeting consumers (B2C) — this skill is B2B-specific [EXPLICIT]

---

## S1 — Prospect Qualification

Before writing a single message, qualify the prospect and identify buying signals. [EXPLICIT]

### 1a. ICP Fit Check

Score the prospect against the Ideal Customer Profile before investing in outreach: [INFERRED]

| Dimension | Questions to Answer |
|-----------|-------------------|
| Firmographic fit | Industry? Company size? Revenue range? Geography? |
| Technographic fit | Do they use tech we integrate with or replace? |
| Behavioral fit | Are they hiring for roles that signal the pain we solve? |
| Timing fit | Recent trigger event? (funding, launch, exec change, expansion) |
| Budget signals | Series B+? PE-backed? Public company? |

**Qualification Score (1-5 per dimension):**
- 20-25: Priority target — invest full personalization effort [INFERRED]
- 14-19: Mid-tier — use semi-personalized templates [INFERRED]
- Below 14: Low fit — exclude or use lowest-cost channel only [INFERRED]

### 1b. Buying Signals (Trigger Events)

Trigger events dramatically increase response rates. Look for: [INFERRED]

| Signal | What It Means | Outreach Angle |
|-------|--------------|----------------|
| Series A/B funding | New budget, new initiatives | "Congrats on the raise — scaling challenges are next..." |
| New C-suite hire | New priorities, open to evaluation | "Fresh eyes often see what has been missing..." |
| Job postings in pain area | Budget allocated to solve this problem | "You are hiring for X — that usually means..." |
| Product launch | Expansion mode, new use cases | "Your launch creates an interesting opportunity..." |
| Competitor win in their space | Fear of missing out | "Your competitor just achieved X..." |
| Conference attendance | Warmer context for connection | "I saw you were at [event] last week..." |

---

## S2 — Outreach Sequence Design

The 5-Touch Model: structured cadence across multiple channels. [EXPLICIT]

### 5-Touch Sequence Framework

```
Touch 1 (Day 1):   LinkedIn connection request + short personal note
Touch 2 (Day 3):   Cold email — value hook + one relevant insight + soft CTA
Touch 3 (Day 7):   LinkedIn InMail or email follow-up — add a new piece of value
Touch 4 (Day 12):  Email — case study or social proof + direct ask
Touch 5 (Day 18):  Break-up message — low pressure, keep the door open
```

**Timing Principles:**
- Never send Touch 1 and Touch 2 on the same day [EXPLICIT]
- Tuesday-Thursday, 7-9am or 1-3pm local time yields highest open rates [INFERRED]
- Avoid Mondays (inbox chaos) and Fridays (disengaged) [INFERRED]
- If any touch gets a response, pause the sequence immediately [EXPLICIT]

### Channel Mix by Persona

| Persona | Best Primary | Best Secondary | Avoid |
|---------|-------------|---------------|-------|
| Founder / CEO | Email (direct) | LinkedIn | Mass sequences |
| VP / Director | LinkedIn InMail | Email | Cold calls without context |
| Manager | Email | LinkedIn | |
| Technical Lead | LinkedIn (content comment) | Email | Generic business pitch |
| Enterprise Procurement | Formal email | Phone | Social messages |

---

## S3 — Personalization Framework

Personalization must be real — not just inserting a first name into a template. [EXPLICIT]

### Personalization Layers

**Layer 1 — Company Specificity (mandatory for all touches):**
- Reference a specific product, news item, or milestone of their company [EXPLICIT]
- Mention a competitor or industry trend directly relevant to them [INFERRED]
- Do NOT use: "I was checking out your website and noticed..." (overused, signals automation)

**Layer 2 — Role Specificity (for Touches 1-3):**
- Map your value to their specific KPIs and responsibilities [INFERRED]
- VP Sales cares about: pipeline, conversion rates, rep ramp time
- VP Engineering cares about: velocity, technical debt, incident rate
- CFO cares about: unit economics, burn rate, cost of capital
- CHRO cares about: retention, time-to-hire, L&D ROI

**Layer 3 — Person Specificity (for high-priority targets):**
- Reference their LinkedIn post, podcast appearance, or published article [EXPLICIT]
- Note a shared connection, alumni network, or event [EXPLICIT]
- Never fabricate a personal detail — only use publicly confirmed information [EXPLICIT]

### Personalization Efficiency

For high-volume sequences (50+ targets), use a semi-personalized approach: [INFERRED]

```
[FIXED]        Generic value proposition paragraph
[PERSONALIZED] Company-specific hook (1 sentence, researched per target)
[FIXED]        CTA and sign-off
```

This allows 80% of the message to be reused while the key hook remains specific. [INFERRED]

---

## S4 — Message Templates by Persona

### Template A: Founder / CEO (Concise, peer-level)

**Touch 1 — LinkedIn note:**
> Hi [Name], saw [Company] just [trigger event]. Building something in the [space] as well — would love to connect.

**Touch 2 — Cold email:**
> Subject: [Company] + [Your Company] — quick thought
>
> [Name],
>
> [1-sentence company-specific hook based on trigger event].
>
> We help [ICP description] [specific result] — [Reference Company] went from [before state] to [after state] in [timeframe].
>
> Worth a 20-minute call to see if there is a fit?
>
> [Your Name]

**Touch 4 — Social proof follow-up:**
> [Name], following up from my earlier note.
>
> We just published a case study on how [Similar Company] [achieved result]. Thought it might be relevant given [company-specific reason].
>
> Still happy to show you how it applies to [Company] specifically.

**Touch 5 — Break-up:**
> [Name], I will stop reaching out after this. If [pain point] becomes a priority, I am one message away.
>
> Best of luck with [specific initiative].

### Template B: VP / Director (Results-oriented)

**Touch 2 — Cold email:**
> Subject: [Specific metric] for [their company name]
>
> Hi [Name],
>
> [Company-specific hook: what you noticed about their situation].
>
> [Your company] helps [role title] at [company type] [achieve metric outcome]. One example: [Reference Company] reduced [metric] by [X]% in [timeframe].
>
> I have 3 ideas specific to [Company] that might help. 15 minutes this week?
>
> [Your Name]

### Template C: Technical Lead (Credibility-first)

**Touch 2 — Cold email:**
> Subject: [Their tech stack tool] + [your product] integration
>
> Hi [Name],
>
> I saw [Company] is using [specific tool from their stack] — we built a native integration that [specific technical outcome].
>
> Happy to share the integration docs if useful. No pitch — just the technical context.
>
> [Your Name]

---

## S5 — Output — Scripts + CSV Tracker Template

### Sequence Output Format

For each sequence, deliver:
1. **Sequence brief** — ICP fit score, trigger event used, personalization notes [EXPLICIT]
2. **Touch 1-5 scripts** — complete message text, ready to copy-paste [EXPLICIT]
3. **Subject line variants** — 3 options per email touch for A/B testing [EXPLICIT]
4. **Response handlers** — what to say if they respond positively, negatively, or ask for more info [INFERRED]

### CSV Tracker Template

```csv
Prospect,Company,Title,LinkedIn,Email,ICP Score,Trigger Event,T1 Date,T1 Status,T2 Date,T2 Status,T3 Date,T3 Status,T4 Date,T4 Status,T5 Date,T5 Status,Response,Response Date,Next Step,Notes
[Name],[Co],[VP Role],linkedin.com/in/...,[email],22,Series B funding,2024-01-15,Sent,2024-01-17,Opened,,,,,,,Positive,2024-01-18,Discovery call booked,[note]
```

**Status values:** Sent / Opened / Clicked / Replied / Bounced / Not sent
**Response values:** Positive / Negative / Neutral / No response
**Next Step values:** Discovery call / Follow-up in 30d / Disqualified / Closed

---

## Trade-off Matrix

| Mode | Personalization | Sequence Length | Volume | Output |
|------|---------------|----------------|--------|--------|
| **High-touch** | Full 3-layer | 5 touches | 5-10 targets/week | Custom scripts per person |
| **Semi-personalized** | Company hook only | 5 touches | 20-50/week | Template + variable fields |
| **Volume play** | Name + industry only | 3 touches | 100+/week | Pure template + A/B variants |

---

## Assumptions & Limits

- Message content must be truthful — no fabricated social proof, case studies, or metrics [EXPLICIT]
- GDPR/CAN-SPAM compliance: include unsubscribe mechanism in all email sequences [EXPLICIT]
- LinkedIn has connection and InMail limits — respect platform rules [EXPLICIT]
- Response rate benchmarks are indicative — actual results vary by industry [INFERRED]
- This skill produces scripts — actual sending is the user's responsibility [EXPLICIT]
- Email patterns are inferred and labeled with confidence level [EXPLICIT]

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| Target is a sole founder with no public contact | Use LinkedIn DM as primary; note limited scalability |
| Company has stated no-cold-email policy | Respect it; use LinkedIn or warm intro only |
| Target replied negatively to Touch 2 | Pause sequence; log for 90-day re-engage window |
| Target works at a direct competitor | Flag to user; proceed only if user confirms specific use case |
| No trigger event found for prospect | Use industry-level hook instead; lower personalization layer |

---

## Good vs Bad Example

**BAD Touch 2 email:**
> "Hi [Name], I hope this message finds you well. I am reaching out to introduce our solution which helps companies improve their processes. Would you like to schedule a call?"

**GOOD Touch 2 email:**
> Subject: Rappi's churn fix — relevant for Pedidos Ya?
>
> Hi Maria,
>
> Pedidos Ya just expanded into 3 new LatAm markets — that usually surfaces retention challenges not visible at smaller scale.
>
> We helped Rappi reduce early churn by 34% in 6 months by instrumenting the activation funnel they could not measure before.
>
> 20 minutes to walk through whether the same approach fits your situation?
>
> Javier

---

## Validation Gate

- [ ] ICP fit score calculated before writing the sequence
- [ ] Trigger event identified and used in Touch 1 and Touch 2 hooks
- [ ] 5-touch sequence complete with dates and channels specified
- [ ] Touch 1 and Touch 2 fully written (complete text, not just described)
- [ ] 3 subject line variants provided for email touches
- [ ] Personalization layer declared (full / company-hook / name-only)
- [ ] Break-up message (Touch 5) included
- [ ] Response handlers written for positive, negative, and no-response outcomes
- [ ] CSV tracker template delivered alongside scripts
- [ ] GDPR/CAN-SPAM compliance acknowledged (unsubscribe mechanism noted)

---

## Reference Files

- `knowledge/body-of-knowledge.md` — Sales methodology and outreach frameworks
- `knowledge/knowledge-graph.md` — Persona-to-pain-to-message mapping
- `evals/` — Scored sequence examples

---

## Related Skills

- `client-dossier` — Research the target before writing the sequence
- `client-prospecting` — Build the lead list that feeds this skill
- `market-intelligence` — Identify trigger events and company signals for personalization
- `executive-pitch` — Extend the sequence into a full pitch for qualified leads
