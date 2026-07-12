# specs/label_taxonomy.md — 홀드아웃 라벨 분류 체계 사전 등록 (WS-3 / F-6)

> **freeze-commit-then-run**: 본 스펙 커밋은 태깅 산출물
> (`analysis/label_tags_holdout.json`)이 존재하기 전에 이루어진다.
> **동결 홀드아웃 수치·스코어보드는 어떤 것도 수정하지 않는다** — 라벨 체계는
> 병기 층이다.

## 1. 문제 — G2 잠정 라벨의 합성어 위험

G2 잠정 라벨은 "restatement"와 "intentional misstatement"를 한 단어에 태운다.
회계 문헌의 표준 구분은 **Big R**(Item 4.02 비신뢰 선언 동반 재작성 — 과거
재무제표를 신뢰하지 말라는 공식 선언) vs **little r**(비신뢰 선언 없는 수정
반영)이다. 홀드아웃 3사가 어느 쪽인지는 submissions JSON에서 기계적으로
판정 가능하며, 집행(AAER) 확정과는 별개다.

## 2. 태깅 규칙 (사전 고정)

- **대상**: 홀드아웃 treatment 3사 (case_71 HUBG · case_72 WMK · case_73 GNE).
- **revelation_date := cutoff_date + 1일** (HOLDOUT_CRITERIA "컷오프 = 폭로일
  전일" 정의의 역산 — 레지스트리 scheme_summary의 8-K 일자와 일치해야 하며,
  불일치 시 fail-closed 보고).
- **neighborhood := revelation_date ± 90일** (사전 등록 — 폭로 사건과 같은
  회계 문제에 속한 비신뢰 선언을 잡되, 무관한 후속 사건을 배제하는 균형).
- **태그**: neighborhood 내 form ∈ {8-K, 8-K/A}이고 WS-1 파서 item 리스트에
  `"4.02"` 포함 → **`bigR`**; 부재 → **`little_r`**.
- **증거 의무**: 태그마다 accession + filingDate + items_raw 기록. 캐시 스냅샷
  최신 filingDate ≥ neighborhood 상한임을 케이스별 확인·기록 (미충족 시
  `insufficient_cache` 플래그 — 태그 대신 플래그).
- **데이터 접근 주석**: 본 태깅은 폭로 **후** 제출물을 읽는다 — 이는 채점측
  ground-truth 작업이며 피평가자 입력이 아니다 (§5-1 look-ahead는 피평가자
  페이로드 규율; 선례 `tools/holdout_rescan.py`의 폭로-후 AAER 모니터링).
  neighborhood 밖 4.02 관측도 참고로 병기한다 (숨기지 않음).

## 3. 기저율 문서화 (재작성 ≠ 집행 — 발행 서사의 사전 방어)

숫자는 검증 조건부로 병기하며, 각 수치의 **분모가 다르다**는 것이 요점이다:

- **~2.2%** — Audit Analytics 재작성 중 SEC 집행 연계 비율 (Karpoff, Koester,
  Lee, Martin, *The Accounting Review* 2017, 데이터베이스 비교 연구).
  → 재작성 관측만으로 집행을 예측하면 기저율상 대부분 틀린다.
- **~89.4%** — GAO 재작성 표본 중 fraud와 무관한 비율; **~26.4%** — 동 표본
  중 irregularity(의도성 시사)로 분류된 비율 (Hennes, Leone, Miller 2008).
  **주의 플래그 (사전 등록)**: 26.4%는 **의도성 프록시**이지 집행률이 아니다 —
  2.2%와 직접 비교 금지 (분모·기준 상이).
- Chu, Dechow, Hui, Wang (2018)은 "AAER 조사 대부분이 재작성 계기"라는 방향을
  정성적으로 지지 — **정확 수치 인용은 소유자 원문 대조 후에만**
  (OWNER_QUEUE 등록, 발행 사용 금지 유지).

## 4. 업그레이드 프로토콜 (사전 등록 — 양방향 대칭)

- **모니터링 윈도 = 각 재작성 공표일로부터 4년** (위반종료→집행 중위
  28.9개월 + 버퍼): HUBG → 2030-02-05 · WMK → 2030-02-20 · GNE → 2030-03-12.
- **상향 경로**: 윈도 내 해당 사를 지명하는 AAER 발행 → 라벨
  provisional → confirmed 상향. 신규 D-엔트리로 기록하고 **병기만** — 동결
  홀드아웃 스코어보드는 절대 수정하지 않는다.
- **대칭 결과 (사전 등록)**: 윈도 만료 시 AAER 부재 → 케이스에 "no enforcement
  within window" 주석. 이것 자체가 라벨 노이즈에 관한 보고 가능한 결과다 —
  기저율(§3)상 이 경로가 다수 기대치임을 지금 명시한다.
- 점검 계기: 기존 월간 홀드아웃 재조사 루틴 (`tools/holdout_rescan.py` 경로).

## 5. 명명 diff (diff-only — 발행 표면 직접 수정 금지)

발행 표면이 홀드아웃 ground truth를 무수식 "misstatement"로 서술하는 지점에
대해, 케이스별로 "Big R restatement (Item 4.02 non-reliance)" 또는
"restatement (little r)"로 교체하는 diff를 `review_packets/RP-15_label_naming_diff.md`
로 제안하고 OWNER_QUEUE 게이트 항목을 등록한다. 서명 전 원문 무변경.

## 6. 산출물

- `analysis/label_tags_holdout.json` — 기계 산출 (증거 accession 포함).
- `analysis/LABEL_REPORT.md` — 태그 표 + 기저율 + 업그레이드 프로토콜 요약.
- `review_packets/RP-15_label_naming_diff.md` + OWNER_QUEUE 항목 2건
  (Chu et al. 원문 대조 · diff 승인).

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
