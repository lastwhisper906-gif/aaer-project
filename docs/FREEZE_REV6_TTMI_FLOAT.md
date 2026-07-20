# FREEZE_REV6_TTMI_FLOAT.md — freeze 개정 #6: TTMI float 단위 이상(원자료 결함)의 기록

> 2026-07-20 작성. status: **ACKNOWLEDGED (owner, 2026-07-20).** 발효는 아래 서명란으로만. **이것은 데이터 수정이 아니라 알려진
> 데이터 결함의 문서화다** — 원 제출값은 스냅샷에 무변경 보존된다.
> **본 엔트리는 cycle_001의 어떤 모델 점수도 존재하기 전에 기록되었다**
> (2026-07-20 실측: `forward/cycle_001/scores.json` 부재).

## 1. 이상 원문 (verbatim)

- 태그: `dei:EntityPublicFloat` (taxonomy `dei`), 단위 `USD`.
- 제출값: **`4165937635000`** (≈ **$4.166조**), `float_asof: 2025-06-30`,
  entityName `TTM TECHNOLOGIES INC`, CIK `0001116942`, 티커 TTMI,
  `universe.json` record `fw001-r11` (selection_rank 11).
- 개연적 의도값: **≈ $4.166B** (~×1000 과대 — 시계열이 일관되게 같은
  배율로 어긋남; OWNER_LAUNCH_GATE §1: "XBRL 원문이 일관되게 ~×1000
  과대"). 참고: 동사의 실제 시장 규모상 $4.17조 float는 물리적으로
  불가능하다.

## 2. 판정 무영향 확인

- $1B 하한 판정: **어느 읽기로도 통과** — 제출값 $4.166T ≥ $1B,
  의도값 추정 $4.166B ≥ $1B. **TTMI의 포함은 이 이상에 영향받지 않는다.**
- 버킷 내 순위(3672, float 내림차순)에 대한 영향은 제출값 기준으로
  기계 계산된 그대로다 — 규칙은 "XBRL 기계 판독"을 명시하므로
  (`UNIVERSE_SELECTION.md` §1-4) 제출값 사용이 규칙 준수다.

## 3. 무엇을 하지 않는가

- **원자료 무수정**: `data/candidates/universe/float_CIK0001116942.json`
  (EDGAR companyfacts 원문 스냅샷)과 `universe.json`의 `float_usd`는
  제출값 그대로 보존한다. 소스 데이터 정정 금지 — 정직 각주만.
- 발행 산출물에서 TTMI float를 인용할 일이 있으면 본 문서를 각주로
  단다 (제출값·개연 의도값 병기).

## 4. 서명란 (한 줄 — 발효)

아래 `PENDING`을 `ACKNOWLEDGED`로 바꾸고 날짜를 기입하면 발효한다:

```
FREEZE_REV6: ACKNOWLEDGED   (owner, 2026-07-20, this session's structured decision responses)
```

- 전제 재확인: **cycle_001 모델 점수 부재 상태에서 기록·서명됨.**
- 서명 후: D-엔트리를 `scoring/decisions_log.md`에 추가 (다음 D-번호,
  본 문서 참조).
