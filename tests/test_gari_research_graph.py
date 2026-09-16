import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from maat.api import app
from maat.research import (
    CANONICAL_GARI_RELATIONS,
    ResearchEdge,
    ResearchEvidenceState,
    ResearchGraphRequest,
    ResearchNode,
    ResearchObjectType,
    build_research_graph,
    demo_research_graph,
)


client = TestClient(app)


def test_all_gari_object_types_are_representable() -> None:
    nodes = [
        ResearchNode(id=f"n-{index}", object_type=object_type, canonical_name=object_type.value)
        for index, object_type in enumerate(ResearchObjectType)
    ]
    graph = build_research_graph(ResearchGraphRequest(title="Universal ontology", nodes=nodes))
    assert len(graph.nodes) == 24
    assert set(graph.summary.type_counts) == {item.value for item in ResearchObjectType}


def test_research_graph_preserves_evidence_branch_owner_and_proof() -> None:
    node = ResearchNode(
        id="claim-1",
        object_type=ResearchObjectType.Claim,
        canonical_name="Bounded claim",
        branch="NEUROFORGE",
        program_id="P-1",
        status="UNRESOLVED",
        evidence_state=ResearchEvidenceState.E2_FORMAL,
        evidence_grade="B",
        owner="GARI-VERITAS",
        source_refs=["source://one"],
        provenance=["THOTH:memory:one"],
        proof_refs=["proof://one"],
    )
    graph = build_research_graph(ResearchGraphRequest(nodes=[node]))
    projected = graph.nodes[0]
    assert projected.branch == "NEUROFORGE"
    assert projected.owner == "GARI-VERITAS"
    assert projected.evidence_state == ResearchEvidenceState.E2_FORMAL
    assert projected.source_refs == ["source://one"]
    assert projected.provenance == ["THOTH:memory:one"]
    assert projected.proof_refs == ["proof://one"]
    assert graph.summary.unresolved == 1


def test_edges_must_reference_existing_nodes() -> None:
    with pytest.raises(ValidationError):
        ResearchGraphRequest(
            nodes=[ResearchNode(id="a", object_type=ResearchObjectType.Source, canonical_name="Source")],
            edges=[ResearchEdge(source="a", target="missing", relation="SUPPORTS")],
        )


def test_duplicate_node_ids_are_rejected() -> None:
    with pytest.raises(ValidationError):
        ResearchGraphRequest(
            nodes=[
                ResearchNode(id="dup", object_type=ResearchObjectType.Source, canonical_name="A"),
                ResearchNode(id="dup", object_type=ResearchObjectType.Claim, canonical_name="B"),
            ]
        )


def test_canonical_gari_relations_include_core_research_edges() -> None:
    assert "SUPPORTS" in CANONICAL_GARI_RELATIONS
    assert "CONTRADICTS" in CANONICAL_GARI_RELATIONS
    assert "TESTS" in CANONICAL_GARI_RELATIONS
    assert "REPLICATES" in CANONICAL_GARI_RELATIONS
    assert "CORRECTS" in CANONICAL_GARI_RELATIONS


def test_demo_tracks_cycle_proof_and_next_question_without_scientific_promotion() -> None:
    graph = demo_research_graph()
    assert graph.contract == "GA-GARI-CASEGRAPH-UNIVERSAL-1.0"
    assert graph.provider == "MAAT-Universal-CaseGraph"
    assert graph.summary.proof_receipts == 1
    evidence = next(node for node in graph.nodes if node.id == "evidence-result")
    assert evidence.payload["scientific_validation_claimed"] is False
    assert evidence.payload["human_cognition_validated"] is False
    assert any(node.id == "next-question" for node in graph.nodes)
    assert "visual projection only" in graph.truth_boundary


def test_gari_api_and_visual_surface() -> None:
    demo = client.get("/gari/research-graph/demo")
    assert demo.status_code == 200
    assert demo.json()["summary"]["nodes"] >= 10

    ui = client.get("/gari")
    assert ui.status_code == 200
    assert "GARI CASEGRAPH UNIVERSAL" in ui.text
    assert "/static/gari.js" in ui.text

    ready = client.get("/ready")
    assert ready.status_code == 200
    assert ready.json()["gari_casegraph_universal"] == "ready"


def test_post_research_graph_returns_traceable_summary() -> None:
    response = client.post(
        "/gari/research-graph",
        json={
            "title": "Test research",
            "program_id": "TEST-1",
            "nodes": [
                {
                    "id": "q1",
                    "object_type": "ResearchQuestion",
                    "canonical_name": "Question",
                    "branch": "GARI-PRIME",
                    "status": "ACTIVE",
                    "evidence_state": "E1_OPERATIONAL",
                },
                {
                    "id": "p1",
                    "object_type": "ProofReceipt",
                    "canonical_name": "Receipt",
                    "branch": "ProofGrid",
                    "status": "VERIFIED",
                    "evidence_state": "E3_EXECUTABLE",
                    "proof_refs": ["proof://p1"],
                },
            ],
            "edges": [{"source": "q1", "target": "p1", "relation": "RELATED_TO"}],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["program_id"] == "TEST-1"
    assert body["summary"]["nodes"] == 2
    assert body["summary"]["proof_receipts"] == 1
    assert body["nodes"][1]["proof_refs"] == ["proof://p1"]
