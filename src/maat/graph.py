from __future__ import annotations

import re

from .models import CaseEdge, CaseGraph, CaseNode, NodeType

_SENTENCE = re.compile(r"(?<=[.!?])\s+|\n+")


def _classify(text: str) -> NodeType:
    low = text.lower()
    if any(k in low for k in ("must", "needs", "requirement", "requires")):
        return NodeType.requirement
    if any(k in low for k in ("risk", "might", "may ", "unknown", "don't know", "do not know")):
        return NodeType.risk
    if any(k in low for k in ("by friday", "deadline", "yesterday", "today", "tomorrow")):
        return NodeType.event
    if any(k in low for k in ("owns", "owner", "assigned")):
        return NodeType.person
    if any(k in low for k in ("deploy", "validate", "verify", "finish", "complete")):
        return NodeType.task
    return NodeType.claim


def build_graph(text: str) -> CaseGraph:
    sentences = [s.strip() for s in _SENTENCE.split(text) if s.strip()]
    nodes = [CaseNode.from_text(_classify(s), s[:88], s) for s in sentences]
    graph = CaseGraph(nodes=nodes)

    for a in nodes:
        low = a.source_text.lower()
        if "depends on" in low or "depends upon" in low:
            for b in nodes:
                if a.id != b.id and any(token in b.source_text.lower() for token in ("api", "schema", "authentication")):
                    graph.edges.append(CaseEdge(source=a.id, target=b.id, relation="depends_on"))
        if "changed" in low:
            for b in nodes:
                if a.id != b.id and "requirement" in b.source_text.lower():
                    graph.edges.append(CaseEdge(source=a.id, target=b.id, relation="changes"))
    return graph
