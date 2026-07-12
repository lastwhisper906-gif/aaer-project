# specs/B3_metasignal.md — B3 결정론 메타신호 기준선 사전 등록 (WS-2 / F-1)

> **freeze-commit-then-run**: 본 스펙 커밋은 `analysis/b3_compute.py`가 git
> 이력에 존재하기 **전에** 이루어진다 (`git log --follow`로 검증 가능).
> 아래 임계·윈도·집계식은 어떤 B3 점수도 계산되기 전에 고정된 것이다.

## 1. 동기 — 귀속 실험

피평가자 체크리스트(CL7)는 제출 연대기 이상 징후를 명시적으로 지시하고,
~236/240 모델 출력이 그 채널을 실제로 사용한다. 그러나 기존 기계 기준선은
비율 스크린 2종뿐이다 (B1 = Beneish M, B2 = Dechow F). **B3는 "사소한, 사전
등록된 연대기 규칙"이 발행된 분리(separation)의 얼마를 포착하는지의 상한을
잰다.** 이는 §8-6 위반이 아니다 — 결정론적 공식 베이스라인은 채점의 일부
(CLAUDE.md 스코프 가드 참고 단서).

## 2. 로스터 (tier별, 절대 pooled 금지)

| tier | treatment | control | 출처 (커밋된 동결 산출물) |
|---|---|---|---|
| wave-1 | 8 (T07 MON·T11 OFIX·T12 LOGI·T13 HTZ·T16 ICON·T17 MRVL·T21 SCOR·T28 KHC) | 22 (V01–V22) | `analysis/baseline_table.csv`의 group 열 (동결 30사 프레임) + cutoff join: T-id → `data/candidates/candidates.json`, V-id → `candidates_v2_controls.json` |
| wave-2 | 9 (T02·T04·T19·T20·T22·T23·T24·T26·T29) | 23 | `data/candidates/candidates_wave2.json` group 필드 (wave2_analyze.py 선례) |
| holdout | 3 (case_71 HUBG·case_72 WMK·case_73 GNE) | 9 (hc: VIASP·UTL·GRDX·RXO·BCO·XPO·GO·SFM·VLGEA) | `candidates_holdout.json` + `candidates_holdout_controls.json` |

candidates 레지스트리 접근은 **채점측(analysis/) 코드의 선례**를 따른다
(`wave2_analyze.py`가 동일 파일을 읽음) — 피평가자측(pipeline/) 코드 아님.
B3 입력은 ticker·cutoff_date·group 3필드만 사용한다 (scheme_summary 등
정답 서사는 읽지 않는다 — 결정론 규칙이므로 접촉 자체가 무의미하나 명시).

## 3. 윈도 (사전 등록 2종)

- **W4** = 365일, **W8** = 730일. 현재 윈도 = `cutoff − window_days <
  filingDate <= cutoff` (컷오프일 **포함**, 길이 정확히 window_days일).
- **W8이 1차(primary)** — 지금, 계산 전에 지정한다. 근거: 분식 은폐 기간은
  1년을 상시 초과하며, 집행 문헌의 위반종료→집행 중위값 ≈ **28.9개월**
  (약 2.4년). 1년 윈도는 은폐 중기의 신호(지연·정정)를 놓칠 수 있다.
  W4는 병기 보고.
- 선행 윈도 k (k=1,2,3): `cutoff − (k+1)·window_days < filingDate <=
  cutoff − k·window_days` (b_8kfreq 전용).

## 4. 이진 지표 6종 (케이스별 0/1, submissions JSON 윈도 내)

| 지표 | 규칙 (form 매칭은 정확히 아래대로) |
|---|---|
| `b_nt` | form이 `NT 10-K` 또는 `NT 10-Q`로 **시작** (각 /A 개정 포함 — 지연의 재확인도 지연 신호) |
| `b_ka` | form == `10-K/A` |
| `b_qa` | form == `10-Q/A` |
| `b_401` | form ∈ {`8-K`, `8-K/A`} 이고 WS-1 파서(`pipeline/payload_v2_extract.parse_items`)의 item 리스트에 `"4.01"` 포함 |
| `b_402` | 동일 규칙, `"4.02"` |
| `b_8kfreq` | 현재 윈도의 form == `8-K` (**/A 제외** — 개정은 새 사건 아님) 건수 > 1.5 × (선행 동일 길이 윈도 3개의 8-K 건수 **중위값**). 캐시 내 최초 filingDate > `cutoff − 4·window_days`이면 선행 3윈도 미충족 → **0으로 fail-closed + `insufficient_history` 플래그** |

- item 매칭은 파싱된 토큰의 **정확 일치** (`"4.01"` == 토큰). 2004-08 이전
  구형 번호 체계(`"5"`, `"7"`)는 매칭되지 않음 — 유니버스 내 모든 윈도가
  2004-08 이후임을 compute가 확인·기록한다.
- 날짜 파싱 불가 → 예외 (fail-closed, skip 금지). submissions 파일 부재 →
  예외, CLI 레벨 coverage 기록 (`coverage: n/N`, fetch 금지).

