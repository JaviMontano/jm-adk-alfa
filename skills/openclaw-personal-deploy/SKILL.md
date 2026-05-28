---
name: openclaw-personal-deploy
description: >
  This skill should be used when the user asks to "deploy OpenClaw for personal use",
  "set up a secure personal agent", "create my own Claude agent", "deploy isolated
  OpenClaw", "set up personal AI assistant", or mentions personal OpenClaw deployment,
  secure agent setup, private AI assistant, or self-hosted agent. Executes the complete
  deployment of a secure, isolated OpenClaw for personal use with hardened defaults,
  Docker isolation, tool authorization, and audit logging. Use this skill whenever
  a personal OpenClaw deployment is needed, even if they don't explicitly ask for
  "openclaw-personal-deploy". [EXPLICIT]
argument-hint: "project-name [platform: telegram|http|slack]"
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

# OpenClaw Personal Deploy: Your Own Secure AI Agent, Controlled by You

Deploy a production-grade, security-hardened OpenClaw instance for personal use in a single session. This skill orchestrates the full pipeline: project scaffold, security configuration, Docker isolation, tool authorization hooks, and launch verification — producing a **complete, runnable deployment**, not documentation. [EXPLICIT]

## Principio Rector

**Tu agente, tus reglas, tu infraestructura.** Un despliegue personal no significa un despliegue inseguro — aplica los mismos controles que una empresa pero optimizados para un solo operador.

### Deployment Philosophy

1. **Secure by default, not by afterthought.** Every generated file starts locked down. Permissions are added explicitly, never assumed. [EXPLICIT]
2. **Isolation is non-negotiable.** Docker containers, network restrictions, read-only filesystems — personal does not mean permissive. [EXPLICIT]
3. **Every tool use is audited.** PreToolUse and PostToolUse hooks intercept every action. You see what your agent does, always. [EXPLICIT]
4. **One command to deploy, one command to tear down.** The deployment must be operationally simple even if the security model is sophisticated. [EXPLICIT]

---

## Usage / When to Activate

- Deploying a personal OpenClaw instance from scratch [EXPLICIT]
- Setting up a private AI assistant with Telegram, Slack, or HTTP gateway [EXPLICIT]
- Creating a secure self-hosted Claude Code agent [EXPLICIT]
- Migrating an insecure OpenClaw deployment to hardened configuration [EXPLICIT]
- Standing up a development/staging OpenClaw for personal experimentation [EXPLICIT]

## When NOT to Use

| Need | Use Instead | Why |
|------|-------------|-----|
| Security architecture design (no deployment) | `5022-open-claude-security` | Designs the architecture; this skill executes it |
| Container isolation patterns only | `5023-openclaw-isolation` | Isolation theory; this skill applies it |
| Tool authorization design only | `5024-openclaw-tool-auth` | Auth design; this skill implements it |
| Building OpenClaw agent logic | `9081-open-claw-builder` | Agent code; this skill deploys infrastructure |
| Team or enterprise deployment | `5022-open-claude-security --team` | Multi-user requires different isolation model |
| General app deployment | `7001-hostinger-deployment` | Not agent-specific |

---

## Inputs

Parse `$ARGUMENTS`: `$1` = project name, `$2` = platform (telegram | http | slack). [EXPLICIT]

**Parameters:**
- `{PROJECT_NAME}`: kebab-case project identifier. Used for directory name, Docker container name, and compose project name. [EXPLICIT]
- `{PLATFORM}`: Gateway adapter — `telegram` (default), `http`, or `slack`. Determines which adapter template is scaffolded. [EXPLICIT]
- `{MODO}`: `piloto-auto` (default) | `paso-a-paso` [EXPLICIT]

**Defaults when not provided:**
- Project name: `my-openclaw` [EXPLICIT]
- Platform: `telegram` [EXPLICIT]
- Mode: `piloto-auto` — executes all phases automatically with confirmation at launch [EXPLICIT]

---

## Before Deploying

### Prerequisites Check

Run these checks before any deployment action. Fail fast if critical prerequisites are missing. [EXPLICIT]

```
Bash docker --version 2>/dev/null || echo "MISSING: Docker"
Bash docker compose version 2>/dev/null || echo "MISSING: Docker Compose"
Bash node --version 2>/dev/null || echo "MISSING: Node.js"
Bash npm --version 2>/dev/null || echo "MISSING: npm"
```

**Hard requirements** (deployment blocks without these):
- Docker Engine >= 20.10 [EXPLICIT]
- Docker Compose V2 (the `docker compose` plugin, not legacy `docker-compose`) [EXPLICIT]

