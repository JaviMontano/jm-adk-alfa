---
name: triad-composition
author: JM Labs (Javier Montaño)
version: 1.0.0
description: "Select a deterministic Lead + Support + Guardian triad from the PRISTINO composition matrix using domain classification, confidence thresholds, stable tie-breakers, execution-mode routing, degraded-mode policy, and Guardian validation. Use when the user or orchestrator asks for triad composition, agent role selection, Lead/Support/Guardian routing, Pristino orchestration, domain-to-agent mapping, committee escalation, or quality-gated multiagent execution planning."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Triad Composition

## When to Activate

Activate when the user or orchestrator needs to select Lead, Support, and Guardian roles for a non-trivial task, route a request through PRISTINO orchestration, classify a task domain, choose between triad vs committee execution, or explain degraded-mode behavior when an agent role fails. [EXPLICIT]

Do not activate for unrelated uses of the word "triad" such as music theory, chemistry, or generic three-item lists unless the request also mentions Pristino, orchestration, agents, or Lead/Support/Guardian routing. [EXPLICIT]

## Deterministic Assets

Load these before composing a triad:

- `assets/composition-matrix.json`: canonical domain -> Lead/Support/Guardian matrix.
- `assets/classification-policy.json`: confidence bands, execution modes, and stable tie-breakers.
- `assets/degraded-mode-policy.json`: explicit partial-delivery rules.
- `assets/triad-output-contract.json`: required output sections and blocked phrases.

Validate packet examples with:

```bash
bash skills/triad-composition/scripts/check.sh
python3 -B skills/triad-composition/scripts/validate_triad_packet.py --contract skills/triad-composition/assets/triad-output-contract.json --packet <packet.md> --scenario requirements
```

## Inputs

Require these before auto-selecting:

| Input | Required | Handling |
|---|---:|---|
| Goal | Yes | Ask if missing. |
| Context | Yes | Ask if missing or infer only with `[INFERRED]`. |
| Constraints | Yes | Ask if safety, brand, runtime, deadline, or quality constraints are unknown. |
| Definition of done | Yes | Ask if success criteria are absent. |
| Match confidence | Optional | If absent, calculate from exact phrase matches, keyword hits, and domain order. |

Do not apply defaults for missing Goal, Context, Constraints, or Definition of done. [EXPLICIT]

## Classification Policy

Apply confidence bands exactly:

| Confidence | Action |
|---:|---|
| `>=0.85` | Auto-select skill, compose triad, execute sequentially. |
| `0.60-0.84` | Present top 3 domain options and ask user to choose. |
| `<0.60` | Ask one clarifying question before matching again. |

Use stable tie-breakers in this order: exact domain phrase match, highest keyword hit count, highest confidence score, earliest domain order in `composition-matrix.json`. [EXPLICIT]

## Execution Mode

| Mode | Use when | Output |
|---|---|---|
| Single | Trivial question, clarification, or lookup. | Direct answer; no triad packet required. |
| Triad | Non-trivial analysis, design, implementation, or review. | Lead -> Support -> Guardian sequence. |
| Committee | Critical cross-cutting decision. | Up to 5 agents with Pristino tiebreaker; document why triad is insufficient. |

Critical scopes include production data retention, security policy, compliance, legal risk, enterprise governance, or decisions spanning four or more domains. [INFERRED]

## Composition Procedure

1. Normalize the request without correcting the user's language. [EXPLICIT]
2. Extract domain signals and required inputs. [EXPLICIT]
3. Score matrix domains from `assets/composition-matrix.json` using deterministic keyword hits and explicit user terms. [EXPLICIT]
4. Apply the confidence band and tie-breakers from `assets/classification-policy.json`. [EXPLICIT]
5. If confidence is `>=0.85`, return the selected Lead, Support, Guardian, execution mode, and G0-G3 gates. [EXPLICIT]
6. If confidence is `0.60-0.84`, return top 3 domain options and ask for a choice; do not execute. [EXPLICIT]
7. If confidence is `<0.60`, ask for missing Goal, Context, Constraints, and Definition of done; do not invent a triad. [EXPLICIT]
8. If any triad member fails, apply `assets/degraded-mode-policy.json` and mark output `[PARTIAL]`. [EXPLICIT]

## Output Contract

Use this packet shape:

```markdown
# Triad Composition Packet

# Input Classification

# Selected Triad

# Execution Mode

# Validation Gates

# Risks and Assumptions
```

Every role selection must name the matrix domain, confidence band, Lead, Support, Guardian, and evidence tag. [EXPLICIT]

## Validation Gate

- [ ] Required inputs are present or explicitly requested with `[OPEN]`.
- [ ] Domain selection cites a matrix row or presents top 3 options.
- [ ] Guardian is always selected for triad or committee mode.
- [ ] Confidence band action matches the threshold policy.
- [ ] No unrelated false-positive use of "triad" activates orchestration.
- [ ] G0-G3 quality gates are named before delivery.
- [ ] Degraded mode is marked `[PARTIAL]` and names the failed role.

## Edge Cases

| Scenario | Handling |
|---|---|
| Minimal input | Ask for Goal, Context, Constraints, and Definition of done. |
| Two close domains | Present top 3 options and ask user to choose. |
| Critical cross-domain decision | Escalate to committee, max 5 agents. |
| Guardian unavailable | Deliver only with `[PARTIAL]` and manual-review warning. |
| False positive "triad" | Route away and do not return orchestration agents. |
| Runtime lacks subagent tools | Apply Lead, Support, and Guardian perspectives sequentially in one response. |

## Related Canon

- `PRISTINO.md`: source for triad pattern, matrix, confidence bands, degraded mode, Constitution XIII/XIV/XVI, and G0-G3 gates. [DOC]
- `AGENTS.md`: runtime bridge exposing the triad pattern for Codex-compatible execution. [DOC]
