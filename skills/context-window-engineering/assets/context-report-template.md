# Context Window Engineering Report: {application}

## Summary

- Max context: `{maxTokens}` tokens.
- Steady state: `{expectedSteadyStateTokens}` tokens.
- Compaction threshold: `{compactionThreshold}`.
- Static prefix blocks: `{staticPrefixIds}`.
- Dynamic tail blocks: `{dynamicTailIds}`.

## Static Prefix

{staticPrefixMarkdown}

## Middle Context

{middleMarkdown}

## Dynamic Tail

{dynamicTailMarkdown}

## Critical Rules

{criticalRulesMarkdown}

## Compaction

- Enabled: `{compactionEnabled}`.
- Preserve blocks: `{preserveBlockIds}`.
- Summarize kinds: `{summarizeBlockKinds}`.

## Validation

- Prefix byte-identical.
- No volatile state in the static prefix.
- Dynamic state is isolated in the final reminder.
- Critical rules are present at both edges.
- Compaction preserves context edges.
- Cache-hit and retention tests are defined.

## Risks

{risksMarkdown}
