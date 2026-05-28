---
name: openclaw-isolation
version: 1.0.0
description: >
  This skill should be used when the user asks to "isolate OpenClaw in Docker",
  "containerize the agent", "set up network isolation", "sandbox OpenClaw",
  "restrict container egress", or mentions Docker security, container isolation,
  network policies, or agent sandboxing. Implements Docker container security,
  network isolation, resource limits, and filesystem restrictions for OpenClaw
  and Claude Code deployments. Use this skill whenever container-level isolation
  needs to be implemented, even if they don't explicitly ask for
  "openclaw-isolation". [EXPLICIT]
argument-hint: "project-name [--personal | --team]"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# OpenClaw Isolation: Docker Container Security & Network Sandboxing

Container isolation is defense-in-depth for OpenClaw deployments. Even when the agent engine is trusted, the tools it invokes (Bash, file system, browser, APIs) operate on the host. A compromised or misbehaving tool call without container isolation has unrestricted access to the host filesystem, network, and processes. This skill produces hardened Docker configurations, network policies, and resource limits that constrain the blast radius of any single tool invocation to the container boundary. [EXPLICIT]

## Principio Rector

**El contenedor no es la defensa — es la jaula de contención.** Docker no previene ataques; limita el daño. La verdadera seguridad es capas: contenedor + red + filesystem + límites de recursos, cada uno independiente del otro.

### Isolation Philosophy

1. **Containers are blast-radius limiters, not firewalls.** A Docker container restricts what a compromised process can reach. It does not prevent the compromise itself. Every container configuration assumes the process inside will attempt escape. [EXPLICIT]
2. **Network isolation is the highest-value control.** An agent that cannot reach the internet cannot exfiltrate data. Default-deny egress with explicit allowlists is the single most impactful isolation measure. [EXPLICIT]
3. **Resource limits prevent denial-of-service.** Without memory and CPU limits, a runaway agent process can starve the host. Hard limits protect collocated services and the host OS. [EXPLICIT]
4. **Filesystem restrictions enforce least privilege.** Read-only root filesystem with targeted writable tmpfs mounts ensures the agent can only write where explicitly permitted. [EXPLICIT]

---

## Usage / When to Activate

Use this skill when:

- Deploying OpenClaw or Claude Code inside Docker containers [EXPLICIT]
- Hardening an existing Docker-based agent deployment [EXPLICIT]
- Setting up network isolation for agent-to-internet traffic [EXPLICIT]
- Implementing resource limits (CPU, memory, PIDs) for agent containers [EXPLICIT]
- Restricting filesystem access within containerized agents [EXPLICIT]
- Building CI/CD pipelines that run agents in sandboxed containers [EXPLICIT]

**Trigger phrases:** "isolate OpenClaw", "containerize the agent", "Docker security for Claude Code", "sandbox the agent", "restrict container egress", "set up network policies for OpenClaw", "agent container hardening" [EXPLICIT]

## When NOT to Use

| Need | Use Instead | Why |
|------|-------------|-----|
| Designing security architecture (not implementing) | `5022-open-claude-security` | Architecture design, not container implementation |
| General app security architecture | `5019-security-architecture` | System-level, not container-level |
| Building OpenClaw from scratch | `9081-open-claw-builder` | Builds agents; this skill isolates them |
| Tool-level authorization controls | `5024-openclaw-tool-auth` | Per-tool auth, not container isolation |
| Full personal deployment | `5025-openclaw-personal-deploy` | End-to-end deploy; this skill handles isolation only |
| Kubernetes orchestration | Out of scope | This skill covers Docker, not K8s |

---

## Inputs

Parse `$ARGUMENTS`: `$1` = project name, `$2` = deployment mode. [EXPLICIT]

