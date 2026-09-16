#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from maat.research import demo_research_graph
from maat.service import build_case

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    build_truth = sorted((ROOT / "build-truth").glob("*.md"))
    if len(build_truth) != 17:
        raise SystemExit(f"expected 17 Build Truth files, found {len(build_truth)}")
    gari_truth = ROOT / "build-truth" / "17-GARI-CASEGRAPH-UNIVERSAL.md"
    if not gari_truth.exists():
        raise SystemExit("missing GARI CaseGraph Universal Build Truth")

    examples = sorted((ROOT / "examples").glob("*.txt"))
    if len(examples) < 3:
        raise SystemExit("expected at least 3 representative case fixtures")

    for fixture in examples:
        result = build_case(fixture.read_text())
        if result.receipt["status"] != "PASS":
            raise SystemExit(f"fixture failed: {fixture.name}")
        if result.receipt["verification_errors"]:
            raise SystemExit(f"fixture invariant failure: {fixture.name}")

    research_graph = demo_research_graph()
    if research_graph.summary.nodes < 10:
        raise SystemExit("GARI research graph demo did not materialize expected objects")
    if research_graph.summary.proof_receipts != 1:
        raise SystemExit("GARI research graph demo proof receipt invariant failed")
    if "visual projection only" not in research_graph.truth_boundary:
        raise SystemExit("GARI research graph truth boundary missing")

    required = [ROOT / "docs" / "SDLC.md", ROOT / "docs" / "OPERATIONS.md", ROOT / "docs" / "SECURITY.md"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"missing lifecycle docs: {', '.join(missing)}")

    print(
        "MAAT preflight PASS: "
        f"build_truth={len(build_truth)} fixtures={len(examples)} gari_nodes={research_graph.summary.nodes}"
    )


if __name__ == "__main__":
    main()
