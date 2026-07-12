# RESUME.md — 무인 세션 재개 상태 (append-only, 매 유닛 후 갱신)

> 세션이 어느 지점에서 죽어도 아무것도 잃지 않도록: 완료 유닛마다 commit+push
> 하고 여기에 정확한 재개 명령을 append한다. 최신 상태가 맨 아래.
> 세션: 2026-07-08 야간 · OWNER-GATE-E 미션 · 전역 HARD CAP 320 evaluatee+grader.

## 미터링 호출 가계부 (running tally)

| 유닛 | evaluatee 호출 | grader 호출 | 누계 | 커밋 |
|---|---|---|---|---|
| (세션 시작) | 0 | 0 | 0 | 15d7366 |
| Phase 0 거버넌스 | 0 | 0 | 0 | b55aaf2 |
| Phase 1 P1 오류해부 | 0 | 0 | 0 | 590556d |
| Phase 1 P3 워크벤치 RP-13 | 0 | 0 | 0 | 00644f9 |
| Phase 2 P2 종합 | 0 | 0 | 0 | c9c9889 |
| Phase 2 E1-E5 사전등록 | 0 | 0 | 0 | c1b85a7 |
| P4 발행정합(README+lint) | 0 | 0 | 0 | 2a07649 |
| E3 개정+거버넌스 (발사 전) | 0 | 0 | 0 | ff9f017 |
| E3 draw-2 | 9 | 0 | 9 | ef63cfc |
| E3 draw-3 + 분석 (R4 유지) | 9 | 0 | 18 | f74bb94 |
| E3 fold-in (summary/synthesis) | 0 | 0 | 18 | 39ffc16 |
| P5 재현성(REPRODUCING+rescan) | 0 | 0 | 18 | b909cb6 |
| P6 RP-13 패킷 + HANDOFF/INDEX | 0 | 0 | 18 | (this) |

## 세션 종료 상태 (2026-07-08)

무-미터링 P1–P6 + E1–E5 사전등록 + E3 실행(R4 확증) 완료. **미터링 18/320.**
E1 보류(§5-1, Q-E03) · E2/E4/E5 launch-ready(Q-E01). 소유자 액션 4 =
`review_packets/RP-13_final_packet.md` §7. 미발행. 다음 세션 = 소유자 회신(Q-E01/02/03)
또는 감독 하 E1 실행. 재개 명령 전량 위 표.

## Phase 3 상태 (미터링)

- **E1 보류** (무인 부적합 — 네트워크 대조군 빌드 §5-1, OWNER_QUEUE Q-E03). 감독 하 이관.
- **E3 실행 예정** (18 피평가자, 채점자 0). 재개 명령:
  - draw-2: `python pipeline/runner.py --cases data/evaluatee/cases_wave2.json --perturbed
    --out runs/wave2/perturbed_redraw/draw_2 --only case_39 case_40 case_52 case_59 case_60
    case_61 case_65 case_66 case_67`
  - draw-3: 위와 동일, `--out runs/wave2/perturbed_redraw/draw_3`
  - 멱등 재개: 완료분 자동 skip. draw 완료마다 verify_blindness --write-manifest + commit+push.
- E2/E4/E5 보류 (Q-E01 spend 게이트).

## 재개 순서 (die-anywhere)

- **Phase 0** (zero-call): OWNER-GATE-E override 기록 + OWNER_QUEUE.md + RESUME.md.
  → commit+push. **[진행 중]**
- **Phase 1** (zero-call): P1 error anatomy → P3 workbench → P2 synthesis →
  P4 publication consistency. 각 산출물 commit+push.
- **Phase 2** (zero-call): E1–E5 사전 등록 (analysis/*_PLAN.md), 발동 전 freeze.
- **Phase 3** (metered): E1 control-build 실행 가능성 판정 → 1호출 smoke test →
  E1(+E3) 실행 or launch-ready 동결. freeze-commit-then-run 준수.
- **Phase 4**: OWNER_QUEUE Q-E01 go/no-go → RP-13 packet → HANDOFF/RESUME 갱신 →
  push → clean stop.

## 재개 명령 (현재 시점)

세션이 지금 죽으면: `git log --oneline -5` 로 마지막 push 확인 → 이 파일의
가계부·Phase 상태에서 다음 미완 유닛부터. 미터링 발사 전이면 spend 없음.

## 스모크 테스트 (freeze 개정 #3 래치 — 2026-07-13 추가, D52)

소유자 행동 전체 (§6-1 키 주입 규약 준수 — 키는 셸에만, 파일 저장 금지):

```bash
read -s ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY   # 또는 Keychain 경유
make smoke        # = AAER_RAW_API_APPROVED=1 tools/smoke_rev3.py --live (30호출, 종량)
```

- 계획 매니페스트는 커밋 완료: `runs/smoke_rev3/DRYRUN_MANIFEST.json` (30호출 —
  pilot 2케이스 × 5draw × 3arm: 하네스 / raw 미핀 / raw temp=0). `--live`는
  커밋된 매니페스트와 재생성본이 다르면 정지한다 (fail-closed).
- 게이트 아님 — 측정 (FREEZE_REV3 §3-3): 케이스별 |median(raw)−median(하네스)|
  > 6.4pp 이면 발행물 L-2 문단 병기 대상 플래그가 SMOKE_REPORT.md에 찍힌다.
- 완료 후: `git add runs/smoke_rev3 && python tools/verify_blindness.py
  --write-manifest && git add runs/MANIFEST.sha256` → 커밋+push. **이 커밋
  전에는 E2 본 발사 금지 (§6-3).** 멱등 — 중단 시 같은 명령으로 재개.

## E2 상태 절 (2026-07-13 append — 위 E3 절의 Q-E01 보류 인용은 역사 기록: Q-E01은 D40에서 RESOLVED)

- **E2 발사 전제 (D66/D67 갱신)**: ① `make smoke` + 결과 커밋 (§6-3 래치,
  소유자 — **유일 잔여 차단**) → ② 발사 =
  `AAER_RAW_API_APPROVED=1 .venv/bin/python tools/e2_runner.py --execute`
  (케이스 파일·레일·후처리 전부 커밋 완료; 크래시 시 같은 명령 재실행, 멱등).
- **정적 감사 전표**: `docs/E2_PREFLIGHT.md` (2026-07-13) — 호출 산술 146
  evaluatee(절단 휴면), 드리프트 플래그 2건(§4), 나머지 전 항목 ✅.
- 재개 명령 상세와 절단·순서 규칙은 동결 `analysis/EARLINESS_PLAN.md` §5.

## 2026-07-13 야간 미션 (subscription-only, HARD CAP 380 evaluatee/probe · grader 0)

> 서면 승인 = 미션 프롬프트 §2 (owner, 2026-07-13). 경로 = freeze 개정 #4
> (docs/FREEZE_REV4_HARNESS_E2.md) — 전 발사 하네스, ANTHROPIC_API_KEY 부재 강제.
> 우선순위 P0 E2(146) → P1 후처리(0) → P2 E4(20) → P3 Q-F05(62) → P4 Q-F06-B(108)
> → P5 E5 w2 arm(32). 레이트 리밋 = commit+push → 백로그(A-8) 블록 → 동일 명령 재시도.

| 유닛 | 호출 (이 유닛) | 누계 | 커밋 | 재개 명령 |
|---|---|---|---|---|
| 세션 시작 (검증: 단일 작성자·키 부재) | 0 | 0 | 5f148d9 | — |
| A-1 freeze 개정 #4 + 큐 갱신 | 0 | 0 | (this) | — |
