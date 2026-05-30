# Changelog

All notable changes to the JM Agentic Development Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — Katas Alignment (Claude Certified Architect)

Systemic upgrades + 30 new skills derived from the 30-kata "Claude Certified Architect" pocket guide. Improves functional capability, predictability, hooks, tool use, and token use.

- **Inventories** (`docs/katas/`): `katas-content.md` (canonical source for all 30 katas), `practices-inventory.md`, `skill-inventory.md`.
- **30 new skills** `skills/katas-*` (one per kata, full 16-file CI-valid scaffold) covering deterministic loops, PreToolUse/PostToolUse hooks, hub-and-spoke isolation, JSON-Schema extraction, MCP errors, Plan Mode, hierarchical/path-conditional memory, prefix caching, context-dilution mitigation, prompt chaining, headless review, few-shot, self-correction, human handoff, message batches, scratchpad, adaptive investigation, provenance, tool descriptions, MCP config, built-in tool selection, commands/skills, sessions, retry-with-feedback, independent review, multi-agent errors, confidence calibration, false-positive criteria.
- **Hooks (Kata 02/03)**: `scripts/pre-tool-guard.sh` is now policy-driven — hot-reloads `references/guardrails/tool-policy.json` and emits a deterministic deny (exit 2) before dangerous Bash or writes to protected paths; `references/reliability/posttooluse-normalization.md` documents runtime output normalization.
- **Reliability (Kata 10/11)**: `references/reliability/prefix-caching.md`, `references/reliability/context-dilution.md`.
- **Structured extraction & headless review (Kata 05/13)**: `references/schemas/annotations.schema.json` + `scripts/post_annotations.py` (stdlib validator); CI now validates review output against the schema.
- **Message Batches (Kata 17)**: `scripts/batch/batch-runner.py` (lifecycle + selective failed-retry, injectable client, `--dry-run`).
- **Path-conditional rules (Kata 09)**: `references/path-rules.md` manifest.
- **Confidence + false positives (Kata 29/30)**: `scripts/qa/run-confidence-fp-tests.py` (calibration, stratified sampling, categorical FP criteria) wired into CI.
- **Tool description quality (Kata 21)**: `validate-skills.py` adds a WARN-only check for generic/empty descriptions.

### Added — Competency skills + deterministic skill improver

- **22 competency skills** (`docs/competencies/`, `scripts/scaffold-competencies.sh`): the buildable capability behind the katas — `hook-engineering`, `agentic-loop-engineering`, `subagent-orchestration`, `structured-output-design`, `mcp-engineering`, `tool-use-design`, `plan-mode-workflow`, `claude-md-architecture`, `context-window-engineering`, `prompt-chaining-design`, `few-shot-engineering`, `self-correction-loops`, `human-escalation-design`, `message-batch-orchestration`, `persistent-memory-design`, `adaptive-investigation-method`, `provenance-engineering`, `custom-tooling-extension`, `session-lifecycle-management`, `validation-retry-design`, `independent-review-design`, `evaluation-confidence-design`. Each is a full 16-file CI-valid skill (filled via parallel fan-out).
- **Deterministic skill improver** (`scripts/improve-skills.py`): additive, idempotent quality pass over every skill — enriches each `knowledge-graph.json` with ontology/evidence/anti-pattern nodes+edges and guarantees the canonical eval edge cases (false-positive, empty input). Dry-run by default; re-running is a no-op. Applied across all skills.
- Counts → 585 skills (1368 components).

### Added — Pristino Persona Calibration (Phase 1)

- Deterministic 8-persona role model: `references/ontology/personas.json` + `references/ontology/persona-protocol.md`.
- `scripts/persona-calibrate.sh` UserPromptSubmit hook — byte-stable persona/mode/optimizer signals injected as additionalContext.
- `skills/pristino-calibration/` — persona on line 1, adaptive prompt optimizer (original/optimized/response), precedence Veracidad>Seguridad>Objetivo>Formato>Estilo, Canvas output contract.
- `scripts/validate-personas.py` schema gate; `/jm-adk:calibrate` command.
- Counts → 533 skills / 267 commands (1316 components).

