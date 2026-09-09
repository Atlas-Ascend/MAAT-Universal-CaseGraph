from __future__ import annotations

from hashlib import sha256

from .models import CaseGraph, ProofReceipt
from .verification import verify_graph

PIPELINE_STAGES = ["INGEST", "GRAPH", "REASON", "PLAN", "VERIFY", "RECEIPT"]


def make_receipt(source_text: str, graph: CaseGraph) -> ProofReceipt:
    digest = sha256(source_text.encode()).hexdigest()
    selected = graph.actions[0] if graph.actions else None
    evidence = [node.source_text for node in graph.nodes if selected and node.id in selected.node_ids]
    errors = verify_graph(graph)

    if not graph.nodes or selected is None:
        status = "UNVERIFIED"
    elif errors:
        status = "FAIL"
    else:
        status = "PASS"

    return ProofReceipt(
        status=status,
        run_id=f"maat-{digest[:12]}",
        input_sha256=digest,
        graph_node_ids=[node.id for node in graph.nodes],
        selected_action=selected,
        evidence=evidence,
        verification_errors=errors,
        pipeline_stages=PIPELINE_STAGES,
    )
