---
name: form-engineering
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements robust web forms with client and server validation, multi-step
  wizards, file upload handling, accessible error messaging, and optimistic
  submission patterns. [EXPLICIT]
  Trigger: "form validation", "multi-step form", "file upload", "form engineering", "wizard"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Form Engineering

> "Forms are the gatekeepers of the web. Make them inviting, not intimidating." — Luke Wroblewski

## TL;DR

Implements robust web forms with layered validation (HTML5, client-side, server-side), multi-step wizards, file upload handling, and accessible error messaging for friction-free data capture. Use this skill when building complex forms, improving form conversion rates, or when form validation is inconsistent across the application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify form requirements: fields, validation rules, submission endpoint
- Review existing form patterns in the codebase for consistency
- Gather UX requirements: inline validation timing, error message placement
- Check accessibility: labels, error associations, keyboard navigation
- Load reusable assets from `assets/`: `form-engineering-policy.json`, `error-message-patterns.json`, `optimistic-submit-template.ts`, and `upload-control-template.html` when designing implementation contracts.

### Step 2: Analyze
- Design validation layers:
  1. **HTML5 native**: required, type, pattern, min/max attributes
  2. **Client-side**: real-time validation with debounced feedback
  3. **Server-side**: authoritative validation (never trust client only)
- Plan multi-step form flow: step sequence, data persistence, back/forward navigation
- Design file upload: accepted types, size limits, progress feedback, preview
- Plan error handling: field-level errors, form-level errors, server errors
- Convert structured specs into a deterministic implementation contract with `scripts/compile-form-contract.py --spec <spec.json>` when the request includes enough field and submission detail.

### Step 3: Execute
- Build forms with proper HTML: label, fieldset/legend, input types, autocomplete attributes
- Implement real-time validation with meaningful error messages (not just "invalid")
- Create multi-step wizard with progress indicator and state preservation
- Implement file upload with drag-and-drop, preview, progress bar, and retry
- Set up optimistic submission: disable button, show loading, handle success/error
- Associate errors with inputs using aria-describedby and aria-invalid
- Implement autosave for long forms to prevent data loss
- Use the generated contract sections as the implementation checklist: validation parity, accessibility hooks, upload controls, optimistic submission, and telemetry.

### Step 4: Validate
- Verify all inputs have associated labels and error message connections
- Confirm server-side validation catches everything client-side does (and more)
- Test keyboard-only form completion (Tab, Enter, Escape)
- Check that error messages are specific and actionable ("Email must include @")
- Run `scripts/check.sh` after changing bundled assets, fixtures, or the deterministic compiler.

## Quality Criteria

- [ ] Every input has a visible label and accessible error association
- [ ] Validation runs on both client and server with consistent rules
- [ ] Error messages are specific, actionable, and politely worded
- [ ] Multi-step forms preserve state on back navigation
- [ ] Evidence tags applied to all claims
- [ ] `assets/manifest.json` declares every reusable form engineering asset
- [ ] `scripts/compile-form-contract.py` rejects specs without validation parity, accessible errors, upload limits, or optimistic submit behavior
- [ ] File upload fields include accepted MIME/extensions, max size, preview/progress, retry, and server storage boundary

## Anti-Patterns

- Client-only validation without server-side verification
- Generic error messages ("Invalid input") that don't help users fix the issue
- Clearing the entire form on submission error, losing user input

## Related Skills

- `accessibility-design` — accessible form patterns and error handling
- `html-semantic` — proper form markup and native validation
- `angular-development` — Angular reactive forms implementation
- `form-builder` — semantic form rendering from JSON schema

## Usage

Example invocations:

- "/form-engineering" — Run the full form engineering workflow
- "form engineering on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/compile-form-contract.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill form-engineering`
- Default behavior: render the contract to stdout; write files only when `--output` is explicit.
- Safety boundary: malformed specs fail nonzero instead of producing partial form guidance.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/form-engineering-policy.json` defines required validation, accessibility, upload, and submission sections.
- `assets/error-message-patterns.json` provides deterministic copy patterns for field and form-level errors.
- `assets/optimistic-submit-template.ts` provides an implementation skeleton for pending, success, failure, and retry state.
- `assets/upload-control-template.html` provides the accessible file upload control baseline.


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