## [4.0.1] - 2026-03-25

### Changed — Ecosystem: SDD v3.4.0 Workspace Sessions Alignment

- Updated `references/ontology/intent-integrity-governance.md` with ecosystem plugin registry
- Added workspace architecture alignment table (JM-ADK ↔ SDD pattern comparison)
- SDD plugin now at v3.4.0: per-task workspace sessions, workspace-aware RAG, dual-write logging, ALM session cards

## [4.0.0] - 2026-03-25

### Added — Automatic Workspace Management

**Core feature**: Every task creates a dated, traceable workspace folder (`workspace/YYYY-MM-DD-slug/`) with tasklog, changelog, plan, and artifacts directory. Fully automatic — no user effort required.

**New files**:
- `scripts/workspace-manager.sh` — Central CRUD: create, status, list, complete, archive, switch, reopen, gate, report, log
- `commands/health.md` — `/jm-adk:health` system diagnostics (read-only)
- `commands/workspace-report.md` — `/jm-adk:workspace-report` narrative summary
- `commands/workspace-cleanup.md` — `/jm-adk:workspace-cleanup` maintenance
- `.jm-adk.json` — Plugin configuration (workspace settings, hook toggles, governance)
- `workspace/.gitkeep` — Directory structure preserved in git, contents gitignored

**Architecture: Hook-Signal / Model-Act**:
- Hooks detect state and emit structured signals (stdout)
- Model (CLAUDE.md) parses signals and acts via workspace-manager.sh
- Single write path for all workspace state — no divergence possible

**Enhanced hooks** (all 5 rewritten):
- SessionStart: system integrity + workspace detection + degraded mode signaling
- UserPromptSubmit: injection detection + orphaned workspace detection
- PostToolUse: auto-logs tool calls to active workspace tasklog (filters read-only tools)
- Stop: session boundary marker + timestamp updates

**Workspace operations**: create, status, list, complete, archive, switch, reopen, gate (sequential only, regression blocked), report

**Self-healing**: corrupted registry auto-recreates, orphaned pointers auto-clear, duplicate slugs auto-deduplicate

### Changed

