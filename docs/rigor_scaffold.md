# Rigor Scaffold — 2024–2026 LLM-eval 지식 체계 → 본 프로젝트 구현 매핑

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 소유자 지시(2026-07-06)의 매핑 명세를 구현 지점·검증 방법과 함께 표로 고정.

| 개념 | 구현 지점 | 검증 방법 |
|---|---|---|
| **[Eval 설계] 분리 차원 루브릭 (3–6차원)** | D4의 4차원 (`scoring/eval_spec.md` §4) | 독립 채점 가능성의 self-red-team 검증 — 발견 12건 반영 완료 (부록 A) |
| **[오염 통제] 시간 홀드아웃** | 컷오프 = 폭로 전일 (`cutoff_date`), `pipeline/cutoff_guard.py` 게이트웨이 | pytest (cutoff_guard 테스트) + 정적 스캔 (`test_no_guard_bypass.py`) — CI |
| **[오염 통제] look-ahead 정적 스캔 / n-gram 중첩 상당물** | 방어 ④ 값 수준 스캔 (`test_build_evaluatee_inputs.py` FORBIDDEN_VALUE_SUBSTRINGS) | CI 자동 (재생성 대조 + 스키마 + 금지 필드 + 값 스캔 4중) |
| **[오염 통제] 축어 회상 프로브** | `scoring/probes.md` ③ — 문서 없이 정확 수치 회상 여부 | Phase 3-2 실행, ±2% 기계 판정, 케이스별 잔여 위험 등급 |
| **[오염 통제] 교란 테스트** | D8: 사명 익명화 + 상수배 재스케일 (`scoring/probes.md` ②) | 원본−교란 delta = 암기 기여 추정 (분석 ④); D7 임계 ≥3/8 사전 등록 (`9f0fb42`) |
| **[오염 통제] 카나리 문자열** | D9: GUID 2개 — genre_tags.md·methodology_limitations.md 말미 삽입 | 차기 사이클 신모델 프로브로 학습 유입 감지 |
| **[백테스트 죄악] look-ahead 편향** | cutoff_guard(피평가자) + `filed<=cutoff` point-in-time(베이스라인·파일럿·페이로드 빌더 전 표면) | 정적 스캔 3곳: pipeline(기존) + `scoring/baselines/test_screens.py`(결정론·오프라인) + Phase 3 러너 스캔(예정 V4/V7) |
| **[백테스트 죄악] 생존·선택 편향** | 전 보고서 의무 문단: "표본은 해소 완료 집행 사건에서 의도적 추출" | 문서 체크리스트 (eval_spec §5, baseline_screens §4에 기재 확인) |
| **[백테스트 죄악] point-in-time 데이터** | companyfacts fact 단위 `filed <= cutoff`, 최신 filed 승리 — 컷오프 후 재작성 배제 | `test_point_in_time_excludes_post_cutoff_filings` + `..._pre_cutoff_amendment_wins` (CI) |
| **[SR 11-7] 개념 건전성** | eval spec + threat model의 review packet 감사 경로 (RP-00~02) | 인간 사후 감사 (packet마다 오버라이드 방법 명기) |
| **[SR 11-7] 결과 분석** | 정답 키 대조 (4차원 채점) + 오류 귀속 (`scoring/error_taxonomy.md` R1→R2→R3) | 분석 ⑤: MODEL 분류 전건 인간 감사 플래그 |
| **[SR 11-7] 상시 모니터링** | 차기 사이클 계획 (Phase 4 메모 §3) + 카나리 + D10 조건부 확장 사전 등록 | Phase 4 산출물 |
| **[SR 11-7] 제3자 모델 규칙** | 전 API 호출에 response.model·타임스탬프·요청 ID·freeze 해시 기록 (러너 요구사항) | Phase 3 run log 검사 |

본 결과는 Claude 기반 단일 파이프라인에 한정된다 (§5-5).
