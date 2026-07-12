"""date_shift.py — perturbation-v2 결정론 날짜 이동 (WS-5/F-2, specs/perturb_v2.md).

순수 함수 2개: offset_for_case(케이스별 주-단위 결정론 오프셋),
shift_payload(렌더 시점 균일 이동 + accession 마스킹).

순서 계약 (스펙 §3): 진짜 cutoff guard·build_payload의 컷오프 필터는 상류의
진짜 날짜에서 이미 완료된 상태다 — 본 모듈은 build_payload(perturb=True)
출력을 받아 렌더 직전에 이동만 한다. 전 날짜 단일 오프셋이므로 컷오프
비교·간격은 항등 불변 (test_date_shift.py가 기계 검증).

이 세션에서 교란 재실행 없음 — v2 프로브 런은 launch-ready (Q-F05).
동결 perturbation-v1 출력 불변.
"""
from __future__ import annotations

import datetime
import hashlib

SALT = "dateshift-v2"
W_LO, W_SPAN = 26, 53  # w ∈ [26, 78] → |offset| ∈ [182, 546]일


def offset_for_case(case_id: str) -> int:
    """케이스별 결정론 오프셋 (일 단위, 7의 배수, 부호 포함) — 스펙 §2."""
    h = hashlib.sha256(f"{case_id}{SALT}".encode()).digest()
    w = W_LO + (int.from_bytes(h[:4], "big") % W_SPAN)
    sign = 1 if h[4] & 1 else -1
    return sign * 7 * w


def shift_date(iso: str, offset_days: int) -> str:
    """ISO 날짜 문자열 이동. 파싱 불가 → 예외 (조용한 통과 금지)."""
    return str(datetime.date.fromisoformat(str(iso)) + datetime.timedelta(days=offset_days))


def shift_payload(payload: dict, offset_days: int | None = None) -> dict:
    """build_payload 출력의 전 가시 날짜에 단일 오프셋 적용 + accession 마스킹.

    입력을 변경하지 않는다 (새 dict 반환). offset_days 미지정 시
    case_id에서 유도. 스펙 §3: case.cutoff_date · 시계열 start/end/filed ·
    연대기 filing_date 전부 동일 오프셋; accession → 케이스 내 순차 중립 ID.
    """
    if offset_days is None:
        offset_days = offset_for_case(payload["case"]["case_id"])

    acc_map: dict[str, str] = {}

    def mask_acc(acc):
        if acc is None:
            return None
        if acc not in acc_map:
            acc_map[acc] = f"acc-{len(acc_map) + 1:03d}"
        return acc_map[acc]

    case = dict(payload["case"])
    case["cutoff_date"] = shift_date(case["cutoff_date"], offset_days)

    series = {}
    for tag, vals in payload["financial_series_point_in_time"].items():
        series[tag] = [{**v,
                        "start": shift_date(v["start"], offset_days) if v.get("start") else v.get("start"),
                        "end": shift_date(v["end"], offset_days),
                        "filed": shift_date(v["filed"], offset_days),
                        "accession": mask_acc(v.get("accession"))}
                       for v in vals]

    chronology = [{**r, "filing_date": shift_date(r["filing_date"], offset_days)}
                  for r in payload["filing_chronology"]]

    out = dict(payload)
    out["variant"] = "perturbed_v2_dateshift"
    out["case"] = case
    out["financial_series_point_in_time"] = series
    out["filing_chronology"] = chronology
    return out
