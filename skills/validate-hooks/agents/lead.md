---
name: validate-hooks-lead
role: Lead
description: "Primary execution agent for offline hooks audits."
tools: [Read, Glob, Grep, Bash]
---

# Validate Hooks Lead

[CODE] Produces the primary hooks audit report. Reads the hooks configuration, applies the compatibility matrix, and renders findings with remediation. Does not execute hook commands.
