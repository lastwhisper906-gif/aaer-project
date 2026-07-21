# ROBUSTNESS_INVENTORY.md — 견고성 인벤토리 (Phase C6, D109 — 감사 전용)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-22 야간.
> 외부 검토 약점 5 대응 — **감사만, 대량 리팩터 없음**. 수리 기준(프롬프트
> 명령): live(비동결) 코드 **이면서** 기존 테스트가 덮는 항목만 즉시 수리,
> 나머지는 큐. 판정 어휘: [leave frozen / config-inject in live code / fix now].
> 동결(frozen) = 발행 수치를 생산했거나 그 재현 경로에 있는 코드 — 동작
> 변경은 재현 주장을 깬다. live = forward·월간 재조사·신규 승인 경로.

## 결론 요약

- **fix now = 0건.** 전수 검토 결과, "live + 기존 테스트 커버 + 실제 결함"
  세 조건을 동시에 만족하는 항목이 없다 — 광역 except는 대부분 provenance/
  exclusion 기록을 남기는 fail-closed-with-record 패턴이고(침묵 삼킴은 동결
  v1 legacy에만 잔존), 경로 하드코드의 live 소비자(cutoff_guard·memo_extract)
  는 이미 파라미터/플래그 주입이 가능하다.
- 큐 이관: config-inject 권고 5건 (아래 표시) — `docs/OWNER_QUEUE.md` Q-O12.

## (i) 광역 `except Exception` (return-None 계열)

| 위치 | 동작 | 동결/live | 권고 |
|---|---|---|---|
| `analysis/legacy/wave2_analyze_v1.py:81` | `except Exception: continue` — **침묵 삼킴** (검토가 지적한 원형) | **동결** (v1 바이트 보존 — E-001/E-002가 그 결함의 공개 기록) | leave frozen |
| `analysis/wave2_analyze.py:206` | run_case 실패 → 유형·메시지를 exclusions에 기록 후 continue (rev2 교정형) | live (rev2 분석, test_synthesis_integrity 계열 커버) | leave — 이미 기록형. 예외 클래스 협소화는 Q-O12 |
| `analysis/synthesis.py:43` (baseline_mf) | 4종 유형별 분류 기록 (T05 rev2에서 typed로 교정 완료) | 동결 재현 경로 | leave frozen |
| `tools/control_screening.py:83` | fetch 실패 → `(None, None, False)` — False 플래그로 결측 표시 | **동결** (RP-08 대조군 풀 생산 코드) | leave frozen |
| `tools/control_screening.py:136,150` · `tools/fetch_control_pool_rp08.py:123,191,244` · `tools/control_v2.py:201,240` | 오류 문자열 기록 후 continue (provenance 규약) | 동결 (풀 생산) | leave frozen |
| `tools/fetch_primary_sources.py:89,106,161,174` · `tools/fetch_xbrl_facts.py:37` | print + failures 목록 적재, 종료 시 보고 — 침묵 없음 | live (코퍼스 재구성 도구) | leave — 이미 보고형 |
| `tools/forward_enumerate.py:47` | 결측 provenance 기록 + `.missing` 마커 파일 (fail-closed) | live (forward, test_forward_tools 커버) | leave — 이미 기록형 |
| `tools/holdout_rescan.py:91` | "egress 차단 포함 — 조용히 실패 금지" 주석대로 기록 | live (월간 재조사) | leave |
| `tools/validate_schemas.py:57` · `tools/prelaunch_check_rp10.py:54` | failures 적재 → 최종 exit 1 (fail-closed) | live (CI 게이트) | leave |

## (ii) `Path.home()` / `~/aaer-data` 하드코드

| 위치 | 동결/live | 권고 |
|---|---|---|
| `scoring/baselines/screens.py:28` (`DATA_DIR`) | **동결** (기준선 생산 — B2에서 full 계층으로 문서화) | leave frozen |
| `pipeline/cutoff_guard.py:26,122` (`DEFAULT_EDGAR_DATA`) | 공유 모듈 — 단 `load_xbrl_facts/load_edgar_chronology/load_document` 전부 `data_dir=` 키워드 주입 가능 (170,217,249행) | leave — 이미 config-inject 가능; 122행 `corpus` 상수화만 Q-O12 |
| `tools/memo_extract.py:103` | live (승인 후계 파이프라인) — `--raw-root` 플래그 기본값 | leave — 이미 주입 가능 |
| `tools/verify_manifest.py` (root `~/aaer-data`) | live 게이트 — 단 root는 매니페스트 계약의 일부 (`"root": "~/aaer-data"` 필드) | config-inject (env 오버라이드) — Q-O12 |
| `tools/dissemination_schedules.py:42,44` · `tools/fetch_short_interest.py:25` | live (B4 계열 수집) | config-inject — Q-O12 |
| `tools/run_control_baselines.py:17` · `tools/run_control_v2_scoring.py:39,40` · `tools/select_control_group_rp08.py` · `tools/rp08_common.py:16` · `tools/fetch_control_pool_rp08.py:147` · `tools/control_v2.py:141` | 동결 (풀·기준선 생산) | leave frozen |
| `tools/blind_memo_extract.py:29` · `tools/gen_fict_names.py:19` | 동결 (OUT-GIL-V1 원본 · 가공명 생산) | leave frozen |
| `tools/compute_edgar_fields.py:24` | live-주변 (payload 보조) | config-inject — Q-O12 |

## (iii) `sys.path.insert`

전수 40건 (conftest.py:3 + pipeline 1 + tools 33 + analysis 5). 일괄 판정:

- `conftest.py:3` — **정본 해법** (macOS 은닉 .pth 재발 사고의 항구 대책;
  메모리 기록 macos-hidden-pth). leave.
- 나머지 전부 — 스크립트 모드 형제(sibling) import 규약. T09 v3가 이
  규약을 **표준으로 확정**했다 (`from pipeline import cutoff_guard`가 아니라
  `import cutoff_guard` — 소유자 승인 v2 잔여 수정 (1)/(2)). 규약을 뒤집는
  리팩터는 동결 호출자(script-mode frozen callers)를 깨는 방향이라 검토
  약점 5의 취지(견고성)와 반대. **전건 leave** — 신규 파일은 conftest 주입
  + 형제 import 규약을 따른다 (규약 문서화만 Q-O12에 포함).

## 한정

본 인벤토리는 grep 3패턴의 전수 나열이며 동작 변경 0. 수리 후보의 실행은
Q-O12 서명 후 별도 커밋. 본 결과는 Claude 기반 단일 파이프라인에 한정.
