# OWNER_LAUNCH_GATE.md — cycle_001 발사 게이트 (유일한 소유자 승인 문서)

> 2026-07-20 작성 (D100). **이 문서의 소유자 승인 없이는 어떤 모델 런도
> 발사되지 않는다.** 규범: `specs/FORWARD_WATCHLIST_V1.md` ·
> `governance/DECISION_FORWARD_UNIVERSE.md`.

## 1. 동결 유니버스

- **12사** (열거 T₀=2026-07-20, `universe.json` sha256
  `95eea6ec31f056e45f7b084ead51ace8764060ab12d269a306cd7c25c7b4aaee`):
  AAPL(3571) · STX(3572) · CSCO(3576) · PANW(3577) · CARR(3585) ·
  LFUS(3613) · GNRC(3621) · CIEN(3661) · QCOM(3663) · ESE(3669) ·
  TTMI(3672) · NVDA(3674). 대기 목록 103사 순서 고정 (1순위 NEE/4911).
- 후보 2,510 · 제외: form_requirement 1,993 / foreign 221 / float<$1B 124 /
  4.02 오염 12 / XBRL 이력 7 / Cycle-1 기출 3 / 결측 35.
- 결정론 재검증: `python tools/forward_enumerate.py --offline` (스냅샷
  `data/candidates/universe/`, SNAPSHOT_MANIFEST.sha256 핀).

### 소유자 인지 필요 2건 (승인 전 확인)

1. **4911(전력 유틸리티) 무배정**: 비어있지 않은 SIC 버킷 13개 > 슬롯 12
   — SIC 오름차순 라운드로빈의 기계적 결과로 4911 최상위(NEE)가 13번째
   = 1순위 대기. 규칙 유지(기본) 또는 FREEZE_REV+D-엔트리로 배정 규칙
   개정 중 택일. **개정은 점수 생성 전에만 가능.**
2. **TTMI float 스케일 이상**: XBRL 원문이 일관되게 ~×1000 과대
   (4.166e12로 제출 — 실제 ≈ $4.2B). $1B 하한 판정에는 무영향 (실제값도
   상회), 기계 규칙은 제출값 그대로 기록. 정직 각주로만 등재.

## 2. 모델·실행 경로 (통화 지출 $0 확약)

- 모델 핀: `claude-sonnet-5` (`pipeline/runner.py::EVALUATEE_MODEL` —
  11월 실행 시점 재확인, 변경 시 PROTOCOL 버전 증분).
- **구독 OAuth 전용**: `claude -p` + `CLAUDE_CODE_OAUTH_TOKEN`
  (`pipeline/cli_client.py`). 종량 자격증명(ANTHROPIC_API_KEY 등)이
  환경에 있으면 러너·forward 도구가 기동 거부 (INVARIANT 4 +
  `forward_common.assert_subscription_only` — 테스트로 검증됨).
- **미터링 과금 필요·허용 없음. 예상 통화 지출: $0** (GitHub free ·
  EDGAR 공개 데이터 · OpenTimestamps 무료).

## 3. 호출 수·quota 계획

- **예상 피평가자 호출: 12** (회사당 1, k=1 draw). 재시도 상한 포함
  최악 36. 채점자 호출 0 (채점 없음 — 워치리스트 봉인만).
- 벽시계: 호출당 median 90s·max 435s (실측) → 동시성 3에서 **약 6–30분**.
- Max 플랜 한도 대비: 12호출은 세션·주간 한도의 무시 가능 비율 — **1일
  1배치**, 분할 불요. 중단(레이트 리밋 exit 3) 시 재개 = **동일 명령
  재실행** (출력 파일 존재+스키마 통과 케이스 자동 skip — 기채점 재채점
  없음, 결정론).

## 4. 실행 창 절차 (2026-11-15 ~ 11-22 — 순서 고정)

```bash
# (0) 사전: 병행 작성자 검사 + 5게이트 green + Q-O08 확인
# (1) 유니버스 신선도 재확인 — 신규 4.02 오염 시 §2 규칙 인용 + alternates 승격
python tools/forward_enumerate.py --offline   # 동결본 재계산 일치 확인
# (2) 입력 수집 (컷오프 가드 경유; retrieval/filing 분리 기록)
#     12사 각: tools/fetch_xbrl_facts.py 경로로 ~/aaer-data 캐시 +
#     forward/cycle_001/source_manifest.json 작성 (스키마: forward_validate 참조)
# (3) 케이스 빌드: data/evaluatee/cases_forward_001.json
#     (case_id = record_id, cutoff_date = 2026-11-15, 정체 가시 프레임)
#     — 빌드 스크립트는 tools/build_evaluatee_inputs.py 파라미터화, 커밋 후 실행
# (4) 발사 (소유자 승인 후):
python pipeline/runner.py --cases data/evaluatee/cases_forward_001.json \
    --out runs/forward/cycle_001
# (5) 조립·검증·봉인:
python tools/forward_assemble.py --cycle forward/cycle_001 --runs runs/forward/cycle_001
python tools/forward_validate.py --cycle forward/cycle_001
python tools/forward_seal.py --cycle forward/cycle_001
# (6) 봉인 직후 (외부 타임스탬프 — 즉시):
git add forward/cycle_001 && git commit -m "SEAL: cycle_001 forward watchlist"
git tag -a forward-cycle-001-seal -m "forward seal"
git push origin main --tags
pip install opentimestamps-client   # (ots 부재 시 1회, 무료)
ots stamp forward/cycle_001/MANIFEST.sha256
git add forward/cycle_001/MANIFEST.sha256.ots && git commit -m "SEAL: OTS anchor" && git push
# (7) 사후 검증:
python tools/forward_verify_seal.py --cycle forward/cycle_001
```

## 5. 정지 조건 (spec §3 — 즉흥 대응 금지)

- 창 내 완료 불가 → cycle_001 `aborted` 마감 + cycle_002 신규 (조용한
  연장 금지).
- 채점 완료 <11/12 → 봉인 금지 (abort 규칙).
- 소스 컷오프 검증 실패 → STOP·기록 (대체 소스 즉흥 투입 금지).
- 종량 자격증명 감지 → 자동 기동 거부.

## 6. 소유자 체크리스트 (발사 승인 = 아래 전부 확인)

- [ ] §1 인지 2건 (4911 라운드로빈 · TTMI 스케일) 확인 — 규칙 유지 또는
      FREEZE_REV 지시
- [ ] Q-O08 (zero-metered vs FREEZE_REV3) 해석 확인 (기본: REV3 무기 정지)
- [ ] screener S-01/S-03 완료 (seal 앵커 사슬 전제 — OWNER_QUEUE 2)
- [ ] 11월 실행 창에서 위 §4 절차 승인 · 발사

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
포지션 없음 · 교육·정보 목적 · 워치리스트는 위법 주장이 아니다.*
