"""베이스라인 스크린의 방법론 규율 테스트.

1. point-in-time 속성 (§5-1의 베이스라인 확장): 컷오프 후 제출 fact는 배제,
   컷오프 전 제출분 중에서는 최신 filed가 승리 — 재작성 수치가 '원본인 척'
   들어오지 못한다는 성질의 기계 강제.
2. 베이스라인 누출 차단: 베이스라인 출력 필드가 피평가자 페이로드
   (data/evaluatee/cases.json + WHITELIST)에 나타나지 않는다.
3. 결정론 정적 스캔: screens.py는 네트워크 라이브러리·현재 시각을 쓰지 않는다.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from screens import _iso, load_facts  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SCREENS_SRC = (Path(__file__).resolve().parent / "screens.py").read_text(encoding="utf-8")

BASELINE_OUTPUT_MARKERS = [
    "m_score", "f_score", "c_score", "beneish", "dechow", "montier", "sloan",
    "DSRI", "GMI", "AQI", "SGI", "DEPI", "SGAI", "LVGI", "TATA", "rsst",
]


def _fake_companyfacts(tmp_path, facts):
    d = tmp_path / "FAKE" / "xbrl"
    d.mkdir(parents=True)
    (d / "CIK0000000001.json").write_text(json.dumps(
        {"facts": {"us-gaap": {"Assets": {"units": {"USD": facts}}}}}), encoding="utf-8")
    return tmp_path


def test_point_in_time_excludes_post_cutoff_filings(tmp_path, monkeypatch):
    facts = [
        # 원본 10-K: 컷오프 전 제출 — 채택되어야 함
        {"end": "2013-12-31", "val": 100, "accn": "0000000001-14-000001",
         "form": "10-K", "filed": "2014-02-01"},
        # 재작성 10-K/A: 컷오프 후 제출 — point-in-time상 존재하지 않아야 함
        {"end": "2013-12-31", "val": 999, "accn": "0000000001-15-000001",
         "form": "10-K/A", "filed": "2015-06-01"},
    ]
    monkeypatch.setattr("screens.DATA_DIR", _fake_companyfacts(tmp_path, facts))
    table = load_facts("FAKE", _iso("2014-05-12"))
    got = table["Assets"][_iso("2013-12-31")]
    assert got["val"] == 100, "컷오프 후 재작성 수치가 원본을 덮어씀 — look-ahead 위반"
    assert got["filed"] == "2014-02-01"


def test_point_in_time_pre_cutoff_amendment_wins(tmp_path, monkeypatch):
    facts = [
        {"end": "2013-12-31", "val": 100, "accn": "0000000001-14-000001",
         "form": "10-K", "filed": "2014-02-01"},
        # 컷오프 전 정정 — 시장이 알고 있던 최신 값이므로 이것이 채택
        {"end": "2013-12-31", "val": 150, "accn": "0000000001-14-000002",
         "form": "10-K/A", "filed": "2014-03-01"},
    ]
    monkeypatch.setattr("screens.DATA_DIR", _fake_companyfacts(tmp_path, facts))
    table = load_facts("FAKE", _iso("2014-05-12"))
    assert table["Assets"][_iso("2013-12-31")]["val"] == 150


def test_baseline_outputs_not_in_evaluatee_payload():
    evaluatee = REPO / "data" / "evaluatee" / "cases.json"
    text = evaluatee.read_text(encoding="utf-8")
    leaked = [m for m in BASELINE_OUTPUT_MARKERS if m.lower() in text.lower()]
    assert not leaked, f"피평가자 파일에 베이스라인 출력 마커 누출: {leaked}"

    builder = (REPO / "tools" / "build_evaluatee_inputs.py").read_text(encoding="utf-8")
    assert "baselines" not in builder, "피평가자 빌더가 베이스라인 모듈을 참조 — 누출 경로"
    m = re.search(r"WHITELIST\s*=\s*\[([^\]]*)\]", builder)
    assert m, "빌더 WHITELIST 미발견"
    whitelist = re.findall(r'"([^"]+)"', m.group(1))
    overlap = [w for w in whitelist if any(mk.lower() in w.lower() for mk in BASELINE_OUTPUT_MARKERS)]
    assert not overlap, f"WHITELIST에 베이스라인 필드: {overlap}"


def test_screens_static_scan_no_network_no_wallclock():
    forbidden = {
        "network import": re.compile(
            r"^\s*(import|from)\s+(requests|urllib|http\.client|httpx|aiohttp|socket)\b", re.M),
        "wall clock": re.compile(r"datetime\.(datetime\.)?now\(|date\.today\(|time\.time\("),
    }
    hits = [label for label, pat in forbidden.items() if pat.search(SCREENS_SRC)]
    assert not hits, f"screens.py 결정론/오프라인 규율 위반: {hits}"
