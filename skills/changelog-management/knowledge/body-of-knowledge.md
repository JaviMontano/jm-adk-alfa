# Changelog Management — Body of Knowledge

## Canon

`changelog.md` is the durable continuity record for material project events. It
is not a task tracker and not a general release-notes generator. It should help
a future session answer what changed, why it mattered, and where evidence lives.

## Entry Types

| Type | Use For | Required Evidence |
|---|---|---|
| `decision` | Durable choice or policy. | rationale and decision source |
| `completion` | Finished work. | validation, PR, task, or review evidence |
| `amendment` | Governance or protocol update. | changed contract/source |
| `insight` | Reusable learning. | source or observation path |
| `blocker` | Condition preventing progress. | blocking condition and owner/next action |
| `discovery` | Newly found relevant fact. | source reference |

## Ordering

Date sections use `YYYY-MM-DD` and newest-first order. Entry dates come from
explicit `as_of_date`, not hidden system time. Existing date sections are reused.

## Duplicate Control

Before append, compute a fingerprint from date, type, normalized description, and
evidence refs. Known duplicates must be skipped or revised; they must not be
appended.

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| Type validity | 100% | Entry type is allowed. |
| Evidence coverage | 100% | Rationale, principles, and evidence refs are present. |
| Duplicate safety | 100% | Duplicate review blocks duplicate append. |
| Ordering safety | 100% | Newest-first date order is preserved. |
| Offline validation | 100% | `bash skills/changelog-management/scripts/check.sh` passes. |

## Anti-Patterns

- Logging task status that belongs only in `tasklog.md`.
- Appending duplicates because the wording changed slightly.
- Using a future date or hidden clock.
- Omitting rationale, principles, or evidence.
- Treating public product release notes as repository continuity entries.