- `CLAUDE.md` → v4.0.0 with Workspace Protocol (decision tree, slug derivation, discipline rules, edge cases)
- `PRISTINO.md` → workspace-aware awakening, session closure writes to tasklog
- `ARCHITECTURE.md` → workspace system documented with design decisions table (D1-D6)
- `commands/init.md` → premium init with workspace setup, acceptance criteria, edge cases
- `commands/workspace.md` → full CRUD with reopen, gate regression guard, lifecycle diagram
- `.claude-plugin/plugin.json` → v4.0.0
- `hooks/hooks.json` → descriptions updated to v4.0.0 behavior
- `README.md` → workspace section, v4.0.0 badge, 1035 components
- `landing.html` → v4.0.0 badge, workspace card, updated meta description
- `.gitignore` → workspace/* excluded, .gitkeep preserved

## [3.2.0] - 2026-03-23

### Changed — Pristino v6.0: Awakening, Input Tolerance, Auto-Prompt

**PRISTINO.md** completely rewritten with 3 new protocols:

1. **Awakening Protocol** (executable, not declarative):
   - Self-check: verify all files accessible, component counts match (256×4)
   - Load context: Constitution → Guardrails → Brand → Index
   - Detect environment: IDE, model tier, triad mode, multimodal capability
   - Greet: report environment + counts + "En que te puedo ayudar?"

2. **Input Tolerance Protocol**:
   - Typos: fuzzy-match intent, NEVER correct user's spelling
   - Voice-transcribed: strip fillers, handle phonetic spelling ("fayerbase" → Firebase)
   - Dyslexia-aware: short sentences, bullet points, no dense paragraphs
   - Multilingual: respond in user's language, process in English internally
   - Multimodal: images, PDFs, URLs analyzed then processed (IDE-dependent)

3. **Auto-Prompt Matching**:
   - User describes what they want in natural language (messy is fine)
   - Pristino fuzzy-matches against PRISTINO-INDEX.md
   - Confidence ≥ 0.85 → auto-execute with triad
   - 0.60-0.84 → present top 3 options
   - < 0.60 → ask clarifying question
   - Official `/jm-adk:command` → skip matching, execute with precision

**All 7 IDE files** updated to v3.2.0 with input tolerance + auto-prompt notes.
**adk-orchestrator.md** updated with `input-tolerance` and `auto-prompt-matching` skills.

## [3.0.0] - 2026-03-22

### Added — Tera Edition: 256x4 = 1024 Components

**8 new domains** with 16 components each (skill + agent + command + prompt):

| Domain | Skills | Key Additions |
|--------|--------|--------------|
| **Business/Marketing** | 16 | marketing-context, CRO, B2B outreach, sales collateral, copywriting, funnel, A/B testing, pricing |
| **DevOps/Infrastructure** | 16 | Docker, monitoring, alerting, logging, incident response, rollback, CDN, SSL, DNS |
| **Data/Analytics** | 16 | KPI framework, dashboard design, ETL, schema evolution, cohort analysis, data privacy |
| **AI/ML Integration** | 16 | prompt engineering, RAG patterns, LLM eval, embeddings, AI safety, multi-model routing |
| **Hooks/Automation** | 16 | PreToolUse guard, UserPromptSubmit filter, Stop validator, error recovery, workflow orchestration |
| **Enterprise/Governance** | 16 | compliance, audit trails, RBAC, SLA, disaster recovery, OKRs, team topology |
| **UX/Design** | 16 | user testing, prototyping, animation principles, color theory, micro-interactions, mobile patterns |
| **Communication/Content** | 16 | technical writing, presentations, video scripts, case studies, whitepapers, microcopy |

**Hooks expanded** from 2 to 5:
- `UserPromptSubmit` — Input filtering and injection detection (from hooks-mastery)
- `PreToolUse` — Block dangerous commands before execution (exit code 2 pattern)
- `Stop` — Final output validation before delivery

**Sources cherry-picked**:
- claude-code-hooks-mastery (hook patterns, PreToolUse blocking)
- marketingskills (marketing-context, CRO, B2B outreach, copywriting frameworks)
- antigravity-kit (auto-agent detection, attribution patterns)
- agent-toolkit (multi-model awareness)
- gemini-3-pro prompt (validated sequential-first, bounded cognition alignment)

**Total**: 256 Skills · 256 Agents · 256 Commands · 256 Prompts = **1024 components**

## [2.0.0] - 2026-03-22

### Added — 128x4 Complementarity (Socratic Debate)
- **4 New Skills**: `error-handling`, `seo-content`, `git-workflow`, `api-documentation`
- **25 New Agents**: `brand-html-crafter`, `client-prospector`, `dossier-builder`, `cv-specialist`, `bdd-strategist`, `guardrails-enforcer`, `lighthouse-auditor`, `git-strategist`, `session-manager`, `changelog-tracker`, `indexability-auditor`, `workspace-manager`, `learning-engine`, `mermaid-diagrammer`, `image-optimizer`, `modal-dialog-builder`, `scheduled-task-builder`, `recaptcha-integrator`, `trade-off-analyst`, `visual-qa-tester`, `error-handler`, `seo-content-writer`, `api-documenter`, `ssh-deployer`, `market-researcher`
- **22 New Commands**: `prospect`, `dossier`, `cv`, `market`, `brand-html`, `bdd`, `optimize-images`, `optimize-fonts`, `git-init`, `session`, `insights`, `index`, `workspace`, `error-patterns`, `seo-content`, `api-docs`, `recaptcha`, `lighthouse`, `ssh-deploy`, `trade-off`, `visual-test`, `constitution`
- **25 New Prompts**: 9 quality (error-handling, visual-regression, lighthouse, BDD, guardrails, indexability, dual-layer, git, API docs), 9 meta (session, environment, triad, guardrail, insight, amendment, workspace, index, brand-html), 7 development (error-boundary, recaptcha, scheduled-function, webhook, bundle, service-worker, schema-markup)

### Architecture — 128x4 Symmetry
All four component types reach 128 through genuine complementarity:
- Skills filled gaps in error handling, SEO content, Git workflow, API docs
- Agents mapped to all 23 new skills from v1.1-v1.5 (Constitution, workshop, guardrails, environment)
- Commands exposed all new agent capabilities to users
- Prompts covered quality, meta, and development gaps

**Total**: 128 Skills · 128 Agents · 128 Commands · 128 Prompts = **512 components**

## [1.5.0] - 2026-03-22

### Added — Brand Design System + Guardrails + Workshop Skills
- **Brand Design System** (`references/brand/`):
  - `design-tokens.json` — Canonical MetodologIA palette, typography, effects
  - `html-template.html` — Base HTML: navy bg, gold accents, glassmorphism, Swiss grid, print-ready
  - All HTML outputs now use this aesthetic by default
- **Guardrails System** (`references/guardrails/`):
  - `guidelines.json`, `constraints.json`, `guardrails.json` — User-declared rules stored as JSON
  - Pristino double-confirms before saving any rule
  - Loaded at bootstrap as internal RAG
  - Guardian checks compliance
- **7 New Skills**:
  - `guardrails-management` — Detect, confirm, store, enforce user rules
  - `client-prospecting` — AI-driven prospecting by geography/sector → branded HTML
  - `client-dossier` — Deep company research → branded HTML dossier
  - `cv-enhancement` — CV/resume improvement → branded HTML
  - `workshop-proposal` — Workshop design → branded HTML proposal
  - `market-intelligence` — Geographic market analysis → branded HTML report
  - `branded-html-output` — Base skill for MetodologIA-branded HTML generation
- **1 New Command**: `/jm-adk:guardrails` — list, add, remove working rules

### Changed
- `PRISTINO.md` — Bootstrap now loads guardrails + brand tokens between Constitution and Index

## [1.4.0] - 2026-03-22

### Added — Environment Detection Protocol + Init/Demo Commands
- `references/ontology/environment-protocol.md` — IDE detection (7 IDEs), model tier detection (Heavy/Medium/Light), triad adaptation rules, capability matrix, auto-priming protocol
- `skills/environment-detection/SKILL.md` — Detect IDE and model at session start, adapt triad mode
- `commands/init.md` — `/jm-adk:init` guided project setup: detect env, analyze repo, generate Constitution + plan + triad
- `commands/demo.md` — `/jm-adk:demo` quick showcase: portfolio / task manager / repo analysis
- `AGENTS.md` — OpenAI Codex CLI agent instructions (7th IDE support)

### Changed
- `PRISTINO.md` — Added Environment Detection section (IDE adaptation + model tiers + auto-prime)
- All 6 IDE files now include self-identification header (IDE, triad mode, tools, capabilities)
- `CLAUDE.md` — Added `## Environment` header
- `GEMINI.md` — Added `## Environment` header
- `.cursorrules` — Added environment comment
- `.windsurfrules` — Added environment comment
- `.github/copilot-instructions.md` — Added `## Environment` header

### Architecture
- **Two-axis detection**: IDE (where) × Model (what) — independent concerns
- **Triad adaptation**: full (Claude Code) / sequential (Gemini, Codex) / checklist (Cursor, Windsurf) / suggestion (Copilot)
- **Model tiers**: Heavy >100K (full load) / Medium 32-100K (Constitution + skills) / Light <32K (active skill only)
- **7 IDEs supported**: Claude Code, Gemini, Cursor, Windsurf, Copilot, Antigravity, Codex

## [1.3.0] - 2026-03-22

### Added — Pristino Robustness: Soul, Triad, IDE-Agnostic
- `PRISTINO.md` — Soul document: identity, bootstrap sequence, triad pattern, delegation rules, vibe coding protocol
- `PRISTINO-INDEX.md` — Auto-generated master registry of all 116 skills, 103 agents, 104 commands, 103 prompts
- `scripts/generate-pristino-index.sh` — Index generation script
- `GEMINI.md` — Root-level Gemini agent instructions (promoted from .agent/rules/)
- `.github/copilot-instructions.md` — VS Code Copilot instructions
- `.cursorrules` — Cursor IDE rules
- `.windsurfrules` — Windsurf IDE rules

### Changed
- `adk-orchestrator.md` — Rewritten as Pristino with triad-first routing (Lead + Support + Guardian)
- `CLAUDE.md` — Added soul bootstrap, triad-first routing table, updated to v1.3.0
- Fixed stale Constitution refs: v4.1.0/v5.1.0 → v5.2.0 in quality-guardian, session-protocol
- All 5 IDE files share common soul (PRISTINO.md) with IDE-specific wrappers

### Architecture
- **Triad pattern**: default operating mode. Every non-trivial request → Lead + Support + Guardian
- **Bootstrap sequence**: PRISTINO.md → Constitution → PRISTINO-INDEX → ready
- **IDE-agnostic**: same orchestrator works in Claude Code, Gemini, Copilot, Cursor, Windsurf

## [1.2.1] - 2026-03-22

### Changed — Sequential-First Discipline (Constitution v5.2.0)
- **Principle XVI rewritten**: "Parallel-Ready Workflow" → "Sequential-First, Parallel-Ready Workflow"
  - Default: sequential along critical path (marco logico)
  - Parallel ONLY when plan has `[PARALLEL-OK]` tags
  - WIP limit: 3 agents maximum concurrent
  - Forward-only: no parallel task waits for another
  - 4-point eligibility check required before parallel launch
- `parallel-workflow` skill v2.0.0 — Sequential-first with eligibility checklist and batch execution
- `pipeline-conductor` agent — Sequential-by-default anti-pattern, plan-gated parallelism
- Constitution version bumped to v5.2.0
- Governance section: sequential-first enforcement, burden of proof on parallelism

## [1.2.0] - 2026-03-22

### Added — Constitution v5.1.0 Upgrade
- `references/ontology/constitution-v5.1.0.md` — 18 principles (added XVII Continuous Learning, XVIII Indexable Repository), Workspace section, Session Protocol, Operational Logs
- **7 New Skills**: `continuous-learning`, `session-protocol`, `workspace-governance`, `changelog-management`, `tasklog-management`, `indexability-validator`, `repository-organization`

### Changed
- Constitution upgraded from v4.1.0 to v5.1.0
- `adk-orchestrator` agent — Added session-protocol and continuous-learning skills, v5.1.0 reference
- `quality-guardian` agent — Added indexability-validator and continuous-learning skills
- `plugin.json` — Bumped to v1.2.0 with 116 skills count

## [1.1.0] - 2026-03-22

### Added — Constitution v4.1.0 Integration
- `references/ontology/constitution-v4.1.0.md` — Supreme governance document (16 principles, 4 quality gates, Socratic debate mechanism)
- **8 New Skills**: `socratic-debate`, `bdd-full-spectrum`, `input-sanitization`, `parallel-workflow`, `ssh-deployment`, `integrity-chain-validation`, `dual-layer-verification`, `lighthouse-ci`
- **2 New Agents**: `socratic-debater` (structured debate when confidence < 0.95), `integrity-validator` (governance chain validation)
- **2 New Commands**: `/jm-adk:debate` (trigger Socratic debate), `/jm-adk:validate-chain` (validate integrity chain)
- **2 New Prompts**: `86-bdd-full-spectrum.md` (multi-angle Gherkin generation), `102-socratic-debate.md` (debate protocol)

### Changed — Harmonization
- `security-testing` skill — Added sanitization hierarchy (strip > escape > allowlist), dual-layer verification
- `test-strategy` skill — Added BDD full-spectrum angles, runner-agnostic Gherkin
- `e2e-testing` skill — Added production URL verification, parallel browser matrix
- `code-review` skill — Added sustainability assessment (Constitution XII)
- `discovery-orchestration` skill — Added plan file generation, Constitution phase gates, Socratic trigger
- `adk-orchestrator` agent — Added Constitution awareness, Socratic routing, Think-Act-Verify workflow
- `quality-guardian` agent — Reconciled G0-G3 with Constitution definitions
- `pipeline-conductor` agent — Added parallel workflow support (Constitution XVI)
- `security-scanner` agent — Added input sanitization audit, dual-layer verification

## [Unreleased]

### Added
- `docs/getting-started.md` — 5-minute quickstart guide
- `docs/mcp-integration.md` — MCP server integration guide
- `docs/catalog.md` — Interactive browsable catalog of all 101 agents, skills, commands
- `docs/architecture-diagram.md` — Mermaid diagrams: pipeline, DSVSR, quality gates, routing
- `docs/advanced/` — Custom skills, custom agents, metacognition deep-dive, production deployment
- `docs/examples/` — Real-world walkthrough examples (e-commerce, task manager, portfolio)
- `commands/onboarding.md` — Guided first-use experience (`/jm-adk:onboarding`)
- `CONTRIBUTING.md` — Contribution guide with Code of Conduct
- `SECURITY.md` — Security policy and vulnerability reporting
- `CHANGELOG.md` — Version history with semantic versioning
- `.github/workflows/validate.yml` — CI: validates frontmatter, counts, links, secrets
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template
- `.github/ISSUE_TEMPLATE/` — Bug report and feature request templates

### Changed
- `README.md` — Rewritten for adoption: badges, onboarding CTA, examples table, docs table, community links

## [1.0.0-alfa] - 2026-03-15

### Added
- **101 Specialist Agents** across 8 categories: Orchestration (5), Discovery (20), Architecture (20), Frontend (20), Backend/Firebase (15), Quality/Testing (12), Deployment (5), Documentation (4)
- **101 Reusable Skills** across 6 domains: Discovery (20), Architecture (20), Frontend (25), Backend/Firebase (20), Quality (10), Deployment (6)
- **101 Slash Commands** for the full development lifecycle: pipeline, discovery, architecture, scaffold, create, quality, deploy
- **101 Prompt Templates** in 6 categories: Discovery (20), Architecture (20), Development (30), Quality (15), Deployment (10), Meta (6)
- **11 Master Workflows**: analyze, develop, scaffold, create, review, evolve, repair, search, ship, menu, status
- **5 Project Templates**: firebase, react, angular, vanilla-js, node-api
- **Governance Framework**: Constitution (7 articles), Intent Integrity Chain, Metacognition Protocol (DSVSR)
- **Quality Gates**: G0 (Security), G1 (Evidence + Constitution), G2 (Lighthouse), G3 (Deployment)
- **Dual Format Support**: Claude Code plugin + Antigravity Kit (`.agent/` directory)
- **Automation**: SessionStart hook, PostToolUse validation, BM25 skill search, skills index generation
- **Stack**: HTML5/CSS3/JS + Angular 18+ + React 19+ + Firebase + Hostinger + Google Ecosystem

### Technical Details
- Plugin manifest: `.claude-plugin/plugin.json`
- Antigravity manifest: `.agent/skills_index.json` (607 lines)
- Python scripts: `generate_index.py`, `search_skills.py`, `validate_skills.py`
- Governance: `.specify/CONSTITUTION.md` with 7 articles
- Metacognition: DECOMPOSE → SOLVE → VERIFY → SYNTHESIZE → REFLECT

---

## Breaking Changes Policy

This project follows semantic versioning:

- **Major** (x.0.0): Breaking changes to skill structure, agent API, or governance model
- **Minor** (0.x.0): New skills, agents, commands, or prompts (backward-compatible)
- **Patch** (0.0.x): Bug fixes, doc improvements, minor enhancements

During the `alfa` phase, breaking changes may occur in minor versions. After `1.0.0` stable release, breaking changes will only occur in major versions with migration guides.

[Unreleased]: https://github.com/JaviMontano/jm-agentic-development-kit/compare/v1.0.0-alfa...HEAD
[1.0.0-alfa]: https://github.com/JaviMontano/jm-agentic-development-kit/releases/tag/v1.0.0-alfa
