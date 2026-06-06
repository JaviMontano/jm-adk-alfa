---
name: changelog-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Maintain changelog.md with semantic entries for decisions, completions, amendments,
  insights, blockers, and discoveries. Cross-session continuity log. [EXPLICIT]
  Trigger: "changelog", "log decision", "record change", "what happened", "session log"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Changelog Management

> "If it's not logged, it didn't happen."

## Purpose

Maintains `changelog.md` as the cross-session continuity log. It records
significant decisions, completions, amendments, insights, blockers, and
discoveries with date, type, description, rationale, principle references, and
evidence. Entry dates use an explicit `as_of_date`; the skill does not rely on a
hidden system clock. [EXPLICIT]

## When to Activate

- The user asks to update `changelog.md`, log a decision, record a change, record
  what happened, capture a blocker, or summarize session history.
- A session closeout or session protocol step needs a continuity entry.
- A material task completion, governance amendment, insight, blocker, or
  discovery needs durable context for future sessions.

Do not activate for unrelated software release notes, public product changelogs,
or "what changed" questions that do not require this repository's `changelog.md`.

---

## Deterministic Resources

- `assets/changelog-contract.json` defines required report fields and evidence tags.
- `assets/entry-type-policy.json` defines allowed entry types and required fields.
- `assets/ordering-policy.json` defines date sections, newest-first order, and
  explicit `as_of_date`.
- `assets/dedupe-policy.json` defines duplicate detection and skip/revise actions.
- `assets/evidence-policy.json` defines rationale, principle, and evidence
  requirements.
- `scripts/validate_changelog_report.py` validates update reports offline.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

---

## Procedure

### Step 1: Discover

1. Read `changelog.md` or mark it missing.
2. Load the five most recent entries when present.
3. Identify the event to log: `decision`, `completion`, `amendment`, `insight`,
   `blocker`, or `discovery`.
4. Record `as_of_date` as `YYYY-MM-DD`; if unavailable, mark entry date as
   `[OPEN]` and do not write.

### Step 2: Analyze

1. Classify the event using `assets/entry-type-policy.json`.
2. Draft a self-sufficient description and rationale.
3. Attach at least one principle reference.
4. Attach at least one local evidence reference, such as PR, validation command,
   review doc, task ID, decision log, or source file.
5. Compute a duplicate fingerprint from date, type, normalized description, and
   evidence references.
6. Check ordering: newest date sections remain at top; existing date section is
   reused when present.

### Step 3: Execute

Allowed writes:

- create `changelog.md` when missing and authorized
- append a new entry under the explicit `as_of_date`
- revise a draft entry only when duplicate review recommends revision

Rules:

- Do not append duplicate entries.
- Do not use dates after `as_of_date`.
- Do not write entries without rationale, principle references, and evidence.
- Do not invent constitutional principles or evidence references.

### Step 4: Validate

- Entry type is allowed.
- Date is `YYYY-MM-DD` and not after `as_of_date`.
- Description and rationale are non-empty.
- Principle references and evidence references are non-empty.
- Duplicate review does not append known duplicates.
- Changelog ordering remains newest-first.
- Machine reports pass `bash skills/changelog-management/scripts/check.sh`.

## Entry Contract

```markdown
## 2026-06-06
- **[decision]**: Keep tasklog stale review approval-gated — prevents automatic closure of stale tasks. [Principle VII] Evidence: PR #78; docs/audits/skills/tasklog-management-review.md
```

## Quality Criteria

- [ ] `changelog.md` was read or missing state was reported.
- [ ] Entry type is one of the six allowed types.
- [ ] Entry date is explicit and valid.
- [ ] Entry description is concise and self-sufficient.
- [ ] Rationale explains why the event matters.
- [ ] Principle references are present and evidence-backed.
- [ ] Evidence references are local or repository-verifiable.
- [ ] Duplicate review was performed before append.
- [ ] Ordering remains newest-first.
- [ ] Validator fixtures pass and unsafe reports fail.

## Related Skills

- `session-protocol` — Reads changelog during state recovery.
- `session-end-cleanup` — Proposes changelog update plans.
- `tasklog-management` — Tracks actionable task state separately.
- `continuous-learning` — Can promote stable insights from changelog entries.

## Usage

Example invocations:

- `/changelog-management`
- `Log the decision from PR #78 as of 2026-06-06.`
- `Record a blocker in changelog.md but do not append duplicates.`

## Assumptions & Limits

- Assumes local access to `changelog.md` and evidence references. [EXPLICIT]
- Does not use network calls, randomness, or hidden system time for validation. [EXPLICIT]
- Does not replace owner approval for governance amendments. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Missing `changelog.md` | Report missing; create only when authorized. |
| Duplicate entry | Skip or revise; do not append duplicate. |
| Future date | Block write and request correct `as_of_date`. |
| Missing rationale or evidence | Block write and request missing fields. |
| Unsupported type | Block write and map to an allowed type. |
