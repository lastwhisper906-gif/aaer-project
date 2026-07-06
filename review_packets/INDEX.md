# Review Packet 색인 — 사후 감사 진입점 (Phase 4-2)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> GA-001 하에서 인간 검토는 이 색인에서 시작한다. 각 항목 = 무엇이 결정됐나 +
> 어디서 + **뒤집는 비용**. 감사가 싸야 비동기 검토가 형해화되지 않는다 (RP-02 §2-①).

## Packet 목록

| # | 파일 | 내용 | 오버라이드 재실행 비용 |
|---|---|---|---|
| 00 | `RP-00_state_reconciliation.md` | 상태 조정·D18 감사·T04/T13 후속·모델 핀 | 핀 변경: freeze 전 0 / 실행 후 전체 재실행(34+26호출) |
| 01 | `RP-01_control_group.md` | 대조군 8 확정 + 실격 4 + 기각 11 | 개별 교체: 커밋 1 + 해당 케이스 재실행 2호출 |
| 02 | `RP-02_freeze.md` | freeze 선언 + D11 회고 | freeze 해체 = §5-6 이력 공개 조건부 재고정 |
| 03 | (예정) 분석 ①~⑦ | 실행 후 작성 | — |
| 04 | `RP-04_billing_audit.md` | 과금 경로 감사 (본 실행 전 게이트) — 1~5 PASS/WARN, 권고 R1·R2 | 감사 자체는 읽기 전용 — 뒤집을 설정 변경 없음 |

## Claude 재량 판단 전수 (인간 미개입 결정 — 감사 대상)

| # | 판단 | 근거 위치 | 뒤집기 방법·비용 |
|---|---|---|---|
| J1 | 피평가자 핀 = claude-sonnet-5 (조항 적용 불능 상태의 수립) | decisions_log "모델 고정 기록" | 실행 전: 핀 2줄 수정, 비용 0 |
| J2 | 채점자 핀 = claude-fable-5 (D6 규칙 기계 적용) + 폴백 opus-4-8 | 상동 | 상동 |
| J3 | T13 근거 등급 상향 (NT 10-Q accession 실측) | RP-00 §3-2 | revelation_source 원복 1커밋, 재실행 불요 |
| J4 | ICON 장르 = mixed (참조 매핑 active(gains)과 불일치) | genre_tags.md | 태그 1행 수정 — 실행 후면 해당 케이스 차원 3 재채점 1호출 |
| J5 | 대조군 실격 4건: Cherokee(AAER-4199)·Gartner(AAER-4411)·Avis(=Cendant AAER-1272/1276)·URI(2008 SEC 화해) | RP-01 §2 | 복권 시 해당 슬롯 재선정 + 2호출 |
| J6 | 대조군 선정 거리함수: \|log 매출비\| 1차, FYE tie-break | RP-01 서두 | 함수 변경 = D17 개정 기록 + 8건 재선정 |
| J7 | D1 구현 형태: control은 null-또는-부재 허용 (스키마는 부재 강제 — 코드가 더 관대) | tools/validate_schemas.py | 코드 2줄 — 비용 0 |
| J8 | red-team 12건의 반영 문언 (밴드 경계 50, maxItems 3, rank-sum p 0.20 등 구체 수치) | eval_spec 부록 A | freeze 개정 절차 (§5-6) — 실행 전이면 재실행 0 |
| J9 | 체크리스트 CL1~8 문언 (freeze 개정 #1 — 실행 전) | eval_spec §5-bis | 상동 |
| J10 | 페이로드 태그 목록(PAYLOAD_TAGS)·연차/분기 일수 창 | pipeline/build_payload.py | 코드 수정 — 실행 후면 전체 재실행 |
| J11 | 교란 k ∈ [0.4,2.5] 로그균등·시드 문자열 | probes.md ② / build_payload | 실행 전 0 / 교란 8 재실행 |
| J12 | 파일럿 중립 ID case_90/91 | pilot/cases_pilot.json | 비용 0 |

## 감사 시 우선 순서 (제안)

1. **J5 (대조군 실격)** — 표본 구성을 바꾸는 판단이며 증거가 전부 1차 소스 링크로
   검증 가능 (AAER 번호, SEC PR 2008-190, CIK 723612).
2. **J1/J2 (모델 핀)** — 실행 전이 마지막 무비용 변경 기회.
3. **J8/J9 (기준 수치)** — freeze로 고정된 임계들의 최종 확인.
4. RP-01 §4-1 (PERY 최약 매칭) 수용 여부.
