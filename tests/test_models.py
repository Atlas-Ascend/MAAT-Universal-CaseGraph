from maat.models import CaseGraph, Finding


def test_collection_defaults_are_isolated() -> None:
    first = CaseGraph()
    second = CaseGraph()
    first.findings.append(Finding(kind="risk", summary="test"))
    assert second.findings == []