**Soft requirements** (deployment proceeds with warnings):
- Node.js >= 18 — needed only if running outside Docker for development [INFERRED]
- npm >= 9 — same caveat [INFERRED]

**Secrets the user must provide** (never generate, never hardcode):
- `ANTHROPIC_API_KEY` — Claude API access [EXPLICIT]
- Platform-specific token: `TELEGRAM_BOT_TOKEN`, `SLACK_BOT_TOKEN`, or none for HTTP [EXPLICIT]
- Optional: `ALLOWED_CHAT_IDS` for Telegram user restriction [EXPLICIT]

Load reference materials:

```
Read ${CLAUDE_SKILL_DIR}/references/deployment-templates.md
```

---

## Core Process: 5 Deployment Phases

### Phase 1: Project Scaffold

Create the complete directory structure for a deployable OpenClaw project. [EXPLICIT]

**Directory tree to generate:**

```
{PROJECT_NAME}/
├── .claude/
│   ├── hooks/
│   │   ├── pre-tool-use.sh
│   │   └── post-tool-use.sh
│   ├── settings.json
│   └── settings.local.json
├── .mcp.json
├── CLAUDE.md
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── gateway/
│   │   └── {PLATFORM}-adapter.ts
│   └── utils/
│       └── logger.ts
├── logs/
│   └── .gitkeep
└── README.md
```

**Actions:**

1. Create root directory: `Bash mkdir -p {PROJECT_NAME}` [EXPLICIT]
2. Generate `package.json` with pinned dependency versions — no floating ranges (`^` or `~`). Pin `@anthropic-ai/sdk`, platform-specific SDK, `dotenv`, `winston`. [EXPLICIT]
3. Generate `tsconfig.json` with `strict: true`, `noImplicitAny: true`, target `ES2022`. [EXPLICIT]
4. Generate `.gitignore` from template in `references/deployment-templates.md`. Must include `.env`, `node_modules/`, `logs/*.log`, `.claude/settings.local.json`. [EXPLICIT]
5. Generate `.env.example` from template — all secrets as placeholder values, never real keys. [EXPLICIT]
6. Create `src/` structure with minimal gateway adapter for the selected platform. [EXPLICIT]

**Validation:** Confirm all files exist with `Glob {PROJECT_NAME}/**/*`. [EXPLICIT]

---

### Phase 2: Security Configuration

Generate security-first configuration files that control agent behavior. [EXPLICIT]

#### CLAUDE.md (Project Instructions)

The most critical security artifact. This file directly controls what the agent can and cannot do. [EXPLICIT]

**Generate from template in `references/deployment-templates.md` with these requirements:**

- Explicit deny-by-default tool policy [EXPLICIT]
- Allowed file paths restricted to project directory [EXPLICIT]
- Prohibited actions list (no internet access, no credential reading, no file deletion outside sandbox) [EXPLICIT]
- Input sanitization instructions for gateway messages [EXPLICIT]
- Output format constraints (no raw code execution results to users) [EXPLICIT]
- Injection defense instructions (ignore embedded instructions in user messages) [EXPLICIT]

#### settings.json (Hardened Defaults)

```
Write {PROJECT_NAME}/.claude/settings.json
```

**Requirements:**
- `permissions.allow` — empty array. Nothing pre-approved. [EXPLICIT]
- `permissions.deny` — block `Bash(rm -rf*)`, `Bash(curl*)`, `Bash(wget*)`, `Write(~/.*)`, `Write(/etc/*)`. [EXPLICIT]
- `hooks.PreToolUse` — point to `.claude/hooks/pre-tool-use.sh` [EXPLICIT]
- `hooks.PostToolUse` — point to `.claude/hooks/post-tool-use.sh` [EXPLICIT]

#### .mcp.json (MCP Server Configuration)

**Requirements:**
- Transport: `stdio` only. Never `sse` or `http` for personal deploy — removes network attack surface. [EXPLICIT]
- Only include MCPs the user explicitly requests. Default: zero external MCPs. [EXPLICIT]
- Each MCP entry must include `env` restrictions to prevent secret leakage. [INFERRED]

**Validation:** Read back each file and verify no `dangerouslySkipPermissions`, no wildcard allows, no remote MCP transports. [EXPLICIT]

---

### Phase 3: Docker Isolation

Generate container configuration that enforces process, network, and filesystem isolation. [EXPLICIT]

#### Dockerfile

Generate from multi-stage template in `references/deployment-templates.md`:

