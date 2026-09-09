from __future__ import annotations

from .models import CaseGraph, Finding


def analyze(graph: CaseGraph) -> CaseGraph:
    for node in graph.nodes:
        low = node.source_text.lower()
        if any(k in low for k in ("don't know", "do not know", "unknown", "unclear", "may invalidate")):
            graph.findings.append(Finding(kind="evidence_gap", summary=f"Unresolved evidence: {node.label}", node_ids=[node.id]))
        if "depends on" in low:
            graph.findings.append(Finding(kind="blocker", summary=f"Dependency requires resolution: {node.label}", node_ids=[node.id]))
        if "changed" in low and "requirement" in low:
            graph.findings.append(Finding(kind="risk", summary=f"Changed requirement may invalidate downstream state: {node.label}", node_ids=[node.id]))
    return graph
