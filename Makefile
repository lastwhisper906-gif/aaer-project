# RP-10 Phase 2.3 — 분석 전체 재현: make analysis (결정론, 네트워크 없음)
.PHONY: analysis verify verify-public verify-full corpus-check docs-refresh
analysis:
	.venv/bin/python analysis/baselines.py
	.venv/bin/python analysis/stats.py
verify:
	.venv/bin/python tools/reproduce_analysis.py
	.venv/bin/python tools/verify_blindness.py
	.venv/bin/python tools/verify_manifest.py
	.venv/bin/python tools/lint_publication.py

# ── 2계층 재현 인터페이스 (D108, Phase B2 — analysis/REVIEW_CLAIMS_AUDIT.md) ──
# verify-public: 외부 데이터 엄격 0 — fresh clone + 커밋 산출물만으로 통과.
#   (증거: HOME=빈 임시 디렉토리 샌드박스 실측 트랜스크립트,
#    audit/verify_public_sandbox_transcript_20260722.txt)
verify-public:
	.venv/bin/python tools/reproduce_analysis.py
	.venv/bin/python tools/lint_publication.py
	.venv/bin/python tools/lint_doc_counts.py
	.venv/bin/python -m pytest pipeline tools scoring analysis -q
	.venv/bin/python tools/verify_manifest.py --schema-only
	.venv/bin/python tools/verify_blindness.py

# verify-full: 원시 코퍼스(~/aaer-data) 의존 경로 전부 — 기준선 재계산 포함.
# 전제 조건·취득 방법은 REPRODUCING.md §2 (corpus-check가 부재 시 안내 후 실패).
verify-full: corpus-check
	.venv/bin/python analysis/baselines.py
	.venv/bin/python analysis/stats.py
	.venv/bin/python analysis/synthesis.py
	.venv/bin/python analysis/calibration_wave2.py
	.venv/bin/python tools/verify_manifest.py
	$(MAKE) verify-public

corpus-check:
	@test -d $$HOME/aaer-data || { \
	  echo "FAIL: ~/aaer-data 부재 — verify-full은 원시 XBRL/EDGAR 캐시가 필요하다."; \
	  echo "  레이아웃: ~/aaer-data/<TICKER>/xbrl/ + <TICKER>/edgar/ (data/README.md)"; \
	  echo "  규모: 디스크 ~2.3 GB (매니페스트 핀 538 파일 / ~586 MB)"; \
	  echo "  취득: tools/fetch_xbrl_facts.py + tools/fetch_primary_sources.py"; \
	  echo "        (SEC fair-access UA 필수; egress 차단 시 fetch 매니페스트 출력)"; \
	  echo "  코퍼스 없이 가능한 검증: make verify-public (외부 데이터 0)"; \
	  exit 1; }

# 문서 내 생성 블록(매니페스트 수·pytest 수·재현 명령 목록) 갱신 — B3
docs-refresh:
	.venv/bin/python tools/lint_doc_counts.py --write

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
