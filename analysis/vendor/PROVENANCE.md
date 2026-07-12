# analysis/vendor — provenance (역방향 vendoring)

screener 저장소 모듈의 문자 그대로 스냅샷. **여기서 절대 수정하지 않는다** —
수정은 원본(screener)에서만, 그 후 재수출 + 이 기록 갱신. (screener의
vendor/aaer_evals 관용구를 역방향으로 재사용 — specs/B4_short_interest.md §8.)

- **원본 저장소**: ~/Documents/screener (github 원격 소유자 생성 전, OWNER_TODO S-03)
- **원본 커밋**: `01a4331ea5c9f76bb3b20426caff1e643b22a459`
- **무결성 테스트**: analysis/test_b4_short_interest.py::test_vendor_integrity

| File | Source path in screener | sha256 |
|---|---|---|
| `short_interest.py` | `ingest/short_interest.py` | `36f7d82a4eebe2e26ca4988980a06170df3d69174a40c9fdc0b96311a5cc1767` |
