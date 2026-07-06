# Review Packet 02 — FREEZE (기계적 고정, 차단 게이트 1 대체)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 이 packet을 포함한 커밋이 **freeze 커밋**이다 (GA-001 (c): freeze-commit-then-run).
> freeze 해시는 러너가 실행 시 `git rev-parse HEAD`로 기록하고, 작업 트리가 깨끗함
> (`git status --porcelain` 공백)을 함께 검증한다. freeze 후 기준·루브릭·임계·케이스
> 명단·프로브 설정 변경은 로그된 개정 + 재실행 노트 필수 (§5-6). 파이프라인 **코드**
> 결함 수정은 허용 (테스트 통과 + run log 기재).

## 1. 고정 대상 (전부 이 커밋 시점의 HEAD 상태)

| 산출물 | 파일 | 상태 |
|---|---|---|
| Eval spec v1.1 (4차원 루브릭 + 실패 기준) | `scoring/eval_spec.md` | red-team 12건 반영 완료 |
| 출력 계약 v1.2 | `schemas/llm_output.json` | misstatement_probability + hypotheses |
| Threat model v1 (V1~V10) | `scoring/threat_model.md` | |
| 오류 분류 체계 v1 (R1→R2→R3 MECE) | `scoring/error_taxonomy.md` | |
| 소유자 결정 대장 D1~D18 + 모델 핀 | `scoring/decisions_log.md` | 피평가자 `claude-sonnet-5` / 채점자 `claude-fable-5` (폴백 `claude-opus-4-8`) |
| 대조군 확정 8 + 기각 기록 | `review_packets/RP-01`, `data/candidates/candidates.json` (38건) | |
| 실험 케이스 파일 v1.2 (16건) | `data/evaluatee/cases.json` + `scoring/id_mapping.json` (시드 20260706) | 4중 방어 + 값 스캔 확장 CI 녹색 |
| 프로브 설정 (D7 임계 ≥3/8, D8 교란 규칙, 축어 ±2%, 카나리) | `scoring/probes.md` | D7 임계는 `9f0fb42`에서 이미 사전 등록 |
| 장르 태그 (정답 키) | `scoring/genre_tags.md` | |
| 베이스라인 결과 (사전 기준선) | `scoring/baselines/` + `docs/baseline_screens.md` | |
| 방법론 매핑 | `docs/rigor_scaffold.md` | |

## 2. D11 회고 (3회 이월분의 서면 이행)

**의제 ① 오버라이드 0건 패턴 (유도 서명 세션)**: GP-0~9 전 항목에서 추천안이
채택됐다 — §9 기준으로는 '고무도장 의심' 신호다. 이번 사이클의 대응은 두 갈래였다:
(a) 추천안 자체를 별도 컨텍스트가 공격하게 함 (eval spec self-red-team — HIGH 6건이
실제로 나왔고 전건 반영됨. **추천안은 공격받기 전까지 신뢰할 수 없다는 실증**),
(b) 인간 검토를 사전 차단에서 사후 감사로 옮기되 오버라이드 비용을 packet마다
명시해 감사를 싸게 만듦. 잔여 위험: 사후 감사가 실제 수행되지 않으면 0건 패턴은
형해화로 남는다 (GA-001 학습 노트 동일 지적).

**의제 ② A형 23/30 분포**: 기준 관대함 vs AAER 선택 편향의 판별은 Week 3 오류
귀속(분석 ⑤)의 F/T 채널 예측-적중 괴리로 예정 (error_taxonomy 사전 등록 점검).
이번 사이클 신규 데이터 포인트: 베이스라인 1차 실행에서 실험군 8 중 **스크린
플래그는 3건뿐** (OFIX/KHC/MRVL-F) — A형 판정(공개 데이터 감지 가능성)과 결정론
스크린 감지가 같은 것이 아님을 실측이 이미 보여준다. A형 기준의 F/T 채널 예측이
과대했는지는 LLM 실행 결과와 삼각 대조해야 확정 가능.

**의제 ③ 게이트 비동기 전환 (GA-001)**: 전환의 실질 안전장치는 (i) freeze-commit-
then-run의 기계적 시간 무결성 (이 커밋), (ii) packet별 오버라이드 경로·재실행 비용
명시, (iii) 저자 표시 강제 (D15). 전환 후 이 세션에서 인간 개입 없이 내린 재량 판단
들(모델 핀, ICON mixed 태그, 대조군 4건 실격 판정 등)은 전부 packet에 기록됨 —
사후 감사 대상 총목록은 Phase 4 색인에서 집계.

## 3. 불확실성·잔여 격차

- **실행 자격 증명 부재** (환경): Phase 3 API 실행은 자격 증명 확보 시까지
  "requires credentials" — freeze는 성립하고, 실행만 대기.
- 대조군 C05(PERY)의 산업축 부분 일치 — RP-01 §4-1.
- 파일럿 2건(VRX/GE)은 실험 16케이스 밖 (T18/T25는 실험군 미포함) — pilot/ 격리
  실행으로 본 실험과 물리 분리.

**학습 노트(§10)**: freeze의 실질은 "변경 금지"가 아니라 **변경의 가시화**다 —
git 이력이 있는 한 무엇이든 바꿀 수 있지만, freeze 커밋 이후의 변경은 전부
'실행 전 고정' 주장에서 빠지게 된다.
