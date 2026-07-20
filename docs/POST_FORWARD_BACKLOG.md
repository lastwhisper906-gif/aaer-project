# docs/POST_FORWARD_BACKLOG.md — 첫 forward seal 이후 백로그 (문서화 전용)

> 2026-07-20, owner plan §7. **어느 항목도 첫 seal(2026-11-15)을 막지 않는다.**
> 이 문서는 등록이지 실행 승인이 아니다 — 각 항목의 게이트는 명시된 대로.

## P1 — 교차 패밀리 채점자 (cross-family grader)

`SPECIFICATION ONLY`. 스펙 `specs/cross_grader.md` 유지 (n=20 스팟체크,
κ ≥ 0.6 판독 사전 등록). **실행 시 인증 경로: 소유자 기존 Codex CLI 구독
인증(`~/.codex/auth.json`) 전용 — 종량 OpenAI API 키 금지** (owner plan
§0.4·§7-P1; Q-F07의 "API 키·과금" 옵션 항목은 이 제약으로 갱신됨).
사유: 인간 최종 확정이 이미 존재 — 실재하나 비크리티컬한 한계 효용,
quota 소비. 게이트: Q-F07 (OPEN).

## P2 — 재식별(re-identification) ablation 스위트

`POST-SEAL RESEARCH`. 날짜 원본 vs 이동 / 원시 vs 상대 연대기 / 표준 태그
vs 정규화 범주 / 구조 시계열 vs 파생 비율 / 식별자 제거 vs 강화 메타데이터
제거 / 구조 지문 인지율 측정. **첫 forward 사이클의 전제가 아니다** —
전향 봉인이 1차 암기 우려를 구조적으로 해소한다 (docs/CLAIM_HIERARCHY.md
Level 3 축). v2ds 인프라(`pipeline/date_shift.py`, Q-F05 실행분)가 출발점.

## P3 — 외부 감사 패킷

`WAIT FOR REVIEWER OR ACTIVE OUTREACH`. 지명된 검토자·대상 독자·검토 요청·
전달 일자가 먼저다. 독자 발송(OWNER_QUEUE 1-④)이 실행되기 전에 신규 검증
인프라를 만들지 않는다 (owner plan §0.3·§6).

## P4 — 감사 워크페이퍼 제품층

`WAIT FOR USER DEMAND`. 주장(assertion) 매핑·절차 생성·워크페이퍼 UI·서명
워크플로. 수요 검증 전 착수 금지 — 첫 seal과 무관 (PROJECT.md §8 스코프
가드의 UI·제품화 금지와 정합).

## P5 — 거버넌스 리팩토링

`MINIMAL CLEANUP ONLY`. 이력 거버넌스 이관 금지. 허용: 현행 사이클 인덱스
1개·해소된 소유자 항목 아카이브. 신규 약어 체계 금지.

## P6 — 광역 테스트 매트릭스

`ADD ONLY WHEN LINKED TO A CONCRETE FAILURE MODE`. 신규 테스트는 정확한
위협·잡는 실패·기존 통제가 놓치는 이유를 명명해야 한다 (D97 NBSP 사례가
기준 판례 — 게이트는 형식이 아니라 탐지기).

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
