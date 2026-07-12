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
| 03 | **결번** (packet 부재 — 이력 확인 완료, RP-06 B5(c)) | Phase 4(a232e70)가 03을 "분석 ①~⑦, 실행 후 작성"으로 예약했으나 D14 번호 규칙은 **생성 순서**다 — 과금 감사가 먼저 생성되어 04, 분석 packet은 그 뒤에 생성되어 05가 되었다. 03에 예정됐던 내용은 전부 RP-05에 있다 — 유실 packet 없음 (git: a232e70 → fd2592d → 79e30c3) | — |
| 04 | `RP-04_billing_audit.md` | 과금 경로 감사 (본 실행 전 게이트) — 1~5 PASS/WARN, 권고 R1·R2 (부록: R1/R2 해소) | 감사 자체는 읽기 전용 — 뒤집을 설정 변경 없음 |
| 05 | `RP-05_results.md` | **본 실행 결과** — D7 CONTAMINATED(6/8)·실패 기준 미발동(p=0.0226, 분리 19pp)·오류 귀속 8건·딥다이브 2건 | 재실행 없이 재해석 가능 (원시 데이터 전량 커밋) — 대칭 교란 재실행은 16호출 |
| 06 | `RP-06_hardening.md` | **결정-핵심 강화** (소유자 addendum) — A1 인지 지속(재추첨 5/8, L-5 의무 주의문) · A2 교차 채점 밴드 일치 6/6 · A3 k=5 밴드 (p 0.0009–0.0226, 분리 4/5, delta 분해 부분 해소) | RP-05 §1 불변 — 재해석만. D-2(원본 재추첨 +32호출)는 유예 등록부 조건부 |
| 06-W | `RP-06_grading_workbench.md` | 채점 26건 소유자 서명대 (⚑MODEL 5 · PROPOSAL 2 · A2 병기) | 서명/오버라이드 자체가 목적 — 재실행 없음 |
| 07 | **결번** — 소유자 지시문(2026-07-07, D19)이 본 패킷 번호를 08로 직접 지정. D14 생성 순서 규칙과의 간극은 지시문 우선으로 기록 | — |
| 08 | `RP-08_selection_memo.md` | **대조군 재선정 PROPOSED** (D19 야간 승인, 기준 커밋 fd90613이 풀 조회 선행) — 선정 8/8 (RP-01과 2/8 일치) · [DISCRETIONARY] 15 (선정 영향 4) · also-ran 3,666 전수 · v1.1 개정 후보 2 | 기준 수정 재선정 = 분 단위 (네트워크 불요, memo §0); 풀 재수집 포함 수십 분. **서명 전 채점 진입 불가 — 피평가자 호출 0** |
| 09/10/11 | `RP-09_control_v2_memo.md` · `RP-10_final.md` · `RP-11_expansion_holdout.md` | (별도 파일 — 대조군 v2 / Issue #0 게이트 / wave-2·홀드아웃 확장) | 각 파일 참조 |
| 13-W | `RP-13_grading_workbench.md` | **채점 35건 소유자 서명대** (wave-2 32 + 홀드아웃 3, flags-first: TIER A 13 · mem-suspect 0/35) · 결정론 생성기 `tools/build_rp13_workbench.py`(verbatim 보증) | 서명/오버라이드 자체가 목적 — 재실행 없음 |
| 13 | `RP-13_final_packet.md` | **OWNER-GATE-E 세션 최종 패킷** — 순서 증명(사전등록 c1b85a7 < 첫채점 ef63cfc) · 호출 18/320 · E3→R4 확증 · E1 보류(§5-1) · 소유자 액션 4 | 실행 증거 — 재실행 없음 |
| 14/15/16 | `RP-14_issue2_narrative_diff.md` · `RP-15_label_naming_diff.md` · `RP-16_calibration_language_diff.md` | (별도 파일 — 발행 서사 diff / 라벨 명명 diff(계류) / 보정 언어 diff) | diff-only — 각 파일 참조 |
| 18 | `RP-18_asymmetry_memo_publication.md` | **D53 비대칭 메모 발행 여부** (소유자 대기) — 게시 가능 완성 영문 텍스트·배치 2안(Issue 1 부록 권장)·게시 명령·가설 표지 검토 노트 | 게시 = 명령 1줄; 기각 = 파일 존치 (비용 0) |
| 17 | `RP-17_denominator_fallback.md` | **D56/D57 사후 분모 개정 분류 판정** (소유자 대기) — 기계 결함 vs 분석 변경, 1차↔재실행 전량 델타(holdout AUC 0.167→0.476), 정확 원복 명령, CLAUDE.md 거버넌스 3줄 제안 diff | 기각 = checkout 원복 커밋 1 + 주석 2줄 (재실행 0) |

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
| J13a~g | 실행층 전환의 실증 재량 7건: --bare 기각 · CONFIG_DIR 격리 기각(2회 실증) · 플래그 기반 격리 확정 · max-turns 2 · 하네스 주입 컨텍스트 수용 · StructuredOutput 예외 · 레이트 리밋 오탐 수정 | decisions_log 개정 #2 부록 + run_log 게이트표 | 전부 실행층 — 기준 무관. 격리 재검증 = 프로브 1호출. **J13-b/c는 RAT-001로 소유자 추인 완료 (2026-07-07, overrides.md)** |
| J14~J19 | 분석 재량 6건: 비대칭 비교 채택 · 인지 정규화 · MW 정확 검정 구현 · 오류 귀속 1차 8건 · Sloan 방향 · 파일럿 채점 산입 | RP-05 §9 | RP-05 §9 병기 (대부분 호출 0 재계산) |
| J20~J23 | RP-06 재량 4건: A1=frozen 프로브 재추첨 해석 (지시문 전제가 frozen 프로토콜과 모순) · A3 입력 집합 = 본 분석 집합 · A2 비플래그 정의+시드 20260706 · A2 채점 변형 = 본 분석 변형 | RP-06 §4 | RP-06 §4 병기 (J20 원본 프로브 신설 8호출 / J21 대칭 교란 32호출 / J22 1호출 / J23 ≤6호출) |
| J24 | RP-08 재량: E4 오탐 수기 통과 14건 (증거 개별 기록, 식별 토큰 재검색 전건 0) · Sealed Air는 W.R. Grace 계보로 보수적 유지 · S2 동률의 0.05 버킷 구현 · E7 코드 정합 수정 (treatment 그룹만 배제) | RP-08 memo §3 + `runs/rp08/e4_manual_overrides.json` | override 1건 삭제 후 재선정 = 분 단위, 호출 0 (PROPOSED 단계 — 채점 미진입) |
| JE-1 | **OWNER-GATE-E 세션 실행층 재량**: (a) "run-to-quota"를 목표로 삼지 않음 — 미터링 E3(18호출)로 한정, E1 보류(§5-1 네트워크 look-ahead), E2/E4/E5 소유자 게이트 이관 (b) E3 개정 A: 고정 payload 모델 재추첨(wave-1 A3 프로토콜, 첫 채점 전) (c) DAR name-ID 규칙-vs-사람 불일치 재채점 금지·병기 | `scoring/overrides.md` JE-1 · `docs/OWNER_QUEUE.md` Q-E01/E02/E03 · `analysis/W2_PERTURB_REDRAW_PLAN.md` 개정 A | (a) spend 재량 = 소유자 추인/재지시 대상 (b) 개정 A는 첫 draw 전이라 재실행 0 (c) Q-E02 규약 선택 시 정합 |

## 감사 시 우선 순서 (제안)

1. **J5 (대조군 실격)** — 표본 구성을 바꾸는 판단이며 증거가 전부 1차 소스 링크로
   검증 가능 (AAER 번호, SEC PR 2008-190, CIK 723612).
2. **J1/J2 (모델 핀)** — 실행 전이 마지막 무비용 변경 기회.
3. **J8/J9 (기준 수치)** — freeze로 고정된 임계들의 최종 확인.
4. RP-01 §4-1 (PERY 최약 매칭) 수용 여부.
