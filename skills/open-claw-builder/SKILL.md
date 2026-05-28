---
name: open-claw-builder
description: 
  Builds production-grade tool-calling AI agents with TypeScript on open LLM stacks (Groq, OpenRouter, Ollama). [EXPLICIT]
  Activates when the user says "build an agent", "create a bot", "scaffold a Telegram bot",
  "make a Discord agent", or "set up an HTTP agent". Also triggers on mentions of tool-calling,
  open LLM stack, Groq agent, or OpenRouter bot. Use this skill even if the user only has a
  vague idea — it interviews for missing details. [EXPLICIT]
argument-hint: agent-name [platform: telegram|discord|http]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
model: opus
context: fork
version: 1.0.0
---

# Open-Claw Agent Builder

Build tool-calling AI agents on open LLM stacks. "Claw" = Claude-like architecture patterns (loop → tool → security) applied to any function-calling LLM. [EXPLICIT]

## Assumptions & Limits

- **Assumes**: Node.js >=18, npm, and target platform API access (Telegram bot token, Discord app ID, or HTTP port)
- **Assumes**: LLM API access (Groq or OpenRouter key) — Ollama for local-only setups
- **Limit**: Single-process architecture — not designed for horizontal scaling (use Redis queues + workers for that)
- **Limit**: Sub-agents run at depth=1 only — no recursive delegation (prevents runaway loops)
- **Trade-off**: SQLite for memory = simple/fast but single-writer; upgrade to PostgreSQL if >100 concurrent users

### When to use this vs other approaches

| Need | Use This | Use Instead |
|---|---|---|
| Telegram/Discord bot with tools | Yes | — |
| HTTP API agent | Yes | — |
| Claude Code extension | No | Agent Creator (`/agent-creator`) |
| Quick prototype | No | Playground skill |
| Enterprise multi-tenant | No | Custom architecture with proper auth |

## Usage

```
/open-claw-builder my-agent telegram
/open-claw-builder api-agent http
/open-claw-builder assistant          # interview for platform
```

Parse `$1` as agent name (kebab-case), `$2` as platform. Default: telegram. [EXPLICIT]

## Before Building

1. **Read architecture specs**: `Read references/file-specs.md` — all 12 source file specifications
2. **Read security spec**: `Read references/security.md` — 3 checkpoint details, regex patterns, threat model
3. **Read patterns**: `Read references/patterns.md` — ADRs, anti-patterns, circular dependency resolution
4. **Check existing**: `Glob */src/agent.ts` — learn from prior implementations

## Architecture: 6 Layers

```
L1 ENTRY      index.ts            Lifecycle, shutdown, error boundaries [EXPLICIT]
L2 CONFIG     config.ts + .env    Env loading, validation, fail-fast [EXPLICIT]
L3 INTERFACE  bot.ts              Platform adapter (Telegram/Discord/HTTP) [EXPLICIT]
L4 ORCHESTR.  agent.ts            The Loop: security → tokens → tools → response [EXPLICIT]
L5 PROVIDERS  llm.ts + memory.ts  LLM abstraction + SQLite conversation store [EXPLICIT]
L6 TOOLS      tools/*.ts          Tool registry, async dispatch, delegation [EXPLICIT]
```

**Iron rule**: Each layer imports ONLY from layers below it. Violations create circular dependencies.

## Build Sequence

### Phase 1: Scaffold

```bash
mkdir -p {name}/src/tools && cd {name}
npm init -y && npm pkg set type="module" name="{name}" version="1.0.0"
npm i grammy groq-sdk better-sqlite3 dotenv
npm i -D @types/better-sqlite3 tsx typescript
npm pkg set scripts.dev="tsx watch src/index.ts" scripts.start="tsx src/index.ts"
```

`tsconfig.json`: `strict: true`, `target: "ES2022"`, `moduleResolution: "bundler"`, `noUnusedLocals: true`, `noUnusedParameters: true`.

### Phase 2: Build bottom-up (dependency-safe order)

| # | File | Purpose | ~LOC | Key Decision |
|---|---|---|---|---|
| 1 | `logger.ts` | `[timestamp][LEVEL]` structured logging | 18 | No deps — foundation for everything |
| 2 | `config.ts` | Env loading + validation + defaults | 65 | Fail-fast: missing required var = crash at startup, not at first use |
| 3 | `security.ts` | 3 checkpoints (sanitize, harden, validate) | 70 | Log-but-don't-block: blocking creates false positives on legit security questions |
| 4 | `tokens.ts` | Estimation, budget calc, history trimming | 50 | `Math.ceil(text.length / 4)` — zero deps, +-15% accuracy |
| 5 | `memory.ts` | SQLite WAL, prepared stmts, 32KB guard | 70 | WAL mode: concurrent reads + one writer; prepared stmts prevent SQL injection |
| 6 | `registry.ts` | Tool Map + async dispatch + delegate slot | 60 | Dynamic executor slot solves circular dep with agent.ts |
| 7 | `get-current-time.ts` | Example tool with IANA timezone | 33 | Proves the tool interface works |
| 8 | `delegate.ts` | Sub-agent definitions + `delegate_to_agent` | 60 | Depth=1 limit prevents runaway delegation |
| 9 | `llm.ts` | Groq primary + OpenRouter fallback, 30s timeout | 115 | Dual-provider: if Groq rate-limits, OpenRouter catches |
| 10 | `agent.ts` | Orchestrator: the agent loop | 185 | Heart of the system — ties everything together |
| 11 | `bot.ts` | Platform adapter, whitelist, msg splitting | 78 | 60s timeout prevents hung conversations |
| 12 | `index.ts` | Lifecycle: init, initDelegation(), shutdown | 42 | SIGINT/SIGTERM handlers for clean exit |

