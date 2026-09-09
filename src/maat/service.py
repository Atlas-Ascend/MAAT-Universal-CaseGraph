from __future__ import annotations

from pydantic import BaseModel

from .graph import build_graph
from .planner import plan
from .reasoner import analyze
from .receipts import make_receipt


class CaseResult(BaseModel):
    graph: dict
    receipt: dict


def build_case(text: str) -> CaseResult:
    graph = plan(analyze(build_graph(text)))
    receipt = make_receipt(text, graph)
    return CaseResult(graph=graph.model_dump(mode="json"), receipt=receipt.model_dump(mode="json"))
