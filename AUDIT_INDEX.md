# AUDIT_INDEX.md — 감사 식별자 안내 + 원장 지도 + 실제 추적 예제

> Authored by Claude Code, pending human audit (GA-001 (b)). 외부 독자용:
> 이 저장소의 결정·검토·동결 식별자가 무엇이고 어디 사는지, 그리고 실제
> 해소된 결정 하나를 끝까지 따라가는 예제.

## 1. 식별자 체계

| 접두 | 의미 | 원장(사는 곳) |
|---|---|---|
| **D-NNN** | 결정(Decision) 원장 항목 — 모든 실행·서명·스코프 변경의 단위 기록. JSON 1줄 + 학습 노트 | `scoring/decisions_log.md` |
| **Q-XNN** | 소유자 판단 대기열 항목 (E=실험, F=발견, M=기타, O=서명 게이트, R=검토발) — 옵션/근거/기본값 형식, 세션은 절대 self-resolve 안 함 | `docs/OWNER_QUEUE.md` |
| **RP-NN** | 검토 패킷(Review Packet) — 비동기 소유자 검토용 완결 문서 (diff·게시 텍스트·판독 포함) | `review_packets/` (진입점 `INDEX.md`) |
| **FREEZE_REV N** | 동결 개정 — 사전 고정된 프로토콜·핀의 명시적 개정 (개정 커밋이 재실행보다 앞서야 유효) | `docs/FREEZE_REV*.md` |
| **GA-NNN** | 거버넌스 수정(Governance Amendment) 원문 | `scoring/overrides.md` |
| **E-NNN** | 정오표(Errata) — 발행 후 발견된 결함의 공개 기록 | `ERRATA.md` |
| **L-N / J-NN** | 방법론 한계 / 분석 재량 판단 기록 | `docs/methodology_limitations.md` · RP-05 §9 |
| **R1–R4 / H1–H3** | 사전 커밋된 결론 발동 규칙 (wave / holdout) | `analysis/*_PLAN.md` (freeze-commit-then-run) |

읽는 순서(거버넌스 지도): `PROJECT.md` → `scoring/decisions_log.md` →
`scoring/overrides.md` → `review_packets/INDEX.md` → 게시 이슈 동결 원문
`analysis/ISSUE_*_DRAFT.md`.

## 2. 실제 예제 — B3 임계 비대칭 발견이 발행 승인까지 간 길

wave-1과 wave-2 사이 B3 귀속비의 비대칭(0.8947 vs 0.1468)이 발견되어
공개 메모로 승인되기까지의 전 과정. 각 단계가 위 식별자 체계의 실제 사용례다.

1. **발견 등록 — D53** (`scoring/decisions_log.md`, 2026-07-13): 비대칭의
   지표 유병률 분해를 `analysis/EXPLORATORY_wave1_b3_asymmetry.md`로 등록.
   규율: EXPLORATORY/not-for-publication 배너, 가설 4건 전부 질문형(인과
   직설법 0), 동결 파일 무수정·재계산 0. — *탐색 발견은 표의 산술 재배열까지만
   허용되고 서사는 소유자 몫이라는 경계가 여기서 강제된다.*
2. **발행 패킷 — RP-18** (`review_packets/RP-18_asymmetry_memo_publication.md`,
   D64): 게시 가능한 완성 영문 텍스트, 배치 2안(독립 Issue vs Issue #2 부록
   코멘트), 게시 명령, 가설 표지 검토 노트를 한 문서로 — 소유자가 1줄로
   결정할 수 있는 형태.
3. **소유자 서명 — D92** (2026-07-16): 배치 (A) Issue #2 부록 코멘트로 승인.
   근거 기록: "N=8/9 산술을 독립 Issue로 띄우면 과대 포장" — 같은 텍스트라도
   게시 형태가 주장 지위를 결정한다는 판단이 원장에 남았다.
4. **게시 텍스트 동결** — `review_packets/RP-18_body.md` (패킷 §2에서 수정 0
   추출). 게시는 소유자 수동 실행 항목으로 대기열에 잔존 (`docs/OWNER_QUEUE.md`
   레버리지 요약 1-②) — 게시 후 URL이 후속 D-엔트리로 기록될 예정.

이 사슬이 보여주는 불변식: **발견 → 격리 등록 → 검토 패킷 → 인간 서명 →
동결 텍스트 → (수동) 게시** — 어떤 단계도 앞 단계의 커밋 타임스탬프 없이
성립하지 않고, 세션(AI)은 3단계를 건너뛸 수 없다.

## 3. 자주 찾는 것

- 특정 발행 수치의 출처: `RESULTS.md` 표의 소스 열 → 해당 JSON.
- 채점 기준이 점수보다 먼저 커밋된 증거: `tools/verify_blindness.py` (이력
  증명 게이트 — CI 매 push 실행).
- 오버라이드·서명 기록: `scoring/overrides.md`.
- 발행 후 결함: `ERRATA.md` (E-001 rev2 불일치 3건, E-002 rev2 비교).
