---
name: meeting-notes
description: >
  Triggers on "meeting notes", "meeting minutes", "acta de reunion", "notas de la reunion".
  Produces structured meeting minutes with attendees, agenda, discussion summary, decisions,
  and action items with owners and due dates. Output: markdown document plus optional branded
  HTML version. [EXPLICIT]
argument-hint: "meeting transcript, agenda, attendee list, date, or raw notes"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Meeting Notes

> TL;DR — Transforms raw meeting input (transcript, rough notes, agenda) into structured
> minutes covering metadata, attendees, agenda items, discussion summaries, decisions log,
> and action items with assigned owners and deadlines. Outputs markdown and optionally a
> branded HTML document ready for distribution.

---

## When to Activate

| Signal | Example |
|--------|---------|
| Direct request | "Write up meeting notes from this transcript" |
| Minutes formatting | "Format these as meeting minutes" |
| Spanish variant | "Redacta el acta de la reunion de hoy" |
| Post-meeting context | "Here are my rough notes from the standup" |
| Action item extraction | "Pull out the action items from this meeting" |

Activate when the user provides meeting content (transcript, notes, agenda) and needs
structured documentation. Do NOT activate for meeting planning (use `workshop-facilitator`)
or retrospective facilitation (use `retrospective-facilitation`).

---

## S1 — Input Processing & Metadata Extraction

### Accepted Input Formats

| Format | Processing |
|--------|-----------|
| Raw transcript | NLP extraction of speakers, topics, decisions |
| Bullet-point notes | Structure into agenda-aligned sections |
| Audio transcript paste | Clean filler words, attribute speakers |
| Agenda + outcomes | Map outcomes to each agenda item |
| Mixed / chaotic notes | Identify threads, group by topic |

### Metadata Block

Extract or ask for:

```markdown
## Meeting Metadata
- **Title**: [Meeting name]
- **Date**: [YYYY-MM-DD]
- **Time**: [HH:MM - HH:MM] [Timezone]
- **Location**: [Room / Video link]
- **Facilitator**: [Name]
- **Note-taker**: [Name or "AI-assisted"]
- **Attendees**: [Name (Role)] per person
- **Absent**: [Name (Role)] if applicable
```

If the user omits metadata fields, mark them `[NOT PROVIDED]` rather than guessing.

---

## S2 — Discussion Summary & Decision Log

### Discussion Summary Structure

For each agenda item:

```markdown
### [Agenda Item Title]

**Context**: Brief background (1-2 sentences).

**Discussion**:
- [Speaker] raised [point]. [Supporting detail].
- [Speaker] countered with [alternative view].
- Group consensus: [outcome summary].

**Status**: Resolved | Deferred | Escalated
```

Rules:
- Attribute statements to speakers when identifiable.
- Maintain neutral tone — do not editorialize or interpret intent.
- Summarize, do not transcribe verbatim (respect copyright and brevity).
- Flag unresolved disagreements explicitly.

### Decision Log

| ID | Decision | Rationale | Owner | Date |
|----|----------|-----------|-------|------|
| D1 | Adopt serverless for MVP | Cost reduction + faster iteration | CTO | 2026-03-27 |
| D2 | Delay mobile app to Q3 | Resource constraints | PM | 2026-03-27 |

Each decision gets a unique ID for traceability across future meetings.

---

## S3 — Action Items & Follow-up

### Action Item Format

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| A1 | Draft serverless architecture proposal | Maria R. | 2026-04-03 | High | Open |
| A2 | Schedule user testing sessions | Carlos P. | 2026-04-10 | Medium | Open |
| A3 | Review vendor contracts | Legal team | 2026-04-07 | High | Open |

Rules:
- Every action item must have an **owner** (person, not team, when possible).
- Every action item must have a **due date** (if not stated, suggest one and mark `[SUGGESTED]`).
- Priority levels: High, Medium, Low.
- Status on creation is always "Open".
- Actions without clear owners are flagged: `[OWNER NEEDED]`.

### Follow-up Section

```markdown
## Next Meeting
- **Date**: [Next meeting date or cadence]
- **Carry-over items**: [List deferred agenda items]
- **Pre-read**: [Documents to review before next meeting]
```

---

## S4 — Output Formatting & Distribution

### Markdown Output (Default)

Clean markdown file following the structure:
1. Metadata block
2. Attendees table
3. Agenda items with discussion summaries
4. Decision log table
5. Action items table
6. Follow-up / next meeting

Filename convention: `YYYY-MM-DD_meeting-title.md`

### Branded HTML Output (Optional)

