from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, Field, model_validator


class ResearchObjectType(StrEnum):
    ResearchQuestion = "ResearchQuestion"
    Hypothesis = "Hypothesis"
    Claim = "Claim"
    Evidence = "Evidence"
    Source = "Source"
    Dataset = "Dataset"
    Experiment = "Experiment"
    Benchmark = "Benchmark"
    Simulation = "Simulation"
    Model = "Model"
    Framework = "Framework"
    ResearchProgram = "ResearchProgram"
    ResearchPacket = "ResearchPacket"
    BranchFinding = "BranchFinding"
    Synthesis = "Synthesis"
    Decision = "Decision"
    SoftwareSpecification = "SoftwareSpecification"
    Publication = "Publication"
    CaseStudy = "CaseStudy"
    CanonNode = "CanonNode"
    Correction = "Correction"
    Supersession = "Supersession"
    TelemetryObservation = "TelemetryObservation"
    ProofReceipt = "ProofReceipt"


class ResearchEvidenceState(StrEnum):
    E0_CANONICAL = "E0_CANONICAL"
    E1_OPERATIONAL = "E1_OPERATIONAL"
    E2_FORMAL = "E2_FORMAL"
    E3_EXECUTABLE = "E3_EXECUTABLE"
    E4_PREDICTIVE = "E4_PREDICTIVE"
    E5_DISCRIMINATIVE = "E5_DISCRIMINATIVE"
    E6_REPLICATED = "E6_REPLICATED"
    E7_INDEPENDENT = "E7_INDEPENDENT"


CANONICAL_GARI_RELATIONS = (
    "DERIVED_FROM",
    "SUPPORTS",
    "CONTRADICTS",
    "TESTS",
    "REPLICATES",
    "SUPERSEDES",
    "IMPLEMENTS",
    "SIMULATES",
    "DEPENDS_ON",
    "PRODUCED_BY",
    "REVIEWED_BY",
    "ROUTED_TO",
    "DEPLOYED_AS",
    "OBSERVED_IN_FIELD",
    "CORRECTS",
    "RELATED_TO",
)


class ResearchNode(BaseModel):
    id: str = Field(min_length=1, max_length=160)
    object_type: ResearchObjectType
    canonical_name: str = Field(min_length=1, max_length=400)
    description: str = ""
    branch: str | None = None
    program_id: str | None = None
    status: str = "UNKNOWN"
    evidence_state: ResearchEvidenceState | None = None
    evidence_grade: str | None = None
    deployment_status: str | None = None
    owner: str | None = None
    version: str | None = None
    access_class: str | None = None
    source_refs: list[str] = Field(default_factory=list)
    provenance: list[str] = Field(default_factory=list)
    proof_refs: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    related_objects: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class ResearchEdge(BaseModel):
    source: str = Field(min_length=1, max_length=160)
    target: str = Field(min_length=1, max_length=160)
    relation: str = Field(min_length=1, max_length=80)
    evidence_refs: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    status: str = "ACTIVE"


