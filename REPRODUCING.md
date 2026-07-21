# REPRODUCING.md — 제3자 재현 가이드

> Authored by Claude Code, pending human audit (GA-001 (b)).
> 2026-07-22 재작성 (Phase B2, D108): 재현 인터페이스를 `make verify-public` /
> `make verify-full` 2계층으로 고정. 계층 배정 기준 = **실제 코드 동작**
> (감사: `analysis/REVIEW_CLAIMS_AUDIT.md`). 종전 명령·시점값 수기 표는
> git 이력에 보존.
> 목적(G2 공공재): 독자가 발행 수치를 **커밋 산출물만으로** 재계산·재검증할 수
> 있게 하는 것.

## 0. 두 명령이 전부다

| 명령 | 외부 데이터 | 내용 |
|---|---|---|
| `make verify-public` | **엄격 0** | 발행 수치 전건 재계산 + 발행 정합 lint + 문서-수치 lint + 전체 pytest + 매니페스트 스키마 정합 + 채점 선행 이력·카나리 증명 |
| `make verify-full` | `~/aaer-data` 필요 | 위 전부 + 결정론 기준선 재계산(baselines·stats·synthesis·calibration) + 원문 코퍼스 sha256 전수 대조 |

`verify-public`의 "외부 데이터 0" 주장은 **HOME을 빈 임시 디렉토리로 돌린
샌드박스에서 실측**해 증명한다 — 트랜스크립트:
`audit/verify_public_sandbox_transcript_20260722.txt`. 코퍼스 의존 pytest
케이스는 코퍼스 부재 시 skip으로 표시된다 (synthetic tier는 전건 실행).

수치·명령 목록은 저장소에서 유도되는 생성 블록이다 (`make docs-refresh`로
갱신, CI가 `tools/lint_doc_counts.py`로 대조):

<!-- BEGIN-GENERATED: repro-facts (refresh: make docs-refresh; CI: tools/lint_doc_counts.py) -->
- data manifest: **538 files** (`data/manifests/aaer_data_manifest.json` · `file_count`)
- pytest: **275 tests collected** (`pipeline tools scoring analysis`)
- `make verify-public` (zero external data):
  - `.venv/bin/python tools/reproduce_analysis.py`
  - `.venv/bin/python tools/lint_publication.py`
  - `.venv/bin/python tools/lint_doc_counts.py`
  - `.venv/bin/python -m pytest pipeline tools scoring analysis -q`
  - `.venv/bin/python tools/verify_manifest.py --schema-only`
  - `.venv/bin/python tools/verify_blindness.py`
- `make verify-full` (requires `~/aaer-data` corpus; see REPRODUCING.md §2):
  - `.venv/bin/python analysis/baselines.py`
  - `.venv/bin/python analysis/stats.py`
  - `.venv/bin/python analysis/synthesis.py`
  - `.venv/bin/python analysis/calibration_wave2.py`
  - `.venv/bin/python tools/verify_manifest.py`
  - `$(MAKE) verify-public`
<!-- END-GENERATED: repro-facts -->

## 1. 1계층 — 완전 포터블 (`make verify-public`, 누구나)

```bash
git clone <repo> && cd aaer-evals
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
make verify-public
```

발행 헤드라인 수치의 재검증은 여기서 끝난다 — **원문 코퍼스 없이** 가능
(검증 가능성의 1차 방어선, PROJECT.md §6-5). CI가 매 push 동일 게이트를
실행한다.

## 2. 2계층 — 코퍼스 의존 전체 경로 (`make verify-full`)

전제 조건 (`corpus-check`가 부재 시 아래 안내를 출력하고 실패):

- **레이아웃**: `~/aaer-data/<TICKER>/xbrl/`(data.sec.gov companyfacts) +
  `<TICKER>/edgar/`(submissions) — 상세 규약 `data/README.md`. git 밖 절대경로.
- **규모**: 디스크 약 2.3 GB (매니페스트 핀 대상은 생성 블록의 파일 수 /
  약 586 MB).
- **취득**: 아래 §3의 fetch 도구 2종 (SEC fair-access User-Agent 필수).
  SEC egress가 막힌 환경이면 도구가 **fetch 매니페스트(필요 URL 목록)**를
  출력하므로 별도 취득 후 배치, 또는 요청 시 제공.

`analysis/synthesis.py`는 이 계층이다 — `scoring/baselines/screens.run_case`를
호출해 Beneish M / Dechow F 기준선을 원시 XBRL에서 **재계산**한다
(`screens.py`의 `DATA_DIR = ~/aaer-data`). 로직은 1계층 재검증 대상 수치를
생산한 동결 코드 그대로다.

```bash
make verify-full   # corpus-check → baselines·stats·synthesis·calibration → 전체 매니페스트 → verify-public
```

## 3. 원시 XBRL 캐시 재구성 (외부 재현자용)

```bash
# CIK별 companyfacts (scoring-side 수집; SEC fair-access UA 필수)
.venv/bin/python tools/fetch_xbrl_facts.py       # 케이스·대조군 CIK companyfacts
.venv/bin/python tools/fetch_primary_sources.py  # submissions/제출 이력
```

provenance는 `runs/*/control_pool_raw/provenance.jsonl` 규약 승계.

## 4. 파이프라인 재실행 (피평가자 채점 — 구독 필요, 재현 선택)

발행 수치 재검증에는 **불필요**(§1로 충분). 채점 자체를 재실행하려면 구독
OAuth(`claude` CLI) 필요, `ANTHROPIC_API_KEY` 부재 assert (zero-metered
명령, D102). 예: E3 재추첨 재현 — `python pipeline/runner.py --cases
data/evaluatee/cases_wave2.json --perturbed --out
runs/wave2/perturbed_redraw/draw_2 --only <9 fraud ids>`
(멱등·핀검증·레이트리밋 재개).

## 5. 월간 홀드아웃 재조사 (`tools/holdout_rescan.py`)

컷오프 후 신규 폭로(8-K Item 4.02)를 한 명령으로 누적 —
`docs/FUTURE_HOLDOUT_CANDIDATES.md` Tier-2를 채우는 절차. §3와 동일한 SEC
fair-access UA, egress 차단 시 fetch 매니페스트 출력.

## 6. 면책

단일 Claude 파이프라인 한정. 발행 수치의 재검증은 커밋 산출물만으로
가능(검증 가능성 = 최선의 방어, §6-5). 채점 재실행은 하네스 매개라 원시
API와 다를 수 있다(L-2).
