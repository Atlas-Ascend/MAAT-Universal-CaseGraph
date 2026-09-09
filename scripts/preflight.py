from __future__ import annotations

from pathlib import Path

from maat.service import build_case

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    build_truth = sorted((ROOT / "build-truth").glob("*.md"))
    if len(build_truth) != 16:
        raise SystemExit(f"expected 16 Build Truth files, found {len(build_truth)}")

    examples = sorted((ROOT / "examples").glob("*.txt"))
    if len(examples) < 3:
        raise SystemExit("expected at least 3 representative case fixtures")

    for fixture in examples:
        result = build_case(fixture.read_text())
        if result.receipt["status"] != "PASS":
            raise SystemExit(f"fixture failed: {fixture.name}")
        if result.receipt["verification_errors"]:
            raise SystemExit(f"fixture invariant failure: {fixture.name}")

    required = [ROOT / "docs" / "SDLC.md", ROOT / "docs" / "OPERATIONS.md", ROOT / "docs" / "SECURITY.md"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"missing lifecycle docs: {', '.join(missing)}")

    print(f"MAAT preflight PASS: build_truth={len(build_truth)} fixtures={len(examples)}")


if __name__ == "__main__":
    main()
