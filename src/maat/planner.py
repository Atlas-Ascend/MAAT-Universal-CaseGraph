from __future__ import annotations

from .models import Action, CaseGraph


def plan(graph: CaseGraph) -> CaseGraph:
    gaps = [f for f in graph.findings if f.kind == "evidence_gap"]
    risks = [f for f in graph.findings if f.kind == "risk"]
    blockers = [f for f in graph.findings if f.kind == "blocker"]

    if gaps:
        focus = gaps[0]
        graph.actions.append(Action(title="Resolve highest-impact evidence gap", rationale=focus.summary, node_ids=focus.node_ids, priority=1))
    if risks:
        focus = risks[0]
        graph.actions.append(Action(title="Validate changed requirement against downstream assumptions", rationale=focus.summary, node_ids=focus.node_ids, priority=2))
    if blockers:
        focus = blockers[0]
        graph.actions.append(Action(title="Clear blocking dependency", rationale=focus.summary, node_ids=focus.node_ids, priority=3))
    if not graph.actions:
        graph.actions.append(Action(title="Confirm case state", rationale="No explicit blockers were detected; verify the normalized graph before action.", node_ids=[n.id for n in graph.nodes[:3]], priority=1))

    graph.actions.sort(key=lambda a: a.priority)
    return graph
