# specs/B4_short_interest.md — B4: 비정상 공매도 잔고(abnormal short interest) 기준선 (사전 등록)

> **freeze-commit-then-run**: 이 스펙 커밋은 `analysis/b4_short_interest.py` 및
> `screener/ingest/short_interest.py`가 git 이력에 존재하기 전, 그리고 어떤 SI 수치의
> 다운로드·계산보다 먼저다 (`git log --follow`로 검증 가능). 임계값·창·집계 규칙은
> 계산 전에 여기서 고정된다. D-엔트리: **D52**.

## §0 왜 B4인가 (시장 조사 결과 = 구속력 있는 설계 입력)

Karpoff & Lou (2010, *Journal of Finance* 65(5)): 비정상 공매도 잔고는 부정 폭로
이전 약 19개월에 걸쳐 꾸준히 상승한다. 즉 **무료 공개 신호 중 진짜 경쟁자는 제출
연대기(B3)가 아니라 공매도 잔고다**. B3는 wave-2 AUC 0.548로 자명성 하한을 세웠지만,
"이 도구가 존재할 이유"의 기준선은 B4다: 무료 공개 신호를 이기거나 최소한 대등하지
못하면 파이프라인의 존재 이유가 없다. 이후 모든 성능 주장은 "최고의 무료 신호 대비"로
표현한다. (연구 종합의 결론을 재론하지 않고 구현한다 — 세션 미션 §0.)

## §1 데이터 소스 (2026-07-13 실측 프로브 기록)

- **원천**: FINRA Consolidated Short Interest (Rule 4560) — 거래소 상장 + OTC 전 종목,
  월 2회(15일·말일 부근 결제일 기준).
- **벌크 파일**: `https://cdn.finra.org/equity/otcmarket/biweekly/shrt{YYYYMMDD}.csv`
  (파이프 구분, 헤더 1행). 필드: `settlementDate, symbolCode, issueName,
  currentShortPositionQuantity, previousShortPositionQuantity, stockSplitFlag,
  averageDailyVolumeQuantity, daysToCoverQuantity, revisionFlag` 등 14개.
- **가용 범위 (프로브 실측)**: 최초 파티션 = 결제일 **2017-12-29** (Query API
  `LESSER 2017-12-29` → 0건, `LESSER 2017-12-30` → 20171229 반환으로 양측 확인).
  최신 확인 = 2026-05-29 (HUBG 실측). **2017-12-29 이전 무료 데이터 없음** —
  그 이전 결제일이 필요한 케이스는 fail-closed (§7).
- **결제일 발견 규칙**: 각 반월의 후보일(15일·말일)에서 시작해 영업일 기준 최대 5일
  역방향 탐침, HTTP 200 + 헤더 검증 통과 첫 파일 채택 (결정론). 실패 시 그 반월 결측
  기록 (조용한 스킵 금지).
- **아카이브**: 케이스 창(§3)에 필요한 결제일 파일의 합집합을
  `~/aaer-data/short_interest/shrt{YYYYMMDD}.csv` 원본 그대로 보관, sha256 체크섬 로그
  동반, `data/manifests/aaer_data_manifest.json`에 등재 (source_url = 위 CDN URL 역산
  — verify_manifest.py에 `short_interest/` 귀속 분기 추가). 스크리너 운영용
  다운로드는 `~/screener-data/short_interest/` (screener 관할, 본 매니페스트 밖).
- **ToS/라이선스**: 발행물에 FINRA 파생 수치 게재 시의 라이선스 조건은 세션이
  판단하지 않는다 — **OWNER_QUEUE Q-M01** (소유자 확인 게이트).

## §2 PIT 규칙 — 배포 지연(dissemination lag) 모델링

공매도 잔고는 결제일로부터 며칠 뒤에야 공표된다. 결제일을 그대로 쓰면 look-ahead다.

- FINRA 일정 (2026-07-13 finra.org 실측): 보고 마감 = 결제일 + 2영업일 18:00 ET,
  공표(publication) ≈ 마감 + 약 7일 → 통상 결제일 + 9~11 캘린더일.
- 파일에 공표일 필드가 없으므로 **보수적 상수 지연을 사전 등록**한다:
  **LAG = 14 캘린더일**. 결제일 t의 보고서는 `t + 14 ≤ cutoff`일 때만 피처에 진입.
- 과거 공표일 실측치(연도별 FINRA 일정표)를 입수하면 상수를 대체할 수 있으나,
  **대체는 신규 D-엔트리로 스펙 개정 후에만** (사후 완화 금지). 입수 가능성 질문은
  **OWNER_QUEUE Q-M02**.
