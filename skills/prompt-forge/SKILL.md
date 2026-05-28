---
name: prompt-forge
description: 
  Creates, reviews, evolves, repairs, and ports system prompts across LLM platforms using the Playbook format,
  a 10-criterion evaluation rubric, and context engineering principles. Activates when the user says "create a
  system prompt", "review this prompt", "optimize this prompt", "port this prompt to GPT", or "fix my prompt". [EXPLICIT]
  Also triggers on mentions of prompt engineering, prompt evaluation, prompt porting, or Playbook format. [EXPLICIT]
  Use this skill even if the user just pastes a prompt without instructions — it defaults to review mode. [EXPLICIT]
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
  - WebSearch
  - WebFetch
version: 1.0.0
---

# Prompt Forge

Turn vague assistant ideas into structured, high-performance system prompts — portable across Claude, GPT, and Gemini. [EXPLICIT]

## Operation Modes

| Mode | Trigger | Action |
|------|---------|--------|
| **Create** | "Create a prompt for...", "I need an assistant that..." | Full forge cycle: capture, draft, evaluate, refine, deliver |
| **Review** | "Review this prompt", "Is this any good?" | Evaluate against rubric, deliver scorecard + prioritized fixes |
| **Evolve** | "Make this better", "Optimize this prompt" | Identify weaknesses, apply targeted improvements |
| **Repair** | "This isn't working", "The AI keeps doing X" | Diagnose failure pattern, apply surgical fix |
| **Port** | "Convert this for Claude/GPT/Gemini" | Adapt format, constraints, and features for target platform |

**Default behavior:** Generate first, confirm after. Produce a strong v1, then iterate on feedback. Do not ask 20 questions before writing.

## Core Design Principles

1. **Hybrid Role** — Composite expert identity (domain + methodology + communication style). Not "You are a marketing expert" but a specific archetype with boundaries. [EXPLICIT]
2. **Conversational Flow** — Structure interaction in phases (discovery, execution, delivery) with entry/exit criteria. [EXPLICIT]
3. **Deliverable-Oriented** — Define what the user walks away with. Concrete output format, not vague "help with X". [EXPLICIT]
4. **Dynamic Intelligence** — Build reasoning techniques (chain-of-thought, structured analysis) into the prompt natively. [EXPLICIT]
5. **Executive Tone** — Professional, decisive. The AI sounds like a senior consultant, not a cautious intern. [EXPLICIT]
6. **Complete Structure** — Use the Playbook format as canonical output. [EXPLICIT]
7. **Iterative Co-Design** — Build self-correction triggers into the prompt. [EXPLICIT]

For deep explanations and examples, read `references/design-principles.md`. [EXPLICIT]

## The Playbook Format

Universal output template for generated prompts:

```markdown
# [Assistant Name] — v[X.Y]

## Role & Archetype
[Composite expert identity: domain + methodology + communication style]

## Objective
[What the user achieves — 1-2 sentences]

## Parameters
- Model: [Target model(s)]
- Temperature: [Recommended setting]
- Context window usage: [Strategy]

## Interaction Flow
### Phase 1: Discovery
[How the assistant gathers context]

### Phase 2: Execution
[How it processes and produces output]

### Phase 3: Delivery
[How it formats and presents results]

## Constraints
[Hard boundaries — what the assistant must NOT do]

## Key Questions
[3-5 questions for ambiguous context]

## Output Template
[Exact format with placeholders]

## Self-Correction Triggers
[Patterns that signal recalibration]
```

For per-section guidance, read `references/playbook-template.md`. [EXPLICIT]

## Evaluation Rubric

Every prompt scored 1-10 on each dimension. Target: 8+ on all for production quality. [EXPLICIT]

| # | Criterion | Measures |
|---|-----------|----------|
| 1 | Foundation | Clear archetype, objective, and constraints? |
| 2 | Accuracy | All claims, frameworks, and techniques correct? |
| 3 | Quality | Writing professional, precise, filler-free? |
| 4 | Density | Maximum value per token? |
| 5 | Simplicity | Non-expert could understand structure? |
| 6 | Clarity | Instructions unambiguous? One interpretation? |
| 7 | Precision | Constraints specific enough to enforce? |
| 8 | Depth | Handles edge cases, failures, advanced scenarios? |
| 9 | Coherence | All sections reinforce each other? |
| 10 | Value | User gets meaningfully better results? |

For detailed scoring and repair protocols, read `references/evaluation-rubric.md`. [EXPLICIT]

## Context Engineering

Modern prompt design manages everything the model sees, not just instruction text. [EXPLICIT]

| Layer | Scope | Example |
|-------|-------|---------|
| L1: Hot | System prompt + current turn | The Playbook itself |
| L2: Warm | Uploaded docs, knowledge base | Reference PDFs, style guides |
| L3: Cold | RAG retrieval, tool outputs | Dynamic data from APIs |

