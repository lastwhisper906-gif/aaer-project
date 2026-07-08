# OWNER_QUEUE.md — 소유자 판단 대기열 (무인 세션이 append, 절대 self-resolve 안 함)

> 이 세션(2026-07-08 야간, OWNER-GATE-E 미션)은 연속 실행 모드다. 소유자 판단이
> 필요한 항목은 여기에 append하고 작업을 계속한다. 각 항목은 소유자가 한 줄로
> 결정 가능하도록 옵션·근거·기본값(default if no answer)을 명시한다.
> 형식: Q-NNN — 질문 / 옵션 / 근거 / 세션 기본 조치 / 상태.

---

## Q-E03 — E1 무인 실행 보류 (네트워크 대조군 빌드 = §5-1 look-ahead 위험) — **OPEN**

- **발견 (실행 가능성 검토)**: E1은 "채점 발사"가 아니라 **2026-era 매칭 대조군 풀을
  새로 빌드**(EDGAR SIC browse + companyfacts fetch, 네트워크)해야 한다 — `~/aaer-data`
  캐시에 홀드아웃 대조군 후보가 없다(wave-2 티커만 존재). 신규 회사의 XBRL을 무인
  fetch하면 각 사의 2026 컷오프에 대한 look-ahead 누출을 **조용히** 낼 수 있고(FPR
  오염), 이는 §5-1(post-cutoff 데이터 접근 필요 시 STOP·보고)의 정지 규칙에 해당.
- **조치**: **E1 무인 실행 보류.** 사전 등록(`HOLDOUT_CONTROLS_PLAN.md`)·순수 선정
  함수는 준비됨. 실행은 **감독 하 1회**(풀 fetch → validate → PROPOSED → 컷오프 검증
  → 채점)로 — wave-2 대조군이 RP-08/09에서 받은 것과 동일한 게이트. 수기 지명 아님.
- **옵션**: (A 기본) 감독 하 실행으로 이관 · (B) 소유자가 "무인 fetch 승인" 시 진행.
- **상태**: OPEN — E1은 P-작업·E3와 달리 네트워크·검증 의존이라 무인 부적합.

---

## Q-E01 — E2·E4·E5 미터링 스코어링의 무인 발사 여부 (spend 게이트) — **OPEN**

- **질문**: E1(+E3) 이후, E2(조기성 ~160호출)·E4(교차모델 ~20)·E5(wave-2 본채점
  재추첨 ~32) ≈ **212 호출**을 이 무인 세션이 발사할까?
- **맥락 (실측)**: 호출당 벽시계 median 90s·max 435s → 212 호출 ≈ 5–6시간+ 연속
  구독 소진. 본 백그라운드 세션이 소유자의 동일 구독 위에서 실행됨. 미션은 320
  호출을 상한으로 허용하나, 세션은 "quota 소진을 목표로 삼지 않는다"는 실행층
  판단(overrides.md OWNER-GATE-E / J14)에 따라 E1(+E3)에서 미터링을 멈추고 이
  결정을 이관한다.
- **옵션**:
  - **(A) 기본** — E2/E4/E5는 발사하지 않고 **launch-ready 상태로 동결** (사전
    등록·페이로드 빌드 완료). 소유자가 임의 시점에 `docs/RESUME.md`의 정확한
    재개 명령으로 분 단위 발사. → 익일 구독 소진 없음.
  - **(B)** E3만 추가 발사(이미 우선). 나머지는 (A).
  - **(C)** E2·E4·E5 전부 무인 발사 승인 (문자 그대로 run-to-quota, 320 상한).
    → 익일 소유자의 Claude Code 사용이 제한될 수 있음을 인지한 승인.
- **근거**: E1은 H2의 실제 구멍(대조군 분포)을 메워 호출당 가치 최고. E2는 가치
  높으나 최대 단일 spend(~160). E4는 exploratory(각주 1문단). E5는 안정성 밴드
  (최저 우선순위). → 가치/호출 곱이 E1≫E3>E2>E4≈E5.
- **세션 기본 조치 (답 없을 시)**: **(A)** — 무인 미터링을 E1(+E3, 실행 가능 시)로
  한정하고 나머지는 launch-ready 동결. 무-미터링 P-작업은 전량 계속 수행.
- **상태**: OPEN — 소유자 한 줄 회신 대기 (A/B/C).

---

## Q-E02 — wave-2 name-ID rate 발행 규약: 21.9%(동결 규칙) vs 25%(사람 판독) — **OPEN**

