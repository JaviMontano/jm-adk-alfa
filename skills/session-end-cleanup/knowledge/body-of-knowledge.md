# Session End Cleanup - Body of Knowledge

## Purpose

Session closeout is a handoff discipline. It turns an agent session into a
bounded record of evidence, outcomes, open work, and next action so the next
session can resume without relying on hidden conversation memory.

## Core Concepts

| Concept | Definition | Required Handling |
|---|---|---|
| Session summary | Short account of the objective and final state | Must include active scope and status |
| Change record | Files, docs, commands, PRs, or artifacts changed | Must separate completed and proposed work |
| Validation evidence | Commands, local checks, CI, PR, or merge proof | Must name exact source and status |
| Durable update | Tasklog or changelog write intended to survive sessions | Must be authorized and scoped |
| Next handoff | First concrete action for the next session | Must be actionable without full transcript |
| Guardian decision | Final pass/block decision | Must name missing evidence when blocked |

## Evidence Rules

- Use `[CODE]` for local files, diffs, commands, PR/CI output, or script output.
- Use `[CONFIG]` for user instructions, repo policy, workflow rules, or branch
  criteria.
- Use `[DOC]` for documentation or review artifacts.
- Use `[INFERENCE]` for reasoned conclusions from evidence.
- Use `[ASSUMPTION]` for unstated or unverified context.

## Anti-Patterns

- Claiming CI green before a PR check exists.
- Marking a task complete because the intended change was planned.
- Hiding failed validation under a generic risk note.
- Updating every tasklog/changelog entry instead of the active row or entry.
- Producing only a summary and omitting next handoff.
- Using wall-clock, network, or random inputs in local closeout validation.

## Deterministic Quality Metrics

| Metric | Target | How To Measure |
|---|---:|---|
| Required section coverage | 100% | Output has all contract sections |
| Evidence tag coverage | 100% | Validator or guardian review finds no untagged factual entries |
| Validation visibility | 100% | Every required command has status and evidence |
| Durable update containment | 100% | Only authorized tasklog/changelog target is written |
| Handoff actionability | 1 first action | Next Handoff names a concrete next step |

## Failure Modes

- Missing evidence: mark `[ASSUMPTION]` or `[OPEN]` and block completion if the
  missing proof affects final status.
- Conflicting evidence: preserve both claims and require owner or CI resolution.
- Unrelated local changes: pause before writing durable logs.
- Long sessions: compress details by outcome, not chronology.
