# RP-10 Phase 2.3 — 분석 전체 재현: make analysis (결정론, 네트워크 없음)
.PHONY: analysis verify
analysis:
	.venv/bin/python analysis/baselines.py
	.venv/bin/python analysis/stats.py
verify:
	.venv/bin/python tools/reproduce_analysis.py
	.venv/bin/python tools/verify_blindness.py
	.venv/bin/python tools/verify_manifest.py
	.venv/bin/python tools/lint_publication.py

# 월간 홀드아웃 재조사 (docs/MONTHLY_RITUAL.md §A) — 네트워크 fetch는 실행 시점
# 소유자 입회 승인 전제. 무인 자동화(cron 등) 금지: PROJECT.md §5-1 — 무감독
# fetch는 각 케이스 컷오프에 대한 look-ahead 누출을 조용히 만들 수 있다 (Q-E03 판례).
# egress 차단 시 fetch 매니페스트를 출력하고 정상 종료 (수기 취득 경로 포함).
SINCE ?= 2026-02-01
.PHONY: rescan
rescan:
	.venv/bin/python tools/holdout_rescan.py --since $(SINCE)

# freeze 개정 #3 스모크 (D52) — 소유자: export ANTHROPIC_API_KEY=… && make smoke
smoke:
	AAER_RAW_API_APPROVED=1 .venv/bin/python tools/smoke_rev3.py --live
smoke-dry:
	.venv/bin/python tools/smoke_rev3.py --dry-run
