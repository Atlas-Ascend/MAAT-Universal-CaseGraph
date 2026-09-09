from maat.service import build_case


DEMO = """Client needs a software prototype by Friday.
Authentication isn't finished.
Sam owns the API.
The deployment depends on the API.
The client changed requirement #4 yesterday.
We don't know whether the new requirement may invalidate the existing database schema."""


def test_build_case_emits_graph_and_receipt():
    result = build_case(DEMO)
    assert result.graph["nodes"]
    assert result.graph["actions"]
    assert result.receipt["status"] == "PASS"
    assert result.receipt["selected_action"] is not None


def test_demo_exposes_evidence_gap():
    result = build_case(DEMO)
    kinds = {finding["kind"] for finding in result.graph["findings"]}
    assert "evidence_gap" in kinds
    assert "blocker" in kinds


def test_receipt_links_action_to_graph_nodes():
    result = build_case(DEMO)
    selected = result.receipt["selected_action"]
    known = set(result.receipt["graph_node_ids"])
    assert set(selected["node_ids"]).issubset(known)
