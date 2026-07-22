# SUPERSESSION — cycle_001 PROTOCOL 해시 재핀 (2026-07-22, 서명 완료)

> **지위: 발효.** 소유자 서명 접수 (owner, 2026-07-22, this session's
> structured decision responses — 최종 패킷 §3 건, 원장 D113).

## 무엇이 무엇을 대체하는가

`forward/cycle_001/PROTOCOL.md`의 2026-07-20 생성본(동결 파일 해시 스냅샷)을
2026-07-22 재생성본이 **대체(supersede)** 한다. 사이클은 아직 봉인 전이다
(첫 seal 2026-11-15, `OWNER_LAUNCH_GATE.md` 미서명) — 봉인 후 수정 금지
조항은 발동 전이며, 이 재핀은 봉인 전 준비 산출물의 갱신이다.

## 재핀 사유 (해시가 바뀐 실제 원인 — 전건 소유자 승인 이력 있음)

1. **remediation/external-review 병합 (D107, 0269b63)** — 외부 검토 교정:
   `pipeline/build_payload.py`(T09 v3 cutoff 계약)·`pipeline/runner.py`
   (T07 지문 멱등)·`schemas/llm_output.json`(T06 단일 출처). 관련 정오표:
   **ERRATA E-002** (wave-2 rev2 비교 — rev2 인용 가능, v1 동결 유지).
2. **C3 하네스 핀 강제 (D109)** — `pipeline/cli_client.py` (첫 호출 전
   fail-closed 버전 대조 + 실측 버전 로그).
3. **D100 이후 main 직행 커밋** — `specs/FORWARD_WATCHLIST_V1.md`
   (ce60095, 점수 조립 규칙 사전 등록 — 소유자 계획 서면 위임분).

무변경 핀: `docs/UNIVERSE_SELECTION.md` · `specs/RISK_SCORE_SEMANTICS.md`
(해시 동일 — 유니버스·서수 의미론은 재핀에서 접촉 없음).

## 불변 확인

- universe.json 정합 재검증 PASS (selected 12, forward_prepare 출력).
- 모델 핀 `claude-sonnet-5` 불변 · screening_cutoff 2026-11-15 불변 ·
  구독 OAuth 전용 경로 불변 · 서수 컷 불변.
- 발사 승인 아님 — OWNER_LAUNCH_GATE는 별도 미서명 상태 유지.
- 주의: 하네스 핀(2.1.201) vs 실측 CLI(2.1.216) 불일치가 미해결(Q-O11) —
  11월 발사 창 전에 해소 필요 (해소 시 cli_client 해시가 다시 바뀌므로
  그 시점 재핀 1회 더 예상).

## 서명

- 소유자 서명: **owner (2026-07-22, this session's structured decision
  responses)** — 원장 D113.
- 서명 효력: 본 재핀 승인 + 2026-07-20 스냅샷의 대체 확정. (Q-O11 (C)
  선택에 따라 실행 창에서 cli_client 해시 재핀 1회 추가 예정 — 그 재핀은
  별도 supersession 건.)
