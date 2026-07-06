# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-07, RP-06 강화 사이클 완결)

> 다음 세션: CLAUDE.md → PROJECT.md → 이 문서 → `review_packets/RP-06_hardening.md`.
> 거버넌스: GA-001 + freeze 개정 #2 + **RP-06 소유자 addendum** (decisions_log
> 말미 verbatim — 기준 무변경, RP-05 §1 불변).

## 현재 위치: **저장소의 나머지는 전부 기계 검증(B2/B3) 또는 소유자 대기다.**

RP-05 결과(불변) 위에 RP-06 강화 사이클 완료: A1 인지 재추첨 8 + A2 교차
채점 6 + A3 표본분산 k=5 64 = **78호출 (FAIL 0 · 핀 불일치 0)**, 전 산출물
runs/hardening/ 커밋. 발행 수치 재현·블라인드·매니페스트는 CI가 매 push
검증한다 (`tools/reproduce_analysis.py` 100/100 · `tools/verify_blindness.py`).

## 소유자 대기열 (이 순서 그대로 — 유일한 미결 목록)

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