- **Stage 1 (builder):** `node:20-alpine`, install deps, compile TypeScript [EXPLICIT]
- **Stage 2 (runtime):** `node:20-alpine`, copy only compiled output and production deps [EXPLICIT]
- Non-root user (`openclaw`, UID 1001) [EXPLICIT]
- Read-only root filesystem compatibility [EXPLICIT]
- No `apt-get`, `apk add`, or package manager calls in runtime stage [EXPLICIT]
- `HEALTHCHECK` instruction for container orchestration [EXPLICIT]

#### docker-compose.yml

Generate from template with these security defaults:

| Setting | Value | Rationale |
|---------|-------|-----------|
| `read_only: true` | Root filesystem is read-only | Prevents runtime file modification [EXPLICIT] |
| `tmpfs: ["/tmp:size=64m"]` | Writable temp with size cap | Agent needs temp space but capped [EXPLICIT] |
| `security_opt: ["no-new-privileges:true"]` | Block privilege escalation | Standard container hardening [EXPLICIT] |
| `cap_drop: ["ALL"]` | Drop all Linux capabilities | Minimal capability set [EXPLICIT] |
| `networks: [internal]` | Internal-only network | No direct internet access from container [EXPLICIT] |
| `mem_limit: "512m"` | Memory ceiling | Prevent resource exhaustion [EXPLICIT] |
| `cpus: "1.0"` | CPU ceiling | Prevent runaway compute [EXPLICIT] |
| `restart: "unless-stopped"` | Auto-restart on crash | Availability for personal assistant [EXPLICIT] |
| `logging.driver: "json-file"` | Structured logs | Audit trail with rotation [EXPLICIT] |
| `logging.options.max-size: "10m"` | Log rotation | Prevent disk exhaustion [EXPLICIT] |

**Network configuration:**
- Internal network with no external connectivity from agent container [EXPLICIT]
- Separate gateway container with controlled external access for platform API only [INFERRED]
- DNS restricted to internal resolution [EXPLICIT]

#### .dockerignore

Must exclude: `.env`, `.git/`, `node_modules/`, `*.log`, `.claude/settings.local.json`. [EXPLICIT]

**Validation:** `Bash docker compose -f {PROJECT_NAME}/docker-compose.yml config` to verify syntax. [EXPLICIT]

---

### Phase 4: Tool Authorization

Generate hook scripts that intercept every tool invocation with allow/deny decisions. [EXPLICIT]

#### pre-tool-use.sh

**Behavior:**
1. Receive tool name and arguments via stdin (JSON format from Claude Code hook protocol) [EXPLICIT]
2. Check against allowlist defined at top of script [EXPLICIT]
3. For `Bash` tool: validate command against regex denylist (no `rm -rf`, `curl`, `wget`, `nc`, `chmod 777`, `eval`, pipe to `sh`) [EXPLICIT]
4. For `Write` tool: validate target path is within project directory [EXPLICIT]
5. For `Read` tool: validate path is not in sensitive locations (`~/.ssh`, `~/.aws`, `/etc/passwd`) [EXPLICIT]
6. Log decision (allow/deny + timestamp + tool + args) to `logs/tool-audit.log` [EXPLICIT]
7. Exit 0 to allow, exit 2 to block with reason [EXPLICIT]

#### post-tool-use.sh

**Behavior:**
1. Receive tool name, arguments, and result via stdin [EXPLICIT]
2. Scan result for potential secret leakage patterns (API keys, tokens, passwords) [EXPLICIT]
3. Log execution result summary (tool, duration, exit code) to `logs/tool-audit.log` [EXPLICIT]
4. If secret detected in output: log warning, optionally redact [EXPLICIT]
5. Exit 0 always (post-hooks should not block retroactively) [EXPLICIT]

**Hook scripts must be:**
- Executable (`chmod +x`) [EXPLICIT]
- Shell-compatible (`#!/usr/bin/env bash`) [EXPLICIT]
- Fast (< 100ms execution) to avoid agent latency [INFERRED]
- Fail-open with logging on script errors (a broken hook should not brick the agent) [INFERRED]

**Validation:** Test each hook with mock input: `echo '{"tool":"Bash","args":{"command":"ls"}}' | bash pre-tool-use.sh` should exit 0. [EXPLICIT]

---

### Phase 5: Verification & Launch

Execute a systematic verification before declaring the deployment ready. [EXPLICIT]

#### 5a: Security Audit Checklist

Run automated checks against the generated project:

