대용량 원문(공시 원문, AAER PDF)은 git에 넣지 않는다.

- 저장 위치: ~/aaer-data/{ticker}/ (로컬, 절대경로)
- 이 repo에는 메타데이터(JSON)와 원문 링크만 커밋한다.
- 모든 데이터 로딩은 pipeline/cutoff_guard.py를 경유한다.
- ~/aaer-data/reference/ : EDGAR 사명·티커 전수 목록 (cik-lookup-data.txt ·
  company_tickers.json, 2026-07-10 fetch) — **가공 사명 충돌 스크린 전용**
  (D36, tools/gen_fict_names.py). 케이스 데이터 아님, 어떤 페이로드에도
  반입되지 않는다.
