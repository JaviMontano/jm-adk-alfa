# Error Recovery Checklist

- Preserve every valid answer after field validation, server validation, upload failure, or network failure.
- Move focus to the first invalid field only after submit or explicit step continuation.
- Show a top summary with links to invalid fields after submit.
- Keep inline errors next to fields and connect them with `aria-describedby`.
- Provide a retry action for network, upload, and server failures.
- Avoid validating on every keypress unless the feedback is non-blocking and debounced.
