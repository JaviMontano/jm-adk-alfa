#!/usr/bin/env python3
"""Message Batches helper for offline, latency-tolerant workloads (Kata 17).

For non-interactive loads (audits, backfills, evals), the Message Batches API
runs thousands of requests at ~50% cost. Each request carries a unique
custom_id that correlates request<->response and isolates partial failures.

This module provides the canonical lifecycle (create -> poll -> results) and
selective retry of only the failed requests (by custom_id), without depending
on a live API key at import time. The actual API client is injected, so the
ciclo is unit-testable and CI-safe.

Anti-pattern this replaces:
    for item in ten_thousand_items:
        r = client.messages.create(**params(item))   # real-time price, no custom_id,
        save(r)                                       # breaks rate limits, no fail-isolation
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class BatchRequest:
    custom_id: str
    params: dict


def build_requests(items: list[dict], prefix: str = "audit") -> list[BatchRequest]:
    """One request per item, each with a UNIQUE custom_id (the only key that maps
    a response back to its input; duplicates = ambiguity)."""
    seen: set[str] = set()
    requests: list[BatchRequest] = []
    for i, item in enumerate(items):
        custom_id = item.get("custom_id") or f"{prefix}-{i}"
        if custom_id in seen:
            raise ValueError(f"duplicate custom_id '{custom_id}' breaks request<->response correlation")
        seen.add(custom_id)
        requests.append(BatchRequest(custom_id=custom_id, params=item.get("params", {})))
    return requests


@dataclass
class BatchResult:
    succeeded: dict[str, dict] = field(default_factory=dict)
    failed: dict[str, dict] = field(default_factory=dict)

    @property
    def partial(self) -> bool:
        return bool(self.failed) and bool(self.succeeded)


def run_batch(client, requests: list[BatchRequest], *, sleep: Callable[[float], None], poll_seconds: int = 30) -> BatchResult:
    """Canonical lifecycle: create -> poll processing_status until 'ended' -> results.
    `client` must expose messages.batches.{create,retrieve,results}. `sleep` is injected
    for testability."""
    batch = client.messages.batches.create(
        requests=[{"custom_id": r.custom_id, "params": r.params} for r in requests]
    )
    while getattr(batch, "processing_status", "ended") != "ended":
        sleep(poll_seconds)
        batch = client.messages.batches.retrieve(batch.id)

    result = BatchResult()
    for entry in client.messages.batches.results(batch.id):
        cid = entry.custom_id
        if getattr(entry.result, "type", "succeeded") == "succeeded":
            result.succeeded[cid] = entry.result
        else:
            result.failed[cid] = entry.result
    return result


def retry_failed(client, original: list[BatchRequest], failed_ids: list[str], *, sleep: Callable[[float], None]) -> BatchResult:
    """Fragment the batch: re-submit ONLY the failed requests (by custom_id), not the
    whole batch. A 99% success batch should deliver 9900 results, not re-pay for all."""
    by_id = {r.custom_id: r for r in original}
    subset = [by_id[cid] for cid in failed_ids if cid in by_id]
    if not subset:
        return BatchResult()
    return run_batch(client, subset, sleep=sleep)


def main() -> int:
    parser = argparse.ArgumentParser(description="Message Batches helper (Kata 17)")
    parser.add_argument("--dry-run", action="store_true", help="Validate request construction without calling the API")
    parser.add_argument("--items", help="Path to a JSON array of {custom_id?, params} items")
    args = parser.parse_args()

    if args.dry_run:
        items = []
        if args.items:
            items = json.loads(open(args.items, encoding="utf-8").read())
        else:
            items = [{"params": {"x": 1}}, {"params": {"x": 2}}]
        requests = build_requests(items)
        print(f"dry-run: built {len(requests)} requests; unique custom_ids="
              f"{len({r.custom_id for r in requests})}")
        return 0

    print("This helper requires an injected Anthropic client. Import run_batch/retry_failed "
          "from your batch driver; use --dry-run to validate request construction.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