```
# 1. No hardcoded secrets
Grep -r "(sk-ant-|xoxb-|xoxp-|ghp_|AKIA)" {PROJECT_NAME}/

# 2. No dangerous permissions
Grep "dangerouslySkipPermissions" {PROJECT_NAME}/

# 3. Docker security options present
Grep "no-new-privileges" {PROJECT_NAME}/docker-compose.yml
Grep "read_only" {PROJECT_NAME}/docker-compose.yml
Grep "cap_drop" {PROJECT_NAME}/docker-compose.yml

# 4. Hooks are executable
Bash test -x {PROJECT_NAME}/.claude/hooks/pre-tool-use.sh && echo "OK" || echo "FAIL"
Bash test -x {PROJECT_NAME}/.claude/hooks/post-tool-use.sh && echo "OK" || echo "FAIL"

# 5. .env not tracked
Grep "\.env" {PROJECT_NAME}/.gitignore

# 6. No wildcard allows in settings
Grep -c '"allow": \[\]' {PROJECT_NAME}/.claude/settings.json
```

If any check fails: **STOP. Fix before proceeding.** [EXPLICIT]

#### 5b: Build Verification

```
Bash cd {PROJECT_NAME} && docker compose build --no-cache
```

Verify clean build with no warnings about security-relevant items. [EXPLICIT]

#### 5c: Health Check

```
Bash cd {PROJECT_NAME} && docker compose up -d
Bash sleep 5 && docker compose ps
Bash docker compose logs --tail=20
```

Confirm: container running, health check passing, no error logs. [EXPLICIT]

#### 5d: Test Message (Platform-Specific)

- **Telegram:** Send test message via BotFather or curl to webhook endpoint [EXPLICIT]
- **HTTP:** `curl -X POST http://localhost:3000/message -d '{"text":"hello"}'` [EXPLICIT]
- **Slack:** Use Slack test event via API [EXPLICIT]

Confirm agent responds and tool audit log shows the interaction. [EXPLICIT]

#### 5e: Launch Confirmation

Present deployment summary to user:

```
## Deployment Complete: {PROJECT_NAME}

| Component | Status | Location |
|-----------|--------|----------|
| Project scaffold | OK | ./{PROJECT_NAME}/ |
| CLAUDE.md security | OK | ./{PROJECT_NAME}/CLAUDE.md |
| Docker isolation | OK | ./{PROJECT_NAME}/docker-compose.yml |
| Tool auth hooks | OK | ./{PROJECT_NAME}/.claude/hooks/ |
| Health check | OK | Container running |
| Test message | OK | Response received |

### Quick Commands
- Start: `cd {PROJECT_NAME} && docker compose up -d`
- Stop: `cd {PROJECT_NAME} && docker compose down`
- Logs: `cd {PROJECT_NAME} && docker compose logs -f`
- Audit: `cat {PROJECT_NAME}/logs/tool-audit.log`
- Rebuild: `cd {PROJECT_NAME} && docker compose build --no-cache && docker compose up -d`
```

---

## Assumptions & Limits

1. **Single-user only.** This deployment has no authentication layer beyond platform-level identity (e.g., Telegram chat ID). Multi-user requires `5022 --team`. [EXPLICIT]
2. **Docker required.** The isolation model depends entirely on Docker. Running without Docker removes most security guarantees. [EXPLICIT]
3. **Internet access model.** The agent container has no direct internet. The gateway container has restricted egress to the platform API only. If the agent needs internet (e.g., web search MCP), the network policy must be explicitly relaxed with documented justification. [EXPLICIT]
4. **API key management.** The `.env` file is the secret store for personal deploy. For production or team use, a proper secrets manager (Vault, AWS SSM, GCP Secret Manager) should replace it. [INFERRED]
5. **No automatic updates.** Dependency versions are pinned. The user is responsible for checking for security updates to base images and npm packages. [EXPLICIT]
6. **Hook limitations.** Shell-based hooks can be bypassed if the agent finds alternative tool invocations that don't trigger the hook protocol. The hook protocol is enforced by Claude Code, not by the container. [INFERRED]
7. **Platform SDK stability.** Telegram Bot API, Slack API, and their SDKs may change. Templates target stable API versions but may need updating. [INFERRED]

---

## Edge Cases

### No Docker Available

If Docker is not installed or the user cannot install it:

1. Warn that isolation guarantees are significantly reduced [EXPLICIT]
2. Fall back to a non-Docker deployment:
   - Generate `start.sh` that runs the Node.js process directly [EXPLICIT]
   - Apply OS-level restrictions where possible (ulimit, chroot on Linux) [INFERRED]
   - Hook scripts still function — they are Claude Code features, not Docker features [EXPLICIT]
3. Add a prominent warning to the generated README and CLAUDE.md [EXPLICIT]

### Windows vs macOS vs Linux

