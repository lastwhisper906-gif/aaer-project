"""Brier score 계산 (Loop-3 3자 비교 지원 — 결정론).

입력: JSON [{"case_id": "case_NN", "p": 0-100}, ...] 경로들 + 정답 매핑.
정답: scoring/id_mapping.json + candidates.json group (treatment=1, control=0).
사용: python tools/brier.py <predictions.json> [<model_outputs.json> ...]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def labels() -> dict:
    mapping = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))
    cands = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8"))["candidates"]}
    out = {}
    for neutral, original in mapping["mapping"].items():
        out[neutral] = 1.0 if cands[original]["group"] == "treatment" else 0.0
    return out


def brier(preds: list[dict], y: dict) -> tuple[float, int]:
    total, n = 0.0, 0
    for row in preds:
        cid = row["case_id"]
        if cid not in y:
            continue
        total += (row["p"] / 100.0 - y[cid]) ** 2
        n += 1
    return (total / n if n else float("nan")), n


def main() -> int:
    y = labels()
    baseline = sum((0.5 - v) ** 2 for v in y.values()) / len(y)
    print(f"constant-0.5 baseline Brier = {baseline:.4f} (n={len(y)})")
    for path in sys.argv[1:]:
        preds = json.loads(Path(path).read_text(encoding="utf-8"))
        score, n = brier(preds, y)
        print(f"{path}: Brier = {score:.4f} (n={n})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