- **질문**: wave-2 이름 예측(name-ID) rate를 발행물에 어느 값으로 쓸까?
- **발견 (P2 synthesis)**: 동결 `name_match` 규칙 = **21.9%(7/32)**; wave2_summary.md
  산문은 **25%(8/32)**. 차이는 단일 경계 케이스 **DAR(Darling Ingredients)** — 프로브
  응답 "Darling International Inc. (now Darling Ingredients Inc.)"는 명백한 정체 인식이나
  동결 규칙이 구명(舊名) 미처리로 False 판정. (fraud는 양쪽 3/9 동일.)
- **옵션**:
  - **(A) 기본** — 동결 규칙 **21.9%**를 1차 발행값, 25%는 각주 병기(방법론:
    "동결 판정 규칙 재해석 금지", name_probes.py 헤더). synthesis.json은 이미 이 형태.
  - **(B)** 산문 25%를 유지하고 name_match 규칙을 rename-aware로 개정 후 **재동결**
    (재채점 = 프레임 변경, freeze-then-run 재실행 필요 — 비용/이력공개 대상).
  - **(C)** DAR를 "인식"으로 수기 오버라이드 계수(8/32=25%)하고 overrides.md 기록.
- **세션 기본 조치**: **(A)** — synthesis는 21.9% 1차 + 25% 병기. wave2_summary.md
  산문 25%는 **무단 수정 안 함**(재채점 금지); 본 큐 해소 시 소유자 규약대로 정합.
- **정성 불변**: 어느 값이든 name-ID 50%→~22–25%→0% 반감 서사·R4 결론 불변.
- **상태**: OPEN.

---

## Q-E04 — 무인 실행 환경에 PIT 캐시(`~/aaer-data`) 부재 → 미터링 플랜 전량 실행 불가 — **OPEN**

- **발견 (2026-07-08 야간 OWNER-GATE-E 재개 세션, 전 사전점검 단계)**: 이 세션은
  신규 임시(ephemeral) 컨테이너에서 저장소만 fresh clone된 상태로 시작됐다. 그런데
  미터링 플랜의 **모든** 유닛(E2 조기성·E5 본채점 재추첨 draw-2/3·E4 교차모델)은
  피평가자 페이로드 생성을 위해 `pipeline/build_payload.load_pit_series` →
  `~/aaer-data/{ticker}/xbrl` 로컬 SEC companyfacts 캐시를 읽는다. **이 컨테이너에
  `/root/aaer-data`가 존재하지 않는다** (git 밖 자산, `data/README.md` 규약대로
  미커밋; `data/manifests/aaer_data_manifest.json` = 402파일 372MB 외부 SEC 데이터).
  실측: `build_payload.build_payload(cases_wave2[0])` → `FileNotFoundError:
  /root/aaer-data/ADAM/xbrl: companyfacts 없음` — **API 호출 이전에** 실패. 즉 어떤
  피평가자/채점자 호출도 발생 불가. **미터링 0 소비 (누계 18/320 불변).**
