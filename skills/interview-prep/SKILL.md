---
name: interview-prep
description: >
  Triggers on "prepare for interview", "interview prep", "preparar entrevista", "mock interview".
  Builds an interview preparation kit with question banks, STAR frameworks, company research checklists, and follow-up templates. Output: prep document. [EXPLICIT]
argument-hint: "role title + company name + interview type (behavioral, technical, panel)"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Interview Preparation Kit

## TL;DR

Produces a structured interview preparation document tailored to a specific role and company. Includes a categorized question bank, STAR-method response scaffolds, company research checklist, talking points aligned to job requirements, and post-interview follow-up templates. Works for job interviews, client discovery calls, and stakeholder meetings.

## When to Activate

- User mentions "prepare for interview", "interview prep", "preparar entrevista", or "mock interview"
- Input contains a job posting, role description, or upcoming meeting context
- Request involves practicing answers, researching a company, or building a question bank
- User asks for STAR-format response help or follow-up email templates

Do NOT activate for resume writing (cv-enhancement), salary negotiation strategy, or job search planning (those are separate skills).

## 1. Context Analysis and Role Mapping

Extract and organize from the user's input:

| Field               | Source           | Evidence Tag |
|---------------------|------------------|--------------|
| Role title          | Job posting/user | [EXPLICIT]   |
| Company name        | Job posting/user | [EXPLICIT]   |
| Interview type      | User/inferred    | [EXPLICIT] or [INFERRED] |
| Key requirements    | Job posting      | [EXPLICIT]   |
| Nice-to-haves       | Job posting      | [EXPLICIT]   |
| Culture signals     | Job posting/web  | [INFERRED]   |
| Interviewer details | User provided    | [EXPLICIT] or [OPEN] |

### Role-Requirement Alignment Matrix

Map the candidate's likely strengths to each listed requirement:

| Requirement              | Candidate Evidence Point    | Confidence | Gap? |
|--------------------------|-----------------------------|------------|------|
| 5+ years experience      | Specific role/project       | High/Med/Low | Y/N |
| Leadership experience    | Team size, scope            | --         | --   |
| Technical skill X        | Project, certification      | --         | --   |

Flag gaps explicitly — these become areas for proactive framing in answers.

## 2. Question Bank by Category

### Behavioral Questions (8-10)

Questions probing past behavior as predictor of future performance:
- "Tell me about a time you handled conflict in a team."
- "Describe a situation where you failed and what you learned."
- "Give an example of leading a project under tight deadlines."

For each question, provide:
- Why interviewers ask it (the competency being tested)
- STAR scaffold (Situation, Task, Action, Result) with prompts
- Common pitfalls to avoid

### Technical/Domain Questions (6-8)

Role-specific knowledge and problem-solving:
- Tailored to the job posting requirements
- Include both knowledge-check and scenario-based formats
- Note which requirements each question maps to

### Situational/Hypothetical Questions (4-6)

Forward-looking scenarios:
- "How would you approach X if you joined tomorrow?"
- "What would you prioritize in your first 90 days?"
- Encourage structured thinking frameworks (prioritization matrices, stakeholder analysis)

### Questions to Ask the Interviewer (5-7)

Strategic questions that demonstrate preparation and genuine interest:
- About the team structure and dynamics
- About success metrics for the role
- About current challenges the team faces
- About growth and development opportunities
- Avoid questions easily answered by the company website

## 3. STAR Response Framework

For the top 5 most likely questions, build complete STAR scaffolds:

```
Question: [specific question]
Competency tested: [what they are evaluating]

S — Situation: [context setting, 1-2 sentences]
T — Task: [your specific responsibility]
A — Action: [what YOU did, step by step — this is the longest section]
R — Result: [quantified outcome + lesson learned]

Transition: [how this connects to the role you are interviewing for]
```

Rules for STAR responses:
- Action section must use first person singular ("I did"), not "we"
- Results must include at least one metric or concrete outcome
- Total response target: 90-120 seconds when spoken
- Each response should map to a different competency

## 4. Company Research Checklist and Follow-Up

### Pre-Interview Research Checklist

- [ ] Company mission, vision, and values — memorize the key phrases
- [ ] Recent news: funding rounds, product launches, leadership changes (last 6 months)
- [ ] Competitor landscape: who are the top 3 competitors and how does this company differentiate
- [ ] Interviewer background: LinkedIn profile, recent posts, shared connections
- [ ] Company culture signals: Glassdoor themes, social media tone, office/remote policy
- [ ] Financial health: public filings or known funding stage
- [ ] Industry trends affecting the company right now

