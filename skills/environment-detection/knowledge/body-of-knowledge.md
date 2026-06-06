# Environment Detection Body of Knowledge

Environment detection is a startup control, not a research task. It should produce the safest orchestration mode from evidence already present in the local runtime.

## Signal Strength

| Strength | Signal | Use |
|----------|--------|-----|
| 1 | Explicit runtime/tool availability | Strongest evidence for what the agent can actually do |
| 2 | User-supplied model/context metadata | Strong evidence when the user or runtime states it directly |
| 3 | Workspace instruction files | Useful host hints but weaker than active tool availability |
| 4 | Repository conventions | Supporting evidence only |
| 5 | Assumptions | Must be tagged and should reduce confidence |

## Mode Mapping

| IDE | Triad mode | Key requirement |
|-----|------------|-----------------|
| `claude-code` | `full` | Subagents plus hooks or MCP evidence |
| `codex` | `sequential` | Shell/read/write available without subagent orchestration |
| `gemini` / `antigravity` | `sequential` | Prompt sequence without full triad tooling |
| `cursor` / `windsurf` | `checklist` | Inline rule/checklist workflow |
| `copilot` | `suggestion` | Limited assistant suggestion flow |
| `unknown` | `sequential` | Conservative fallback |

## Model Tiers

- `heavy`: context budget `>=100000`; one active L3 resource is normally safe.
- `medium`: context budget `32000..99999`; prefer L1/L2 with one carefully justified L3.
- `light`: context budget `<32000`; avoid L3 except the active tiny skill when explicitly required.
- `unknown`: no budget evidence; default to L1/L2 and list missing evidence.

## Rejected Evidence

Network lookups, current dates, random probes, browser cookies, account dashboards, and private history are not valid detection evidence because they are unstable or outside the local report contract.