- **개정판(revision) 규칙**: 결제일 t의 값은 t 자신의 파일에서 읽는다
  (최초 공표값). 근거 한 줄: 파일 1개만으로 PIT가 성립해 지연 가정이 최소화된다.
  다음 파일의 `revisionFlag=R`은 진단 카운트로만 기록 (값 대체 없음).

## §3 지표 정의 (Karpoff/Lou 착안, 우리 데이터로 계산 가능한 형태)

케이스 (ticker, cutoff) 에 대해, 사용 가능 보고서 = `settlement + 14 ≤ cutoff`인
결제일 시계열 {t_i}, 각 t_i에서:

1. **SIR_t = currentShortPositionQuantity_t / shares_outstanding_t**
   - 분자: FINRA 파일의 해당 symbolCode 행.
   - 분모: payload_v2 (WS-1, D44) `extract_share_facts(ticker, cutoff)`의
     `dei:EntityCommonStockSharesOutstanding` instant 사실 중 **end ≤ t** 이고
     **t − 400일 ≤ end** (신선도 밴드)인 것 가운데 (end, filed) 최신 승리.
     extract_share_facts 자체가 filed ≤ cutoff PIT를 강제하므로 이중 안전.
     해당 사실 없으면 그 보고서는 사용 불가 (fail-closed, 플래그).
   - 심볼 매핑: FINRA symbolCode == 레지스트리 ticker 정확 일치가 기본. 불일치
     발견 시 케이스별 매핑을 **계산 전 이 파일 §11에 추가 커밋**한 뒤에만 사용
     (사후 임의 매핑 금지). 미해결 불일치 = 그 케이스 fail-closed.
2. **비정상 SI: aSIR_t = SIR_t − median(SIR over trailing 12개월)**
   - trailing 창 = settlement ∈ [t − 365일, t) 의 보고서들 (t 제외, 자기 자신
     포함 시 중앙값이 자기 값에 끌림). **최소 12개** 필요 (이론 최대 ~24), 미달 시
     `insufficient_history` → 그 보고서에서 aSIR 계산 불가.
3. **레벨**: `B4_level = aSIR_{t_last}` — cutoff 직전 마지막 사용 가능 보고서.
4. **기울기**: `slope4` = 마지막 4개 연속 사용 가능 보고서의 aSIR에 대한 OLS 기울기
   (보고 주기 단위, x = 0,1,2,3). 4개 미만이거나 결제일 연속성(반월 결측 없음)이
   깨지면 slope 사용 불가 플래그.

## §4 점수 2종 — 사전 등록, slope-augmented가 1차

- **B4_level** = aSIR_{t_last} (병기).
- **B4_slope_aug** = aSIR_{t_last} + slope4 (**1차**).
  근거 한 문장: Karpoff/Lou의 발견은 폭로 전 비정상 SI의 *수준*이 아니라 *꾸준한
  상승*이므로, 추세 항이 레벨만으로는 없는 신호를 담는다.
- 두 점수 모두 계산 후 어떤 재가중·재정의도 금지 (B3 §5와 동일한 반과적합 규율).
  둘 다 실수값, 동률은 tie-aware AUC가 처리.

## §5 평가 기계 (B3 §6과 동일 기계, 시드만 신규)

- tie-aware AUC = `analysis/stats.py::auc` 의미론 `(gt + 0.5·eq) / (na·nb)`.
- bootstrap percentile 95% CI: `stats.py::boot_auc_ci`, N_BOOT = 10,000.
- 단측 순열 (treatment > control, 평균차): `stats.py::perm_test_mean`, N_PERM = 100,000.
- **SEED_B4 = 20260713** (신규 선언; tier×window 블록마다 `random.Random(SEED_B4)`
  재시드 — b3_compute와 동일한 순서 독립 결정론 관용구).
- **tier별 절대 비pooled** (wave-1 / wave-2 / holdout+controls).
- **precision@k 신설**: k_tier = ceil(N_tier / 10) → wave-1 k=3, wave-2 k=4,
  holdout k=2. 대상 = 커버리지 있는 케이스만의 순위. **주의 문구 의무**: tier는
  처치 농축 표본(기저율 ~25–30%)이므로 이 precision@k는 유니버스 top-30
  precision@30(기저율 ~3%/yr)과 **수치 비교 불가** — 서술적 동반 지표일 뿐.
  유니버스 스케일 precision@30은 sealed-forecast 프로토콜(스크리너 §5 개정)의 관할.
