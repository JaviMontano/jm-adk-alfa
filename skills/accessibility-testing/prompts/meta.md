---
name: accessibility-testing-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the Accessibility Testing skill."
---

# Accessibility Testing — Self-Improvement

## Evaluate

1. Does `knowledge/body-of-knowledge.md` still reflect current accessibility testing evidence needs?
2. Do the 4 sub-agents cover automated testing, keyboard, screen reader, contrast, motion, suppressions, and claim safety?
3. Does `templates/output.md` force scope, status, evidence, not-verified areas, findings, and retest criteria?
4. Do evals catch false passes, missing target scope, broad suppressions, and remediation boundary drift?
5. Have real projects exposed new AT/browser pairings, component patterns, or dynamic states?
6. Has the related skill landscape changed: `accessibility-audit`, `accessibility-design`, modal/dialog/navigation skills?

## Improve

1. Update evidence models and status semantics with new findings.
2. Add evals for any false pass or unsupported compliance claim observed in practice.
3. Refine quality criteria based on failed retests and missing evidence.
4. Update knowledge graph with new concepts, tools, and related skills.
5. Test templates with edge-case inputs before accepting the change.
6. Propose a broader guardrail only when the ambiguity repeats across skills.

## Trigger

Run this meta-prompt when:
- Skill hasn't been reviewed in 30+ days
- User reports unexpected output quality
- New related skills added to the kit
- Insights file updated with relevant patterns