- **왜 무인 자가복구 안 함**: 캐시 재생성 = `tools/fetch_xbrl_facts.py` +
  `fetch_primary_sources.py`로 data.sec.gov에서 402파일 네트워크 fetch. 이는 미션의
  최상위 금지("신규 회사 데이터를 네트워크로 fetch해야 하면 STOP·기록·이동 —
  single most important don't")·§5-1 look-ahead 정지 규칙에 정면으로 해당한다.
  추가로, 지금(2026-07) 재fetch한 companyfacts는 정정(restatement)·수정으로 **동결
  매니페스트 sha256과 불일치**할 수 있어 PIT 재구성의 바이트 동일성을 보장 못 한다
  (재현성 오염 위험). → 무인 fetch 부적합, E1/홀드아웃과 동급 감독 대상.
- **부수 관측(환경, 미조치)**: 이 clone은 **shallow**(50커밋, `.git/shallow`)라
  `tools/verify_blindness.py`의 채점커밋 `03b91aa` git-이력 검사가 로컬에서 오브젝트
  부재로 중단된다 — **블라인드 위반 아님**(80ad1df에서 CI green으로 통과). 순수
  환경 아티팩트. `reproduce_analysis`(100/100)·`lint_publication` 로컬 PASS.
- **옵션**:
  - **(A 기본)** 이 무인 세션에서 미터링 플랜 전량 **미실행 동결**. 네트워크 fetch
    안 함. 캐시 복원(신뢰 캐시를 `~/aaer-data`에 재배치, 또는 매니페스트 대조 하
    감독 fetch)이 된 **감독 세션**에서 `docs/RESUME.md`의 재개 명령대로 발사.
  - **(B)** 소유자가 신뢰 `~/aaer-data` 스냅샷(동결 매니페스트 sha256 일치)을 컨테이너에
    제공 → 그때 E5/E4는 기존 러너 재사용으로 즉시 launch-ready, E2는 조기성 하네스
    구현이 선행 필요(아래 Q-E05).
  - **(C)** 소유자가 명시적으로 "감독 하 재fetch 승인" — 매니페스트 sha256 대조 +
    컷오프 재검증을 통과분만 채용. (무인 아님.)
- **세션 기본 조치 (답 없을 시)**: **(A)** — 미터링 0, 네트워크 fetch 0, 프로즌 불침해,
  전 유닛 동결 이관. 본 세션은 여기서 clean stop.
- **상태**: OPEN — 환경 precondition 미충족. 소유자/감독 세션 사안.

---

## Q-E05 — E2 조기성 하네스가 **미구현**(설계만) — 발사 전 구현+오프라인 검증 필요 — **OPEN**

- **발견**: 미션은 E2(조기성)를 "launch-ready"로 기술하나, E5/E4와 달리 E2는 기존
  러너로 바로 못 돈다. 스냅샷 그리드(스냅샷 j 컷오프 = 컷오프 이전 j번째 최신
  10-K/10-Q filed일 +1일) 생성기 + 스냅샷별 케이스 파일 + 스냅샷별 cutoff_guard
  "allowed" 기록 통합이 **존재하지 않는다**. `docs/EARLINESS_DESIGN.md` §5는 이를
  명시적으로 "설계만, 실행 없음"으로 두고, 실행 전 소유자 결정 3건을 열거했다(그
  3건은 `analysis/EARLINESS_PLAN.md`가 사전등록으로 이미 해소: 교란만·k=1·RP-01 8).
  즉 **사전등록(기준)은 완료, 구현(코드)은 미완**. Q-E04로 어차피 이번 세션 실행 불가.
- **look-ahead 성격**: E2는 E1과 달리 **데이터가 이미 캐시(로컬)**이고 스냅샷 컷오프는
  결정론적 날짜 계산이라 **오프라인·0-미터링으로 기계 검증 가능**(각 스냅샷
  load_pit_series 반환에 filed>컷오프 항목 0 + 스냅샷 컷오프 ≤ 폭로 컷오프를
  test_build_payload 패턴으로 강제). 따라서 E1-급 금지 대상은 아니나, **신규 하네스를
  무인·무검토로 짜서 예산 절반(~160호출)을 그 산출에 쓰는 것**은 부적합.
- **옵션**: (A 기본) 감독 세션에서 하네스 구현 → 오프라인 컷오프 검증 CI green →
  그 후 발사. (B) 소유자가 "무인 구현+airtight 오프라인 검증 후 발사" 승인.
- **세션 기본 조치**: **(A)** — 구현/발사 모두 이관. 본 세션 미착수(Q-E04로 무의미).
- **갱신 (무인 재개 세션 #2, 소유자 "keep going / 권한 최종" 지시 반영)**:
  하네스를 **오프라인·0-미터링으로 구현·검증 완료**(발사는 미착수, 여전히 owner-gate):
  - `pipeline/earliness_grid.py` — look-ahead-critical 스냅샷 그리드 순수 함수 + G1(폭로
    상한)/G2(인접 제출 누출)/G3(중복일) 가드. `test_earliness_grid` 10건 CI 상주(캐시 불요).
  - `pipeline/build_payload.py` — base_id 시드(스냅샷 간 동일 교란 k·정체), 하위호환.
    `test_build_payload_base_id` 4건.
  - `tools/build_earliness_snapshots.py` — 적격 선정(데이터드리븐 21=fraud13+control8) +
    그리드 + 스냅샷별 cutoff_guard 경계검사(≤폭로, fail-closed). `--plan` 캐시 불요.
    `test_build_earliness_snapshots` 5건(합성 EDGAR 픽스처).
  - `docs/EARLINESS_RUNBOOK.md` — 발사 절차(캐시 복원 + `EARLINESS-LAUNCH: YES` 게이트 +
    160 cap 균일절단 + 스냅샷0 재사용 + verify_blindness/commit/CI 규율).
  - 검증: 전체 91 passed 4 skipped(캐시), reproduce 100/100, lint PASS.
  - **잔여(감독)**: (i) 캐시 복원(Q-E04) → `--emit`로 그리드/가드 실측·감사, (ii) 소유자
    `EARLINESS-LAUNCH: YES` → runner.py 발사(~≤160). **구현 검토(diff)는 소유자 서명 대상.**
- **상태**: OPEN(구현·검증 완료, 발사 owner-gate 대기 — 권한 최종).

---