### Post-Interview Follow-Up Templates

**Thank-you email** (send within 24 hours):
- Reference a specific conversation point from the interview
- Reinforce fit for one key requirement discussed
- Express enthusiasm without desperation
- Keep under 150 words

**Follow-up after no response** (send after 5-7 business days):
- Brief, professional, forward-looking
- Add new value (share a relevant article or insight)
- Keep under 100 words

## Trade-off Matrix

| Decision                    | Option A                | Option B                | Recommendation          |
|-----------------------------|-------------------------|-------------------------|-------------------------|
| Preparation depth           | Cover all question types| Deep-dive on top 5      | Deep-dive — mastery beats breadth |
| Response style              | Scripted answers        | Bullet-point scaffolds  | Scaffolds — sound natural, not rehearsed |
| Company research scope      | Exhaustive              | Focused on role context | Focused — show targeted knowledge |
| Questions to ask            | Many prepared           | 3-4 strong ones         | 3-4 strong — quality signals preparation |
| Mock practice               | Solo rehearsal          | With a partner          | Partner preferred — feedback loop matters |

## Assumptions and Limits

- Assumes the user provides the job posting or role description; quality degrades without it [EXPLICIT]
- Company research is based on publicly available information unless user provides internal context [INFERRED]
- STAR responses are scaffolds, not verbatim scripts — user must personalize with real experiences [EXPLICIT]
- Does not simulate a live mock interview with real-time feedback (that requires interactive session) [EXPLICIT]
- Interview norms may vary by culture and region; defaults to North American/European professional standards [INFERRED]

## Edge Cases

1. **No job posting available** — Work from role title + company name only. Generate likely requirements from industry norms. Tag all inferences as `[INFERRED]` and flag lower confidence.
2. **Client discovery call (not job interview)** — Shift from "proving fit" to "understanding needs." Replace STAR with SPIN (Situation, Problem, Implication, Need-Payoff) framework. Adjust question bank to discovery-oriented probes.
3. **Panel interview with multiple interviewers** — Add section on managing multi-person dynamics: eye contact rotation, addressing the question-asker then the group, noting each interviewer's likely focus area based on their role.
4. **Internal promotion interview** — Adjust framing: leverage institutional knowledge as a strength, address "fresh perspective" concern proactively, reference internal metrics and relationships.
5. **Second/final round interview** — Include a section on building on first-round themes, escalating depth of responses, and preparing for culture-fit or executive-level questions.

## Good vs Bad Example

### Good
```
Role: Senior Product Manager at Acme Corp
Interview type: Behavioral + Case Study (Round 2)

Question: "Tell me about a time you had to make a product decision with incomplete data."
Competency: Decision-making under ambiguity

S — Led pricing redesign for SaaS platform serving 2,000 customers.
T — Had to decide between usage-based and tier-based model with only 60% of customer data analyzed.
A — Built a lightweight conjoint survey for top 50 accounts, ran 2-week pilot with both models on a cohort, synthesized directional signals.
R — Tier-based model won with 23% higher expansion revenue in pilot. Shipped to all customers, validated at scale within 90 days.
Transition — Acme's product decisions likely require similar speed-vs-rigor tradeoffs given your growth stage.

Evidence: [EXPLICIT] from job posting emphasis on "data-informed but action-oriented"
```

### Bad
```
Question: Tell me about yourself.
Answer: I have 10 years of experience and am passionate about products.
(No structure, no specifics, no connection to role, no evidence tag)
```

## Validation Gate

Before delivering the prep document, confirm every item:

- [ ] Context analysis completed with role, company, and interview type identified
- [ ] Role-requirement alignment matrix filled with gap identification
- [ ] Behavioral question bank of 8+ questions with competency labels
- [ ] Technical/domain question bank of 6+ questions mapped to requirements
- [ ] STAR scaffolds built for top 5 most likely questions
- [ ] Company research checklist populated with actionable items
- [ ] Questions to ask the interviewer (5+) that demonstrate preparation
- [ ] Follow-up email templates included (thank-you + no-response)
- [ ] Every inference tagged with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`
- [ ] Edge cases reviewed against user context (interview type, round, format)

## Reference Files

| File | Purpose |
|------|---------|
| `references/star-framework.md` | STAR method deep-dive with anti-patterns and timing guide |
| `references/question-banks.md` | Master question bank by competency category and seniority level |
| `references/followup-templates.md` | Email templates for thank-you, follow-up, and rejection response |
