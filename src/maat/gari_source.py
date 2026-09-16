from __future__ import annotations

import json
import time
from typing import Any
from urllib.request import Request, urlopen

from .research import ResearchCaseGraph, ResearchGraphRequest, build_research_graph

GARI_CANONICAL_SNAPSHOT_URL = (
    "https://raw.githubusercontent.com/Atlas-Ascend/Ghost-Atlas-Research-Institute/"
    "main/data/gari_casegraph_canonical_snapshot.json"
)
_CACHE_TTL_SECONDS = 60.0
_cache: tuple[float, dict[str, Any]] | None = None


def _fetch_snapshot(url: str = GARI_CANONICAL_SNAPSHOT_URL) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "MAAT-GARI-CaseGraph/0.3"})
    with urlopen(request, timeout=12) as response:  # fixed public GitHub source by default
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("canonical GARI snapshot must be a JSON object")
    return payload


def load_snapshot(*, force: bool = False) -> dict[str, Any]:
    global _cache
    now = time.monotonic()
    if not force and _cache and now - _cache[0] < _CACHE_TTL_SECONDS:
        return _cache[1]
    payload = _fetch_snapshot()
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