class ResearchGraphRequest(BaseModel):
    title: str = Field(default="GARI Research Graph", min_length=1, max_length=300)
    program_id: str | None = None
    nodes: list[ResearchNode] = Field(default_factory=list, max_length=10_000)
    edges: list[ResearchEdge] = Field(default_factory=list, max_length=40_000)

    @model_validator(mode="after")
    def validate_graph(self) -> ResearchGraphRequest:
        ids = [node.id for node in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("research graph node IDs must be unique")
        known = set(ids)
        for edge in self.edges:
            if edge.source not in known or edge.target not in known:
                raise ValueError(f"edge references unknown node: {edge.source}->{edge.target}")
        return self


class ResearchGraphSummary(BaseModel):
    nodes: int
    edges: int
    contradictions: int
    proof_receipts: int
    unresolved: int
    type_counts: dict[str, int]
    branch_counts: dict[str, int]
    evidence_state_counts: dict[str, int]
    status_counts: dict[str, int]


class ResearchCaseGraph(BaseModel):
    contract: str = "GA-GARI-CASEGRAPH-UNIVERSAL-1.0"
    provider: str = "MAAT-Universal-CaseGraph"
    graph_id: str
    title: str
    program_id: str | None = None
    nodes: list[ResearchNode]
    edges: list[ResearchEdge]
    summary: ResearchGraphSummary
    canonical_relations: tuple[str, ...] = CANONICAL_GARI_RELATIONS
    generated_at: str
    truth_boundary: str = (
        "visual projection only: GARI/LABCORE/THOTH remain canonical research-memory owners; "
        "CaseGraph does not promote claims or replace source/provenance systems"
    )


def _graph_id(request: ResearchGraphRequest) -> str:
    canonical = json.dumps(request.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return f"gari-cg-{sha256(canonical.encode()).hexdigest()[:20]}"


def build_research_graph(request: ResearchGraphRequest) -> ResearchCaseGraph:
    type_counts = Counter(node.object_type.value for node in request.nodes)
    branch_counts = Counter(node.branch for node in request.nodes if node.branch)
    evidence_counts = Counter(node.evidence_state.value for node in request.nodes if node.evidence_state)
    status_counts = Counter(node.status for node in request.nodes)
    contradictions = sum(1 for edge in request.edges if edge.relation == "CONTRADICTS")
    proofs = sum(1 for node in request.nodes if node.object_type == ResearchObjectType.ProofReceipt)
    unresolved = sum(1 for node in request.nodes if node.status.upper() in {"UNRESOLVED", "UNKNOWN", "BLOCKED"})

    return ResearchCaseGraph(
        graph_id=_graph_id(request),
        title=request.title,
        program_id=request.program_id,
        nodes=request.nodes,
        edges=request.edges,
        summary=ResearchGraphSummary(
            nodes=len(request.nodes),
            edges=len(request.edges),
            contradictions=contradictions,
            proof_receipts=proofs,
            unresolved=unresolved,
            type_counts=dict(sorted(type_counts.items())),
            branch_counts=dict(sorted(branch_counts.items())),
            evidence_state_counts=dict(sorted(evidence_counts.items())),
            status_counts=dict(sorted(status_counts.items())),
        ),
        generated_at=datetime.now(UTC).isoformat(),
    )


def demo_research_graph() -> ResearchCaseGraph:
    nodes = [
        ResearchNode(
            id="program-s33",
            object_type=ResearchObjectType.ResearchProgram,
            canonical_name="GARI Brain Cycle 001",
            description="Bounded synthetic model-comparison research cycle.",
            branch="NEUROFORGE",
            program_id="GARI-BRAIN-CYCLE-001",
            status="COMPLETE",
            evidence_state=ResearchEvidenceState.E3_EXECUTABLE,
            owner="GARI",
            proof_refs=["SPRINT_33_GARI_BRAIN_CLOSURE_PASS"],
        ),
        ResearchNode(
            id="question-coupling",
            object_type=ResearchObjectType.ResearchQuestion,
            canonical_name="Coupled-loop model discrimination",
            description="Can a coupled predictor outperform an independent-loop baseline when coupling is present?",
            branch="NEUROFORGE",
            program_id="GARI-BRAIN-CYCLE-001",
            status="ANSWERED_BOUNDED",
            evidence_state=ResearchEvidenceState.E2_FORMAL,
            owner="GARI-PRIME",
        ),
        ResearchNode(
            id="source-nhcm",
            object_type=ResearchObjectType.Source,
            canonical_name="NHCM / Cognitive Systems source-lock",
            description="Source-locked coupling/model-comparison commitments used by the benchmark.",
            branch="LABCORE",
            program_id="GARI-BRAIN-CYCLE-001",
            status="SOURCE_LOCKED",
            evidence_state=ResearchEvidenceState.E0_CANONICAL,
            owner="THOTH / LABCORE",
        ),
        ResearchNode(
            id="hypothesis-primary",
            object_type=ResearchObjectType.Hypothesis,
            canonical_name="Coupled predictor advantage",
            description="Coupled predictor should beat the independent baseline only when cross-loop coupling is present.",
            branch="NEUROFORGE",
            program_id="GARI-BRAIN-CYCLE-001",
            status="PARTIALLY_SUPPORTED_SYNTHETIC",
            evidence_state=ResearchEvidenceState.E2_FORMAL,
            owner="NEUROFORGE",
        ),
        ResearchNode(
            id="model-coupled",
            object_type=ResearchObjectType.Model,
            canonical_name="Coupled-loop predictor",
            branch="NEUROFORGE",
            program_id="GARI-BRAIN-CYCLE-001",
            status="EXECUTED",
            evidence_state=ResearchEvidenceState.E3_EXECUTABLE,
            owner="NEUROFORGE / Twinforge",
        ),
        ResearchNode(
            id="model-baseline",
            object_type=ResearchObjectType.Model,
            canonical_name="Independent-loop baseline",
            branch="NEUROFORGE",
            program_id="GARI-BRAIN-CYCLE-001",
            status="EXECUTED",
            evidence_state=ResearchEvidenceState.E3_EXECUTABLE,
            owner="NEUROFORGE / Twinforge",
        ),
        ResearchNode(
            id="benchmark-001",
            object_type=ResearchObjectType.Benchmark,
            canonical_name="Synthetic coupled-vs-independent benchmark",
            branch="GARI-Twinforge",
            program_id="GARI-BRAIN-CYCLE-001",
            status="PASS",
            evidence_state=ResearchEvidenceState.E3_EXECUTABLE,
            owner="GARI-Twinforge",
        ),
        ResearchNode(
            id="evidence-result",
            object_type=ResearchObjectType.Evidence,
            canonical_name="Primary pattern observed",
            description="Synthetic benchmark result retained at the executable/formal evidence boundary.",
            branch="GARI-VERITAS",
            program_id="GARI-BRAIN-CYCLE-001",
            status="PRIMARY_PATTERN_OBSERVED",
            evidence_state=ResearchEvidenceState.E3_EXECUTABLE,
            owner="GARI-VERITAS",
            payload={"scientific_validation_claimed": False, "human_cognition_validated": False},
        ),
        ResearchNode(
            id="proof-cycle-001",
            object_type=ResearchObjectType.ProofReceipt,
            canonical_name="Sprint 33 Cycle 001 verified receipt",
            branch="ProofGrid",
            program_id="GARI-BRAIN-CYCLE-001",
            status="VERIFIED",
            evidence_state=ResearchEvidenceState.E3_EXECUTABLE,
            owner="ProofGrid",
            proof_refs=["e5f1f30fbb1bbd71eee41247505f520eb3fef4b6e665370d43a63e4ec1589951"],
        ),
        ResearchNode(
            id="next-question",
            object_type=ResearchObjectType.ResearchQuestion,
            canonical_name="Equal-capacity nonlinear competitor test",
            description=(
                "Does the coupled-loop advantage survive an equal-capacity structurally different competing model "
                "and a nonlinear or switching generator?"
            ),
            branch="NEUROFORGE",
            program_id="GARI-BRAIN-CYCLE-002",
            status="ACTIVE_NEXT_QUESTION",
            evidence_state=ResearchEvidenceState.E2_FORMAL,
            owner="GARI-PRIME",
        ),
    ]
    edges = [
        ResearchEdge(source="source-nhcm", target="question-coupling", relation="DERIVED_FROM"),
        ResearchEdge(source="question-coupling", target="hypothesis-primary", relation="PRODUCED_BY"),
        ResearchEdge(source="hypothesis-primary", target="model-coupled", relation="TESTS"),
        ResearchEdge(source="hypothesis-primary", target="model-baseline", relation="TESTS"),
        ResearchEdge(source="model-coupled", target="benchmark-001", relation="TESTS"),
        ResearchEdge(source="model-baseline", target="benchmark-001", relation="TESTS"),
        ResearchEdge(source="benchmark-001", target="evidence-result", relation="PRODUCED_BY"),
        ResearchEdge(source="evidence-result", target="proof-cycle-001", relation="VERIFIED_BY"),
        ResearchEdge(source="evidence-result", target="next-question", relation="PRODUCED_BY"),
        ResearchEdge(source="program-s33", target="question-coupling", relation="RELATED_TO"),
        ResearchEdge(source="program-s33", target="proof-cycle-001", relation="RELATED_TO"),
    ]
    return build_research_graph(
        ResearchGraphRequest(
            title="GARI CaseGraph Universal — Brain Cycle 001 → 002",
            program_id="GARI-BRAIN-CYCLE-001",
            nodes=nodes,
            edges=edges,
        )
    )
