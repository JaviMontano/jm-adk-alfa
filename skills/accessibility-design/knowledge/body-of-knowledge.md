# Accessibility Design — Body of Knowledge

## Canon

Accessibility design defines how a UI should behave before users encounter
barriers. The default order is native HTML, design-system tokens, explicit
interaction behavior, then targeted ARIA only when native semantics are not
enough.

## Design Principles

| Principle | Design Requirement |
|---|---|
| Perceivable | Text alternatives, visible labels, contrast, zoom/reflow, non-color cues, readable content. |
| Operable | Keyboard support, visible focus, skip links, pointer alternatives, no traps, reduced motion. |
| Understandable | Predictable navigation, clear instructions, helpful errors, plain language, consistent controls. |
| Robust | Semantic HTML, valid ARIA when needed, name/role/value/state, compatibility with assistive tech. |

## Component Pattern Checklist

| Pattern | Required Decisions |
|---|---|
| Dialog / modal | Trigger, initial focus, labelled title, focus trap, Escape behavior, close control, return focus. |
| Tabs | Tablist semantics, selected state, arrow-key model, panel association, focus vs activation behavior. |
| Accordion / disclosure | Button semantics, expanded state, heading relationship, keyboard behavior, content visibility. |
| Menu button | Button trigger, popup role only when menu behavior is real, arrow navigation, Escape/blur behavior. |
| Combobox / listbox | Input ownership, active descendant or roving tabindex, filtering behavior, selected state, announcements. |
| Forms | Visible labels, programmatic labels, descriptions, required state, error summary, inline errors, first-invalid focus. |
| Toast / status | Live region politeness, announcement timing, dismissal, no focus stealing. |
| Icon button | Visible or accessible name, target size, state, tooltip independence. |
| Data table | Header associations, caption/summary, sort state, keyboard support for interactive cells. |

## Design Token Requirements

| Token Area | Requirement |
|---|---|
| Text contrast | Normal text meets 4.5:1; large text meets 3:1 unless an explicit exception applies. |
| Non-text contrast | UI component boundaries, icons, focus indicators, and meaningful graphical objects meet 3:1. |
| Focus | Focus ring is visible across surfaces and not removed without replacement. |
| Error/success/warning | State is not conveyed by color alone; text/icon/ARIA/status behavior is specified. |
| Motion | Reduced-motion alternative exists for non-essential animation. |

## Output Contract

Every design deliverable should include component scope, user journey, semantic
HTML/ARIA decision log, keyboard map, focus plan, screen reader expectations,
content and error requirements, contrast/token evidence or not-verified status,
implementation notes, acceptance criteria, and validation matrix.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Pattern completeness | 100% | Required decisions are present for each in-scope component |
| Native-first semantics | 100% | Native HTML considered before ARIA |
| Keyboard coverage | 100% | Key map includes Tab, Shift+Tab, Enter/Space, Escape, and pattern-specific arrows when relevant |
| Focus coverage | 100% | Initial, visible, trapped/contained, return, and route-change focus are addressed when relevant |
| Contrast evidence | 100% | Ratios or not-verified status provided for text and non-text states |
| Acceptance criteria | 100% | Each component has testable acceptance criteria |

## References
- WCAG 2.1 AA / POUR model.
- WAI-ARIA Authoring Practices for custom widgets.
- Project-local design-system tokens and component conventions when present.
