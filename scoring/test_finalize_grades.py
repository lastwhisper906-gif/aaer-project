"""finalize_grades 안전 로직 테스트 (게이트·dry-run·flip) — 합성 픽스처, CI 상주."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import finalize_grades as fg


def _setup(tmp, hf=False, gate=False):
    d = tmp / "scoring" / "grades_wave2"
    d.mkdir(parents=True)
    for cid, band in (("case_01", 2), ("case_02", 1)):
        (d / f"{cid}.json").write_text(json.dumps(
            {"dim1_probability_band": band, "_meta": {"human_finalized": hf}}), encoding="utf-8")
    ov = tmp / "scoring" / "overrides.md"
    ov.write_text("... RP-13-FINALIZE: YES ..." if gate else "no gate", encoding="utf-8")
    return d, ov


def _patch(monkeypatch, tmp, ov):
    monkeypatch.setattr(fg, "REPO", tmp)
    monkeypatch.setattr(fg, "DIRS", ["scoring/grades_wave2"])
    monkeypatch.setattr(fg, "OVERRIDES", ov)


def test_pending_lists_unfinalized(tmp_path, monkeypatch):
    d, ov = _setup(tmp_path)
    _patch(monkeypatch, tmp_path, ov)
    assert len(fg.pending()) == 2


def test_commit_refused_without_gate_changes_nothing(tmp_path, monkeypatch):
    d, ov = _setup(tmp_path, gate=False)
    _patch(monkeypatch, tmp_path, ov)
    assert fg.main(commit=True) == 2  # 거부
    assert json.loads((d / "case_01.json").read_text())["_meta"]["human_finalized"] is False


def test_dry_run_changes_nothing(tmp_path, monkeypatch):
    d, ov = _setup(tmp_path, gate=True)  # 게이트 있어도 dry-run은 안 바꿈
    _patch(monkeypatch, tmp_path, ov)
    assert fg.main(commit=False) == 0
    assert json.loads((d / "case_01.json").read_text())["_meta"]["human_finalized"] is False


def test_commit_with_gate_finalizes(tmp_path, monkeypatch):
    d, ov = _setup(tmp_path, gate=True)
    _patch(monkeypatch, tmp_path, ov)
    assert fg.main(commit=True) == 0
    assert json.loads((d / "case_01.json").read_text())["_meta"]["human_finalized"] is True
    assert fg.pending() == []
