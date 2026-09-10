from maat.hypernet_v3 import consume_hypernet_event_v3


def test_casegraph_acknowledges_hypernet_v3_event():
    event = {
        "event_id": "dhv3-proof-20260910-001",
        "entity_type": "system",
        "entity_id": "data-hypernet-v3",
        "operation": "verified",
        "truth_state": "VERIFIED",
        "payload": {"state": "vertical-slice", "seca": "PASS"},
        "lineage": {"proof_id": "PRF-DATA-HYPERNET-V3-001"},
        "provenance": {"origin": "hypernet-v3"},
        "content_hash": "dhv3-proof-hash-001",
    }
    ack = consume_hypernet_event_v3(event)
    assert ack.event_id == event["event_id"]
    assert ack.consumer == "UNIVERSAL_CASEGRAPH"
    assert ack.status == "ACK"
    assert ack.node_ids
    assert len(ack.content_hash) == 64