## 5. 집계 — 비가중 합

**B3 점수 = 6개 지표의 비가중 합 (0–6). 가중치 적합·로지스틱 회귀 금지.**
반과적합(anti-overfitting) 근거를 사전 등록한다: tier당 N = 30/32/12로
6개 계수를 정직하게 추정하기에 어림도 없다. 적합된 가중치는 표본 특이성
(idiosyncrasy)의 재서술이 되고, "사소한 규칙" 기준선의 자격을 잃는다.

## 6. 지표 통계 (동결 분석 계획 미러)

- **tie-aware AUC**: `analysis/stats.py::auc`와 동일 의미론
  ((gt + 0.5·eq) / (na·nb)). B3는 0–6 정수라 동률이 많다 — tie-aware가 필수.
- **bootstrap percentile 95% CI**: `stats.py::boot_auc_ci` 동일 의미론,
  N_BOOT = 10,000. 군별 독립 재추출.
- **단측 순열 검정** (treatment > control, 평균차): `stats.py::perm_test_mean`
  동일 의미론, N_PERM = 100,000.
- **seed 규율**: 신규 seed **SEED_B3 = 20260712** (본 스펙에서 선언 — 동결
  분석의 20260707과 분리, 재현 결정론 동일).
- tier별 보고 (wave-1, wave-2, holdout+controls), **절대 pooled 금지**.
- LLM AUC는 **재계산하지 않는다** — 커밋 동결 산출물에서 읽는다:
  wave-1 = `results_stats.json` primary.auc **0.8239**, wave-2 =
  `wave2_results.json` original.auc **0.829**. holdout은 동결 LLM AUC가
  존재하지 않음 (N=3, per-case 프레임) — holdout tier는 B3 자체 수치만
  보고하고 LLM 귀속비는 계산하지 않는다.

## 7. 사전 등록 해석 규칙 (R2b 아날로그 — 계산 전 고정)

`gap = AUC_LLM − 0.5` (tier별, 동결값). 판정은 **wave-2 · W8(1차)**에서:

- **(AUC_B3 − 0.5) / gap ≥ 0.5** → 판정 = "메타신호가 분리의 과반을 설명" →
  발행 표면의 능력 해석을 완화하는 **diff 제안 작성 의무** (diff-only,
  `review_packets/` + OWNER_QUEUE 게이트 — 직접 수정 금지).
- **≤ 0.2** → 판정 = "분리는 사소한 연대기 규칙에 귀속되지 않음" →
  비자명성 주장을 강화. **병기(co-report)만**, 주장 문언 무변경.
- **0.2 초과 0.5 미만** → 부분 귀속으로 보고, 어느 방향으로도 주장 변경 없음.

수치 대입 (wave-2 gap = 0.329): 경계값은 AUC_B3 = 0.6645(상단)·0.5658(하단).
wave-1은 동일 비를 **참고 병기**한다 (판정 tier는 wave-2 — 암기 교란이 덜한
tier에서의 귀속이 문제의 실체).

## 8. E2 통합 계약

`analysis/b3_compute.py`는 다음 시그니처를 **import 가능한 순수 함수**로
노출한다:

```python
def b3_score(ticker: str, cutoff: datetime.date, window_days: int) -> dict
# 반환: {"score": 0-6, "indicators": {...}, "flags": {"insufficient_history": bool},
#        "counts": {"eightk_current": int, "eightk_trailing": [int,int,int]}}
```

이미 동결된 E2 조기성 실험이 분기 스냅샷마다 zero-design-work로 호출할 수
있게 하기 위함이다. **E2 동결 파일은 어떤 것도 수정하지 않는다** — 인터페이스
제공까지가 본 워크스트림의 전부다.

## 9. 산출물

- `analysis/results_b3.json` — tier×윈도 전 지표, 케이스별 지표 벡터,
  coverage, 해석 규칙 판정 브랜치.
- `analysis/B3_REPORT.md` — tier별 표 (B1/B2/B3/LLM AUC 병렬, CI, 순열 p,
  coverage). B1/B2 동결 AUC가 존재하는 tier(wave-1: M 0.5104·F 0.5729)만
  해당 칸을 채우고, 부재 tier는 "동결값 없음"으로 명기 (재계산 금지).
- 해석 규칙 ≥0.5 브랜치 발화 시: `review_packets/` diff 제안 + OWNER_QUEUE
  게이트 항목.

## 10. 테스트 계약 (`analysis/test_b3_compute.py`, 픽스처 재사용/신설)

1. 윈도 경계: filingDate == cutoff 포함, == cutoff − window_days 제외.
2. 다중 item 문자열(`"2.02,9.01"` 등)에서 4.01/4.02 정확 토큰 매칭.
3. insufficient-history fail-closed: 선행 이력 부족 → b_8kfreq=0 + 플래그.
4. 비가중 합 산술.
5. (주의) 4게이트의 pytest 명령은 `pipeline/ tools/ scoring/`만 순회한다 —
   본 테스트는 phase 경계에서 **명시 실행**하고 커밋 메시지에 결과를 남긴다.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
