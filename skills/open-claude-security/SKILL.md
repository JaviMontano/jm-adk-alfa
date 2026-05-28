---
name: open-claude-security
description: >
  This skill should be used when the user asks to "design secure Claude Code environment",
  "harden Claude Code configuration", "audit Claude Code security", "secure MCP servers",
  "review CLAUDE.md for injection", "design agent permission model", "secure OpenClaw
  deployment", "isolate agent tools", or mentions Claude Code security, OpenClaw isolation,
  MCP authentication, hook security, prompt injection defense, agent isolation, subagent
  security, or agent team boundaries. Produces comprehensive security architecture for
  Claude Code and OpenClaw deployments covering threat modeling, injection defense,
  permission design, MCP transport security, multi-agent isolation, container isolation,
  and audit trails. Use this skill whenever Claude Code or OpenClaw security posture
  needs to be designed or evaluated, even if they don't explicitly ask for
  "open-claude-security". [EXPLICIT]
argument-hint: "project-or-org-name [--personal | --team | --enterprise]"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
version: 1.0.0
---

# Open Claude Security: Designing Secure Claude Code & OpenClaw Architectures

Claude Code and OpenClaw expose a layered attack surface: **Gateway** (messaging adapters) → **Core** (agent engine on local machine or Docker) → **Tools** (File System, Terminal/Bash, Browser, APIs). This skill produces comprehensive security architectures that map every layer and extension point to defense controls, threat models, and isolation strategies. [EXPLICIT]

## Principio Rector

**Cada capa es una frontera de confianza. Cada herramienta es un privilegio, no un derecho.** La arquitectura segura no depende de un perimetro — aisla cada capa, restringe cada herramienta, y audita cada accion.

### Security Architecture Philosophy

1. **Every layer is a trust boundary.** The OpenClaw architecture has 3 trust boundaries: Gateway (messaging → agent), Core (agent → tools), and Tools (agent → external systems). Security controls must exist at each boundary, not just the perimeter. [EXPLICIT]
2. **Every tool is a privilege, not a right.** File System, Terminal/Bash, Browser, APIs — each tool grants capabilities that can be weaponized. Start with zero tools, add with documented justification, enforce with hooks. [EXPLICIT]
3. **Isolation is the foundation.** Docker containers for the Core, network policies for egress, separate MCP scopes per agent role. Defense in depth, not defense in hope. [EXPLICIT]
4. **Personal deployments need the same rigor as enterprise.** A single-user OpenClaw on your laptop has the same attack surfaces as a team deployment — the difference is blast radius, not threat model. [EXPLICIT]

---

## Inputs

Parse `$ARGUMENTS`: `$1` = project/org name, `$2` = deployment mode. [EXPLICIT]

