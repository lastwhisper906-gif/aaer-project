# LAUNCH_SEQUENCE.md — 소유자 잔여 실행 지도 (2026-07-13, D58 기준)

> **새 결정 없음** — 아래 전부가 이미 서명·사전 등록된 것의 실행 순서다
> (Q-R02 GO·FREEZE_REV3 §6·D51/D58·D43 계획 4). 각 단계는 이전 단계 완료가
> 조건이며, 중단 시 같은 명령으로 재개된다 (멱등).

## 0단계 — 준비 (키는 셸에만, 파일 저장 금지 — FREEZE_REV3 §6-1)

```bash
cd ~/Documents/aaer-evals
read -s ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
```

## 1단계 — 스모크 (~30호출 종량, FREEZE_REV3 §6-3 래치)

```bash
make smoke          # 계획 = runs/smoke_rev3/DRYRUN_MANIFEST.json (커밋 완료, 불일치 시 자동 정지)
git add runs/smoke_rev3 && python tools/verify_blindness.py --write-manifest \
  && git add runs/MANIFEST.sha256 && git commit -m "smoke rev3 결과" && git push
```

- 게이트 아님 — 측정: `runs/smoke_rev3/SMOKE_REPORT.md`에 케이스별
  |median(raw)−median(하네스)| > 6.4pp 플래그가 찍히면 발행물 L-2 문단 병기
  대상 (자동 판독, 재량 없음). **이 커밋 전 E2 발사 금지.**

## 2단계 — E2 조기성 (~112–160호출, AAER_RAW_API_APPROVED=1 필요)

> **기대치 설정 (D60, analysis/B4_VENUE_MEMO.md)**: E2는 **무료 신호(B4)
> 대결을 해소하지 않는다** — E2 신규 스냅샷 146개 중 B4 점수 계산 가능 3개(전부 UAA)
> (실험군 케이스 커버 2/13 = 15% < §4b 성립 조건 70%, 구조적 미달 — D61 로스터 교정 반영). E2가 사는
> 것은 LLM vs **B3** 리드타임 판정(§4)이다. LLM vs B4의 첫 증거는 5단계 첫
> seal의 4분기 창 만료(**≈ 2027-11**), 4연속 stage-gate 최초 개방 가능
> 시점은 **≈ 2028-08**. E2 발사 여부 판단에 이 편익을 계상하지 말 것.

```bash
export AAER_RAW_API_APPROVED=1     # 배치 단위 opt-in (영구 프로필 금지)
# 실행 상세 = analysis/EARLINESS_PLAN.md (동결) + docs/RESUME.md 재개 명령 절
# 케이스 경계마다 commit·push (runs/ 추가 시 --write-manifest 동반)
```

## 3단계 — 판정 (무호출, 결정론)

```bash
# (a) 어댑터: E2 산출물 → analysis/e2_trajectories.json
#     스키마 = specs/ENGINE_DECISION.md §1 (+§4b: 스냅샷별 b4_slope_aug —
#     동결 b4_score 재계산, 무비용) — 어댑터 작성은 E2 완료 세션 몫
.venv/bin/python analysis/engine_verdict.py      # → analysis/engine_verdict.json
.venv/bin/python analysis/buyer_metrics_build.py --logs-dir logs/<E2 로그 디렉토리> \
    --price-in <USD/MTok> --price-out <USD/MTok>  # → analysis/BUYER_METRICS.md
# 판정 결과를 신규 D-엔트리로 원장 기록 + commit·push
```

## 4단계 — 판정 브랜치별 의미 (specs/ENGINE_DECISION.md §4·§4b — 기계 판정, 재해석 불가)

| branch | 뜻 | 즉시 행동 |
|---|---|---|
| `a_llm_engine` | LLM lead ≥ B3+1분기 (그리고 B4에 지배당하지 않음) | screener stage-2 활성 — FUNNEL §2 설계 그대로 |
| `b_rules_engine` (`b_strict`/`b_residual`/`b4_dominated`) | 무료 규칙(B3 또는 B4)이 대등 이상 | stage-2 제거, LLM은 리포트 초안 보조. screener는 rules-only로 계속 — 단 `b4_dominated`는 E2 산출물에서 트리거 불능 (D60 산술: §4b 커버리지 구조적 미달, seal 판정 관할) |
| `c_terminated` | 어느 쪽도 폭로 직전 분기를 넘는 리드 없음 | 도구 경로 종료 — screener 아카이브, aaer-evals는 과학 산출물로 존속 |

- 어느 브랜치든 **결과 그대로 발행** (PROJECT.md §10 — 나쁜 결과 미화 금지).

## 5단계 — 첫 seal (2026-11-15 목표, screener 리포)

screener/OWNER_TODO.md S-01(UA)→S-03(원격)→S-04(첫 ingest + FINRA 아카이브)
→S-05(N=30 선정 + `seal create`, B4 top-30 동봉·lint 게이트 자동) 순서.
seal 판정·4연속 게이트는 `seal/verdict.py` 계산 필드 (프로토콜 §5·§5b).

## 병행 인간 작업 (순서 무관, D43 서명분)

독자 warm 5–7 발송 · Zenodo 토글+v1.0.0 재발행 · RP-15/RP-16 서명 ·
FINRA ToS 확인(Q-M01/S-08) · 변호사 2종(S-10/S-13) — 전체 목록은
docs/HANDOFF.md 소유자 통합 체크리스트.
