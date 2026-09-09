from __future__ import annotations

from .models import CaseGraph


def verify_graph(graph: CaseGraph) -> list[str]:
    """Return invariant violations. An empty list means the graph is structurally valid."""
    errors: list[str] = []
    node_ids = [node.id for node in graph.nodes]
    known = set(node_ids)

    if len(node_ids) != len(known):
        errors.append("duplicate_node_ids")

    for edge in graph.edges:
        if edge.source not in known:
            errors.append(f"edge_source_missing:{edge.source}")
        if edge.target not in known:
            errors.append(f"edge_target_missing:{edge.target}")

    for action in graph.actions:
        missing = sorted(set(action.node_ids) - known)
        if missing:
            errors.append(f"action_references_missing_nodes:{','.join(missing)}")

    return errors
