from __future__ import annotations

from hashlib import sha256

from .models import CaseGraph, ProofReceipt


def make_receipt(source_text: str, graph: CaseGraph) -> ProofReceipt:
    selected = graph.actions[0] if graph.actions else None
    evidence = [n.source_text for n in graph.nodes if selected and n.id in selected.node_ids]
    return ProofReceipt(
        status="PASS" if selected and graph.nodes else "UNVERIFIED",
        input_sha256=sha256(source_text.encode()).hexdigest(),
        graph_node_ids=[n.id for n in graph.nodes],
        selected_action=selected,
        evidence=evidence,
    )
