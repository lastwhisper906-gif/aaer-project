# Orientation Check — Day 1 (2026-07-03)

> 작성: 채점 보조 Claude. 상태: **정보 정리 문서 — 판정 아님.** 불일치 항목의 스키마 수정 여부는 §7상 본인 확정 사항.

## (a) §7 협업 모델 — 3문장

원칙은 **AI-first, human sign-off**: 판단이 걸린 산출물(A/B형 판정, 채점, 오류 귀속, trust boundary 표)은 Claude가 근거(원문 인용·데이터 포인트)를 반드시 첨부해 1차 수행하고, 인간이 근거를 검토해 서명하거나 오버라이드한다 — 근거 없는 판정은 서명 대상 자체가 아니다. 채점 기준·프로토콜의 사전 고정과 변경 승인, 킬 스위치 GO/STOP, 수혜자 가설, 발행 결정은 본인 전속 확정 사항이며 Claude는 자료·논거 제공까지만 한다. 구조적 안전장치로 오버라이드는 `scoring/overrides.md`에 기록되어 trust boundary의 1차 데이터가 되고("llm_judgment_error" 귀속은 본인 전수 검토), 파이프라인 안의 피평가자 Claude와 이 개발·채점 보조 세션은 역할이 분리되어 보조 세션이 피평가자의 답을 대신 생성할 수 없다.

## (b) 3개 스키마가 각각 지배하는 것

| 스키마 | 지배 대상 | 핵심 강제점 |
|---|---|---|
| `case_input.json` | 16케이스 메타데이터 | look-ahead 가드의 앵커: `first_revelation_date`(AAER 발행일 아님) → `cutoff_date` = 폭로 전일. 대조군은 매칭 실험군의 날짜 복사. §7 게이트 필드 `ab_classification`+`ab_signed_off` |
| `llm_output.json` | 피평가자 파이프라인의 케이스당 출력 | §5-4 태스크 분해: 닫힌 질문 체크리스트 + 근거 필수(인용·accession no·위치·computed_by), `risk_tier` 3단계 강제(열린 서술 금지), `documents_used`의 filing_date = 컷오프 증적. 파싱 실패 = 파이프라인 오류 귀속 |
| `score_record.json` | 케이스당 채점 기록 | §7 구현체: 항목별 verdict + AAER 원문 대조 rationale + proposed_by, `sign_off`(signed/overridden/pending) 필수, `override_ref` → `scoring/overrides.md`, `scored_against_protocol_version` = 프로토콜 git hash(사전 고정 증적) |

## (c) 문서 간 불일치 및 채택한 보수적 해석

| # | 불일치 | 보수적 해석 (오늘 채택) |
|---|---|---|
| 1 | `case_input.scheme_type`이 `required`인데, 자체 description은 대조군 생략 허용을 요구 — 스키마 내부 모순 | 오늘 산출물은 실험군 후보뿐이므로 충돌 미발생. `required` 유지. 스키마 수정은 §7상 본인 승인 필요 → REVIEW.md 항목화 |
| 2 | `llm_output.documents_used`가 선택 필드 — 그러나 유일한 컷오프 증적이며 CLAUDE.md는 cutoff_guard 경유를 의무화 | 실무상 필수로 취급. cutoff_guard가 모든 접근을 로그로 남겨 스키마 밖에서 증적 확보 (Stage 2) |
| 3 | `score_record.learning_note`가 선택 필드 — §10·CLAUDE.md는 판정 산출물에 학습 노트 의무 | 오늘부터 모든 판정 인접 산출물에 학습 노트 의무 적용 (스키마보다 엄격하게) |
| 4 | 대조군의 `first_revelation_date`는 "매칭 실험군 복사"인데 매칭 관계를 담는 필드(`matched_case_id`)가 없음 | 대조군 선정은 오늘 스코프 밖(hard rule). 스키마 보완 필요 항목으로 REVIEW.md에 기록만 |
| 5 | PROJECT.md §5-1 "분식 **공표일** 이전" — AAER 발행일로 오독 가능. 스키마는 명시적으로 `first_revelation_date` 기준 | 더 이른(=더 엄격한) 앵커인 `first_revelation_date` 채택. 스키마가 옳고 PROJECT.md 문구가 뒤처진 것으로 문서화 |
| 6 | 스키마 v1이 "일괄 승인, 상세 검토 없이"(commit a333ee4) 확정됨 — 불변 조항 3(인간 서명)의 형해화 사례. 실제로 불일치 #1이 v1에 잔존 | 정직하게 기록된 점은 유효. 단, 파이프라인 코드가 스키마에 의존하기 전 실검토 재서명을 REVIEW.md 최상단에 배치 |
| 7 | `llm_output.risk_tier` 3단계 ↔ `score_record.case_verdict.outcome` 이진(TP/FP/TN/FN) 매핑 미정의 | 실행 전 채점 프로토콜에서 사전 고정해야 할 자유도로 명시 (§5-6). 오늘은 정의하지 않음 — 기준 설계는 본인 확정 영역 |
| 8 | 사용자 지시 "확정 불가 시 first_revelation_date에 `UNRESOLVED` 기재" ↔ 스키마 `format: date` | 날짜 조작(fabrication)이 format 위반보다 더 위험 → `UNRESOLVED` 문자열 기재. 검증 시 해당 케이스는 **의도된 실패**로 분류·목록화 |
| 9 | 후보 단계인데 `case_id` 패턴 `^(T\|C)[0-9]{2}$` 강제 — 스키마는 확정 케이스용으로 설계됨 | 잠정 ID `T01~`을 부여하되 "킬 스위치 판정 전 잠정"임을 COLLECTION_NOTES에 명시. 확정 시 재번호 가능 |

**학습 노트 (§10)**: 스키마의 `required` 배열만이 강제력을 갖는다 — description 문자열에만 존재하는 규칙은 검증기가 그냥 통과시키는 규칙이며, 이번 v1의 모순(#1)이 "검토 없는 일괄 승인"을 통과한 것이 그 실증 사례다.
