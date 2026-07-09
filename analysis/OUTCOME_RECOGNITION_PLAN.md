# OUTCOME_RECOGNITION_PLAN.md — wave-2 outcome-recognition 프로브 사전 등록 (D34, freeze-commit-then-run)

> 2026-07-10 기입. **본 문서와 `analysis/outcome_recognition.py`(결정론 분석기)는
> 프로브 호출 전에 커밋된다.** 2차 외부 검토 잔여 항목 — dose-response의 x축을
> name-ID(대리 지표)에서 outcome-knowledge(직접 지표)로 승격하기 위한 계기 정렬.

## 1. 목적 (명시)

- 현행 dose-response의 x축(name-ID rate)은 **정체 지목**의 대리 지표다 — Tier-③
  (홀드아웃)의 게이트는 **사건 인지(knows_event)** 를 직접 측정하므로 두 축의
  계기가 다르다. 본 프로브는 wave-2 32사에 동일 knows_event 계기를 적용해
  **Tier ①②와 ③의 계기를 정렬**한다 (①은 후속 사이클 대상 — 본 Phase는 wave-2만).
- **무분기(branchless) 측정 실험**: 어떤 임계도 R/H 판정을 변경하지 않는다.
  기존 name-ID 서사(50% → 21.9% → 0%)는 그대로 유지·병기 — 대체 아님.

## 2. 대상·계기·호출 (32 호출)

- 대상: **wave-2 전 32사** (실험군 9 + 대조군 23, `data/candidates/candidates_wave2.json`
  roster) — identity-exposed (실명+티커 노출).
- 계기: **동결 `tools/holdout_probe.py` 그대로** (문구·스키마 무수정 — 홀드아웃
  게이트와 동일 질문: restatement / 4.02 non-reliance / misstatement / SEC 회계
  조사 / 재무보고 관련 임원 이탈의 인지 여부).
- 출력: `runs/wave2/outcome_recognition/{TICKER}.json` (`--kind wave2-outcome`
  `--context "wave-2 outcome-recognition probe (D34, branchless)"`).
- 실행 순서: **티커 알파벳순** (사전 고정 — 시간 절단이 생겨도 결과 독립).
- **케이스 경계 커밋**: 1사 = 1호출 = 1 commit·push (D27 방식 계승, 중간 결과를
  보고 중단할 수 없는 구조). 각 커밋 전 `verify_blindness --write-manifest`.
- 재개 안전: transcript가 이미 존재하는 티커는 스킵 (멱등).

## 3. 사전 고정 보고 형식 (D35에서 이 형식 그대로)

1. **그룹별 인지율 + Clopper-Pearson 95% CI**: 실험군 x/9 · 대조군 y/23
   (CP 구현은 동결 `analysis/holdout_controls_analyze.py.clopper_pearson` 재사용).
2. **§reconcile — name-ID와의 불일치 조정표**: 4분면 (이름 지목∩사건 인지 /
   이름 지목만 / **사건 인지만(이름 상기 불능이나 사건은 앎)** / 둘 다 아님).
   name-ID는 동결 `name_match` 규칙값(unified_table.csv `recognized` 열) 기준.
3. dose-response 표를 **2축 병기**로 확장 (synthesis.md · README 양어):
   name-ID 축(기존 서사 불변) / outcome-knowledge 축(신규) 나란히.
   wave-1은 본 계기 미측정 — 표에서 "미측정(후속 사이클)"로 정직 표기.
4. 해석 경계 (사전 고정): 실험군 인지율이 높게 나와도 이는 **오염 측정의
   개선(직접 지표)** 이지 R4 판정의 변경 사유가 아니다 (R3/R4 규칙의 입력은
   perturbation dominance이지 본 계기가 아님 — 무분기 명시). 대조군 인지율은
   비집행 회사의 회계 사건 상기(리콜) 배경률로만 기술한다.

## 4. 불변량

- 발행 동결값·R/H 판정·name-ID 21.9% 전부 무변경 — 신규 축은 병기 전용.
- 예산: Phase 2 = 32호출 (세션 누계 13 → 45 예정, cap 60). 초과·낭비 호출은
  가계부 정직 기록 (D26 gate_incident 형식).
