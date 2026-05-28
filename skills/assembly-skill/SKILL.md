---
name: assembly-skill
description: 
  This skill should be used when the user asks to "run the full skill
  pipeline", "improve this skill end to end", "take this skill to
  production", "one-command skill upgrade", or "assembly line this skill". [EXPLICIT]
  Orchestrates the complete skill quality pipeline — from diagnostic
  through intervention to certification — in a single invocation with
  configurable depth. Use this skill whenever someone wants the full
  x-ray → surgeon → certify workflow without running each skill
  separately, or when they say "make this skill great" without
  specifying which step to run. [EXPLICIT]
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
  - Agent
model: opus
version: 1.0.0
---

# Skill Assembly Line

One-command skill engineering pipeline. Runs diagnostic → intervention → certification in sequence, adapting depth to the skill's current state — so a single invocation takes a skill from whatever state it's in to production-certified. [EXPLICIT]

## Why This Exists

Running x-ray-skill, surgeon-skill, and certify-skill separately requires 3 invocations, manual handoff between steps, and context switching. The assembly line eliminates that friction: one command, one report, one result. [EXPLICIT]

The trade-off: less granular control than running each skill individually. Use individual skills when you want to inspect or approve each phase. Use assembly-skill when you trust the pipeline and want results. [EXPLICIT]

## Usage

```
/assembly-skill /path/to/skill                    # standard mode (default)
/assembly-skill /path/to/skill --mode quick        # diagnostic only
/assembly-skill /path/to/skill --mode deep         # full pipeline + trigger optimization
```

## Pipeline Modes

| Mode | Phases | Time | When to Use |
|------|--------|------|-------------|
| **quick** | X-Ray only | 3-5 min | "What's the state of this skill?" — diagnostic, no changes |
| **standard** | X-Ray → Surgeon → Certify | 10-20 min | "Make this skill production-ready" — the default |
| **deep** | X-Ray → Surgeon → Certify → Trigger optimization → Re-certify | 20-40 min | "Make this skill excellent" — includes description optimization |

### Mode Selection Logic

If no mode specified, auto-select based on initial assessment: [EXPLICIT]

| Initial State | Auto-Selected Mode | Reasoning |
|--------------|-------------------|-----------|
| Score < 5 (BLOCKED) | standard | Needs structural work before optimization makes sense |
| Score 5-7 (needs work) | standard | Infrastructure + content fixes are the priority |
| Score 7-8 (polish) | deep | Structure is solid; trigger optimization has highest marginal value |
| Score 8+ (minor tweaks) | quick | Already strong; report the state, don't over-intervene |

## The Assembly Process

### Phase A: Diagnostic (all modes)

Run x-ray-skill internally. Produce the full scorecard: [EXPLICIT]
- Inventory all files
- Validate frontmatter
- Audit body sections
- Score 10 rubric dimensions
- Run 13-point gate
- Check systemic coherence

**Gate A:** If score >= 8 and gate passes 13/13, skip to Phase D (certification). No intervention needed.

**Output:** X-Ray scorecard (kept as internal artifact for Phase B).

### Phase B: Intervention (standard + deep modes)

Run surgeon-skill internally using Phase A's scorecard: [EXPLICIT]
- Select applicable improvement patterns based on gap analysis
- Present the plan to the user:

```
Assembly Line — Intervention Plan: [EXPLICIT]
Score: {current}/10 → projected {projected}/10 [EXPLICIT]
Interventions: {N} across {M} layers [EXPLICIT]
{numbered list with pattern IDs and descriptions}
Proceed? [Y/n]
```

**Gate B:** Wait for user confirmation before modifying files. The assembly line automates sequencing, not decision-making.

After confirmation, execute all interventions with snapshot-verify-document protocol. [EXPLICIT]

### Phase C: Certification (standard + deep modes)

Run certify-skill internally on the improved skill: [EXPLICIT]
- All structural checks
- All content checks
- Rubric re-scoring
- Produce certification verdict

**Gate C:** If CERTIFIED, proceed to Phase D (report) or Phase C+ (if deep mode). If CONDITIONAL or BLOCKED, report the remaining issues.

### Phase C+ : Trigger Optimization (deep mode only)

