from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from . import __version__
from .graph import build_graph
from .planner import plan
from .reasoner import analyze
from .receipts import make_receipt


class CaseResult(BaseModel):
    graph: dict[str, Any]
    receipt: dict[str, Any]
    meta: dict[str, Any] = Field(default_factory=dict)


def build_case(text: str) -> CaseResult:
    source = text.strip()
    if not source:
        raise ValueError("case text must contain non-whitespace content")

    graph = plan(analyze(build_graph(source)))
    receipt = make_receipt(source, graph)
    meta = {
        "system": "MAAT",
        "version": __version__,
        "run_id": receipt.run_id,
        "pipeline": receipt.pipeline_stages,
        "counts": {
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
            "findings": len(graph.findings),
            "actions": len(graph.actions),
        },
    }
    return CaseResult(
        graph=graph.model_dump(mode="json"),
        receipt=receipt.model_dump(mode="json"),
        meta=meta,
    )
