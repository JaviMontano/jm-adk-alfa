# Prompt Engineering - Knowledge Graph

<!-- Zettelkasten-ready: use [[wikilinks]] for Obsidian compatibility -->

## Core Concepts

- [[prompt-pattern]] — A reusable structure for prompting LLMs
- [[zero-shot]] — No examples, relies on model's training
- [[few-shot]] — 2-5 examples calibrate output format and style
- [[reasoning-scaffold]] — Private multi-step decomposition with concise rationale
- [[system-instruction]] — Persistent behavioral constraints
- [[meta-prompt]] — Prompt that generates prompts
- [[constitutional-ai]] — Self-correcting with value alignment
- [[structured-output]] — Schema-bound prompt output
- [[prompt-packet]] — Pattern, prompt, guardrails, tests, metrics, and risks

## Relationships

```
prompt-pattern
├── zero-shot (simplest, when task is well-defined)
├── few-shot (adds examples for calibration)
│   └── depends-on: example-quality
├── reasoning-scaffold (multi-step reasoning without hidden transcript)
├── system-instruction (persistent constraints)
│   ├── composes-with: few-shot
│   └── composes-with: reasoning-scaffold
├── meta-prompt (generates prompts)
│   └── requires: prompt-evaluation
└── constitutional-ai (self-correction)
    └── requires: value-criteria
```

## Tags

#prompt-engineering #llm #ai #patterns #zettelkasten

## Cross-References

- [[rag-patterns]] — Prompts that integrate retrieved context
- [[structured-output]] — Schema-constrained prompt output
- [[ai-safety]] — Guardrails and injection prevention
- [[context-window-management]] — Token budgeting for prompts
- [[llm-evaluation]] — Measuring prompt effectiveness
- [[prompt-creator]] — Durable prompt file generation

## Decision Heuristics

| If... | Then use... | Because... |
|-------|------------|-----------|
| Task is well-defined, model knows the domain | Zero-shot | Simplest, lowest cost |
| Output format matters but task is clear | Few-shot (2-3 examples) | Examples calibrate format |
| Task requires reasoning or math | Reasoning scaffold | Decomposition improves accuracy without exposing hidden reasoning |
| Agent needs persistent behavior | System instruction | Constraints survive across turns |
| Need to generate prompts at scale | Meta-prompt | One prompt generates many |
| Output must align with values | Constitutional | Self-correction loop |
