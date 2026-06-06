---
name: environment-detection
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Detect IDE and model at session start. Adapt triad mode, skill loading,
  and capability profile. Auto-prime for optimal performance per environment. [EXPLICIT]
  Trigger: "detect environment", "what IDE", "configure environment", "auto-prime"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Environment Detection

> Detect the runtime from evidence before choosing orchestration depth.

## TL;DR

Detect the active assistant host, model tier, available capabilities, and safe bootstrap loading plan from deterministic local signals. Use `assets/signal-policy.json`, `assets/capability-profile-policy.json`, `assets/model-tier-policy.json`, and `assets/loading-policy.json` as the source contracts. Validate JSON reports with `scripts/check.sh`. [EXPLICIT]

## Procedure

### Step 1: Discover
- Collect local instruction markers: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, Copilot config, or user-provided runtime notes. [EXPLICIT]
- Collect available tool markers from the active session: read/write/shell, subagent support, hooks/MCP support, browser access, and network access. [EXPLICIT]
- Collect model context data only when supplied by the runtime or user; do not infer capacity from the current date, network, marketing pages, or random guesses. [EXPLICIT]
- Assign every signal a stable `id`, `source`, `kind`, `value`, and evidence tag. [EXPLICIT]

### Step 2: Analyze
- Map IDE to triad mode using `assets/capability-profile-policy.json`: `claude-code=full`, `codex|gemini|antigravity=sequential`, `cursor|windsurf=checklist`, `copilot=suggestion`, `unknown=sequential`. [EXPLICIT]
- Map model tier by context budget using `assets/model-tier-policy.json`: heavy `>=100000`, medium `32000..99999`, light `<32000`, unknown when budget is unavailable. [EXPLICIT]
- Treat conflicting signals as `warn`; select the safest capability mode supported by actual tools rather than the most ambitious file marker. [EXPLICIT]
- Prefer conservative loading when evidence is missing: no L3 full history, no all-skills preload, no private transcript persistence. [EXPLICIT]

### Step 3: Execute
- Emit an environment report that includes signals, capabilities, decisions, loading plan, validation status, and residual risks. [EXPLICIT]
- Use L1/L2/L3/SKIP levels from `assets/loading-policy.json`; allow at most one L3 resource unless the user explicitly authorizes a deeper investigation. [EXPLICIT]
- Persist only summarized session state when an approved target is present. [EXPLICIT]
- Report environment to user with evidence tags:
  ```
  Environment detected:
    IDE: {ide} | Model: {model} | Tier: {tier}
    Triad: {mode} | Tools: {available_tools}
    Signals: {count} | Confidence: {confidence}
  ```

### Step 4: Validate
- Confirm detected IDE matches local signals and tool availability. [EXPLICIT]
- Confirm model tier matches the supplied context budget. [EXPLICIT]
- Confirm the loading plan is bounded for the tier. [EXPLICIT]
- Run `bash skills/environment-detection/scripts/check.sh` when a JSON report is produced. [EXPLICIT]
- If mismatch remains, emit `warn` or `block` rather than a false `pass`. [EXPLICIT]

## Quality Criteria

- [ ] IDE is backed by at least one local signal or explicitly marked `unknown`.
- [ ] Triad mode matches the deterministic IDE policy and actual capabilities.
- [ ] Model tier matches context budget thresholds or is explicitly `unknown`.
- [ ] Loading plan is bounded to the tier and avoids full transcript/history persistence.
- [ ] Conflicts degrade to `warn` or `block`; they never produce confident `pass`.
- [ ] Evidence tags appear on all report signals and decisions.
- [ ] Machine-readable reports pass the offline validator.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Assuming Claude Code always | May be running in Codex, Cursor, Copilot, Gemini, or unknown host | Detect from local signals and tools |
| Loading full index in light/unknown tier | Exhausts context window or hides critical user input | Use L1/L2 and one active L3 only when justified |
| Calling network to identify the model | Makes detection non-reproducible and time-dependent | Use provided runtime/model data or mark unknown |
| Treating conflicting signals as pass | Produces false confidence and wrong orchestration | Emit `warn` with explicit conflicts |
| Persisting full transcript | Leaks context and bloats future sessions | Persist only summarized state with authorization |

## Related Skills

- `session-protocol` — Environment detection is Step 0 of session init
- `context-optimization` — Context budget depends on detected tier
- `session-start-bootstrap` — Consumes detection results during startup
- `context-window-management` — Applies tier-specific budget controls

## Usage

Example invocations:

- "Detect this environment and give me the safe bootstrap plan."
- "Which IDE/model tier are we in, and what mode should the agent use?"
- "Run environment detection before starting the session."

## Assumptions & Limits

- Assumes access to local workspace signals and the active tool list. [EXPLICIT]
- Does not identify a model from private account state, browser cookies, or remote webpages. [EXPLICIT]
- Uses conservative defaults when context budget or model identity is unavailable. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No instruction files | Use tool signals and mark file evidence as missing |
| Conflicting IDE markers | Select safest supported mode and emit `warn` |
| Unknown context budget | Mark tier `unknown` and avoid L3/full-history loading |
| Network-only model claim | Reject as evidence; ask for local/runtime signal |
| User requests full preload | Require explicit risk acknowledgement and budget evidence |

## Deterministic Resources

| Resource | Purpose |
|----------|---------|
| `assets/signal-policy.json` | Allowed and rejected detection signals |
| `assets/capability-profile-policy.json` | IDE to triad/capability mapping |
| `assets/model-tier-policy.json` | Context budget thresholds |
| `assets/loading-policy.json` | Tier-safe bootstrap loading |
| `assets/environment-report-contract.json` | Required JSON report fields |
| `scripts/check.sh` | Offline fixture validation |
