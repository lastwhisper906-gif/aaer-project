# EARLINESS_RUNBOOK — E2 조기성 실행 절차 (owner-gated, 권한 최종)

> Authored by Claude Code (무인 재개 세션 #2, 2026-07-08). 사전등록: `analysis/EARLINESS_PLAN.md`
> (freeze `c1b85a7`, 불변). 설계: `docs/EARLINESS_DESIGN.md`. 구현: `pipeline/earliness_grid.py`
> (순수 그리드) + `pipeline/build_payload.py`(base_id) + `tools/build_earliness_snapshots.py`(생성기).
> **이 라운드에서 채점은 발사하지 않았다 (미터링 0). 발사는 소유자 권한이 마지막 단계다.**

## 0. 왜 런북인가 (구현 완료, 발사 미완)

무인 재개 세션 #2는 미터링 플랜을 실행하려 했으나 `~/aaer-data` PIT 캐시 부재로
전 유닛이 API 호출 전 실패했다(OWNER_QUEUE Q-E04). 그 시간에, "launch-ready"로
기술됐지만 실제로는 **미구현**이던 E2 조기성 하네스(Q-E05)를 **오프라인·0-미터링**으로
구현·검증했다. 남은 것은 (1) 캐시 복원과 (2) 소유자 발사 승인뿐이다.

## 1. 발사 전 조건 (전부 충족 시에만)

1. **캐시 복원** — 신뢰 `~/aaer-data`를 매니페스트 sha256(`data/manifests/aaer_data_manifest.json`)
   대조로 복원(감독). 무인 재fetch 금지(§5-1, Q-E04). `~/aaer-data` 있으면 아래 단계 가동.
2. **CI green** — `git status` clean, 마지막 push CI 성공.
3. **소유자 발사 게이트** — `scoring/overrides.md`에 `EARLINESS-LAUNCH: YES` 한 줄 기록·커밋
   (RP-09-FINAL 선례와 동일). 이 줄이 없으면 채점 발사 금지. runner.py 자체엔 게이트가
   없으므로 **발사는 소유자가 직접 개시**한다(절차적 게이트, 권한 최종).

## 2. 절차

### Step 1 — 그리드 감사 (0-미터링, 캐시 필요)
```
python tools/build_earliness_snapshots.py                 # --plan(기본): 선정+그리드 출력만
```
- 적격 = fraud detected(p>=50) 13 + RP-01 대조군 8 = **21** (커밋 산출물로 결정, 캐시 불요로도 확인 가능).
- 캐시 있으면 케이스별 `depth / snaps / drop[사유]`를 출력. **모든 스냅샷 컷오프 ≤ 폭로
  컷오프**, drop 사유(exceeds_revelation / adjacent_filing_leak)를 사람이 눈으로 확인.
- `⚑빈약(<6)` 표시 케이스(잔존 제출 <6, §1 바닥 미달)는 궤적 신뢰도 주의(OFIX 2점 등).

### Step 2 — 160 cap 균일 절단 (사전등록 §5)
- Step 1의 총 스냅샷이 **160(E2 하위 cap)** 초과면 `--max-snapshots`를 8→7→… 균일 하향해
  총계 ≤160 (그리고 전역 320 잔여 이내). 대조군은 동일 플래그로 자동 동일 깊이 매칭.
  ```
  python tools/build_earliness_snapshots.py --max-snapshots 7   # 예: 총계 확인 후 조정
  ```
- **깊은 이력부터 절단**(모든 케이스 동일 깊이) = 결과 독립 보장(§5). 특정 케이스 편애 금지.

### Step 3 — emit (스냅샷 케이스 + 폭로 레지스트리 + 가드 기록, 캐시 필요)
```
python tools/build_earliness_snapshots.py --max-snapshots <N> --emit
```
- 기록: `runs/earliness/cases_earliness.json`(러너 입력) · `revelation_registry.json`(가드용) ·
  `access_log.jsonl`(스냅샷별 cutoff_guard **allowed** 기록). 가드 verdict가 전부 `allowed`가
  아니면(위반) 중단·조사. runs/ 기록이므로 커밋 전 `verify_blindness.py --write-manifest`.

### Step 4 — 스냅샷0 재사용 (재호출 없음)
- 스냅샷 0 = 폭로 컷오프 = 기존 본실행 점수. 재채점 금지: wave-1은 `runs/main/case_NN.json`,
  wave-2는 `runs/wave2/scores/case_NN.json`의 p를 궤적 t=0 점으로 **복사**(불변, IMMUTABILITY).

### Step 5 — 채점 발사 (owner 게이트 통과 후, 미터링)
```
# 얕은 것(폭로 근접, _s1)부터, 케이스 알파벳순 (§5 채점 순서). 교란 프레임(헤드라인).
python pipeline/runner.py --cases runs/earliness/cases_earliness.json --perturbed \
    --out runs/earliness/perturbed --only <case_NN_s1 ... 얕은 순>
```
- 피평가자 핀 claude-sonnet-5, payload guard·cutoff(load_pit_series)·pin 전건 활성(기존 러너).
- 멱등: 완료 스냅샷 자동 skip. 서브배치마다 verify_blindness --write-manifest → commit → push
  → CI green → RESUME 가계부 갱신(정확한 호출수). **전역 320 cap 초과 직전 STOP.**

### Step 6 — 분석 (사전등록 §3 지표)
- **탐지 선행시간** = 궤적이 p≥50을 처음 넘는 스냅샷의 t(폭로까지 분기).
- 전체 p(t) 궤적 + inside-noise 밴드(RP-07 per-case σ 중위 6.3pp) — **형태만** 판독, 점별
  유의성 주장 금지. 대조군 궤적(평평 기대)과 병치. d2 텍스트-증거 조기성(RP-10 Phase 3)과 교차검증.
- 산출은 NEW 경로(`analysis/earliness_*`), Issue #1 §earliness 초안. **발행 안 함**(소유자 게이트).

## 3. 원본 프레임 부분 (Unit 4, EARLINESS_PLAN 부록)

- detected 케이스만 원본(정체 노출) 궤적 — `--perturbed` 없이 동일 절차, 별도 out 경로
  `runs/earliness/original`. base_id로 프레임 일관. 교란=하한 anchor / 원본=entangled 상한,
  **케이스별 병치(풀·평균 금지)**. 예산 잔여 시에만, 높은 선행시간 detected부터.

## 4. 불변 준수 요약

- BLINDNESS: runner의 payload guard(EVALUATEE_FORBIDDEN_MARKERS) 전건 · 교란 프레임 정체 마스킹.
- CUTOFF: load_pit_series(filed≤스냅샷컷오프) + earliness_grid G1/G2 + guard_snapshot(≤폭로) 3중.
- IMMUTABILITY: runs/main·wave2/scores·frozen grades 무침해. 스냅샷0 복사(재채점 아님). NEW 경로만.