**Implementation details for each file**: `Read references/file-specs.md`

### Phase 3: Verify

```bash
npx tsc --noEmit  # Zero errors required
```

### Phase 4: Harden (quality rubric review)

## Security Deep Dive

```
User Input → [CP1: sanitize] → [CP2: harden prompt] → Agent Loop → [CP3: validate output] → User [EXPLICIT]
```

| Checkpoint | Function | Strategy | Why |
|---|---|---|---|
| CP1 | `sanitizeInput` | Strip control chars, enforce max length, 8 regex injection patterns | First line of defense — catches obvious attacks |
| CP2 | `buildSecurePrompt` | Append SECURITY_SUFFIX to system prompt | Defense in depth — even if CP1 misses something, prompt instructions resist override |
| CP3 | `validateOutput` | Scan for role confusion, leaked prompts, "unrestricted AI" claims | Catches successful jailbreaks in the output |

**All checkpoints**: Log-but-don't-block. Blocking creates false positives when users ask legitimate security questions. **Full regex patterns and SECURITY_SUFFIX**: `Read references/security.md`

## Token Management

```
available = modelContext - maxTokens - systemPrompt - 10% safetyMargin
```

- Estimate: `Math.ceil(text.length / 4)` (zero deps, +-15% English)
- Trim strategy: oldest messages first, NEVER drop most recent user message
- Budget recalculated before each LLM call (tool responses change the math)

## Multi-Agent Delegation

Sub-agents in `delegate.ts`: `{name, description, systemPrompt, tools[]}`. Main agent (depth=0) has `delegate_to_agent` tool. Spawned sub-agent runs at depth=1 with restricted tools and NO delegation capability (prevents infinite loops). [EXPLICIT]

**Circular dependency resolution**: `delegate.ts` defines agent data → `registry.ts` holds executor function slot → `agent.ts` fills the slot at startup via `initDelegation()`. This breaks the import cycle.

## Naming Conventions

| Artifact | Convention | Example |
|---|---|---|
| Files | kebab-case | `get-current-time.ts` |
| Tool names | snake_case | `get_current_time` |
| Interfaces | PascalCase | `AgentDeps` |
| Functions | camelCase | `runAgent` |
| Constants | SCREAMING_SNAKE | `MAX_ITERATIONS` |
| Env vars | SCREAMING_SNAKE | `TELEGRAM_BOT_TOKEN` |

## Quality Rubric (10/10 target)

| # | Dimension | 10/10 | Red Flag |
|---|---|---|---|
| 1 | Fundamento | Every decision traceable to ADR | "I did it this way because" without reference |
| 2 | Veracidad | Zero gap between docs and code | Commented-out code contradicts docs |
| 3 | Calidad | Zero `as any`, all errors caught+logged | Any `as any` cast |
| 4 | Densidad | Every function earns existence | Helper that's called once |
| 5 | Simplicidad | YAGNI/KISS everywhere | Premature abstractions |
| 6 | Claridad | Self-documenting names, linear flow | Nested ternaries, clever one-liners |
| 7 | Precision | All inputs validated, outputs typed | `any` in function signatures |
| 8 | Profundidad | All 3 CPs + tokens + delegation working | Security checkpoint skipped |
| 9 | Coherencia | Same patterns everywhere | Different error handling styles |
| 10 | Valor | Agent works: receives → thinks → tools → replies | Demo fails on happy path |

## Edge Cases

- **Groq rate limit**: OpenRouter fallback activates automatically; log the switch
- **Message too long for platform**: bot.ts splits at message limit (4096 Telegram, 2000 Discord)
- **Tool throws unexpected error**: agent.ts catches all tool errors, sends error description back to LLM for self-correction
- **User sends image/file**: Log unsupported media type, respond with text-only capability message
- **Concurrent users**: SQLite WAL handles concurrent reads; writes serialize (fine for <100 users)

## Validation Gate

- [ ] `npx tsc --noEmit` → zero errors
- [ ] Zero `as any` casts in entire codebase
- [ ] All 3 security checkpoints implemented
- [ ] Token budget prevents context window overflow
- [ ] Graceful shutdown on SIGINT/SIGTERM
- [ ] All env vars validated at startup (fail-fast)
- [ ] No bare `console.log` (use logger)
- [ ] Sub-agent delegation works with depth=1 limit
- [ ] Platform message splitting handles edge cases
- [ ] `.env.example` documents all required variables

---
**Author:** Javier Montaño | **Last updated:** March 12, 2026