- LLM AUC 재계산 금지 — 동결값 인용만: wave-1 0.8239 (`results_stats.json`),
  wave-2 0.829 (`wave2_results.json`), holdout 없음(N=3). B1/B2/B3도 동결값 인용만.

## §6 커버리지 정직 규칙 (계산 전 산술로 이미 알려진 것)

데이터 하한 2017-12-29 + trailing 12개월 + LAG 14일 ⇒ **사용 가능 cutoff 하한
≈ 2019-01-27** (= 2017-12-29 + 365 + 14 + 반월 여유). 레지스트리 cutoff_date와의
날짜 산술만으로 (SI 값 무접촉) 도출한 **기대 커버리지**:

| tier | 기대 커버리지 | 판정 |
|---|---|---|
| wave-1 (8T/22C) | ~3/30 (KHC·GIS·CPB, cutoff 2019-02-20) | <70% → **서술 전용** |
| wave-2 (9T/23C) | ~4/32 (UAA·CTAS·LEVI·RL, cutoff 2019-11-02) | <70% → **서술 전용** |
| holdout (3T/9C) | 12/12 (cutoff 2026-02~03) | ≥70% → 통계 보고 |

- **사전 등록 규칙**: 커버리지 <70% tier는 per-case 서술값·coverage n/N만 보고,
  AUC/CI/p를 계산하되 **헤드라인 주장 금지** + 표에 "coverage-limited" 라벨 의무.
  실제 커버리지가 기대와 다르면 (심볼 불일치·분모 결측) 그대로 n/N 보고.
- 케이스 단위 fail-closed: 필요한 파일·행·분모가 하나라도 없으면 그 케이스는
  결측으로 기록, 대체·보간 금지.
- 홀드아웃은 커버리지 100%지만 N=3 처치 — B3와 동일하게 절대값 보고만, 단독
  헤드라인 금지.

## §7 해석 규칙 — 엔진 결정 결합 (지금 못박는다)

- **비교 성립 조건**: 어느 tier에서든 (i) 커버리지 ≥70% AND (ii) 동결 LLM AUC 존재.
  현재 두 조건을 동시에 만족하는 tier는 **없다** (wave-1/2는 커버리지 미달, holdout은
  동결 LLM AUC 부재). 즉 **회고 채점만으로는 "LLM vs B4" 판정이 성립하지 않으며**,
  이 사실 자체를 B4_REPORT에 명기한다 — 무료 신호 벤치마크는 본질적으로
  전향(prospective) 비교다.
- **결합 조항 (미래 실행에 구속)**: 비교 성립 조건이 충족되는 모든 미래 시점 —
  E2 스냅샷 채점, sealed 분기 판정(스크리너 프로토콜 개정판), 또는 커버리지 있는
  신규 tier — 에서 **LLM(또는 워치리스트) 성능 ≤ B4 성능이면, 그 결과는 E2 평결과
  동일한 가중치로 엔진 결정(engine-decision) 입력에 들어간다.** 이 문장은 이후
  개정에서 완화 금지 (완화 시도는 이력 공개 조건 상기 — PROJECT.md §5-4).
- E4/E5 등 다른 실험 결과와의 종합은 소유자 관할 — 세션은 표와 결합 규칙 적용까지.

## §8 E2 통합 계약

```python
def b4_score(ticker: str, cutoff: datetime.date,
             data_dir: Path = SI_DATA_DIR, facts_dir: Path = DATA_DIR) -> dict
# 반환: {"score_level": float|None, "score_slope_aug": float|None,
#        "sir_last": float|None, "abnormal_sir_last": float|None,
#        "slope4": float|None, "n_reports_trailing12m": int,
#        "last_settlement": "YYYY-MM-DD"|None,
#        "flags": {"insufficient_history": bool, "no_si_file": bool,
#                  "no_shares_denominator": bool, "slope_unavailable": bool,
#                  "revision_seen_diagnostic": int},
#        "cutoff": "YYYY-MM-DD"}
```
- b3_score와 동일하게 **import 가능한 순수 함수** — 동결 E2 파일 무수정, E2가
  스냅샷마다 zero marginal cost로 호출. 사용 가능 보고서 없음 = 예외가 아니라
  `score_* = None` + 플래그 (E2 루프를 죽이지 않는다). 데이터 파일 부재는
  no_si_file 플래그로 기록 (fetch 금지 — 아카이브는 사전 단계).
- 정본 구현은 `screener/ingest/short_interest.py` (다운로더·파서·PIT 정렬기·스코어러).
  aaer-evals는 **스크리너의 vendor 관용구를 역방향으로 재사용**: 스냅샷 사본
  `analysis/vendor/short_interest.py` + PROVENANCE(원본 경로·커밋·sha256) + 무결성
  테스트. 수정은 원본에서만, 사본은 재수출.