Design for all three layers. A great L1 with poor L2 design underperforms. [EXPLICIT]

For context hierarchy patterns and token optimization, read `references/context-engineering.md`. [EXPLICIT]

## Multi-Platform Deployment

| Platform | System Prompt | Knowledge Base | Tools |
|----------|--------------|----------------|-------|
| Claude Projects | Project instructions | Project knowledge files | MCP servers |
| ChatGPT Custom GPTs | Instructions field | Uploaded files | Actions (API) |
| Gemini Gems | System instructions | Google Docs/Drive | Extensions |
| API / Code | `system` parameter | RAG pipeline | Function calling |

For platform-specific limits and deployment guides, read `references/platform-guides.md`. [EXPLICIT]

## Workflow by Mode

### Create (most common)
1. **Capture** — domain, user outcome, target platform. [EXPLICIT]
2. **Draft** — fill every Playbook section. Generate first, confirm after. [EXPLICIT]
3. **Evaluate** — score against rubric. Fix anything below 8. [EXPLICIT]
4. **Deliver** — format for target platform with deployment instructions. [EXPLICIT]

### Review
1. Read the prompt completely. [EXPLICIT]
2. Score against rubric. [EXPLICIT]
3. Deliver scorecard + prioritized fix list. [EXPLICIT]

### Evolve
1. Identify weakest rubric dimensions. [EXPLICIT]
2. Apply targeted improvements (density compression, constraint sharpening, flow restructuring). [EXPLICIT]
3. Re-evaluate to confirm improvement. [EXPLICIT]

### Repair
1. Diagnose the failure pattern. [EXPLICIT]
2. Apply surgical fix to the specific section causing issues. [EXPLICIT]
3. Add a self-correction trigger to prevent recurrence. [EXPLICIT]

### Port
1. Identify source platform features and constraints. [EXPLICIT]
2. Map to target platform equivalents. [EXPLICIT]
3. Adapt format, adjust for token limits, replace unsupported features. [EXPLICIT]

## Antipatterns

| Problem | Bad Pattern | Fix |
|---------|-------------|-----|
| Wall of text | 2000-word flat instruction | Break into Playbook sections with flow |
| Vague role | "You are helpful" | Composite archetype: domain + method + style |
| No output format | "Help users with X" | Define exact deliverable template |
| Over-constraining | 50 rules in ALL CAPS | Explain *why* behind each constraint |
| Platform-blind | Same text everywhere | Adapt to each platform's affordances |
| No feedback loop | Static, never improved | Build self-correction triggers + versioning |

## Assumptions & Limits

- Prompt quality is platform-dependent. A perfect Claude Project prompt may underperform on GPT without adaptation.
- The Playbook format is a starting point, not a cage. Some domains need additional sections; others need fewer.
- Evaluation scores are relative to the prompt's purpose. A chatbot prompt and a data analysis prompt have different ceilings on "Depth."
- Context window limits vary by platform and model. Always check current limits before optimizing token usage.
- Self-correction triggers work best in models with strong instruction-following. On weaker models, constraints may be ignored.

## Edge Cases

- **Prompt for a non-conversational use case (batch processing, API-only):** Omit Interaction Flow. Focus on Constraints and Output Template.
- **User provides a prompt in a language other than English:** Write the Playbook in the user's language. Criterion names in the rubric remain universal.
- **Extremely long knowledge base (100+ pages):** Design for L2/L3 context. The system prompt should reference, not contain, the knowledge.
- **User wants a prompt that breaks platform rules:** Decline. Note the specific platform policy it would violate.
- **Evolve mode finds no weaknesses:** Possible for well-crafted prompts. Report that all criteria meet threshold, suggest testing with adversarial inputs.
- **Porting between very different platforms (e.g., Claude to a fine-tuned open model):** Some features (tool use, retrieval) may not translate. Document what was lost in porting.

## Validation Gate

Before delivering a prompt, confirm:

- [ ] Playbook format is complete (all mandatory sections present)
- [ ] Role is a composite archetype, not a generic label
- [ ] At least one constraint defines what the assistant must NOT do
- [ ] Output template includes concrete format with placeholders
- [ ] All rubric criteria score 8+ (or deficits are documented)
- [ ] Platform-specific formatting applied if a target was specified
- [ ] Self-correction triggers are present and testable

## Reference Files

- `references/design-principles.md` — Deep dive into the 7 principles with examples and antipatterns
- `references/evaluation-rubric.md` — Full scoring parameters, failure criteria, repair protocols
- `references/playbook-template.md` — Complete template with per-section guidance
- `references/platform-guides.md` — Platform-specific formatting, limits, deployment for Claude, GPT, Gemini, API
- `references/context-engineering.md` — Context hierarchy, token optimization, RAG integration

---
**Author:** Javier Montaño | **Last updated:** March 12, 2026

## Usage

Example invocations:

- "/prompt-forge" — Run the full prompt forge workflow
- "prompt forge on this project" — Apply to current context

