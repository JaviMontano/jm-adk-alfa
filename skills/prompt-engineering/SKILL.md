---
name: prompt-engineering
author: JM Labs (Javier Montaño)
version: 2.0.0
description: Design, evaluate, and optimize LLM instruction packages using deterministic pattern selection, source-grounded context, structured output contracts, guardrails, adversarial test cases, and script-backed evaluation packets. Use when the user asks for prompt engineering, system instruction design, few-shot examples, prompt optimization, prompt evaluation, guardrails, meta-prompting, or prompt design. [EXPLICIT]
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
sub-agents:
  - agents/lead.md
  - agents/support.md
  - agents/guardian.md
  - agents/specialist.md
knowledge:
  - knowledge/knowledge-graph.md
  - knowledge/body-of-knowledge.md
templates:
  - templates/output.html
  - templates/output.docx.md
  - templates/output.xlsx.md
---

# Prompt Engineering

> "A prompt is not a question — it is an architecture for reasoning."

## TL;DR

Design, evaluate, and optimize LLM instruction packages. This skill covers the full lifecycle: define task and sources, select the pattern, write the instruction package, create deterministic test cases, validate guardrails, and produce a versioned evaluation packet. [EXPLICIT]

## When to Activate

Use this skill when the user asks to:

- design or improve an LLM instruction package
- choose among zero-shot, few-shot, structured-output, system, meta, RAG-grounded, or constitutional/self-critique patterns
- audit a prompt for injection risk, output schema drift, ambiguous instructions, missing examples, or weak guardrails
- create an evaluation matrix for a prompt with test cases and metrics
- adapt a prompt for a target model without inventing model-specific guarantees

Do not use this skill to generate durable agent prompt files; route that work to `prompt-creator`. Do not use it to create a full agent constitution; route that work to `agent-constitution-creator`.

## Sub-Agents

| Agent | Role in Triad | File |
|-------|--------------|------|
| `prompt-lead` | Designs and writes the prompt | `agents/lead.md` |
| `prompt-support` | Reviews for bias, edge cases, injection risk | `agents/support.md` |
| `prompt-guardian` | Evaluates output quality, validates evidence | `agents/guardian.md` |
| `prompt-specialist` | Deep expertise in advanced patterns (meta, constitutional) | `agents/specialist.md` |

## Procedure

### Step 1: Discover
- Identify the task the prompt must accomplish
- Determine the target model family only from user input or source evidence
- Gather examples of desired input/output pairs
- Capture required sources, forbidden sources, safety boundaries, output schema, and success metrics
- If required source context is missing, return an `ask` or `coverage_gap` packet instead of writing a speculative prompt
- Read `knowledge/body-of-knowledge.md` for pattern catalog
- Check `knowledge/knowledge-graph.md` for related concepts
- Apply `assets/pattern-decision-matrix.json` and `assets/prompt-engineering-checklist.md`

### Step 2: Analyze
- Select the pattern:
  - **Zero-shot**: task is well-defined, model has sufficient training data
  - **Few-shot**: task needs examples to calibrate output format/style
  - **Reasoning scaffold**: task requires multi-step reasoning, but hidden reasoning must not be exposed
  - **System instruction**: task needs persistent behavioral constraints
  - **Meta-prompt**: task is to generate other prompts
  - **Constitutional**: task needs value-aligned, self-correcting output
  - **Structured output**: task needs schema-constrained output
  - **RAG-grounded**: task must use retrieved context and cite source boundaries
- Evaluate trade-offs: precision vs cost, latency vs quality, generality vs specificity
- Identify guardrails needed (output format, length, safety)
- Record pattern decision, rejected alternatives, and confidence band

### Step 3: Execute
- Write the prompt following the selected pattern
- Structure: role → context → task → constraints → output format → examples
- Add guardrails: output schema, safety filters, refusal patterns
- Create at least three deterministic test cases covering happy path, edge case, and adversarial/injection input
- Document the prompt with evidence tags
- Produce a prompt engineering packet with `task`, `target_model`, `pattern`, `prompt`, `guardrails`, `output_contract`, `test_cases`, `metrics`, and `risks`

### Step 4: Validate
- Run evaluation suite: accuracy, consistency, edge case handling
- Check for prompt injection vulnerability
- Verify output format compliance
- Validate the packet with `scripts/validate_prompt_packet.py`
- Generate deliverable using appropriate template only after validation

## Deterministic Contract

- Do not invent target-model capabilities, source facts, examples, metrics, dates, or hidden system behavior.
- Use provided examples or clearly marked synthetic fixtures; never imply synthetic fixtures are production evidence.
- Use stable IDs for test cases: `PE-001`, `PE-002`, sorted by id.
- Keep hidden reasoning private; ask for concise rationale or decision trace instead of chain-of-thought transcripts.
- Include refusal or escalation behavior for prompt injection, unsupported sources, and schema mismatch.
- If the user wants a reusable prompt file, hand off to `prompt-creator` after this skill produces the optimization packet.

## Quality Criteria

- [ ] Pattern selection justified with evidence
- [ ] Prompt tested with at least three diverse inputs
- [ ] Edge cases identified and handled
- [ ] Injection resistance verified
- [ ] Output format consistent across runs
- [ ] Guardrails prevent harmful/off-topic output
- [ ] Evidence tags on all claims
- [ ] Prompt engineering packet passes `scripts/validate_prompt_packet.py`
- [ ] `assets/prompt-engineering-checklist.md` applied

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| "Just ask nicely" | No structure = inconsistent results | Use role-context-task-format pattern |
| Massive single instruction | Exceeds attention, dilutes focus | Decompose into focused steps |
| No examples | Model guesses output format | Add 2-3 few-shot examples |
| Invented model behavior | Claims unsupported guarantees | State only source-backed model constraints |
| No evaluation | "It looks right" isn't evidence | Test with diverse inputs, score metrics |
| Exposed hidden reasoning | Leaks reasoning traces unnecessarily | Ask for concise rationale or decision summary |

## Related Skills

- `ai-safety` — Guardrails and output validation
- `structured-output` — JSON mode, schema-constrained generation
- `context-window-management` — Token budgeting for long prompts
- `rag-patterns` — Prompts that integrate retrieved context
- `llm-evaluation` — Systematic prompt evaluation methods

## Knowledge

- `knowledge/knowledge-graph.md` — Zettelkasten concept map
- `knowledge/body-of-knowledge.md` — Pattern catalog and references

## Templates

- `templates/output.html` — Branded HTML prompt documentation
- `templates/output.docx.md` — Word document spec for prompt library
- `templates/output.xlsx.md` — Evaluation matrix spreadsheet

## Assets

- `assets/prompt-engineering-checklist.md` defines the reusable deterministic review gate.
- `assets/pattern-decision-matrix.json` defines pattern selection criteria, required evidence, and risk controls.

## Scripts

- `scripts/validate_prompt_packet.py` validates prompt engineering packets.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

## Usage

Example invocations:

- "/prompt-engineering" — Run the full prompt engineering workflow
- "prompt engineering on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Uses the user's language unless the prompt artifact or target platform requires another language [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