| Concern | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Docker runtime | Docker Desktop (WSL2 backend) | Docker Desktop | Docker Engine native [EXPLICIT] |
| Hook scripts | Git Bash or WSL required for `.sh` hooks | Native bash | Native bash [EXPLICIT] |
| File permissions | NTFS ACLs — `chmod` has no effect | Standard POSIX | Standard POSIX [EXPLICIT] |
| Path separators | Backslash in host, forward slash in container | Forward slash | Forward slash [EXPLICIT] |
| Line endings | Generate with LF, not CRLF — add `.gitattributes` | LF native | LF native [EXPLICIT] |

On Windows: generate `.gitattributes` with `* text=auto eol=lf` to prevent CRLF corruption in hook scripts. [EXPLICIT]

### Existing Project Integration

If the user wants to add OpenClaw to an existing project rather than creating a new one:

1. Detect existing files: `Glob package.json tsconfig.json docker-compose.yml CLAUDE.md` [EXPLICIT]
2. **Do not overwrite** existing files. Generate as `*.openclaw.example` and instruct the user to merge. [EXPLICIT]
3. Merge strategy for `package.json`: add OpenClaw deps to existing deps, warn on version conflicts. [EXPLICIT]
4. Merge strategy for `docker-compose.yml`: add OpenClaw service alongside existing services, create shared network. [EXPLICIT]
5. Merge strategy for `CLAUDE.md`: append security section, do not modify existing instructions. [EXPLICIT]

---

## Good vs Bad Example

### Good: Complete Secure Deployment

```
User: "Deploy OpenClaw for personal use — my-assistant telegram"

Result:
- my-assistant/ directory with 15+ files
- CLAUDE.md with deny-by-default policy and injection defense
- settings.json with empty allow list and explicit deny patterns
- Docker isolation: read-only FS, no-new-privileges, 512MB cap
- Hooks: pre-tool-use blocks rm/curl/wget, post-tool-use scans for secrets
- .env.example with placeholders (user fills in real keys)
- docker compose build succeeds
- docker compose up starts healthy container
- Test message gets response with audit log entry
- All security checks pass
```

### Bad: Quick-and-Dirty Deploy

```
User: "Deploy OpenClaw for personal use"

Result:
- Single directory with index.js
- No CLAUDE.md — agent has unrestricted behavior
- No Docker — runs as user's own process with full system access
- No hooks — every tool use is unaudited
- API key hardcoded in source file
- No .gitignore — secrets committed to git
- Bash tool unrestricted — agent can rm -rf /
- No health check — silent failures
- No audit log — no forensic capability
```

**Why the bad example is dangerous:** A personal agent with unrestricted Bash access and no audit logging is equivalent to giving an autonomous process full control of your machine with no accountability. The agent could delete files, exfiltrate data via curl, or modify system configuration — and you would have no record of what happened. [EXPLICIT]

---

## Validation Gate

Before marking deployment complete, ALL must be checked:

- [ ] All generated files pass security audit (no hardcoded secrets, no dangerous permissions) [EXPLICIT]
- [ ] Docker builds successfully with no security warnings [EXPLICIT]
- [ ] Container starts and passes health check within 30 seconds [EXPLICIT]
- [ ] Pre-tool-use hook correctly blocks `rm -rf /` test case [EXPLICIT]
- [ ] Post-tool-use hook logs tool execution to audit file [EXPLICIT]
- [ ] `.env` is in `.gitignore` and not tracked by git [EXPLICIT]
- [ ] CLAUDE.md contains injection defense instructions [EXPLICIT]
- [ ] settings.json has empty allow list and populated deny list [EXPLICIT]
- [ ] Test message through gateway produces response and audit log entry [EXPLICIT]

---

## Companion Skills

| Skill | Relationship | When to Chain |
|-------|-------------|---------------|
| `5022-open-claude-security` | Architecture parent | Before this skill — when designing the security model first [EXPLICIT] |
| `5023-openclaw-isolation` | Isolation patterns | Reference during Phase 3 for advanced isolation options [EXPLICIT] |
| `5024-openclaw-tool-auth` | Auth patterns | Reference during Phase 4 for custom authorization logic [EXPLICIT] |
| `9081-open-claw-builder` | Agent builder | After this skill — when building the agent's conversation logic [EXPLICIT] |
| `9038-hook-creator` | Hook engineering | When hooks need custom behavior beyond the templates [EXPLICIT] |

---

## Reference Files

| File | Contents |
|------|----------|
| `references/deployment-templates.md` | Complete templates: .env.example, Dockerfile, docker-compose.yml, CLAUDE.md, settings.json, .gitignore, hook scripts, verification script |
