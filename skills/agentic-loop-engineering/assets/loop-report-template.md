# Agentic Loop Report: {name}

## Summary

- Model constant: `{modelConstant}`
- Client call: `{clientCall}`
- Budget: `{maxIterations}` iterations
- Stop reasons handled: `{stopReasons}`
- Tool handlers: `{handlers}`

## Generated Loop

```python
{generatedCode}
```

## Validation

- Control routes through `stop_reason`.
- `tool_use` dispatches named handlers and reinjects `tool_result`.
- `end_turn` returns the response.
- Unknown stop reasons raise `UnhandledStop`.
- Budget exhaustion raises `BudgetExceeded`.
- Instrumentation emits transition events.