**Deployment modes:**
- `--personal`: Single-user, local machine or Docker. Optimizes for privacy and minimal surface. [EXPLICIT]
- `--team`: Multi-developer shared environment. Adds collaboration controls and scope hierarchy. [EXPLICIT]
- `--enterprise`: Organization-wide with managed policies. Adds compliance mapping and centralized governance. [EXPLICIT]
- Default: auto-detect from existing configuration files. [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso` [EXPLICIT]
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{VARIANTE}`: `ejecutiva` (~40% — S1 + S3 + S7) | `tecnica` (full 7 sections, default)

## When to Use

- Designing security architecture for Claude Code or OpenClaw deployments [EXPLICIT]
- Setting up a personal OpenClaw with controlled tool access [EXPLICIT]
- Auditing existing CLAUDE.md, settings.json, .mcp.json configurations [EXPLICIT]
- Hardening the Gateway → Core → Tools pipeline [EXPLICIT]
- Designing subagent vs agent-team isolation boundaries [EXPLICIT]
- Securing Docker-containerized OpenClaw Core instances [EXPLICIT]
- Planning multi-agent workflows with tool authorization controls [EXPLICIT]

## When NOT to Use

| Need | Use Instead | Why |
|------|-------------|-----|
| General app security architecture | `5019-security-architecture` | System-level, not agent-level |
| Building OpenClaw from scratch | `9081-open-claw-builder` | Builds agents; this skill secures them |
| Creating hooks (not auditing) | `9038-hook-creator` | Builds hooks; this skill audits them |
| Configuring MCP (not securing) | `9070-mcp-creator` | Sets up MCP; this skill evaluates posture |
| Container isolation implementation | `5023-openclaw-isolation` | Implements Docker/network isolation |
| Tool authorization implementation | `5024-openclaw-tool-auth` | Implements per-tool auth controls |
| Personal deployment execution | `5025-openclaw-personal-deploy` | Executes the secure deployment |

---

## Before Generating Architecture

Detect existing configuration and deployment context:

```
Glob .claude/settings.json .claude/settings.local.json .mcp.json CLAUDE.md
Glob **/CLAUDE.md
Glob docker-compose*.yml Dockerfile .dockerignore
Glob .claude/hooks/*.sh .claude/hooks/*.py
```

Load reference materials:

```
Read ${CLAUDE_SKILL_DIR}/references/security-patterns.md
Read ${CLAUDE_SKILL_DIR}/references/threat-model.md
Read ${CLAUDE_SKILL_DIR}/references/openclaw-architecture.md
```

If an existing configuration is found, start with baseline audit. If no configuration exists, generate security-first templates from scratch. [EXPLICIT]

---

## Delivery Structure: 7 Sections

### S1: OpenClaw Architecture Threat Model

The OpenClaw architecture has 3 layers with distinct trust boundaries. Apply STRIDE to each layer and its components. [EXPLICIT]

**Architecture layers:**

```
┌─────────────────────────────────────────────────────────┐
│  GATEWAY LAYER                                          │
│  WhatsApp / Slack / Telegram / HTTP API                 │
│  Trust boundary: External message → Agent input         │
├────────────────────┬────────────────────────────────────┤
│                    │  Local & Private                    │
│                    ▼                                     │
│  ┌─────────────────────────────────────┐                │
│  │  CORE LAYER (Local Machine/Docker)  │                │
│  │  Agent Engine + Security Checkpoints│                │
│  │  Memory (SQLite) + Config           │                │
│  └──────┬──────┬──────┬──────┬────────┘                │
│         │      │      │      │                          │
│         ▼      ▼      ▼      ▼                          │
│  ┌──────┐ ┌────┐ ┌───────┐ ┌────┐                      │
│  │ File │ │Term│ │Browser│ │APIs│  TOOL LAYER           │
│  │System│ │Bash│ │  MCP  │ │MCP │  Trust boundary:      │
│  └──────┘ └────┘ └───────┘ └────┘  Agent → External    │
└─────────────────────────────────────────────────────────┘
```

**STRIDE per layer:**

| Layer | S | T | R | I | D | E | Top Risk |
|-------|---|---|---|---|---|---|----------|
| Gateway | Message spoofing, user impersonation | Payload tampering in transit | No sender audit trail | User data in message logs | Flood/spam disabling agent | Gateway bypass to Core | Unauthenticated message access [EXPLICIT] |
| Core | CLAUDE.md fake system instructions | Config injection, context manipulation | No action logging by default | Context leak between agents | Resource exhaustion, recursive spawning | dangerouslySkipPermissions, hook bypass | Instruction injection via CLAUDE.md [EXPLICIT] |
| Tools | MCP server impersonation | Tool result injection | No tool use audit trail | Data exfiltration via remote MCP | Tool hang blocking agent | Shell injection via Bash tool | Uncontrolled Bash execution [EXPLICIT] |

**Attacker profiles:**

| Profile | Access | Targets | Personal Deploy Risk |
|---------|--------|---------|---------------------|
| External message sender | Gateway only | Prompt injection via message content | High if gateway is public [EXPLICIT] |
| Malicious MCP package | Tool layer | Supply chain, code execution | Medium — personal deploys use fewer MCPs [EXPLICIT] |
| Local process on same machine | Core layer | Env vars, config files, memory DB | High if not containerized [EXPLICIT] |
| Compromised dependency | All layers | Transitive code execution | High — personal deploys often skip audits [INFERRED] |

Detailed STRIDE tables and attack trees in `references/threat-model.md`. [EXPLICIT]

---

### S2: CLAUDE.md & Configuration Injection Defense

CLAUDE.md is the highest-risk extension point — it directly controls agent behavior and is modifiable by anyone with repository write access. [INFERRED]

**Injection patterns** (details in `references/security-patterns.md`):

| Pattern | Detection | Severity |
|---------|-----------|----------|
| Hidden Unicode instructions | Regex: `[\u200B-\u200F\u2028-\u202F\uFEFF]` | Critical [EXPLICIT] |
| HTML comment injection | Grep `<!--` with imperative verbs | High [EXPLICIT] |
| Subdirectory CLAUDE.md override | `find . -name "CLAUDE.md"` — flag non-root | High [EXPLICIT] |
| Social engineering phrases | Scan for "per Anthropic", "admin override", "ignore previous" | High [EXPLICIT] |
| Scope confusion | CLAUDE.md referencing settings.json fields | Medium [EXPLICIT] |

**Defense controls:**

| Control | Implementation | Priority |
|---------|---------------|----------|
| Pre-commit validation | Reject CLAUDE.md with non-printable chars or authority claims | P0 [EXPLICIT] |
| Location allowlist | Only permit CLAUDE.md at documented locations | P0 [EXPLICIT] |
| PR review gate | Security-aware reviewer for CLAUDE.md changes | P1 [EXPLICIT] |
| Content hash verification | SHA-256 at session start, verify on subsequent reads | P2 [INFERRED] |

---

### S3: Permission Model & Tool Authorization

Design least-privilege tool configurations. The OpenClaw Tool Layer (File System, Terminal/Bash, Browser, APIs) requires per-tool authorization — not blanket access. [EXPLICIT]

**Role-based permission templates:**

| Role | allowed-tools | Tool Layer Access | Rationale |
|------|--------------|-------------------|-----------|
| Read-only analyst | `Read`, `Glob`, `Grep` | File System (read) | Cannot modify or execute [EXPLICIT] |
| Standard developer | `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash` | File System + Terminal | Full dev workflow [EXPLICIT] |
| Personal OpenClaw | `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash` + selected MCPs | File System + Terminal + controlled APIs | Personal use with explicit MCP selection [EXPLICIT] |
| CI/CD agent | `Read`, `Glob`, `Grep`, `Bash` | File System (read) + Terminal | No source modification [EXPLICIT] |
| Restricted agent | `Read`, `Glob`, `Grep` | File System (read) only | Minimum surface for research tasks [EXPLICIT] |

**Settings scope hierarchy** (highest precedence first):

| # | Scope | File | Git | Security Role |
|---|-------|------|-----|---------------|
| 1 | Project local | `.claude/settings.local.json` | No | Personal overrides, secrets [EXPLICIT] |
| 2 | Project shared | `.claude/settings.json` | Yes | Team baseline [EXPLICIT] |
| 3 | User global | `~/.claude/settings.json` | No | Personal defaults [EXPLICIT] |
| 4 | Enterprise | Managed policy | Central | Enforced floors [INFERRED] |

**dangerouslySkipPermissions**: This flag removes all permission checks. There is no legitimate production use case. Scan: `grep -r "dangerouslySkipPermissions" .claude/ ~/.claude/`. CI/CD gate: block any commit containing this flag. [EXPLICIT]

---

### S4: MCP Server & Transport Security

Each MCP server is a trust boundary in the Tool Layer. Personal deployments typically use fewer MCPs but often skip vetting. [EXPLICIT]

**Transport security:**

| Transport | Security | Personal Deploy Recommendation |
|-----------|----------|-------------------------------|
| stdio | No network exposure. Child process on same machine. | Preferred for all local tools [EXPLICIT] |
| HTTP | Requires TLS 1.3. Auth via headers. Network-exposed. | Only for essential remote APIs [EXPLICIT] |
| SSE | Deprecated. | Never use [EXPLICIT] |

**MCP vetting checklist:**

| Check | Method | Severity |
|-------|--------|----------|
| Source verification | npm/GitHub audit, known publisher | Critical [EXPLICIT] |
| Transport encryption | TLS 1.3 for HTTP; local for stdio | Critical [EXPLICIT] |
| Auth mechanism | Token in env var, rotation policy | High [EXPLICIT] |
| Tool scope | Minimal tools, no unnecessary capabilities | High [EXPLICIT] |
| Data classification | Document data types flowing to server | High [EXPLICIT] |
| Network egress | Where does the MCP connect externally | Medium [INFERRED] |
| Dependency health | `npm audit`, SBOM | Medium [EXPLICIT] |

**Personal deployment MCP strategy**: Use stdio-only MCPs for maximum isolation. If a remote MCP is needed, use HTTP with TLS and env-var tokens. Keep the total MCP count minimal — each server increases the attack surface. [EXPLICIT]

---

### S5: Subagent & Agent Team Security

Two multi-agent patterns require different security controls. Both are relevant for personal OpenClaw workflows. [EXPLICIT]

**Pattern 1: Subagents** (Main Agent spawns workers, collects results)

```
Main Agent → Spawn Subagent → Work → Result → Report
                                                 ↑
            (each subagent isolated, reports back to main)
```

| Security Concern | Risk | Control |
|-----------------|------|---------|
| Context inheritance | Forked context includes parent conversation with potential secrets | Pass only task-specific data, not full conversation [EXPLICIT] |
| Permission inheritance | Sub-agent inherits parent allowed-tools | Define per-subagent allowed-tools restriction [INFERRED] |
| Recursive spawning | Subagent spawns subagents → resource exhaustion | Enforce depth=1 limit [EXPLICIT] |
| Result injection | Subagent result contains instruction-like content | Treat all subagent results as untrusted data [EXPLICIT] |

**Pattern 2: Agent Teams** (Team Lead assigns tasks, teammates communicate)

```
Team Lead → Shared Task List → Teammates claim & communicate
                                    ↕ (peer communication)
```

| Security Concern | Risk | Control |
|-----------------|------|---------|
| Shared task list poisoning | Compromised teammate injects malicious tasks | Task validation before execution [INFERRED] |
| Inter-agent communication | Teammate sends instruction injection to peer | Content isolation between agents [INFERRED] |
| Shared MCP access | All teammates access same MCP servers | Per-role MCP access restrictions [INFERRED] |
| Task escalation | Teammate claims tasks above its permission level | Task-permission matrix enforcement [INFERRED] |

**Personal deployment recommendation**: Use the Subagent pattern (simpler, easier to secure). Reserve Agent Teams for complex workflows where peer communication adds measurable value. Every additional agent multiplies the attack surface. [INFERRED]

---

### S6: Container Isolation & Network Security

For personal OpenClaw deployments, Docker containerization provides the strongest isolation layer. [EXPLICIT]

**Isolation architecture:**

| Layer | Isolation Method | What It Protects |
|-------|-----------------|------------------|
| Core process | Docker container with restricted capabilities | Host system from agent actions [EXPLICIT] |
| File system | Bind mount only the working directory, read-only where possible | Host files outside project scope [EXPLICIT] |
| Network | Docker network policy: block all egress except allowed endpoints | Data exfiltration, phone-home [EXPLICIT] |
| Secrets | Docker secrets or env-file (not in image) | Credentials from container inspection [EXPLICIT] |
| Resources | CPU/memory limits via Docker | Resource exhaustion DoS [EXPLICIT] |

**Docker security baseline for personal OpenClaw:**

```yaml
# docker-compose.yml security defaults
services:
  openclaw:
    security_opt: ["no-new-privileges:true"]
    read_only: true
    tmpfs: ["/tmp"]
    cap_drop: ["ALL"]
    cap_add: ["NET_BIND_SERVICE"]  # only if needed
    mem_limit: "2g"
    cpus: "2.0"
    networks: ["openclaw-net"]

networks:
  openclaw-net:
    driver: bridge
    internal: true  # no external access by default
```

**Network egress control**: Start with `internal: true` (no internet). Add specific allowed endpoints as needed. Document every egress exception with justification. [EXPLICIT]

For full container isolation implementation, use companion skill `5023-openclaw-isolation`. [EXPLICIT]

---

### S7: Audit Trail & Compliance

**Audit logging requirements:**

| Event | What to Log | Method |
|-------|-------------|--------|
| Tool execution | Tool name, input (redacted), timestamp, duration | PostToolUse hook [EXPLICIT] |
| MCP communication | Server, tool called, request size, status | MCP transport logging [EXPLICIT] |
| Hook execution | Event, script, exit code, duration | Hook wrapper script [EXPLICIT] |
| Gateway messages | Sender, platform, timestamp (not content) | Gateway adapter logging [EXPLICIT] |
| Agent lifecycle | Start, end, tool count, agent tree depth | Session metadata [INFERRED] |
| Security events | Blocked tools, injection attempts, timeout kills | Security hook logging [EXPLICIT] |

**Compliance mapping:**

| Control | SOC 2 | ISO 27001 | Personal Deploy |
|---------|-------|-----------|-----------------|
| Least privilege | CC6.1 | A.9.2.3 | Role-based allowed-tools [EXPLICIT] |
| Secrets management | CC6.7 | A.10.1.2 | Env vars, no hardcoded [EXPLICIT] |
| Audit logging | CC7.2 | A.12.4.1 | PostToolUse hooks [EXPLICIT] |
| Transport encryption | CC6.7 | A.13.1.1 | TLS for HTTP MCPs [EXPLICIT] |
| Container isolation | CC6.8 | A.13.1.3 | Docker with network policy [EXPLICIT] |

For operational hardening steps, load `references/hardening-checklist.md`. [EXPLICIT]

---

## Companion Skill Kit

This skill is the architecture layer. For implementation, use the companion skills:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `5023-openclaw-isolation` | Docker container security, network policies, resource limits | After architecture is approved, during implementation [EXPLICIT] |
| `5024-openclaw-tool-auth` | Per-tool authorization hooks, gateway auth, API scope management | When implementing tool-level controls [EXPLICIT] |
| `5025-openclaw-personal-deploy` | End-to-end personal secure deployment with hardened defaults | When deploying OpenClaw for personal use [EXPLICIT] |

**Recommended workflow**: `5022` (design architecture) → `5023` (isolation) → `5024` (tool auth) → `5025` (deploy). [EXPLICIT]

---

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|----------|---------|------------|-------------|
| Docker containerization | Host isolation, resource limits | Added complexity, Docker dependency | Personal and team deploys [EXPLICIT] |
| Zero tools default | Maximum security | Must add each tool explicitly | All environments [EXPLICIT] |
| stdio-only MCPs | No network exposure | No remote API integration | Data-sensitive, personal use [EXPLICIT] |
| PreToolUse security hooks | Deterministic tool policy | 5s latency per tool call | Compliance-required [EXPLICIT] |
| Subagent over Agent Team | Simpler security, depth control | No peer communication | Personal deploys, simple workflows [INFERRED] |
| Network internal:true | Zero egress by default | Must allowlist every endpoint | Maximum isolation [EXPLICIT] |

---

## Assumptions & Limits

**Assumptions:**
- Deployment uses Claude Code, OpenClaw, or compatible agent framework [EXPLICIT]
- User has Docker available for container isolation (recommended but not required) [EXPLICIT]
- MCP servers are sourced from known publishers or built internally [INFERRED]
- Personal deployments prioritize privacy and minimal attack surface over feature breadth [EXPLICIT]

**Limits:**
- Does not implement container configs — use `5023-openclaw-isolation` [EXPLICIT]
- Does not implement tool auth hooks — use `5024-openclaw-tool-auth` [EXPLICIT]
- Does not execute deployment — use `5025-openclaw-personal-deploy` [EXPLICIT]
- Cannot detect runtime prompt injection — designs static defenses and monitoring [EXPLICIT]
- Plugin security model is evolving — recommendations as of March 2026 [EXPLICIT]

---

## Edge Cases

1. **Personal deploy on bare metal (no Docker)**: No container isolation available. Compensate with: strict allowed-tools (no Bash unless hooked), stdio-only MCPs, PreToolUse validation hooks for every tool, file system access limited to project directory via CLAUDE.md instructions. Reduced isolation — document accepted risk. [EXPLICIT]

2. **OpenClaw with public Gateway (WhatsApp/Telegram)**: Gateway accepts messages from anyone. Implement: sender allowlist (only your phone number/user ID), rate limiting, message content sanitization before agent processing, no auto-execution of commands from messages. [EXPLICIT]

3. **Multi-agent personal workflow (3+ agents)**: Personal user runs multiple specialized agents (code-review, test-writer, deployment). Each agent needs separate allowed-tools. Use Subagent pattern with depth=1. Restrict MCP access per agent role. Monitor total resource consumption. [EXPLICIT]

4. **Air-gapped personal deployment**: No internet access. stdio-only MCPs, local LLM (Ollama), no remote plugins. Verify all dependencies are pre-installed. Document offline operation constraints in CLAUDE.md. [INFERRED]

5. **Migrating from permissive to hardened config**: User has been running with `dangerouslySkipPermissions: true`. Phase the transition: (1) enable logging hooks without blocking, (2) add PreToolUse hooks in monitor-only mode, (3) switch to blocking mode, (4) remove dangerouslySkipPermissions. [EXPLICIT]

---

## Good vs Bad Example

### Good: Personal Hardened OpenClaw

```json
// .claude/settings.json
{
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Glob", "Grep"],
    "deny": ["Bash(rm -rf *)", "Bash(curl * | sh)"]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "command": "python3 .claude/hooks/validate-bash.py",
      "timeout": 5000
    }],
    "PostToolUse": [{
      "command": "python3 .claude/hooks/audit-log.py",
      "timeout": 3000
    }]
  }
}
```

```yaml
# docker-compose.yml
services:
  openclaw:
    build: .
    security_opt: ["no-new-privileges:true"]
    read_only: true
    cap_drop: ["ALL"]
    mem_limit: "2g"
    volumes: ["./workspace:/app/workspace"]
    env_file: [".env"]
    networks: ["isolated"]
networks:
  isolated:
    internal: true
```

**Why good**: Minimal tools, Bash gated by hook, audit logging, Docker isolation with no egress, read-only filesystem, capabilities dropped, secrets in env-file. [EXPLICIT]

### Bad: Wide-Open Personal Deploy

```json
// .claude/settings.json
{ "permissions": { "allow": ["*"], "dangerouslySkipPermissions": true } }
```

```json
// .mcp.json with hardcoded token, committed to git
{ "mcpServers": { "all-apis": { "type": "http", "url": "http://api.example.com/mcp",
  "headers": { "Authorization": "Bearer sk-live-abc123" } } } }
```

**Why bad**: All tools unrestricted, no permission checks, HTTP without TLS, hardcoded token in git, no container isolation, no audit trail, no hooks. [EXPLICIT]

---

## Validation Gate

- [ ] Threat model covers Gateway + Core + Tool layers with STRIDE analysis [EXPLICIT]
- [ ] CLAUDE.md injection defenses with 3+ detection methods and controls [EXPLICIT]
- [ ] Permission model with role-based templates including personal deployment role [EXPLICIT]
- [ ] MCP vetting checklist applied to every configured server [EXPLICIT]
- [ ] Hook security reviewed: shell injection, env leakage, timeout [EXPLICIT]
- [ ] Subagent OR Agent Team isolation strategy defined with context controls [EXPLICIT]
- [ ] Container isolation specified (Docker security baseline or accepted risk if bare metal) [EXPLICIT]
- [ ] Network egress policy: default-deny with documented exceptions [EXPLICIT]
- [ ] Audit trail captures tool use, hooks, MCP, and gateway events [EXPLICIT]
- [ ] Companion skill workflow documented: 5022 → 5023 → 5024 → 5025 [EXPLICIT]
- [ ] Hardening checklist applied across all 5 phases [EXPLICIT]

---

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/threat-model.md` | STRIDE per layer, attack trees, risk register | S1 — always load [EXPLICIT] |
| `references/security-patterns.md` | 7 attack surface catalogs with payloads + defenses | S2-S5 — load for pattern matching [EXPLICIT] |
| `references/hardening-checklist.md` | 5-phase operational hardening guide | S3, S7 — load for implementation steps [EXPLICIT] |
| `references/openclaw-architecture.md` | OpenClaw Gateway→Core→Tools architecture, Docker isolation patterns, network policies | S1, S6 — load for architecture-specific controls [EXPLICIT] |

---

**Complexity tier**: Standard (references/) [EXPLICIT]
**Companion skills**: `5023-openclaw-isolation`, `5024-openclaw-tool-auth`, `5025-openclaw-personal-deploy` [EXPLICIT]
**Author:** Javier Montano | **Last updated:** 2026-03-27
