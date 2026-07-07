# AUDIT_STATE — 증분 감사 대장 (RP-09 Stage 6)

> 규약: 매 라운드 직전 라운드 최종 커밋 이후의 **diff만** I1–I3·테스트 건강
> 기준으로 감사한다. 전체 저장소 재감사 금지 (RP-09 지시).

## 감사 #1 — 2026-07-07 (RP-09 라운드)

- **감사 구간**: `bfe56e8` (RP-08 D20, 직전 라운드 최종) → 본 커밋 HEAD
- **최종 감사 커밋**: 본 파일을 포함하는 커밋 (git log에서 본 파일 최종 변경
  커밋 = last-audited)

### I3 (결과 불변성) — PASS

- 동결 경로 diff **공백** 확인: `git diff bfe56e8..HEAD -- runs/main
  runs/perturbed runs/hardening scoring/probe_results
  review_packets/RP-05_results.md review_packets/RP-06_hardening.md
  scoring/rp05_stats.json scoring/rp06_hardening_stats.json` = 0줄.
- `scoring/grades/` + `pilot/grades/`: 유일 변경 = Stage 0의 **인가된**
  `_meta.human_finalized` false→true + basis 필드 추가 (인가: 소유자 지시
  986a893, D21). 채점 내용(dim/rationale) 변경 0줄 — 기계 확인
  (`git diff ... | grep -v human_finalized|mapping_access_note` = 0).
- 신규 산출물은 전부 **신규 경로** (runs/rp07, runs/rp09,
  scoring/probe_results_v2 예약, scoring/grades_v2 예약) — 동결 경로 불침.

### I1 (블라인드) — PASS

- 피평가자 페이로드 경로(`pipeline/build_payload.py`) 무변경.
- pipeline/ 변경 2건: probe_runner 병렬화(--concurrency) + --out-root —
  페이로드·가드 로직 불침. `pipeline/test_no_guard_bypass.py` PASS.
- RP-07 32호출: guard_payload 경유 (runner.py 무변경 재사용), 카나리 적중 0.

### I2 (컷오프) — PASS

- RP-07 재추첨 = 기존 페이로드 결정론 재생성 (filed≤cutoff 필터 무변경).
- Stage 2 풀 수집은 채점측 메타데이터 수집 (피평가자 입력 아님 —
  fetch_primary_sources 규약 승계, criteria §6-v2).

### 테스트 건강 — PASS

- `pytest pipeline/ tools/ scoring/` **74 passed** (신규: control_v2 규칙 10 +
  grader --candidates 스텁 정합).
- `tools/reproduce_analysis.py` **PASS 100/100** (발행 수치 재현).
- `tools/verify_manifest.py` PASS. `tools/verify_blindness.py`: 감사 시점
  일시 FAIL(d) = **v2 풀 수집 진행 중 신규 파일의 매니페스트 미기재** —
  수집 완료 후 `--write-manifest` 재생성으로 해소 (Stage 2 산출물 커밋에
  포함). 실명/카나리 스캔 자체는 통과 (WARN 2건은 기존 등록된 비누출 어휘).

### 관찰 (결함 아님, 기록)

- grader_runner/test 수정은 채점 인프라 확장(--candidates)으로 기존 답 키
  경로 기본값 불변 — 기존 채점 재현성에 영향 없음 (테스트가 고정).
- RP-08 v1.1 산출물(ed2e132)은 세션 경계에서 미커밋으로 남아 있던 것을
  기록 보존 커밋한 것 — freeze-commit-then-run 위반 아님 (기준 커밋 bfe56e8이
  실행보다 선행).
