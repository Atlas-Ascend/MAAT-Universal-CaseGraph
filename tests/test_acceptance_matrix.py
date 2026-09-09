from pathlib import Path

import pytest

from maat.service import build_case

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(
    "filename",
    ["messy_case.txt", "incident_case.txt", "research_case.txt"],
)
def test_representative_cases_pass_pipeline(filename: str) -> None:
    result = build_case((EXAMPLES / filename).read_text())
    assert result.receipt["status"] == "PASS"
    assert result.receipt["verification_errors"] == []
    assert result.graph["nodes"]
    assert result.graph["actions"]
    assert result.meta["counts"]["nodes"] == len(result.graph["nodes"])
