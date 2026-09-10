from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Any

from .graph import build_graph


@dataclass(frozen=True)
class HypernetAckV3:
    event_id: str
    consumer: str
    status: str
    node_ids: tuple[str, ...]
    edge_count: int
    content_hash: str
    metadata: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["node_ids"] = list(self.node_ids)
        return data


def _stable_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(raw).hexdigest()


def consume_hypernet_event_v3(event: dict[str, Any]) -> HypernetAckV3:
    """Project a Data Hypernet V3 event through MAAT's existing CaseGraph builder."""
    required = ("event_id", "entity_type", "entity_id", "operation", "payload", "content_hash")
    missing = [key for key in required if key not in event]
    if missing:
        raise ValueError(f"CASEGRAPH_HYPERNET_V3_MISSING_FIELDS:{','.join(missing)}")

    text = json.dumps(
        {
            "event_id": event["event_id"],
            "entity_type": event["entity_type"],
            "entity_id": event["entity_id"],
            "operation": event["operation"],
            "truth_state": event.get("truth_state"),
            "payload": event["payload"],
            "lineage": event.get("lineage", {}),
            "provenance": event.get("provenance", {}),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    graph = build_graph(text)
    node_ids = tuple(node.id for node in graph.nodes)
    ack_payload = {
        "event_id": event["event_id"],
        "consumer": "UNIVERSAL_CASEGRAPH",
        "status": "ACK",
        "node_ids": list(node_ids),
        "edge_count": len(graph.edges),
        "source_hash": event["content_hash"],
    }
    return HypernetAckV3(
        event_id=str(event["event_id"]),
        consumer="UNIVERSAL_CASEGRAPH",
        status="ACK",
        node_ids=node_ids,
        edge_count=len(graph.edges),
        content_hash=_stable_hash(ack_payload),
        metadata={"source_hash": event["content_hash"]},
    )
