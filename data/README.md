대용량 원문(공시 원문, AAER PDF)은 git에 넣지 않는다.

- 저장 위치: ~/aaer-data/{ticker}/ (로컬, 절대경로)
- 이 repo에는 메타데이터(JSON)와 원문 링크만 커밋한다.
- 모든 데이터 로딩은 pipeline/cutoff_guard.py를 경유한다.
