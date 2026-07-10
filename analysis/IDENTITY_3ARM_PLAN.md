# IDENTITY_3ARM_PLAN.md — 정체 3-arm 인과 방향 실험 사전 등록 (D36, freeze-commit-then-run)

> 2026-07-10 기입. **본 문서·가공 사명 매핑(`data/evaluatee/fict_names_wave2.json`)·
> arm (b) 러너(`tools/run_identity_arms.py`)·분석기(`analysis/identity_3arm_analyze.py`)는
> 피평가자 호출 전에 커밋된다.** 신규 호출은 arm (b)의 9건뿐.

## 1. 설계 (wave-2 실험군 9사)

| arm | 정체 토큰 | 수치 | 출처 | 신규 호출 |
|---|---|---|---|---|
| (a) 익명 | "Company CASE_NN" + XXnn | 교란 재스케일(k) | **동결** `runs/wave2/perturbed` | 0 |
| (b) 가공 사명 | 가공 회사명 + 가공 티커 | 동일 교란 재스케일(동일 k) | 본 실험 `runs/wave2/identity_arm_b` | **9** |
| (c) 실명 | 실명 + 실티커 | 원본 | **동결** `runs/wave2/scores` | 0 |

- arm (b)는 동결 `build_payload(perturb=True)` 페이로드에 **정체 토큰(사명·티커)만
  중첩** — k·시계열·연대기·TASK·스키마·페이로드 가드 전부 동일. (a)와의 유일한
  차이 = "회사명이 있는가", (c)와의 유일한 차이 = "그 이름이 실명인가".
- 동결 pipeline/ 무수정 — import 재사용 (신규 tool, holdout 러너들과 동일 방식).
- 실행: case_id 알파벳순, **케이스 경계 commit·push** (D27 방식), 멱등 skip.

## 2. 가공 사명 생성 (결정론 + 실존 충돌 전수 스크린 — §6 기계 강제)

- 시드: `sha256(case_id + "fictname-v1" + attempt)` — attempt=0부터, 충돌 시
  attempt+1 재생성, **전 이력 로그** (`fict_names_wave2.json` history).
- 충돌 스크린 (전수): (a) 코인어 core가 **EDGAR 전 filer 사명 목록**
  (`cik-lookup-data.txt`, 1,049,982행, 2026-07-10 fetch)에 부분 문자열로도 부재
  (b) 가공 티커가 실존 티커 목록(`company_tickers.json`, 10,418건)에 부재.
- 참조 파일은 `~/aaer-data/reference/` (git 밖, `data/README.md` 규약) —
  **스크린(배제) 전용, 어떤 페이로드에도 반입되지 않음**. 케이스 재무 데이터가
  아니므로 §5-1 look-ahead 채널 아님 (스크린을 통과한 이름은 정의상 실존 회사와
  무관 = 미래 데이터가 케이스 입력에 누출될 경로 자체가 없음).

## 3. 사전 고정 판독 규칙 (분석기가 기계 적용)

케이스별 paired delta: `b−a`(이름 존재 효과) · `c−b`(실명 효과). 집계 =
**median + 부호 검정(정확 이항, 동률 제외, 병기 전용)**. "≈" 임계는 기존 사전
등록 10pp 바 재사용 (Issue #0 §4의 인지 효과 바와 동일).

- **(i)** |median(b−a)| < 10pp **AND** median(c−b) ≥ 10pp →
  "**실명 토큰이 점수를 끌어올린다는 방향 증거** — 암기 기여가 이름 채널에
  실린다 (가공명은 익명과 다르지 않은데 실명만 올라감)."
- **(ii)** |median(b−a)| < 10pp **AND** |median(c−b)| < 10pp →
  "**암기의 점수 기여가 작다는 방향 증거** (a≈b≈c)."
- **(iii) 그 외** → "**해석 보류 + 기록** — 사전 문장으로 덮이지 않는 패턴은
  서술하지 않고 수치만 발행 표면에 병기, 소유자 검토 이관."

**프레이밍 제약 (사전 고정)**: N=9 — **방향 증거(directional evidence)** 로만
서술한다. "인과 확인/causality confirmed" 서술 금지. 어떤 결과도 R3/R4/H 판정을
변경하지 않는다 (판정 입력이 아님 — 무분기). per-case σ≈3.2pp(E3)·L-3 비결정론
점추정 한계가 그대로 적용된다.

## 4. 불변량·예산

- 동결 결과((a)·(c)·전 발행값) 무변경 — arm (b)는 신규 병기 축.
- 예산: Phase 3 = 9호출 (누계 45→54, cap 60). 초과·낭비 정직 기록.
- 채점자(grader) 미투입 — 본 실험의 판독은 p 점수(피평가자 출력)만 사용.
