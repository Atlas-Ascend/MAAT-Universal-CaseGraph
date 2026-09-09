from __future__ import annotations

from enum import Enum
from hashlib import sha256
from typing import Literal

from pydantic import BaseModel, Field


class NodeType(str, Enum):
    person = "person"
    organization = "organization"
    requirement = "requirement"
    event = "event"
    claim = "claim"
    evidence = "evidence"
    risk = "risk"
    task = "task"
    decision = "decision"
    constraint = "constraint"
    artifact = "artifact"


class CaseNode(BaseModel):
    id: str
    type: NodeType
    label: str
    source_text: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    @classmethod
    def from_text(cls, node_type: NodeType, label: str, source_text: str) -> "CaseNode":
        raw = f"{node_type.value}:{label}:{source_text}".encode()
        return cls(id=sha256(raw).hexdigest()[:12], type=node_type, label=label, source_text=source_text)


class CaseEdge(BaseModel):
    source: str
    target: str
    relation: str


class Finding(BaseModel):
    kind: Literal["risk", "evidence_gap", "contradiction", "blocker"]
    summary: str
    node_ids: list[str] = []


class Action(BaseModel):
    title: str
    rationale: str
    node_ids: list[str] = []
    priority: int = 1


class CaseGraph(BaseModel):
    nodes: list[CaseNode] = []
    edges: list[CaseEdge] = []
    findings: list[Finding] = []
    actions: list[Action] = []


class ProofReceipt(BaseModel):
    status: Literal["PASS", "FAIL", "UNVERIFIED"]
    input_sha256: str
    graph_node_ids: list[str]
    selected_action: Action | None = None
    evidence: list[str] = []
