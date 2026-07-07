# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-07, RP-09 진행 중)

> 다음 세션: CLAUDE.md → PROJECT.md → 이 문서 → `review_packets/RP-09_instructions.md`.
> 거버넌스: GA-001 + freeze 개정 #2 + RP-06 addendum + **RP-09 소유자 지시
> (verbatim 커밋 986a893)** — 소유자 접점은 §Final의 단일 결정 하나뿐.

## RP-09 스테이지 상태 (재개 시 첫 미완 스테이지부터)

- [x] **Stage 0** — 채점 26건 human_finalized=true (D21, 인가: 986a893).
  이 커밋부터 scoring/grades/ + pilot/grades/ **I3 동결**. 실험군 정답 평가 종결.
- [ ] Stage 1 — RP-07 D-2 원본 재추첨 32호출 + delta 분해 + draw-3 판정
- [ ] Stage 2 — CONTROL_CRITERIA_v2 + 재선정 (16–24) → runs/rp09/control_group_v2.json
- [ ] Stage 3 — 채점 준비 패키지 (런북·대조군 프로브·검정력 사전 계산·병렬화) — 발사 금지
- [ ] Stage 4 — docs/EARLINESS_DESIGN.md
- [ ] Stage 5 — docs/FUTURE_HOLDOUT_CANDIDATES.md
- [ ] Stage 6 — 증분 감사 docs/AUDIT_STATE.md
- [ ] Final — 소유자 단일 결정: "control_group_v2 승인 + 채점 발사: YES / AMEND"

## 이전 사이클 위치 (참고): RP-06 완결 + RP-08 v1.1 산출물 커밋 (ed2e132)

RP-05 결과(불변) 위에 RP-06 강화 사이클 완료: A1 인지 재추첨 8 + A2 교차
채점 6 + A3 표본분산 k=5 64 = **78호출 (FAIL 0 · 핀 불일치 0)**, 전 산출물
runs/hardening/ 커밋. 발행 수치 재현·블라인드·매니페스트는 CI가 매 push
검증한다 (`tools/reproduce_analysis.py` 100/100 · `tools/verify_blindness.py`).

## 소유자 대기열 (RP-09로 재편 — ③④ 완료, ⑦ superseded)

> RP-09 지시로: ③ 워크벤치 검토 + ④ 채점 26건 확정 = **완료 (Stage 0, D21)**.
> ⑦ RP-08 아침 게이트의 v1.1 PROPOSED는 **Stage 2의 v2로 supersede** — 서명
> 대상은 이제 control_group_v2 하나. 잔여 소유자 항목: ② Console $0.00 확인,
> ⑤ A1/A3 판독, ⑥ 발행 결정, 그리고 **RP-09 §Final 단일 결정**.

1. ~~**RAT-001 서명**~~ — ✅ **완료 (2026-07-07)**: 소유자 추인 서명
   (세션 내 직접 진술 전사 — `scoring/overrides.md` RAT-001 서명 블록).
2. **Console 대시보드 $0.00 확인** (RP-04 check C) — 구독 외 종량 과금
   부재의 소유자측 확인. (참고 합계: RP-06 total_cost_usd $24.83 — 기록
   전용, 과금은 구독 OAuth 경로.)
3. **워크벤치 검토** — `review_packets/RP-06_grading_workbench.md`,
   **MODEL 귀속 5건(⚑ SKEPTICAL-REVIEW) 먼저**, UNCLASSIFIED 2건(MRVL)의
   DATA(설계) PROPOSAL 판정 포함. 참고: A2 교차 채점 밴드 일치 6/6 ·
   Ryder 오탐은 k=5 중 최대값 1회 관측 (RP-06 §3-2 각주 자료).
4. **채점 26건 확정** — human_finalized=False → true 갱신, 오버라이드는
   overrides.md 기록 ("채점: Claude 보조 + 인간 최종 확정").
5. **A1/A3 판독 → 발행 프레이밍 확정** — RP-06 §1/§3: **정체 인지
   주의문("perturbation disrupts memorized NUMBERS, not IDENTITY
   recognition")은 README 헤드라인 문장에 이미 병기** — 유지 여부가 소유자
   결정. A3 밴드 문구(p·AUC 강건 / 분리 4/5 / delta 분해 부분 해소)의 주장
   강도 서열 확인 (RP-06 §5).
6. **발행 결정** (소유자 확정 사항 — §7). GO 시 README.md가 발행 관문
   (보고 언어 제약 3-6 적용 완료 상태).
7. **RP-08 아침 게이트** (2026-07-07 야간 산출, D19 사전 승인) —
   `review_packets/RP-08_selection_memo.md` §0 순서대로: 메모 통독 →
   스팟체크 3건(T12 Fortinet → T17 First Solar → T28 Campbell) →
   `docs/CONTROL_CRITERIA_v1.md` 서명/수정 (v1.1 개정 후보 2건 포함) →
   `runs/rp08/control_group_PROPOSED.json` 서명/기각. **서명 전 채점
   파이프라인 진입 금지** (status 필드 강제). 기각 재실행은 분 단위
   (memo §0 명령). ①~⑥과 독립 — RP-05 결과·RP-01 확정 대조군 불변.

## 유예 등록부 (DEFERRED — 실행 금지, 소유자 지시로만 개시)

- **D-1**: 논문/공개 모니터 write-up 초안 — 대기열 ④·⑤ **이후에만**
  (프레이밍이 A1/A3와 확정 채점에 의존).
- **D-2**: k>5 에스컬레이션 — A3 분해가 미해결(케이스 단위 delta 4/8 잡음
  분리 불능; 병목은 **원본 쪽 k=1**이므로 실체는 원본 재추첨 +32호출)이고
  **동시에** 발행 GO일 때만.

## 이 사이클의 고정값 (불변 — 이전과 동일 + RP-06 추가분)

- freeze `82a7717` + 로그된 개정 2건 + RP-06 addendum (기준 무변경 —
  `git diff 9dfcf44..HEAD -- review_packets/RP-05_results.md scoring/grades/`
  = 공백으로 증명).
- 모델 실측: 피평가자 claude-sonnet-5 단독 서빙 (72호출) / 채점 fable-5
  (본채점, 폴백 0) · opus-4-8 (A2 스팟체크 6호출 — 설계 고정). 하네스
  v2.1.201 재확인. 인증 = 구독 OAuth, API 키 부재 전 호출 assert.
- 원시: runs/ (MANIFEST.sha256 변조 증거) · scoring/grades/ (무변경) ·
  runs/hardening/ (신규 — probe_recognition·regrade_opus·draws, 본채점 비병합).

## 금지·주의 (유효 지속)

- 세션 내 피평가자 판정 생성 금지 — 러너 경유만. runs/hardening 출력을
  scoring/grades/ 에 병합 금지 (SPOT-CHECK 라벨).
- 보고 언어 제약 전부 유지 (% 헤드라인 금지 / 상한 명기 / 오염 명시 /
  BOUND-not-eliminate / 선택·생존 편향 / **L-5 정체 인지 주의문 헤드라인
  병기** / L-2~L-4 인용).
- 로컬 커밋은 기록이 아니다 — push까지.
