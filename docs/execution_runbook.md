# 실행 런북 — Phase 3 (requires credentials)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 전제: freeze 커밋 `82a7717` 이후 기준 무변경 (러너가 clean tree를 강제).
> **자격 증명**: `ant auth login` 또는 `export ANTHROPIC_API_KEY=...` +
> `pip install anthropic` (.venv). 이 두 가지가 이 런북의 유일한 외부 전제다.
> 비용 추정: 호출 34회 (프로브 16 + 파일럿 2 + 본 16 + 교란 8 — 프로브 verbatim 8 별도)
> × 페이로드 ~20-60K 입력 토큰 — sonnet-5 기준 대략 $10-25; 채점 26회 fable-5 ~$15-40.

## 순서 (역순 금지 — D7 분기가 본 실행 해석을 결정)

```bash
source .venv/bin/activate && pip install anthropic
python tools/verify_manifest.py                      # PASS 확인

# 1. 인지 프로브 (교란 페이로드, 실험군 8) → D7 분기
python pipeline/probe_runner.py --recognition --cases scoring/perturbed_cases.json
#    → scoring/probe_results/recognition/ 판독: 실명 일치 수 n
#    n>=3: CONTAMINATED — 본 분석 = 교란 실행, 원본은 부록 상한 (전 보고서 헤드라인 명시)
#    n<3 : 본 분석 = 원본 실행, delta = 암기 기여 추정
#    분기 결정을 logs/run_log.md + RP-03에 문서화

# 2. 축어 회상 프로브 (원본 필드만, 실험군 8) → 케이스별 잔여 위험 등급
python pipeline/probe_runner.py --verbatim --cases scoring/perturbed_cases.json

# 3. 파일럿 (VRX/GE — pilot/ 격리, 본 실험 디렉토리 금지)
python pipeline/runner.py --cases pilot/cases_pilot.json --out pilot/runs
python scoring/grader_runner.py --runs pilot/runs --out pilot/grades   # 매핑은 id_mapping_pilot
#    항목별 정답 키 대조 → 파이프라인 결함 발견 시 코드 수정(테스트 통과 + run log 기재)
#    → pilot/runs 비우고 재실행 clean 확인 후 본 실행

# 4. 본 실행 (원본 16 + 교란 8, 변형당 1회 — D5)
python pipeline/runner.py --cases data/evaluatee/cases.json --out runs/main
python pipeline/runner.py --cases scoring/perturbed_cases.json --perturbed --out runs/perturbed

# 5. 채점 (grader = fable-5, 폴백 opus-4-8 로그)
python scoring/grader_runner.py --runs runs/main --out scoring/grades/main
python scoring/grader_runner.py --runs runs/perturbed --out scoring/grades/perturbed

# 6. 스키마 검증 + Brier/판별 통계 (결정론)
#    각 runs/*.json을 schemas/llm_output.json으로 검증 — 실패는 파이프라인 오류 귀속
python tools/brier.py <(python - <<'PY'
import json,glob;print(json.dumps([{"case_id":json.load(open(f))["case_id"],
"p":json.load(open(f))["misstatement_probability"]} for f in sorted(glob.glob("runs/main/case_*.json"))]))
PY
)
```

## 실행 중 의무 기록 (SR 11-7 제3자 모델 규칙)

- `logs/api_run_log.jsonl`: 호출별 response.model(서버 보고 문자열)·request id·토큰·
  시간·freeze 상태 — 러너가 자동 기록. 실행 후 이 파일 커밋.
- 파일럿 결함 수정 시: 코드 diff + 사유를 run_log.md에 기재 (post-freeze 코드 수정 규약).
- grader 폴백 발동 시: _meta.fallback_used=true 건수를 RP-03에 집계.

## 실행 후 → 분석 (RP-03, 3-5 ①~⑦)

① 케이스별 판정+인용+근거 등급 (grades + 잔여 위험 등급 병기) ② Loop-3: **skipped —
no sealed predictions** (run_log 2026-07-06) ③ LLM vs 4스크린+Piotroski (사전 기준선
docs/baseline_screens.md §3 — 누락 장르 커버 여부가 핵심 질문) ④ 원본−교란 delta
(또는 D7 오염 분기 보고) ⑤ 오류 1차 분류 (error_taxonomy R1→R2→R3; MODEL 전건 인간
감사 플래그) ⑥ 장르 비대칭 ⑦ D10 조건부 평가 (데이터로만).

보고 언어 제약(3-6): 정밀도 % 헤드라인 금지 / n=8 ±35pp / 상한 명기 / D5 단일 실행
문구 / 선택·생존 편향 문단 / "Claude 기반 단일 파이프라인 한정" / 오염 프로브 문서
헤더 "these controls BOUND memorization risk; they do not eliminate it."
