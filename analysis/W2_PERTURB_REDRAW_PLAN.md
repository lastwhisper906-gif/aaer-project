# E3 사전 등록 — wave-2 교란 재추첨 (R4 헤드라인의 draw 잡음 방어)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08, OWNER-GATE-E.
> **E3 첫 채점 전 커밋 (freeze-then-run).** **결론 규칙 사전 확정 — 서사가 아니라
> 규칙이 결정한다.** 범위 한정(§5-5): Claude 단일 파이프라인.
>
> **개정 A (2026-07-08, 첫 채점 전 — 실행 가능성 검토가 계기, 결과 독립):** 최초 §1이
> "perturb_factor를 draw별로 변주"로 적었으나 이는 wave-1 A3(k=5 표본분산) 프로토콜과
> 불일치다. wave-1의 "draw σ≈12pp"는 **고정 페이로드 위 모델 표본 재추첨**의 분산이었다
> (perturb_factor는 case_id 결정론 고정 — `build_payload.perturb_factor`). E3도 동일하게:
> **동일 perturbed 페이로드(factor 고정) + 모델 표본 재추첨 2회**, identity 점수는 동결
> draw-1 고정, perturbed(pt2)만 재추첨. 파이프라인 무변경(런너 재실행만). 채점 전 개정,
> 어떤 draw도 아직 실행 안 됨 → §5-6 준수(기준이 결과보다 먼저).

## 0. 동기

wave-2 R4(잔여 능력) 결론은 정체-교란 단일 draw에 의존한다. wave-1 교훈: draw σ ≈
12pp. 단일 draw의 delta-dominance(현재 3/9)가 draw 잡음에 흔들릴 수 있다. E3은 추가
draw로 안정성을 측정하고, 사전 규칙으로 R4/R3을 재판정한다.

## 1. 설계

- **실험군 9사 각 +2 draw** (교란 프레임). **개정 A**: perturb_factor는 case_id 결정론
  고정 — draw는 **동일 perturbed 페이로드 위 모델 표본 재추첨**(wave-1 A3 프로토콜).
  총 **18 피평가자 호출** (9×2). 원본(identity) 프레임 재추첨 안 함(delta = identity−
  perturbed에서 identity는 동결 draw-1 고정).
- **채점자 호출 불요(0)**: E3 지표(delta-dominance)는 **점수 기반**(§2) — dim 채점
  불필요. E3 총 미터링 = **18 피평가자 호출** (당초 36 추정에서 하향).
- 산출: `runs/wave2/perturbed_redraw/draw_{2,3}/case_NN.json` (새 out_dir → 멱등 skip이
  draw-1 불침해). 동결 draw-1(`runs/wave2/perturbed/`) 불변.
- cutoff_guard·forbid-markers·pin-verify(claude-sonnet-5) 전건. verify_blindness 신규 배치.
  런너 멱등·레이트리밋 재개 기제 그대로.

## 2. 지표 (사전 지정)

- **delta = identity_score − perturbed_score** (정체 노출이 점수를 얼마나 올리는가 =
  암기 기여 대리). draw별 delta, 그리고 **케이스별 median delta**(draw 1·2·3).
- **delta-dominance count**: delta가 임계(정체-교란 임계, 동결 R3 정의와 동일)를
  넘는 케이스 수 / 9. **draw별 재계산 + median delta 기준 재계산** 둘 다 보고.
- draw σ 밴드: 케이스별 3-draw 표준편차 → wave-1 σ≈12pp와 대조.

## 3. 결론 규칙 (사전 확정 — 규칙이 결정)

- **median-delta dominance ≥ 5/9 이면**: **R3가 wave-2에서 R4를 supersede**
  (암기 지배). 이 경우 **모든 드래프트를 자동 갱신** — wave2_summary·Issue #1·
  synthesis(per_wave_rule wave2 → R3)·dose-response 규칙 라벨. 규칙이 정하며 서사
  선호가 아니다.
- **median-delta dominance ≤ 4/9 이면**: **R4 유지**, 재추첨 안정성(σ 밴드)을 병기
  보고 ("단일 draw가 아니라 3-draw median에서도 dominance 미달").
- 경계(정확히 5/9)는 규칙상 R3(≥5) 발동. 동률 케이스의 임계 판정은 동결 R3 정의
  그대로(재해석 금지).

## 4. 채점 순서 (사전 고정)

케이스 알파벳순(ticker): BRX·CGI·CSC·HAIN·MDXG·OSIR·TNGO·UAA·WFT, 각 draw-2 먼저
전 케이스 → draw-3 전 케이스. draw 경계·케이스 경계마다 freeze·commit·push.
절단 시 완료 draw까지 median 대신 2-draw로 보고(규칙: 최소 draw-2 완료분만 dominance
재계산, draw-3 부분은 미사용 — 결과 독립).

## 5. 호출 추정 (개정 A)

**18 피평가자 호출** (9 실험군 × 2 draw), 채점자 0 (점수 기반 지표). 전역 320 cap 계상.
재계산은 결정론(동결 R3 정의 `wave2_analyze.py` — `delta=fr[s]−pt2[s]`, cross iff
`abs(delta)≥0.5(fr[s]−cmed)` or `contrib≤0`, fires iff cross≥5/9). 재해석 금지.

## 6. 면책

단일 Claude 파이프라인, k=3(원본 draw-1 + 재추첨 2). 발행 안 함(소유자 게이트).
draw-1 published 수치는 불변(E3는 안정성 밴드이지 교체 아님, 단 §3 규칙 발동 시
결론 라벨만 규칙대로 갱신).