## §9 산출물

- `analysis/results_b4.json` — 스키마는 results_b3.json 구조 준용 (spec, spec_commit,
  seed, n_perm, n_boot, tiers{coverage, missing, per_case, stats}, interpretation).
  차이: windows 대신 scores{level, slope_aug} 축; precision@k 블록 추가.
- `analysis/B4_REPORT.md` — **5열 표: B1 / B2 / B3 / B4 / LLM, tier별** (동결값 인용,
  재계산 0; 커버리지 라벨 의무). 결합 조항(§7)과 "비교 성립 tier 현재 없음" 문장 포함.
- 본 결과는 Claude 기반 단일 파이프라인의 보조 기준선 문서에 한정 (PROJECT.md §5-5).

## §10 테스트 계약

`analysis/test_b4_short_interest.py` (구현과 같은 커밋 또는 후행 커밋, 실행 결과보다 선행):
- PIT 경계: settlement + 14 == cutoff 포함 / +13 == cutoff − 1 배제 산술.
- trailing 중앙값: 12개 미만 → insufficient_history; 자기 자신 제외 확인.
- slope4: 연속 4개 요건, 결측 시 slope_unavailable, OLS 산술 고정 케이스.
- 분모 신선도 밴드 (end ≤ t, t − 400 ≤ end)와 (end, filed) 최신 승리.
- 파서: 파이프 구분·헤더 검증·심볼 정확 일치 fail-closed.
- 픽스처는 합성 CSV — 실데이터 무접촉 (네트워크 금지 테스트).

## §11 심볼 매핑 예외 테이블 (계산 전 커밋만 유효)

(현재 비어 있음 — 항목 추가는 이 파일 수정 커밋으로만, 커밋이 계산보다 선행해야 함)

## §12 소유자 큐 등록 (이 스펙과 동시)

- **Q-M01**: FINRA 데이터 ToS/라이선스 — 발행물 게재 조건 확인 (소유자).
- **Q-M02**: 과거 공표일(dissemination date) 실측 입수 가능성 — 입수 시 LAG 상수
  대체는 신규 D-엔트리 스펙 개정으로만.

## §13 개정 1 (D53, 2026-07-13) — 분모 우선순위 사슬 (이력 공개 조건 하 개정)

**공개**: 이 개정은 D52 1차 실행 결과(커밋 287a92a — coverage wave1 3/30 ·
wave2 1/32 · holdout 7/12, holdout AUC 0.1667)를 **본 뒤** 작성되었다. 동기는
성능이 아니라 커버리지다: §3의 dei 단일 분모가 다중 클래스 발행사(HUBG·GNE·
UAA·RL·VIASP·VLGEA)에서 체계적으로 결측 — SEC companyfacts API가 차원(클래스별)
사실을 평탄화하지 않아 undimensioned dei 사실 자체가 없다. §6의 사전 등록 기대
커버리지(holdout 12/12)와의 불일치가 개정 계기이며, 분모 선택은 방향 중립
(부호가 아니라 커버리지를 결정)이다. 1차 결과는 git 이력에 보존된다.

**개정 규칙 (재실행 전 커밋)**:
- 분모 소스 우선순위 (전부 D44 payload_v2 화이트리스트 내, 신규 태그 0):
  1. `dei:EntityCommonStockSharesOutstanding` (instant)
  2. `us-gaap:CommonStockSharesOutstanding` (instant)
  3. `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` (duration, end 앵커)
  4. `us-gaap:WeightedAverageNumberOfSharesOutstandingBasic` (duration, end 앵커)
- **케이스당 단일 소스**: t_last에서 신선도 밴드를 통과하는 최상위 소스를
  채택하고, 그 케이스의 전 보고서에 그 소스만 사용한다 (시계열 내 소스 혼합
  금지 — 레벨 차이가 aSIR 중앙값 차분을 오염시키는 것 방지). 채택 소스가 특정
  보고서에서 신선 사실이 없으면 그 보고서만 사용 불가 (기존 규칙 유지).
- duration 사실의 as-of 앵커 = `end`. 동일 (end, filed)의 연간·분기 중복은
  **짧은 기간(분기) 승리** (더 최신 평균) — 결정론 tie-break.
- 가중평균 주식수는 기간 평균이지 시점 잔고가 아니다 — 정직 한계로 기록.
  케이스 내 일관 사용이므로 aSIR(자기 중앙값 차분)에는 수준 편차가 상쇄된다.
