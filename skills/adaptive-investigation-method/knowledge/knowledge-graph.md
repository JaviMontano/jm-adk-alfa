# Adaptive Investigation Method -- Knowledge Graph

## Core Concepts

- `adaptive-investigation-method`: bounded investigation loop for unknown domains.
- `hard-budget`: total exploration limit and decrementing counter.
- `cheap-surface-map`: low-cost structure and signal scan before full reads.
- `ranked-hypotheses`: prioritized falseable claims tied to candidate nodes.
- `selective-deep-dive`: expensive read of only the highest-value node.
- `disciplined-replan`: replan only after `hypothesis_invalidated`.
- `typed-scratchpad`: persisted `plan`, `hypotheses`, and `findings`.

## Flow

`Goal` -> `hard-budget` -> `cheap-surface-map` -> `ranked-hypotheses` -> `selective-deep-dive` -> `disciplined-replan or deliverable`
