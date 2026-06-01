---
name: follow-up-email
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Generates personalized follow-up emails after meetings or events, extracting
  action items and sending individualized messages to each responsible party. [EXPLICIT]
  Trigger: "follow up", "seguimiento", "send follow-up", "action items email"
status: production
tags: [email, follow-up, meetings, automation, office]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__send_gmail_message
  - mcp__workspace-mcp__draft_gmail_message
  - mcp__workspace-mcp__search_gmail_messages
  - mcp__workspace-mcp__manage_event
---

# Follow-Up Email Generator

Generates personalized follow-up emails after meetings or events. Extracts action items from meeting notes and sends individualized messages to each responsible party with only their relevant tasks, deadlines, and context. [EXPLICIT]

## When to Activate

This skill activates when the user: [EXPLICIT]
- Requests follow-up emails after a meeting or event
- Wants to distribute action items to attendees
- Says "seguimiento", "follow up", "send action items", "meeting recap"
- Provides meeting notes and asks to notify participants
- Needs reminders created for upcoming deadlines from a meeting

## Execution Flow

### Step 1: Extract Action Items from Meeting Notes

Parse the meeting notes (provided as text, file, or document link) to identify: [EXPLICIT]

1. **Meeting metadata**: title, date, location, duration
2. **Attendees**: name, email, role/title (if available)
3. **Action items**: task description, assignee, deadline, priority, context
4. **Decisions made**: key agreements that provide context for action items
5. **Next meeting**: date/time if scheduled

**Parsing rules:**
- Look for patterns: "ACTION:", "TODO:", "- [ ]", "@name will...", "name se encarga de..."
- Associate deadlines with tasks: "para el viernes", "by Friday", "deadline: 2026-04-10"
- When assignee is ambiguous, flag for user confirmation before sending
- Group items by person for individualized emails

### Step 2: Generate Personalized Emails Per Person

For each attendee with action items: [EXPLICIT]

1. Use the `templates/follow-up-action-items.md` template
2. Use `assets/email-copy-tokens.json` for default subject, sign-off, tone, and draft-first policy
3. Use `scripts/render-follow-up-email.py --data <meeting.json> --recipient <email>` when the meeting notes have been normalized into JSON
4. Include ONLY that person's action items (never leak others' tasks)
5. Add relevant context from meeting decisions that affect their tasks
6. Include next steps that apply to everyone
7. Set appropriate tone: professional but warm, action-oriented

**Personalization rules:**
- Address by first name
- Reference their specific contributions from the meeting
- Order action items by deadline (earliest first)
- Flag high-priority items with bold formatting
- Include meeting title and date for reference

### Step 3: Optionally Create Calendar Reminders

When deadlines are identified: [EXPLICIT]

1. Ask user if they want calendar events created for deadlines
2. Use `mcp__workspace-mcp__manage_event` to create reminders
3. Set reminder 24h before each deadline
4. Include action item description in event body
5. Invite the responsible person

### Step 4: Send or Draft for Review

Default behavior: **draft first, send after user approval.** [EXPLICIT]

1. Use `mcp__workspace-mcp__draft_gmail_message` to create drafts
2. Present summary: who gets what, how many items per person
3. On user approval, use `mcp__workspace-mcp__send_gmail_message` to send
4. Log sent emails with timestamps

**Safety rules:**
- NEVER auto-send without explicit user confirmation
- Show preview of each email before sending
- Allow user to edit individual emails before sending
- If no email address found for an attendee, flag and skip

## Quality Criteria

| Criterion | Requirement |
|-----------|-------------|
| Completeness | Every action item from notes appears in exactly one email |
| Accuracy | Correct assignee for each task, correct deadlines |
| Privacy | No person sees another person's action items |
| Tone | Professional, warm, actionable — not robotic |
| Timing | Follow-up sent within 24h of meeting (best practice) |
| Template | Uses branded template consistently |
| Confirmation | User approves before any email is sent |
| Assets | `assets/manifest.json` declares every reusable output asset |
| Determinism | Scripted rendering is one-recipient-at-a-time and privacy tested |

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Sending all action items to everyone | Personalize: each person gets only their items |
| Auto-sending without review | Always draft first, send after approval |
| Vague action items ("handle the thing") | Preserve original specificity from notes; flag vague items |
| Missing deadlines | If no deadline specified, flag and ask user |
| Generic greeting ("Dear team member") | Use attendee's actual first name |
| Ignoring meeting context | Include relevant decisions that affect each task |
| Sending to people with no action items | Skip attendees with zero items (or send optional summary-only) |

## Agent Composition

| Agent | Role |
|-------|------|
| Lead | Parses meeting notes, extracts action items, generates email content |
| Support | Formats emails, applies templates, handles calendar event creation |
| Guardian | Validates completeness (all items assigned), privacy (no cross-leak), tone |
| Specialist | Email deliverability, personalization optimization, multi-language support |

## Example Input

```
Meeting: Q2 Planning - April 1, 2026
Attendees: Ana (ana@company.com), Carlos (carlos@company.com), Maria (maria@company.com)

Decisions:
- Budget approved for new marketing campaign
- Launch date set for May 15

Action items:
- Ana: Prepare campaign brief by April 8
- Carlos: Set up analytics dashboard by April 10
- Carlos: Review vendor proposals by April 5
- Maria: Schedule kickoff with design team by April 4
- Maria: Draft social media calendar by April 12
```

## Example Output

Three personalized emails, each containing only the recipient's items, with meeting context and next steps.

## Deterministic Script Contract

- Runtime script: `scripts/render-follow-up-email.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill follow-up-email`
- Default behavior: render to stdout; write files only with `--output`.
- Safety boundary: scripts render drafts only; they never send email.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every asset and where it is used.
- `assets/email-style.css` styles HTML previews.
- `assets/email-copy-tokens.json` carries subject, sign-off, tone, and draft-first policy defaults.
