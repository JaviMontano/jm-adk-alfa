---
name: assembly-skill
version: 1.0.0
description: "Use when the user asks to run the full skill quality pipeline, improve a skill end to end, take a skill to production, run x-ray plus surgeon plus certify, or assembly-line one skill. Orchestrates one target skill through deterministic diagnostic, intervention, certification, and optional trigger optimization gates."
argument-hint: "path-to-skill [--mode quick|standard|deep]"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---
# Skill Assembly Line

Run the skill-quality pipeline for exactly one target skill: Phase A diagnostic, Phase B intervention, Phase C certification, optional Phase C+ trigger optimization, and Phase D report.

## When to Activate

Activate when the user asks to:

- run the full skill pipeline
- improve this skill end to end
- take this skill to production
- run x-ray -> surgeon -> certify
- assembly-line a skill
- make one skill production-ready without separately invoking each phase

Do not activate for general "assembly" work such as assembling a deck, product, CI pipeline, package, or document bundle.

## Deterministic Contract

- Scope is one target skill directory. Never process multiple skills in one run.
- Read `assets/mode-policy.json` before selecting a mode.
- Read `assets/assembly-report-contract.json` before producing the final report.
- Use `assets/assembly-report-template.md` for report shape.
- Run `scripts/validate_assembly_contract.py` against any final report before delivery.
- Use caller-supplied elapsed buckets or `not-measured`; do not derive durations from wall-clock time.
- Use only fixed trigger-query fixtures for deep mode, or record generated query sets before scoring.
- Do not modify files before Gate B approval is explicit.

## Required Inputs

1. Exactly one target skill path.
2. Mode: `quick`, `standard`, `deep`, or absent for deterministic auto-selection.
3. User intent: diagnostic-only, improve, certify, or optimize triggers.
4. Write approval for Phase B if files may change.

If the target path is missing, multiple skill paths are supplied, or `SKILL.md` is absent, return `BLOCKED` and do not proceed.

## Modes

| Mode | Phases | Writes | Use |
|---|---|---|---|
| quick | A + D | No | Diagnostic snapshot only |
| standard | A + B + C + D | After Gate B | Production-readiness repair |
| deep | A + B + C + C+ + re-certify + D | After Gate B | Trigger optimization after structural repair |

## Auto-Selection

Use the Phase A scorecard as the only score source:

| Condition | Mode |
|---|---|
| score < 5 | standard |
| score >= 5 and score < 7 | standard |
| score >= 7 and score < 8 | deep |
| score >= 8 and gate 13/13 and user did not request changes | quick |
| score >= 8 and user requested changes | standard |

If context pressure is high, fall back to `standard` and report the fallback.

## Phase Protocol

### Phase A: Diagnostic

Apply `x-ray-skill` logic to produce a scorecard, gate count, top gaps, and recommended mode. If Phase A cannot run, report `BLOCKED`.

### Gate A: Intervention Decision

Skip intervention only when auto-selection returns `quick` and the user did not ask for changes.

### Phase B: Intervention

Apply `surgeon-skill` logic only after Gate B approval. Present the intervention plan first:

```markdown
Assembly Line Intervention Plan
Target: {skill}
Current score: {score}
Projected score: {score}
Interventions: {count}
Gate B: approve / trim / reject
```

If Gate B is rejected, stop writes and produce a diagnostic-only report.

### Phase C: Certification

Apply `certify-skill` logic to the post-intervention state. The final verdict must come from certification evidence, not from wording.

### Phase C+: Trigger Optimization

Deep mode only. Apply `trigger-skill` logic with a recorded query set, then re-certify. If trigger optimization degrades certification, report `CONDITIONAL` or `BLOCKED`.

### Phase D: Assembly Report

Use `assets/assembly-report-template.md`. The report must include:

- target skill
- mode
- result
- phase evidence
- before/after score and gate delta
- Gate B status
- certification formula source
- every modified file, or `No files modified`
- specific next step

## Validation Gate

- [ ] `scripts/validate_assembly_contract.py` passes for the final report.
- [ ] Mode selection follows `assets/mode-policy.json`.
- [ ] Gate B approval appears before any write action.
- [ ] Quick mode is read-only and does not claim `CERTIFIED`.
- [ ] Standard/deep modes include Phase B and Phase C evidence.
- [ ] Deep mode includes Phase C+ trigger metrics and re-certification.
- [ ] Missing target path or missing `SKILL.md` fails closed.
- [ ] The final report uses `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` evidence tags.

## Reference Files

| File | Load When |
|---|---|
| `assets/mode-policy.json` | Always, before mode selection |
| `assets/assembly-report-contract.json` | Always, before reporting |
| `references/pipeline-modes.md` | When explaining mode behavior |
