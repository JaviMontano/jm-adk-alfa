---
name: social-media-strategy
description: >
  Triggers on "social media strategy", "content calendar", "social media plan", "estrategia redes sociales".
  Builds a platform selection matrix, content pillars, posting cadence, hashtag strategy, and engagement tactics. Output: content calendar + platform-specific guidelines. [EXPLICIT]
argument-hint: "brand/product name + target audience + goals (awareness, leads, engagement)"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Social Media Strategy

## TL;DR

Generates a complete social media strategy from brand context and audience definition. Produces a platform selection matrix, content pillar framework, posting cadence calendar, hashtag taxonomy, and engagement playbook. Final deliverable is a content calendar with platform-specific guidelines ready for execution.

## When to Activate

- User mentions "social media strategy", "content calendar", "social media plan", or "estrategia redes sociales"
- Input contains a brand or product needing social presence planning
- Request involves choosing platforms, defining content types, or scheduling posts
- User asks for engagement tactics or hashtag research for a specific niche

Do NOT activate for one-off post writing, ad campaign management, or influencer outreach (those are separate skills).

## 1. Platform Selection Matrix

Evaluate each major platform against the user's context:

| Criteria            | Instagram | LinkedIn | X/Twitter | TikTok | YouTube | Facebook |
|---------------------|-----------|----------|-----------|--------|---------|----------|
| Audience fit        | --        | --       | --        | --     | --      | --       |
| Content format fit  | --        | --       | --        | --     | --      | --       |
| Resource demand     | --        | --       | --        | --     | --      | --       |
| Organic reach       | --        | --       | --        | --     | --      | --       |
| Conversion path     | --        | --       | --        | --     | --      | --       |
| Competitor presence | --        | --       | --        | --     | --      | --       |

Score each cell 1-5. Recommend the top 2-3 platforms with justification. Tag each recommendation with evidence level: `[EXPLICIT]` when user stated preference, `[INFERRED]` when derived from audience data, `[OPEN]` when assumption-based.

### Platform-Specific Format Guidelines

For each selected platform, define:
- Optimal image/video dimensions and aspect ratios
- Character limits and best-practice lengths
- Native features to leverage (Stories, Reels, Carousels, Polls, Threads)
- Best posting times by audience timezone
- Algorithm signals that boost visibility

## 2. Content Pillar Framework

Define 3-5 content pillars that balance brand authority with audience interest:

1. **Educational** — Teach something relevant to the audience's problems
2. **Behind-the-Scenes** — Humanize the brand with process, team, culture
3. **Social Proof** — Testimonials, case studies, user-generated content
4. **Engagement** — Polls, questions, challenges, trending participation
5. **Promotional** — Direct offers, launches, CTAs (keep under 20% of total)

For each pillar, specify:
- Content ratio (percentage of total output)
- Sample post formats per platform
- Tone and visual style notes
- KPI it primarily serves (reach, engagement, conversion, retention)

## 3. Posting Cadence and Calendar

Build a weekly template calendar:

| Day       | Platform A        | Platform B        | Platform C      |
|-----------|-------------------|-------------------|-----------------|
| Monday    | Pillar + format   | Pillar + format   | --              |
| Tuesday   | --                | Pillar + format   | Pillar + format |
| Wednesday | Pillar + format   | --                | --              |
| Thursday  | Pillar + format   | Pillar + format   | Pillar + format |
| Friday    | Pillar + format   | --                | Pillar + format |
| Saturday  | --                | --                | --              |
| Sunday    | Pillar + format   | --                | --              |

Rules:
- Minimum 3 posts/week on primary platform, 2 on secondary
- Stories/ephemeral content daily on visual platforms
- Never post the same content verbatim across platforms — adapt format and tone
- Schedule high-engagement content (polls, questions) on peak-activity days

## 4. Hashtag Strategy and Engagement Tactics

### Hashtag Taxonomy

Organize hashtags into three tiers:
- **Branded** (1-2): unique to the brand, trackable
- **Niche** (5-8): specific to the industry/topic, moderate competition
- **Broad** (2-3): high-volume discovery tags, used sparingly