Run trigger-skill internally to optimize the description: [EXPLICIT]
- Generate 15-20 test queries (should-trigger + should-not-trigger)
- Test triggering accuracy
- Iterate on description (up to 3 iterations)
- Produce optimized description

Then re-run certification to verify the optimization didn't degrade other dimensions. [EXPLICIT]

### Phase D: Assembly Report

Synthesize all phases into a single unified report: [EXPLICIT]

```markdown
# Assembly Report: {skill-name}

**Mode:** {quick/standard/deep}
**Duration:** {time}
**Result:** {CERTIFIED / CONDITIONAL / BLOCKED}

## Before → After
| Dimension | Before | After | Delta |
|-----------|--------|-------|-------|
| {1-10} | /10 | /10 | +N |
| Average | /10 | /10 | +N |
| Gate | N/13 | N/13 | +N |

## Interventions Applied
{changelog from Phase B, if run}

## Certification
{certification report from Phase C}

## Trigger Optimization (deep mode)
{trigger report from Phase C+, if run}

## Files Modified
| File | Action | Lines Changed |
|------|--------|--------------|
{list of every file touched}

## Next Steps
{what the user should do next, if anything}
```

## Gate Protocol

The assembly line has 3 decision gates. Each is explicit — the pipeline never makes destructive decisions autonomously. [EXPLICIT]

| Gate | Question | Options |
|------|----------|---------|
| A | Should we intervene? | Auto-skip if score >= 8 + gate 13/13. Otherwise proceed. |
| B | Approve the intervention plan? | User confirms. User can remove specific interventions. |
| C | Did certification pass? | If yes: report success. If no: report remaining issues. |

**Why gates matter:** Automation without checkpoints produces surprises. The assembly line is fast, not reckless. Each gate ensures the user stays in control of what changes.

## Assumptions & Limits

- This skill orchestrates x-ray-skill, surgeon-skill, certify-skill, and optionally trigger-skill. It doesn't contain its own diagnostic or improvement logic — it delegates.
- Requires Agent tool permission to spawn internal skill executions.
- The user must confirm the intervention plan (Gate B) before any files are modified. No auto-apply.
- Deep mode adds 10-20 minutes for trigger optimization. Use standard mode when time is constrained.
- Cannot orchestrate across multiple skills simultaneously. Run assembly-skill once per skill directory.
- Context window pressure: a deep-mode run on a 10+ file skill may approach context limits. If so, the pipeline falls back to standard mode and reports the limitation.

### Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| Phase A score >= 8 but user wants improvements | User says "improve anyway" | Override Gate A auto-skip. Run Phase B with user-specified focus areas. |
| Phase B plan rejected | User rejects the plan | Ask what to change. Re-plan with user constraints. |
| Phase C fails after Phase B | Certification BLOCKED despite interventions | Report what improved and what still blocks. Suggest manual fixes. |
| Context window exhaustion | Pipeline stalls mid-phase | Save progress. Report what completed. Suggest continuing in a new session. |
| Skill has no SKILL.md | Phase A can't start | Report immediately. Suggest creating SKILL.md first. |

## Edge Cases

- **Skill already CERTIFIED:** Quick mode auto-selected. Report: "Skill meets production standards. Score: {N}/10." No changes made.
- **Skill in terrible state (score < 3):** Standard mode. Focus Phase B entirely on Layer A (infrastructure). Don't attempt content or DX fixes until structure exists.
- **User wants to skip phases:** Respect it. `/assembly-skill ./path --mode quick` is just x-ray. The modes are the control mechanism.
- **Deep mode trigger optimization degrades rubric scores:** Re-certify catches this. Report the regression and revert the description change.
- **Mid-pipeline user abort:** Save all progress to that point. Phase A report is still useful even if Phase B was skipped.

## Validation Gate

Before delivering the assembly report: [EXPLICIT]

- [ ] Every phase that ran produced a complete output
- [ ] User confirmed the intervention plan before files were modified (Gate B)
- [ ] Before/After delta table shows accurate scores from Phase A and Phase C
- [ ] Every modified file is listed in the Files Modified table
- [ ] Certification result matches the formula (not assigned by feel)
- [ ] Next Steps are specific and actionable

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/pipeline-modes.md` | Detailed mode configurations, auto-selection logic, phase dependencies, timing estimates | Always — needed to configure the pipeline run |

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