When the user requests HTML output or distribution-ready format:

- **Brand tokens**: navy #122562 background header, gold #FFD700 accent on decision badges,
  blue #137DC5 for links and action item highlights.
- **Typography**: Poppins 600 for section headings, Inter 400 for body.
- **Layout**: dark header with meeting title and date, light body for readability,
  action items in a highlighted card section.
- **Print styles**: clean black-on-white with visible table borders.
- **Self-contained**: single HTML file, no external dependencies beyond Google Fonts.

### Distribution Checklist

- [ ] Review for sensitive information before sharing externally.
- [ ] Confirm all attendee names are spelled correctly.
- [ ] Verify action item owners have been notified.
- [ ] Attach to calendar invite for the next meeting.

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Detail level | Verbatim transcript | Executive summary | Summary with key quotes |
| Attribution | Name every speaker | Anonymize discussion | Attribute when relevant |
| Format | Markdown only | Markdown + HTML | Both — markdown for archive, HTML for distribution |
| Action item dates | Only stated dates | Suggest dates for undated items | Suggest with [SUGGESTED] tag |
| Language | Single language | Bilingual ES/EN | Match meeting language; bilingual if mixed |

---

## Assumptions & Limits

- Assumes the user provides accurate input; the skill does not verify claims made in meetings. [EXPLICIT]
- Does not record, transcribe, or access audio/video — works from provided text only. [EXPLICIT]
- Speaker attribution accuracy depends on input quality; ambiguous speakers are marked
  `[SPEAKER UNCLEAR]`. [INFERRED]
- Does not send emails, calendar invites, or notifications to attendees. [EXPLICIT]
- Decision IDs and action item IDs are session-scoped; cross-meeting tracking requires
  external tooling. [INFERRED]

---

## Edge Cases

1. **Transcript with no clear agenda** — Infer topic clusters from discussion flow; present
   as "Discussion Topics" rather than "Agenda Items" and note that no formal agenda was provided.
2. **Meeting with no decisions or action items** — Explicitly state "No decisions were recorded"
   and "No action items were identified" rather than omitting the sections.
3. **Highly technical meeting with jargon** — Preserve technical terms exactly as stated;
   add a glossary section at the end if 5+ specialized terms appear.
4. **Multilingual meeting (mixed ES/EN)** — Write notes in the dominant language; include
   key terms in both languages where they first appear: "sprint planning (planificacion de sprint)".

---

## Good vs Bad Example

### Good

```markdown
### API Migration Timeline

**Context**: Team needs to migrate from REST v2 to GraphQL before Q3 launch.

**Discussion**:
- Maria proposed a phased migration starting with read-only endpoints.
- Carlos raised concerns about client SDK compatibility.
- Group agreed on a 3-phase approach with a compatibility layer.

**Status**: Resolved

| ID | Decision | Owner | Date |
|----|----------|-------|------|
| D1 | Phased migration with compatibility layer | Maria R. | 2026-03-27 |

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| A1 | Draft migration RFC | Maria R. | 2026-04-03 | High | Open |
| A2 | Audit client SDK dependencies | Carlos P. | 2026-04-01 | High | Open |
```

Why it works: clear context, attributed discussion, linked decision and actions, dates assigned.

### Bad

```markdown
## Meeting Notes

We talked about the API migration. Some people think we should do GraphQL.
There was some disagreement. We decided to move forward.

TODO: someone should write something up about this.
```

Why it fails: no attribution, no decision detail, vague action item with no owner or date.

---

## Validation Gate

Before delivering the final meeting notes, confirm every item:

- [ ] Metadata block includes date, time, attendees, and facilitator (or marked [NOT PROVIDED])
- [ ] Each agenda/discussion item has context, discussion summary, and status
- [ ] Decision log uses unique IDs with rationale and owner columns
- [ ] Every action item has an assigned owner (person name, not team)
- [ ] Every action item has a due date (actual or [SUGGESTED])
- [ ] Speaker attribution is present where identifiable
- [ ] No editorializing or interpreting speaker intent
- [ ] Unresolved items are explicitly marked as Deferred or Escalated
- [ ] HTML output (if requested) uses brand colors #122562, #FFD700, #137DC5
- [ ] Follow-up section includes next meeting date and carry-over items

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/minutes-template.md` | Standard meeting minutes markdown template |
| `references/action-item-patterns.md` | Action item writing patterns with examples |
| `references/html-minutes-template.html` | Branded HTML template for distribution |
| `references/decision-log-schema.md` | Decision log format and cross-meeting tracking |
