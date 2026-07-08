"""earliness_analyze.py — E2 조기성 지표 (사전등록 EARLINESS_PLAN §3). 미터링 0.

순수 지표 함수(궤적→선행시간·기울기·교차·잡음밴드)를 분리해 합성 궤적으로 전수
검증(test_earliness_analyze.py, 캐시/점수 불요). I/O 래퍼는 채점 산출물이 있을 때만
(runs/earliness/) 실측 궤적을 조립한다 — 없으면 "pending" 보고. 형태 판독 전용,
점별 유의성 주장 금지(잡음밴드 병기).
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FLAG_THRESHOLD = 50
QUARTER_DAYS = 91.3125
RP07_SIGMA_MEDIAN = 6.3   # inside-noise 참조 밴드 (RP-07 per-case σ 중위, pp)


def quarters_before(revelation: dt.date, snapshot_cutoff: dt.date) -> float:
    """폭로까지 남은 분기 (t). snapshot_cutoff <= revelation 전제 → t >= 0."""
    return round((revelation - snapshot_cutoff).days / QUARTER_DAYS, 2)


def detection_lead_time(trajectory: list[tuple[float, float]]) -> float | None:
    """궤적이 p>=50을 처음 넘는(폭로 접근 방향에서 가장 이른) 스냅샷의 t.

    trajectory = [(t, p)] (t=폭로까지 분기, 정렬 무관). 폭로에서 과거로 거슬러 볼 때
    '처음 신호가 켜진' 시점 = p>=50인 점들 중 t가 가장 큰(가장 이른) 것. 하나도 없으면
    None(플래그 안 켜짐). 비단조 궤적은 crossings()로 전체 교차를 별도 보고."""
    flagged = [t for t, p in trajectory if p >= FLAG_THRESHOLD]
    return max(flagged) if flagged else None


def crossings(trajectory: list[tuple[float, float]]) -> list[float]:
    """t 내림차순(과거→폭로)으로 훑을 때 임계선을 아래→위로 넘는 지점의 t 목록.
    비단조 궤적의 정직한 보고용 (여러 번 켜졌다 꺼지면 다 기록)."""
    traj = sorted(trajectory, key=lambda x: -x[0])  # 먼 과거부터
    out, prev_on = [], False
    for t, p in traj:
        on = p >= FLAG_THRESHOLD
        if on and not prev_on:
            out.append(t)
        prev_on = on
    return out


def ols_slope(trajectory: list[tuple[float, float]]) -> float | None:
    """p ~ t 최소자승 기울기 (pp per quarter). t가 클수록 과거이므로 음의 기울기 =
    폭로 접근 시 상승. 점 <2개면 None."""
    n = len(trajectory)
    if n < 2:
        return None
    sx = sum(t for t, _ in trajectory)
    sy = sum(p for _, p in trajectory)
    sxx = sum(t * t for t, _ in trajectory)
    sxy = sum(t * p for t, p in trajectory)
    denom = n * sxx - sx * sx
    if denom == 0:
        return None
    return round((n * sxy - sx * sy) / denom, 3)


def neighbor_moves_within_band(trajectory: list[tuple[float, float]],
                               sigma: float = RP07_SIGMA_MEDIAN) -> list[bool]:
    """이웃 스냅샷(연속 t) 간 |Δp|가 잡음밴드(σ) 안이면 True("변화 없음"). 형태 판독 보조."""
    traj = sorted(trajectory, key=lambda x: x[0])  # t 오름차순
    return [abs(traj[i + 1][1] - traj[i][1]) <= sigma for i in range(len(traj) - 1)]


# ---------- I/O 래퍼 (채점 산출물 있을 때만) ----------

def _snapshot0_p(case_id: str) -> int | None:
    for d in (REPO / "runs" / "main", REPO / "runs" / "wave2" / "scores"):
        f = d / f"{case_id}.json"
        if f.is_file():
            return json.loads(f.read_text(encoding="utf-8"))["misstatement_probability"]
    return None


def assemble_trajectory(base_case_id: str, revelation: dt.date, snapshot_dir: Path,
                        snapshot_cases: list[dict]) -> list[tuple[float, float]]:
    """스냅샷0(본실행 재사용) + 채점된 스냅샷 j → [(t, p)] 궤적."""
    traj: list[tuple[float, float]] = []
    p0 = _snapshot0_p(base_case_id)
    if p0 is not None:
        traj.append((0.0, float(p0)))
    for sc in snapshot_cases:
        f = snapshot_dir / f"{sc['case_id']}.json"
        if not f.is_file():
            continue
        p = json.loads(f.read_text(encoding="utf-8"))["misstatement_probability"]
        t = quarters_before(revelation, dt.date.fromisoformat(sc["cutoff_date"]))
        traj.append((t, float(p)))
    return sorted(traj, key=lambda x: x[0])


def main() -> int:
    out_dir = REPO / "runs" / "earliness" / "perturbed"
    cases_f = REPO / "runs" / "earliness" / "cases_earliness.json"
    if not cases_f.is_file() or not out_dir.exists():
        print("runs/earliness 채점 산출물 부재 → 분석 pending (감독 세션에서 채점 후).")
        print("순수 지표 함수는 test_earliness_analyze로 검증됨(캐시/점수 불요). 미터링 0.")
        return 0
    print("채점 산출물 감지 — 궤적/선행시간 분석 (형태 판독, 점별 유의성 주장 금지).")
    # 실제 조립·집계는 채점 후 감독 세션에서 (여기선 경로만 확정).
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
