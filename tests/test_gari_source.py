from fastapi.testclient import TestClient

from maat.api import app
from maat.gari_source import GARI_CANONICAL_SOURCE, build_canonical_gari_graph, load_snapshot

client = TestClient(app)


def snapshot() -> dict:
    return {
        "graph_id": "gari-test-canonical",
        "title": "Canonical GARI Test",
        "program_id": "GARI-TEST",
        "truth_boundary": "projection does not promote science",
        "objects": [
            {
                "id": "program",
                "object_type": "ResearchProgram",
                "canonical_name": "Cognition Architecture",
                "branch": "NEUROFORGE",
                "status": "ACTIVE",
                "evidence_state": "E0_CANONICAL",
                "owner": "GARI",
            },
            {
                "id": "framework",
                "object_type": "Framework",
                "canonical_name": "NHCM",
                "branch": "NEUROFORGE",
                "status": "CANONICAL",
                "evidence_state": "E2_FORMAL",
                "owner": "Ghost Atlas Institute",
                "source_refs": ["canonical-source"],
            },
            {
                "id": "proof",
                "object_type": "ProofReceipt",
                "canonical_name": "Bounded execution receipt",
                "branch": "GARI-Provenance",
                "status": "VERIFIED",
                "evidence_state": "E3_EXECUTABLE",
                "owner": "ProofGrid",
                "proof_refs": ["proof-1"],
            },
        ],
        "edges": [
            {"source": "program", "target": "framework", "relation": "RELATED_TO"},
            {"source": "proof", "target": "framework", "relation": "VERIFIES"},
        ],
    }


def test_canonical_snapshot_build_preserves_graph_identity_and_boundary() -> None:
    graph = build_canonical_gari_graph(snapshot())
    assert graph.graph_id == "gari-test-canonical"
    assert graph.title == "Canonical GARI Test"
    assert graph.summary.nodes == 3
    assert graph.summary.edges == 2
    assert graph.summary.proof_receipts == 1
    assert graph.summary.evidence_state_counts["E2_FORMAL"] == 1
    assert graph.summary.evidence_state_counts["E3_EXECUTABLE"] == 1
    assert graph.truth_boundary == "projection does not promote science"


def test_bundled_public_safe_projection_is_full_canonical_map() -> None:
    payload = load_snapshot(force=True)
    assert payload["graph_id"] == "GARI-CANONICAL-RESEARCH-MAP-20260916"
    assert "Ghost-Atlas-Research-Institute@main" in GARI_CANONICAL_SOURCE
    graph = build_canonical_gari_graph(payload)
    assert graph.summary.nodes >= 60
    assert graph.summary.edges >= 70
    assert graph.summary.proof_receipts >= 3
    names = {node.canonical_name for node in graph.nodes}
    assert "NHCM" in names
    assert "CSA-95" in names
    assert "Consciousness Cartography OS Ω9" in names
    assert "Walking Until The Machine Wakes" in names
    assert "GARI Brain Cycle 001 Governed Closure" in names
    assert "GARI Brain Cycle 002 — Memory Continuation" in names


def test_canonical_endpoint_uses_source_projection(monkeypatch) -> None:
    graph = build_canonical_gari_graph(snapshot())
    monkeypatch.setattr("maat.api.build_canonical_gari_graph", lambda: graph)
    response = client.get("/gari/research-graph/canonical")
    assert response.status_code == 200
    body = response.json()
    assert body["graph_id"] == "gari-test-canonical"
    assert body["summary"]["nodes"] == 3
    assert body["truth_boundary"] == "projection does not promote science"


def test_live_canonical_endpoint_uses_bundled_projection() -> None:
    response = client.get("/gari/research-graph/canonical")
    assert response.status_code == 200
    body = response.json()
    assert body["graph_id"] == "GARI-CANONICAL-RESEARCH-MAP-20260916"
    assert body["summary"]["nodes"] >= 60
    assert body["summary"]["edges"] >= 70


def test_ready_reports_canonical_gari_source() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["gari_casegraph_universal"] == "ready"
    assert response.json()["gari_canonical_source"] == "configured"
