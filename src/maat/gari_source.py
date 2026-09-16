from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .research import ResearchCaseGraph, ResearchGraphRequest, build_research_graph

GARI_CANONICAL_SOURCE = (
    "Atlas-Ascend/Ghost-Atlas-Research-Institute@main:"
    "data/gari_casegraph_canonical_snapshot.json"
)
BUNDLED_SNAPSHOT = Path(__file__).resolve().parents[2] / "data" / "gari_casegraph_canonical_snapshot.json"
_CACHE_TTL_SECONDS = 60.0
_cache: tuple[float, dict[str, Any]] | None = None


def _load_bundled_snapshot() -> dict[str, Any]:
    payload = json.loads(BUNDLED_SNAPSHOT.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("bundled canonical GARI snapshot must be a JSON object")
    if payload.get("graph_id") != "GARI-CANONICAL-RESEARCH-MAP-20260916":
        raise ValueError("bundled GARI snapshot identity mismatch")
    return payload


def load_snapshot(*, force: bool = False) -> dict[str, Any]:
    """Return the verified public-safe projection mirror of private GARI canon.

    Ghost-Atlas-Research-Institute remains the canonical source of truth. MAAT is a
    public visualization provider, so it ships the source-reviewed projection
    instead of requiring credentials to the private Institute repository at runtime.
    """
    global _cache
    now = time.monotonic()
    if not force and _cache and now - _cache[0] < _CACHE_TTL_SECONDS:
        return _cache[1]
    payload = _load_bundled_snapshot()
    _cache = (now, payload)
    return payload


def build_canonical_gari_graph(snapshot: dict[str, Any] | None = None) -> ResearchCaseGraph:
    payload = snapshot if snapshot is not None else load_snapshot()
    request = ResearchGraphRequest.model_validate(
        {
            "title": payload["title"],
            "program_id": payload.get("program_id"),
            "nodes": payload.get("objects", []),
            "edges": payload.get("edges", []),
        }
    )
    graph = build_research_graph(request)
    graph.graph_id = payload.get("graph_id", graph.graph_id)
    graph.truth_boundary = payload.get("truth_boundary", graph.truth_boundary)
    return graph