Provide a bank of 20-30 researched hashtags categorized by tier and content pillar.

### Engagement Playbook

- **Reactive**: respond to comments within 2 hours during business hours, like/reply to mentions
- **Proactive**: comment on 5-10 accounts in target audience daily, engage with industry leaders
- **Community**: create a branded hashtag challenge monthly, feature UGC weekly
- **Collaboration**: identify 3-5 micro-influencers or complementary brands for cross-promotion

## Trade-off Matrix

| Decision                     | Option A               | Option B               | Recommendation         |
|------------------------------|------------------------|------------------------|------------------------|
| Platform breadth             | Focus on 2 platforms   | Spread across 4+       | Focus — quality beats presence |
| Content frequency            | Daily posting          | 3-4x/week high quality | Quality cadence unless team supports daily |
| Original vs curated          | 100% original          | 70/30 original/curated | 80/20 for most brands  |
| Organic vs paid amplification| Pure organic            | Boosted posts          | Boost top 10% organic performers |
| Trend participation          | Always join trends     | Selective only         | Selective — brand alignment first |

## Assumptions and Limits

- Assumes the user has or can create visual assets; does not generate images [EXPLICIT]
- Hashtag effectiveness estimates based on general patterns, not real-time API data [INFERRED]
- Posting time recommendations use general industry benchmarks unless user provides analytics [INFERRED]
- Does not manage ad spend, paid campaigns, or influencer contracts [EXPLICIT]
- Platform algorithm behavior is inferred from public knowledge, subject to change [OPEN]

## Edge Cases

1. **B2B with no visual product** — Shift pillar emphasis to thought leadership, data visualizations, and employee advocacy. Prioritize LinkedIn and X over Instagram/TikTok.
2. **Regulated industry (finance, healthcare)** — Add compliance review step before publishing. Flag disclaimers, avoid guarantees, note approval workflows.
3. **Multi-language audience** — Define primary and secondary content languages. Recommend separate accounts vs bilingual posts based on audience segmentation data.
4. **Zero existing presence** — Include a 30-day launch runway: profile optimization, initial content bank of 15-20 posts, follower seeding strategy before public launch.
5. **Crisis/reputation recovery** — Prepend a listening audit. Adjust tone pillars toward transparency and empathy. Reduce promotional content to under 5%.

## Good vs Bad Example

### Good
```
Platform: LinkedIn (primary), Instagram (secondary)
Pillar: Educational (40%), Social Proof (25%), BTS (20%), Engagement (10%), Promo (5%)
Cadence: LinkedIn 4x/week, Instagram 3x/week + daily Stories
Hashtag bank: 25 tags across 3 tiers, mapped to pillars
Evidence: [INFERRED] from B2B SaaS audience profile and competitor benchmarking
```

### Bad
```
Post on all platforms every day.
Use trending hashtags.
Share the same content everywhere.
(No pillar structure, no evidence tags, no platform rationale)
```

## Validation Gate

Before delivering the strategy, confirm every item:

- [ ] Platform selection matrix completed with scores and justification
- [ ] 3-5 content pillars defined with ratios summing to 100%
- [ ] Weekly posting cadence calendar filled for all selected platforms
- [ ] Hashtag bank of 20+ tags organized by tier and pillar
- [ ] Engagement playbook includes reactive, proactive, and community tactics
- [ ] Every recommendation tagged with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`
- [ ] Platform-specific format guidelines (dimensions, limits, features) documented
- [ ] Trade-offs explicitly stated with reasoning
- [ ] Edge cases reviewed against user context
- [ ] Output formatted as content calendar + platform guidelines document

## Reference Files

| File | Purpose |
|------|---------|
| `references/platform-benchmarks.md` | Industry posting frequency and engagement rate benchmarks |
| `references/hashtag-research.md` | Hashtag research methodology and tier classification guide |
| `references/content-calendar-template.md` | Weekly/monthly calendar template with pillar mapping |
