# Review Packet 04 — 과금 경로 감사 (본 실행 전 게이트, 읽기 전용)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 실행 일시: 2026-07-06 / Claude Code 버전: 2.1.201 / 감사 모드: 읽기 전용
> (설정 무수정 — 권고만). 시크릿 값은 어디에도 출력·기록하지 않음.

## 판정표

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | 환경변수 (셸 + 영속 소스) | **PASS** | ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / CLAUDE_CODE_OAUTH_TOKEN / ANTHROPIC_BASE_URL / CLAUDE_CONFIG_DIR 전부 UNSET. ~/.zshrc·~/.zprofile clean, 나머지 rc 파일 부재. 홈·리포에 .env/.envrc 없음. crontab 관련 항목 없음. LaunchAgents 3종(Google/Grammarly)에 ANTHROPIC 주입 없음 |
| 2 | 크레덴셜 저장소 | **PASS** | ~/.claude/.credentials.json 부재 = macOS 키체인 저장(정상). 키체인 "Claude Code-credentials" (acct: chaeryeollee): `claudeAiOauth` 존재, **subscriptionType = max**, rateLimitTier = default_claude_max_20x, scopes에 user:inference 포함. 값 미출력 |
| 3 | 설정 파일 우회 경로 | **PASS** | ~/.claude/settings.json: apiKeyHelper 없음, env 블록 ANTHROPIC 주입 없음. 리포 .claude/settings.json·settings.local.json·.mcp.json 부재 |
| 4 | 이중 설치 | **WARN** | Claude Desktop(/Applications/Claude.app) + standalone CLI(/opt/homebrew/bin/claude, 2.1.201) 공존 — 크레덴셜 저장소 공유로 구독 로그인이 API 과금으로 오분류된 사례가 보고된 조합. 현재 오분류 징후는 없음(항목 2가 구독 OAuth로 확인) — 인간 확인 A(/status 육안)로 최종 판별 |
| 5 | 러너 코드 정합 | **PASS (관찰 1건)** | pipeline/·scoring/·tools/ 코드에 ANTHROPIC_API_KEY·api_key 참조 0건. 러너는 `anthropic.Anthropic()` 무인자 생성 — 현 환경(항목 1)에서는 종량 과금 자격 증명을 발견할 수 없어 조용한 API 과금이 **구조적으로 불가능**한 상태 |

## 관찰 (판정 외 — 정합성 메모)

1. **문서 잔존 2건**: `docs/execution_runbook.md:5`, `docs/HANDOFF.md:18`이
   `export ANTHROPIC_API_KEY=...`를 재개 절차로 안내 — 코드가 아니라 문서이나,
   구독 전용 실행 방침과 모순. 아래 권고 R1.
2. **"개정 #2" 기록 부재**: 감사 지시문은 "개정 #2 이후 구독 경로만"을 전제하나,
   저장소의 decisions_log/run_log에는 freeze 개정 #1(체크리스트)까지만 기록됨.
   구독 헤드리스 실행 방식(예: Claude Code 세션 경유 러너 구동)이 결정이라면
   §5-6 규약상 로그된 개정으로 남겨야 함. 아래 권고 R2.
3. 러너의 SDK 자격 증명 해석 순서상, 키체인의 Claude Code OAuth는 Python SDK가
   직접 소비하는 경로가 아님 — 구독 실행은 Claude Code CLI 경유(headless `claude -p`
   등)를 의미하게 됨. 실행 형태 확정은 R2와 함께 인간 결정 사항.

## 권고 (인간이 직접 실행 — 이 세션은 무수정)

- **R1 (문서 정정)**: 아래 두 파일에서 API 키 안내를 구독 경로 안내로 교체:
  `docs/execution_runbook.md` 5행, `docs/HANDOFF.md` 18행.
  (FAIL 아님 — 문서이므로 실행 전 정정이면 충분.)
- **R2 (개정 기록)**: 구독 전용 실행 결정을 decisions_log에 "freeze 개정 #2"로
  기입 (실행 형태·러너 구동 방법 명시). 기록 전 본 실행 착수 비권장.
- 수정 명령 예시는 없음 — 제거할 키·설정이 발견되지 않았다.

## 감사 후 인간 확인 항목 (에이전트 대행 불가)

- **A.** 대화형 세션에서 `/status` → Auth가 구독 OAuth(Claude Max)인지 육안 확인
  (WARN 항목 4의 최종 판별).
- **B.** claude.ai 설정의 Usage credits 토글 OFF 유지 재확인.
- **C.** 파일럿 실행 직후 Console 사용량 대시보드 $0.00 유지 확인.

**게이트 판단은 인간이 한다** — 본 감사는 판정표 1~5 전 항목에서 종량 과금 경로가
닫혀 있음을 확인했고(WARN 1건은 A로 판별), R1/R2 정리 후 A~C 확인이 남은 조건이다.
