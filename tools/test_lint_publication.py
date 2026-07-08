"""lint_publication — canon 동결값 + deprecated 차단 (감사 A3 회귀). CI 상주."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import lint_publication as lp


def test_canon_loads_and_returns_frozen_strings():
    c = lp.canon()  # 동결 JSON 로드 성공 + 값 반환
    assert c["wave1_perm_p"] == "0.00114"
    assert c["wave2_auc"] == "0.829"
    assert c["name_id_w2_frozen"] == "21.9%"


def test_deprecated_rp05_patterns_present_and_match():
    pats = [p for p, _ in lp.STALE]
    assert any(re.search(p, "wave-1 p = 0.0226") for p in pats)
    assert any(re.search(p, "AUC 0.797 reported") for p in pats)


def test_lint_doc_flags_deprecated_value(tmp_path, monkeypatch):
    (tmp_path / "README.md").write_text(
        "현행 wave-1 permutation p = 0.0226 이다.", encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    monkeypatch.setattr(lp, "controls", lambda: set())  # unified_table 미의존
    viol = lp.lint_doc("README.md")
    assert any("0.0226" in m or "RP-05" in m for _, m in viol)
