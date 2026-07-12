# specs/draw_k3.md — median-of-3 병기 1차값 사전 등록 (WS-6 / F-3, SPEC ONLY)

> **launch-ready 동결 — 이 세션에서 실행하지 않는다** (미터링 0 계약).
> 발사는 소유자 예산 게이트 **Q-F06** 서명 후에만. **동결 draw-1 발행
> 수치는 불변**이며, median-of-3은 **병기(co-report) 1차값**으로만 추가된다.

## 1. 설계

- **k = 3 draws/케이스**: 기존 draw-1 (동결) + 신규 draw-2·draw-3.
- **median-of-3 = 병기 1차값**. FLAG = 50 불변. 채점 루브릭·dims 재계산
  없음 — dims는 draw-1 채점 유지 (신규 draw는 **피평가자 호출만**, 채점자
  호출 0 — median은 misstatement 점수·플래그 통계이지 채점이 아니다).
- **홀드아웃은 k=5 유지** (D27/D33 기완료 — 본 스펙 범위 밖).
- temp=0이 배포 API에서 결정론을 보장하지 않으므로 median-of-k는 **분산
  완화이지 제거가 아니다** — 이 문장을 발행 표면 인용 시 동반한다.

## 2. 미터링 예산 (repo 계수 산술 — 추정 아님)

- wave-1 발행 프레임: treatment 8 + control(v2) 22 = **30 케이스**
  (`analysis/baseline_table.csv` 30행).
- wave-2: treatment 9 + control 23 = **32 케이스** (`cases_wave2.json`).
- 케이스당 추가 draw 2 → **(30 + 32) × 2 = 124 피평가자 호출, 채점자 0**.
- **재사용 옵션 (사전 등록)**: wave-1 treatment 8은 커밋된
  `runs/hardening/draws/draw_2·draw_3` (RP-06 A3, 동일 원본 프레임)을
  median 산입에 재사용 가능 → 신규 124 − 16 = **108 호출**. 단서:
  hardening 출력의 grades 병합 금지 규약은 불변 (median은 병합이 아니라
  통계 병기); 재사용 여부는 Q-F06에서 소유자가 (A) 전량 신규 124 /
  (B) 재사용 108 중 선택.
- v1 8 대조군(cases.json, 발행 프레임 밖)은 범위 제외.

## 3. 사전 등록 산출물 — flip-rate 표

- tier별 표: **draw-1 플래그 상태(≥50)와 median-of-3 플래그 상태가
  다른 케이스** 수 + 케이스 목록 (방향 포함: 플래그 획득/상실).
- 분리 통계(순열 p·AUC)는 median 점수로 재계산해 **병기** — 동결 draw-1
  수치와 나란히, 대체 금지.
- per-case 밴드: draw 3개의 min–max (E5§7의 5-draw 밴드와 동일 표기).

## 4. 실행 규율 (발사 시)

- freeze-commit-then-run: 발사 전 본 스펙 + 러너 배선 커밋이 선행.
- 러너 경유만 (세션 내 피평가자 판정 생성 금지). 케이스/draw 경계
  commit·push (D31–D38 미터링 가계부 선례).
- Q-R02 발효(raw API 이행)와 같은 배치면 FREEZE_REV3 §6 래치(스모크 선행)
  적용.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
