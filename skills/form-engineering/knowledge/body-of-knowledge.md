# Form Engineering — Body of Knowledge

## Canon

Robust form engineering is the implementation layer that keeps user input reliable from the first keystroke to server persistence. The contract is stronger than visual form construction: it must specify client validation, authoritative server validation, accessible error recovery, file upload boundaries, optimistic submit behavior, autosave or draft handling, and telemetry for failure analysis.

## Required Engineering Decisions

| Area | Required Decision | Failure If Missing |
|---|---|---|
| Validation parity | Every rule has a client check, server check, and actionable message. | Client and server disagree, creating false success or data loss. |
| Accessibility | Labels, field errors, summary, keyboard path, and aria-live feedback are explicit. | Users cannot locate or recover from errors. |
| Uploads | Accept list, max size, preview, progress, retry, and storage boundary are declared. | Unsafe or opaque uploads reach production. |
| Optimistic submit | Pending, success, failure, and retry strategy are defined. | Users double-submit or lose drafts under network failure. |
| Telemetry | Start, error, upload failure, submit attempt, success, and failure events are named. | Form failures cannot be diagnosed after launch. |

## Scripted Contract

Use `scripts/compile-form-contract.py --spec <spec.json>` when requirements can be represented as JSON. The script loads `assets/form-engineering-policy.json` and `assets/error-message-patterns.json`, rejects missing parity, and emits a deterministic Markdown implementation contract.

## Asset Usage

- `assets/form-engineering-policy.json`: source of truth for required sections and allowed field types.
- `assets/error-message-patterns.json`: stable copy patterns for field, upload, server, network, and summary errors.
- `assets/optimistic-submit-template.ts`: implementation skeleton for idempotent optimistic submit behavior.
- `assets/upload-control-template.html`: accessible upload control baseline.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Validation parity | 100% | Each field rule includes client, server, and message. |
| Upload safety | 100% | Every file field declares accept, max size, preview, progress, retry, and storage boundary. |
| Accessibility coverage | 100% | Labels, field errors, summary, keyboard path, and aria-live are declared. |
| Determinism | 100% | Fixture output is stable under `scripts/check.sh`. |
