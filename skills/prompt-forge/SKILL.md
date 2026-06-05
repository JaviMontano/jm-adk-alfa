---
name: prompt-forge
version: 1.0.0
description: Create, review, evolve, repair, and port system prompts using a deterministic Playbook format, source-boundary rules, platform portability notes, rubric scorecards, adversarial test cases, and script-backed forge packet validation. Use when the user asks to create a system prompt, review a prompt, optimize or repair prompt behavior, port prompts across Claude, ChatGPT, Gemini, or API runtimes, or apply Prompt Forge / Playbook format. [EXPLICIT]
argument-hint: "mode: create|review|evolve|repair|port domain or prompt-path [--platform claude-project|custom-gpt|gemini-gem|api]"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Prompt Forge

Turn assistant ideas or existing prompts into structured, production-ready instruction packages. The skill works in five modes: create, review, evolve, repair, and port. Every mode produces a deterministic forge packet before delivery.

## When to Activate

Activate when the user requests any of the following:

- Create a system prompt, project instruction, Custom GPT instruction, Gemini Gem instruction, or API system message.
- Review, score, optimize, repair, or port an existing prompt.
- Apply Prompt Forge, Playbook format, prompt rubric, prompt portability, prompt repair, or prompt deployment instructions.
- Paste a prompt and ask whether it is good, why it fails, or how to improve it.

Do not activate for reminders such as "prompt me tomorrow", conceptual Q&A such as "what is a system prompt?", or durable prompt-file generation that belongs to `prompt-creator` unless Prompt Forge analysis is explicitly requested first.

## Required Inputs

Capture the minimum viable context before writing final output:

- Mode: create, review, evolve, repair, or port.
- Prompt goal and primary user outcome.
- Target platform: `claude-project`, `custom-gpt`, `gemini-gem`, `api`, or `unknown`.
- Source boundary: what facts, files, policies, or retrieved snippets the assistant may rely on.
- Output contract: expected format, required fields, and refusal or coverage-gap behavior.
- Constraints: safety, brand, tone, workflow, and tool boundaries.

If input is incomplete, ask only the missing questions that affect the Playbook contract. Do not ask a broad interview before producing a useful draft or review.

## Deterministic Contract

- Do not invent domain facts, platform limits, policies, citations, tools, or source material.
- Treat current platform limits as unknown unless supplied by the user or cited from a dated source.
- Keep hidden reasoning private. Use concise rationale, decision trace, or checklist evidence instead of exposed reasoning transcripts.
- Make every source-grounded prompt define unsupported-source behavior, usually `coverage_gap` or refusal.
- Preserve machine-readable output contracts exactly when evolving or repairing prompts.
- For porting, state source platform, target platform, mapped features, unsupported features, and losses.
- Run `scripts/validate_forge_packet.py` for JSON forge packets when producing or changing a structured artifact.

## Assets And Scripts

Use these local assets before drafting:

- `assets/prompt-forge-checklist.md` - deterministic review checklist.
- `assets/playbook-contract.json` - required Playbook sections, modes, platforms, rubric criteria, and test coverage.
- `assets/platform-portability-matrix.json` - local platform mapping for Claude Project, Custom GPT, Gemini Gem, and API deployment.
- `scripts/validate_forge_packet.py` - deterministic forge packet validator.

## Operation Modes

| Mode | Trigger | Deterministic Output |
|------|---------|----------------------|
| Create | "Create a prompt for...", "I need an assistant that..." | Full Playbook plus source boundary, output contract, rubric, tests, and risks. |
| Review | "Review this prompt", "Is this any good?" | Rubric scorecard, blockers, prioritized fixes, and validation gaps. |
| Evolve | "Make this better", "Optimize this prompt" | Before/after changes, preserved contracts, rubric delta, and regression tests. |
| Repair | "This is not working", "The AI keeps doing X" | Failure diagnosis, surgical fix, self-correction trigger, and adversarial test. |
| Port | "Convert this for Claude/GPT/Gemini/API" | Platform mapping, adapted prompt, unsupported features, losses, and validation checklist. |

Default pasted-prompt behavior is review mode unless the user explicitly asks to create, evolve, repair, or port.

## Playbook Format

Generated prompts use this canonical section set unless a non-conversational batch/API use case requires an explicitly documented omission:

```markdown
# [Assistant Name] - v[X.Y]

## Role & Archetype
[Composite expert identity: domain + method + communication style]

## Objective
[What the user achieves]

## Parameters
- Platform:
- Source boundary:
- Output contract:
- Temperature or determinism note:

## Interaction Flow
### Phase 1: Discovery
### Phase 2: Execution
### Phase 3: Delivery

## Constraints
[Hard boundaries, including what the assistant must not do]

## Key Questions
[Only questions needed to complete the contract]

## Output Template
[Exact format with placeholders]

## Self-Correction Triggers
[Observable failure patterns and recovery actions]
```

## Evaluation Rubric

Score every generated or reviewed prompt on these criteria. Scores below 8 require a repair note.

| Criterion | Measures |
|---|---|
| Foundation | Clear archetype, objective, and constraints. |
| Accuracy | Claims, sources, and methods are supported. |
| Quality | Professional, precise, filler-free writing. |
| Density | High value per token without losing constraints. |
| Simplicity | Structure remains understandable. |
| Clarity | Instructions have one practical interpretation. |
| Precision | Boundaries are enforceable. |
| Depth | Edge cases and failure modes are handled. |
| Coherence | Sections reinforce each other. |
| Value | User receives a materially better prompt. |

## Output Packet

When responding, include:

1. Mode and activation decision.
2. Source boundary and assumptions.
3. Playbook or scorecard.
4. Rubric scores and required repairs.
5. Test cases: happy path, edge case, adversarial.
6. Platform notes when applicable.
7. Validation result from checklist or script.
8. Risks and coverage gaps.

## Validation Gate

Before delivery, confirm:

- Playbook sections match `assets/playbook-contract.json`.
- Source boundary and unsupported-source behavior are explicit.
- Constraints include no-invention and hidden-reasoning privacy.
- Output contract is preserved or intentionally revised with rationale.
- Rubric has all criteria and every score below 8 has a repair.
- Test cases include happy path, edge case, and adversarial coverage.
- Porting outputs document unsupported features and losses.
- No remote assets, unstated current-platform claims, or hidden reasoning transcripts are included.

## References

- `assets/prompt-forge-checklist.md`
- `assets/playbook-contract.json`
- `assets/platform-portability-matrix.json`
- `references/design-principles.md`
- `references/evaluation-rubric.md`
- `references/playbook-template.md`
- `references/platform-guides.md`
- `references/context-engineering.md`
- `references/domain-knowledge.md`
