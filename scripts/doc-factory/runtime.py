"""Runtime helpers for deterministic doc-factory execution."""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone


def timestamp_iso() -> str:
    """Return an ISO timestamp, honoring deterministic build inputs."""
    explicit = os.environ.get("DOC_FACTORY_TIMESTAMP")
    if explicit:
        return explicit

    source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        return datetime.fromtimestamp(int(source_date_epoch), timezone.utc).isoformat()

    return datetime.now(timezone.utc).isoformat()


def timestamp_slug(timestamp: str | None = None) -> str:
    """Return a stable filename/id-friendly timestamp slug."""
    timestamp = timestamp or timestamp_iso()
    compact = re.sub(r"[^0-9A-Za-z]+", "-", timestamp).strip("-")
    return compact or "unknown-time"


def display_timestamp(timestamp: str | None = None) -> str:
    """Return a compact timestamp for human-facing document footers."""
    timestamp = timestamp or timestamp_iso()
    return timestamp[:16].replace("T", " ")
