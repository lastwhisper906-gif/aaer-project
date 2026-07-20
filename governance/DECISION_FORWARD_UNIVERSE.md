# governance/DECISION_FORWARD_UNIVERSE.md — forward 유니버스 결정 기록 (§4A)

> 2026-07-20, owner plan §4A. status: **owner-decided (2026-07-16, D95) —
> 신규 소유자 결정 불요.** 이 문서는 계획 §4A가 요구하는 결정 기록을,
> 이미 존재하는 소유자 서명 결정의 확인·정량화로 충족한다.

## 1. 기존 승인 규칙 검증 (§4A.1)

**forward 스크리닝에 적용 가능한 소유자 승인 유니버스 선정 규칙이 이미
존재한다.** 발명하지 않았다. 원본:

- `docs/UNIVERSE_SELECTION.md` — 사전 등록 D89 (2026-07-16, 후보 조회 전
  커밋), 소유자 서명 발효 D95 (2026-07-16): §6 확정 절 verbatim —
  "섹터 SIC 집합: **(A) 하드웨어·전력 사슬 협의** · 선정 수: **12** ·
  규모 하한: **`dei:EntityPublicFloat` ≥ $1B**."
- 원장: `scoring/decisions_log.md` D95 · 큐: `docs/OWNER_QUEUE.md` Q-O04
  RESOLVED.
- 회고용 대조군·홀드아웃 기준(`docs/CONTROL_CRITERIA_v*.md`,
  `docs/HOLDOUT_CRITERIA.md`)은 forward 규칙이 **아니다** — 백테스트 전용.

## 2. 확정 규칙 요약 (UNIVERSE_SELECTION.md §1–§3, §6 — 원문이 규범)

- **포함**: 최근 24개월 10-K ≥1 및 10-Q ≥2 (외국사 40-F/20-F 제외) ·
  SIC ∈ {3674, 3672, 3661, 3663, 3669, 3571, 3572, 3576, 3577, 3612, 3613,
  3621, 3585, 4911} · companyfacts XBRL 제출 ≥8건(그중 10-K ≥2) ·
  최근 `dei:EntityPublicFloat` ≥ $1B.
- **제외**: 트레일링 24개월 내 Item 4.02 / 공매도 리포트 대상 / AAER·집행
  → post-hoc 트랙 강등 · Cycle-1 케이스 기출 회사 (자기 오염).
- **선정**: 적격 >15면 SIC 버킷별 float 내림차순 라운드로빈으로 12개,
  동률 CIK 오름차순, 잔여는 순서 보존 대기 목록(alternates).
- **개정**: 첫 열거 후에는 FREEZE_REV + D-엔트리로만.

## 3. 정량 추정 (§4A.2 — 계획 요구 항목)

- **회사 수**: 12 확정 (적격 초과분은 alternates). 적격 풀 규모는 열거
  시점 EDGAR 실측으로 확정 — 협의 SIC 14코드 × float ≥$1B 는 대략 수십 사
  수준으로 추정되며, 정확 수치는 열거 산출물(`universe.json`의
  `candidate_count`/`excluded_by_reason`)이 기록한다.
- **피평가자 호출 수**: **회사당 1호출 × 12 = 12호출** (가정 명시: v1
  러너 패턴 — 케이스당 단일 draw, JSON 스키마 강제, k=1; 재추첨 밴드는
  백로그 P-항목이며 첫 사이클 프로토콜에 없음).
- **구독 quota**: 실측 호출당 벽시계 median 90s·max 435s (Q-E01 기록)
  → 12호출 ≈ 동시성 3에서 **약 10–30분**. Max 플랜 세션/주간 한도 대비
  무시 가능 수준 — **단일 배치, 단일 일자**로 충분. 그래도 중단 대비
  재개는 결정론: 러너 멱등(출력 파일 존재+스키마 통과 시 skip) — 재실행
  = 동일 명령, 기채점 레코드 재채점 없음.
- **통화 지출: $0** — 구독 OAuth(`claude -p` + `CLAUDE_CODE_OAUTH_TOKEN`)
  전용, INVARIANT 4 가드 강제 (`pipeline/cli_client.py`).

## 4. 주장 경계·선택 편향 함의 (§4A.2)

- 이 유니버스의 forward 결과는 **해당 유니버스 정의 안**의 Level 3 잠재
  증거일 뿐이다 (`docs/CLAIM_HIERARCHY.md`) — "미국 상장사 일반"으로
  일반화 불가 (Level 4 미지지).
- 협의 SIC 절단의 편향: 재고·장기계약·capex가 무거운 업종으로 기울며
  (선정 근거 자체), 소프트웨어·무형 중심 회계 이슈는 표본 밖.
- float ≥$1B 절단: 대형사 기울임 — 소형사 리스크 프로파일 미대표.
- 현재 상장사 열거의 생존 편향: 라이브 모니터 정의상 결함이 아니나
  (UNIVERSE_SELECTION §5), 백테스트와의 비교 서술에는 각주 의무 (Q-F08).
- 첫 사이클의 성공 기준은 **봉인 무결성(Level 0)**이지 통계적 검정력이
  아니다 — 12사는 이 기준에 적합한 소형 유니버스다.

## 5. 열거(enumeration) 상태와 권한

- D95는 열거를 "차기 소유자 감독 세션 1번 작업"으로 이관했다 (Q-E03
  선례 — 무인 네트워크 fetch의 look-ahead 위험).
- **owner plan 2026-07-20 §4.4/§8은 결정 기록·스펙 동결 후 유니버스의
  결정론적 생성을 서면 지시한다** — 야간 서면 승인 선례(Q-F05/Q-F06)와
  동일한 위임 형식. forward 유니버스 열거는 회고 케이스 컷오프를 갖지
  않으므로(스크리닝 컷오프 2026-11-15는 미래) Q-E03의 look-ahead 위험
  축이 성립하지 않는다.
- 따라서 본 세션은 스펙 동결 후 열거를 실행하고, 원시 응답을
  `data/candidates/universe/`에 보존한다 (UNIVERSE_SELECTION §5 규약).
  실행 결과·실패 여부는 `forward/cycle_001/` 산출물과 OWNER_LAUNCH_GATE에
  기록한다. **소유자 확인 후에만 모델 런이 발사된다.**

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
