# Context Optimizer — Knowledge Graph

## Core Concepts
- context-optimizer: budget-preserving context planner
- loading-level: L1 index, L2 summary, L3 full context
- compression-plan: retention summaries for completed work
- eviction-safety: no active, unresolved, or risk-flagged source removed
- metrics: reduction and utilization from explicit token counts

## Dependencies
- Upstream: input-analysis, session-lifecycle-management
- Downstream: pre-compact-context, context-window-management

## Skill Relationships
Use `pre-compact-context` for handoff packets and `context-window-management`
for global window policy. Use this skill for active-session budget decisions.