**Deployment modes:**
- `--personal`: Single-user, local Docker. Tighter limits, simpler network. [EXPLICIT]
- `--team`: Multi-container shared environment. Adds inter-container policies and shared volumes. [EXPLICIT]
- Default: `--personal` [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso` [EXPLICIT]
  - **piloto-auto**: Auto for Dockerfile generation and compose config, HITL for network rules and resource limits. [EXPLICIT]
  - **desatendido**: Full auto. All decisions documented as assumptions. [EXPLICIT]
  - **supervisado**: Autonomous with checkpoint at network egress rules and resource limits. [EXPLICIT]
  - **paso-a-paso**: Confirm every Dockerfile instruction, compose option, and network rule. [EXPLICIT]
- `{FORMATO}`: `markdown` (default) | `yaml` | `dual`

---

## Before Building

Detect existing Docker and project context:

```
Glob Dockerfile docker-compose*.yml .dockerignore
Glob .claude/settings.json .claude/settings.local.json .mcp.json CLAUDE.md
Glob **/Dockerfile **/docker-compose*.yml
Bash(docker --version 2>/dev/null || echo "Docker not installed")
Bash(docker compose version 2>/dev/null || echo "Docker Compose not available")
```

Load reference materials:

```
Read ${CLAUDE_SKILL_DIR}/references/docker-patterns.md
```

Cross-reference with security architecture if available:

```
Glob skills/**/5022-open-claude-security/SKILL.md
```

**Decision tree:**
- If Docker is not installed → provide installation guidance, then proceed with file generation [EXPLICIT]
- If existing Dockerfile found → audit it against hardening checklist before generating new [EXPLICIT]
- If existing docker-compose.yml found → diff against hardened template and report gaps [EXPLICIT]
- If no Docker files found → generate complete hardened configuration from scratch [EXPLICIT]

---

## Core Process: 4 Sections

### S1: Dockerfile Security

Build a multi-stage, minimal, non-root Dockerfile for the OpenClaw agent. [EXPLICIT]

**Requirements:**

1. **Multi-stage build.** Stage 1 (`builder`) installs dependencies and compiles. Stage 2 (`runtime`) copies only the built artifacts. This eliminates build tools, package managers, and source code from the final image. [EXPLICIT]
2. **Minimal base image.** Use `node:22-alpine` or `debian:bookworm-slim` depending on project requirements. Never use `node:latest` or `ubuntu:latest` — these include hundreds of unnecessary packages that expand attack surface. [EXPLICIT]
3. **Non-root user.** Create a dedicated `openclaw` user (UID 1001) and group. Set `USER openclaw` before the `CMD` instruction. The agent process must never run as root inside the container. [EXPLICIT]
4. **No secrets in layers.** Never use `COPY .env .` or `ARG SECRET_KEY=...`. Secrets enter via Docker secrets, mounted files, or environment variables at runtime only. Every layer is inspectable via `docker history`. [EXPLICIT]
5. **Pinned versions.** Pin the base image digest (`node:22-alpine@sha256:abc...`) and all package versions (`npm ci --ignore-scripts`). Reproducible builds prevent supply chain drift. [EXPLICIT]
6. **Minimal filesystem.** Remove package caches (`rm -rf /var/cache/apk/*`), disable shell access where possible, and set `WORKDIR /app` with restricted permissions. [EXPLICIT]
7. **Health check.** Include `HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:${PORT}/health || exit 1` to enable orchestrator-level liveness detection. [INFERRED]

**Template Dockerfile:**

```dockerfile
# === Stage 1: Builder ===
FROM node:22-alpine@sha256:<pinned-digest> AS builder
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts --production=false
COPY . .
RUN npm run build && npm prune --production

# === Stage 2: Runtime ===
FROM node:22-alpine@sha256:<pinned-digest> AS runtime
RUN addgroup -g 1001 openclaw && adduser -u 1001 -G openclaw -s /bin/false -D openclaw
RUN rm -rf /var/cache/apk/* /tmp/* /root/.npm
WORKDIR /app
COPY --from=builder --chown=openclaw:openclaw /build/dist ./dist
COPY --from=builder --chown=openclaw:openclaw /build/node_modules ./node_modules
COPY --from=builder --chown=openclaw:openclaw /build/package.json ./
USER openclaw
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

**Validation checks for S1:**
- [ ] No `RUN apt-get install` in runtime stage [EXPLICIT]
- [ ] `USER` directive present and not `root` [EXPLICIT]
- [ ] No `COPY .env`, `ARG PASSWORD`, or secret-bearing instructions [EXPLICIT]
- [ ] Base image pinned by digest [EXPLICIT]

---

### S2: Docker Compose Security

Produce a hardened `docker-compose.yml` with security options, capability restrictions, and resource limits. [EXPLICIT]

**Security options applied:**

1. **`security_opt: [no-new-privileges:true]`** — Prevents the container process from gaining additional privileges via setuid/setgid binaries. This blocks a common container escape vector. [EXPLICIT]
2. **`cap_drop: [ALL]`** — Drops all Linux capabilities. The agent does not need `NET_RAW`, `SYS_ADMIN`, `MKNOD`, or any other capability. If a specific capability is genuinely needed, add it back with `cap_add` and document the justification. [EXPLICIT]
3. **`read_only: true`** — Sets the root filesystem to read-only. Combined with targeted `tmpfs` mounts, this prevents the agent from writing to unexpected paths. [EXPLICIT]
4. **`tmpfs` mounts** — Writable temporary storage for `/tmp` and `/app/workspace` with size limits. The agent can write to these paths but nowhere else. [EXPLICIT]
5. **`mem_limit` and `cpus`** — Hard resource ceilings. Personal deployments: 1GB RAM, 1 CPU. Team deployments: 2GB RAM, 2 CPUs. These prevent runaway processes from starving the host. [EXPLICIT]
6. **`pids_limit`** — Restricts the number of processes the container can spawn. Prevents fork bombs. Default: 100. [EXPLICIT]
7. **`restart: unless-stopped`** — Ensures the container recovers from crashes but does not restart if explicitly stopped. [INFERRED]

**Resource limit guidelines:**

| Deployment | Memory | CPU | PIDs | tmpfs /tmp | tmpfs /app/workspace |
|------------|--------|-----|------|------------|---------------------|
| `--personal` | 1024m | 1.0 | 100 | 64m | 256m |
| `--team` | 2048m | 2.0 | 200 | 128m | 512m |

[EXPLICIT]

**Template docker-compose.yml (personal mode):**

```yaml
version: "3.9"
services:
  openclaw-agent:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: openclaw-agent
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=64m,noexec,nosuid
      - /app/workspace:size=256m,noexec,nosuid
    mem_limit: 1024m
    mem_reservation: 256m
    cpus: "1.0"
    pids_limit: 100
    networks:
      - openclaw-internal
    env_file:
      - .env
    ports:
      - "127.0.0.1:3000:3000"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

networks:
  openclaw-internal:
    driver: bridge
    internal: true
```

**Validation checks for S2:**
- [ ] `no-new-privileges` set to true [EXPLICIT]
- [ ] All capabilities dropped [EXPLICIT]
- [ ] Resource limits defined (mem, cpu, pids) [EXPLICIT]
- [ ] Root filesystem read-only with explicit tmpfs mounts [EXPLICIT]

---

### S3: Network Isolation

Implement network policies that restrict container egress to only approved destinations. [EXPLICIT]

**Principles:**

1. **Default-deny egress.** The container cannot reach the internet unless explicitly allowlisted. Use Docker's `internal: true` network driver to block all external traffic by default. [EXPLICIT]
2. **Egress allowlist.** For agents that need API access (Claude API, GitHub API), use a sidecar proxy (e.g., Squid, mitmproxy) or iptables rules that allowlist specific domains/IPs. [EXPLICIT]
3. **No host network.** Never use `network_mode: host`. This eliminates all network isolation. [EXPLICIT]
4. **Port binding to localhost.** Exposed ports bind to `127.0.0.1` only, not `0.0.0.0`. This prevents external access to the agent's HTTP interface. [EXPLICIT]
5. **DNS restriction.** In high-security deployments, configure the container to use a local DNS resolver that only resolves allowlisted domains. [INFERRED]

**Egress allowlist implementation with iptables (host-level):**

```bash
#!/bin/bash
# egress-allowlist.sh — Restrict container egress to approved IPs
# Run on the Docker host, not inside the container

CONTAINER_SUBNET="172.20.0.0/16"
ALLOWED_IPS=(
  "104.18.0.0/16"    # Anthropic API (api.anthropic.com)
  "140.82.112.0/20"  # GitHub API
)

# Default deny all egress from container subnet
iptables -I FORWARD -s $CONTAINER_SUBNET -j DROP

# Allow established connections (responses to allowed requests)
iptables -I FORWARD -s $CONTAINER_SUBNET -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow specific destinations
for ip in "${ALLOWED_IPS[@]}"; do
  iptables -I FORWARD -s $CONTAINER_SUBNET -d $ip -j ACCEPT
done

# Allow DNS resolution (to host DNS only)
iptables -I FORWARD -s $CONTAINER_SUBNET -d 172.20.0.1 -p udp --dport 53 -j ACCEPT
```

**Network architecture (personal mode):**

```
┌─────────────────────────────────────────────┐
│  Docker Host                                 │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ openclaw-internal (bridge, internal) │   │
│  │                                      │   │
│  │  ┌──────────────┐  ┌─────────────┐  │   │
│  │  │ openclaw-    │  │ egress-     │  │   │
│  │  │ agent        │──│ proxy       │  │   │
│  │  │ (no egress)  │  │ (allowlist) │  │   │
│  │  └──────────────┘  └──────┬──────┘  │   │
│  │                           │          │   │
│  └───────────────────────────┼──────────┘   │
│                              │               │
│  ┌───────────────────────────┼──────────┐   │
│  │ openclaw-egress (bridge)  │          │   │
│  │                           ▼          │   │
│  │                    [Allowlisted IPs] │   │
│  └──────────────────────────────────────┘   │
│                              │               │
└──────────────────────────────┼───────────────┘
                               ▼
                         Internet (filtered)
```

**Validation checks for S3:**
- [ ] No `network_mode: host` anywhere in compose [EXPLICIT]
- [ ] Internal network declared with `internal: true` [EXPLICIT]
- [ ] Ports bound to `127.0.0.1`, not `0.0.0.0` [EXPLICIT]
- [ ] Egress allowlist documented and implemented [EXPLICIT]

---

### S4: Volume & Filesystem Security

Configure bind mounts, volume permissions, and path blocking to enforce least-privilege filesystem access. [EXPLICIT]

**Principles:**

1. **Read-only root filesystem.** Set `read_only: true` in compose. The container root is immutable at runtime. [EXPLICIT]
2. **Targeted writable mounts.** Use `tmpfs` for `/tmp` (ephemeral scratch) and `/app/workspace` (agent work area). Both have size limits and `noexec,nosuid` flags. [EXPLICIT]
3. **Bind mount restrictions.** If the agent needs access to host files (e.g., project source), mount them as read-only (`:ro`). Never mount `/`, `/etc`, `/var/run/docker.sock`, or the user's home directory. [EXPLICIT]
4. **Docker socket prohibition.** Mounting `/var/run/docker.sock` inside the container grants full Docker API access — equivalent to root on the host. This is categorically forbidden. [EXPLICIT]
5. **Sensitive path blocking.** The following host paths must never be mounted into the container: [EXPLICIT]
   - `/var/run/docker.sock` — Docker daemon control
   - `/etc/shadow`, `/etc/passwd` — Host credential files
   - `~/.ssh/` — SSH private keys
   - `~/.aws/`, `~/.gcloud/` — Cloud provider credentials
   - `~/.gnupg/` — GPG private keys
   - `/proc`, `/sys` — Kernel interfaces (beyond default Docker masking)

**Volume configuration template:**

```yaml
services:
  openclaw-agent:
    volumes:
      # Project source — read-only
      - ./project:/app/project:ro
      # Agent output — writable, host-accessible
      - ./output:/app/output:rw
    tmpfs:
      - /tmp:size=64m,noexec,nosuid,nodev
      - /app/workspace:size=256m,noexec,nosuid,nodev
    read_only: true
```

**Validation checks for S4:**
- [ ] No Docker socket mount [EXPLICIT]
- [ ] No mounts to sensitive host paths (`.ssh`, `.aws`, `.gnupg`) [EXPLICIT]
- [ ] Host source mounts are `:ro` [EXPLICIT]
- [ ] `tmpfs` mounts have size limits and `noexec` [EXPLICIT]

---

## Assumptions & Limits

1. **Docker Engine >=24.0 required.** Security options (`no-new-privileges`, `pids_limit`, `read_only`) require Docker Engine 24.0+. Older versions may silently ignore these options. [EXPLICIT]
2. **Linux kernel features assumed.** Seccomp, AppArmor/SELinux, and cgroup v2 are assumed available. These underpin Docker's isolation guarantees. macOS Docker Desktop and WSL2 provide these via their Linux VM. [EXPLICIT]
3. **No Kubernetes.** This skill produces Docker Compose configurations, not Kubernetes manifests. For K8s deployments, the patterns translate but require Pod Security Standards, NetworkPolicies, and ResourceQuotas instead. [EXPLICIT]
4. **Single-host scope.** Network isolation via iptables assumes a single Docker host. Multi-host deployments need overlay networks and additional tooling (Calico, Cilium). [EXPLICIT]
5. **iptables rules are fragile.** Host-level iptables rules can be flushed by Docker daemon restarts or system updates. Persistent rules require `iptables-persistent` or equivalent. [INFERRED]
6. **Secrets management is external.** This skill configures containers to receive secrets at runtime but does not manage the secret lifecycle. Use `5006-secrets-management` for vault integration. [EXPLICIT]

---

## Edge Cases

### Edge Case 1: Bare Metal (No Docker)

If Docker is not installed or cannot be installed (embedded systems, restricted environments), provide alternative isolation using:
- **systemd sandboxing:** `ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`, `NoNewPrivileges=yes` in a systemd service unit. [EXPLICIT]
- **firejail:** Lightweight sandboxing for Linux desktops without Docker. [INFERRED]
- Document the isolation gap: no cgroup resource limits, no network namespace isolation. [EXPLICIT]

### Edge Case 2: WSL2 on Windows

Docker Desktop for Windows runs containers inside a WSL2 Linux VM. Key differences:
- Network isolation works but iptables rules must be set inside the WSL2 VM, not on the Windows host. [EXPLICIT]
- File system performance for bind mounts from Windows paths (`/mnt/c/...`) is significantly degraded. Mount from the Linux filesystem (`~/project`) instead. [EXPLICIT]
- Docker socket permissions may require the user to be in the `docker` group inside WSL2. [INFERRED]
- Memory limits apply within the WSL2 VM's allocated memory, configured via `.wslconfig`. [EXPLICIT]

### Edge Case 3: Rootless Docker

Rootless Docker runs the Docker daemon and containers without root privileges. Implications:
- `iptables` rules require `slirp4netns` or `pasta` for network isolation instead of kernel-level iptables. Egress filtering is more limited. [EXPLICIT]
- Port binding below 1024 is not available. Use ports >=1024 for all services. [EXPLICIT]
- cgroup v2 delegation must be configured for resource limits to work. [EXPLICIT]
- Rootless mode is more secure by default but has reduced network isolation capabilities. Document the tradeoff. [EXPLICIT]

---

## Good vs Bad Example

### Bad: Permissive docker-compose.yml

```yaml
# DO NOT USE — Every line is a security gap
version: "3.9"
services:
  agent:
    image: node:latest              # Unpinned, bloated image
    network_mode: host              # No network isolation
    privileged: true                # Full host access
    volumes:
      - /:/host                     # Entire host filesystem
      - /var/run/docker.sock:/var/run/docker.sock  # Docker API
    environment:
      - API_KEY=sk-ant-xxxxx       # Secret in compose file
    ports:
      - "3000:3000"                 # Bound to 0.0.0.0
```

**Issues:** [EXPLICIT]
- `node:latest` — unpinned, includes build tools, 900MB+
- `network_mode: host` — zero network isolation
- `privileged: true` — equivalent to running on host as root
- `/:/host` — entire host filesystem exposed
- Docker socket mounted — container can control Docker daemon
- API key in environment definition — visible in `docker inspect`
- Port bound to all interfaces — accessible from network

### Good: Hardened docker-compose.yml

```yaml
version: "3.9"
services:
  openclaw-agent:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: openclaw-agent
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=64m,noexec,nosuid,nodev
      - /app/workspace:size=256m,noexec,nosuid,nodev
    mem_limit: 1024m
    mem_reservation: 256m
    cpus: "1.0"
    pids_limit: 100
    volumes:
      - ./project:/app/project:ro
      - ./output:/app/output:rw
    networks:
      - openclaw-internal
    env_file:
      - .env
    ports: ["127.0.0.1:3000:3000"]
    restart: unless-stopped
networks:
  openclaw-internal:
    driver: bridge
    internal: true
```

**Why secure**: cap_drop ALL, read-only root, sized tmpfs, resource limits, internal network, localhost-only port, env-file secrets. [EXPLICIT]

---

## Validation Gate

Before delivering the isolation configuration, verify:

- [ ] **Dockerfile uses multi-stage build** with non-root user and pinned base image [EXPLICIT]
- [ ] **docker-compose.yml includes** `security_opt`, `cap_drop: ALL`, `read_only`, resource limits [EXPLICIT]
- [ ] **Network is internal** with `internal: true` and ports bound to `127.0.0.1` [EXPLICIT]
- [ ] **No Docker socket mount** and no sensitive host path mounts (`.ssh`, `.aws`, `.gnupg`) [EXPLICIT]
- [ ] **Egress rules documented** — either iptables allowlist, proxy config, or explicit "no egress needed" [EXPLICIT]
- [ ] **Resource limits set** — `mem_limit`, `cpus`, `pids_limit` all defined with justified values [EXPLICIT]
- [ ] **tmpfs mounts** have `noexec,nosuid,nodev` flags and size limits [EXPLICIT]
- [ ] **Good/Bad comparison reviewed** — final config matches "Good" pattern, not "Bad" [EXPLICIT]

---

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/docker-patterns.md` | Dockerfile best practices, compose security, network drivers, seccomp, AppArmor | Always [EXPLICIT] |
