# Issue #4 — EQ Memo #1: Gildan Activewear (GIL)

> **FINAL — owner-signed 2026-07-16 (Q-O01·Q-O03, this session's structured
> decision responses; ledger D93). This is the copy-paste text for posting;
> the posting act itself is the owner's.** Format follows ISSUE_2 conventions
> (an "ISSUE_3_DRAFT" file does not exist in the repo — Issue #3 was posted
> from ISSUE_2_HOLDOUT_DRAFT.md; noted for the record).
>
> **Confirmed title (owner choice: proposal 1):**
> `EQ Memo #1 — Gildan Activewear (GIL): what pre-report filings alone reconstruct`

---

## Proposed issue body (final text)

This is the project's first **Tier 2** output (PROJECT.md §3): an earnings-quality
memo on a current company, produced by the pipeline whose trust boundary was
measured in Issues #0–#3.

**Scoring: Claude-assisted, human-finalized.** Results are limited to a single
Claude-based pipeline. This memo does **not** allege accounting impropriety or
wrongdoing; every item is based on the company's own public filings, with links.
No position is held in GIL securities. Educational and informational purposes
only; not investment advice.

### Selection background (read this first)

GIL was not selected at random. At selection time we were aware of a short-seller
report (Jehoshaphat Research, published **2026-06-16** — allegations, which the
company has denied). The model's input, however, was **code-enforced to a
2026-06-15 cutoff** (look-ahead guard, access-logged): only filings submitted
before the report were used; the report, news, and the selection rationale were
excluded from the input. This memo is therefore **not a "random screening hit"**
— it is a **sealed pre-report replication**: could the same area of signal be
reconstructed from pre-report filings alone? It neither confirms nor rebuts the
report; readers can compare the flags against the public claims themselves.

### The memo

Full memo (five flags, verbatim quotes with accession numbers, verification
paths, citation-verification appendix): **[`output/GIL_memo_v1.md`](../output/GIL_memo_v1.md)**
· Korean publication draft: `runs/gil_memo_v1/memo_draft.md`.

Headline flags (each stated as disclosed fact + unverified hypothesis, condensed):

1. **GAAP net loss / doubled operating cash outflow vs. positive adjusted earnings** — Q1 2026 net loss $(65.8)M vs adjusted net earnings $80.0M; OCF $(279.5)M. Largest adjustment: Hanes inventory step-up $106.3M (+$95M residual). *(high confidence)*
2. **Hanes (~45% of net sales) excluded from ICFR/DC&P evaluation scope** — a permitted transition accommodation, during the integration-accounting window. *(high)*
3. **Three diverging leverage ratios** — headline 3.3x vs 3.4x (bank covenant) vs 3.8x (USPP); pro-forma EBITDA includes $472.0M pre-ownership Hanes add-back (~32%). *(high)*
4. **Off-balance-sheet receivables factoring balance swung $777.0M → $667.3M in one quarter**, moving reported AR, payables, and operating-cash-flow optics. *(medium)*
5. **Customer concentration: largest customer 33.2% of total sales, top ten 72.5%**, no minimum-purchase contracts. *(medium)*

### Why trust the method (and how far)

- Citation integrity: 19 verbatim quotes machine-checked — 14 exact; 5
  ellipsis-merged quotes hand-traced fragment-by-fragment (0 fabricated);
  machine verdicts published unmodified.
- Which signal types moved scores in the backtest (descriptive only, treatment
  vs control side by side — including the types that fire on controls too):
  [`analysis/EVIDENCE_LINES.md`](EVIDENCE_LINES.md).
- What a threshold buys you (detection / false positives / cost per detection,
  all with Clopper–Pearson 95% intervals): `analysis/DECISION_TABLE.md`
  *(post only after owner signature — Q-O02)*.
- The trust boundary itself: Issues #0–#3 (wave-1/wave-2 backtests, post-cutoff
  holdout, matched controls).

**Feedback wanted** (Tier 3, PROJECT.md §9): ① What did you learn that you
didn't know? ② What would you now do differently? ③ What is missing?

---

## 부록 (검토용 — 게시 여부는 소유자 선택): PROJECT.md §6 자가 감사

| §6 항목 | 판정 | 근거 |
|---|---|---|
| 1. 사실/가설 분리 · "분식/fraud/조작" 어휘 금지 | **PASS** | memo 전 항목 "사실/Anomaly(인용)" vs "해석 가설/hypothesis" 구조. 금지 어휘 0회 — 리포트 언급도 "주장(allegations)·회사 부인"으로 한정. grep 검증: `grep -icE "분식|fraud|manipul" output/GIL_memo_v1.md runs/gil_memo_v1/memo_draft.md` → 양판 히트 0 (2026-07-16 실측) |
| 2. 공개 데이터만 · 전 수치 공시 원문 링크 | **PASS** | 40-F·6-K EDGAR 직링크 + accession no; 인용 19건 기계 대조 14 VERIFIED, 5건 수기 판정(병합 인용, 날조 0 — 서명 대기 `citation_adjudication.md`) |
| 3. 포지션 없음 고지 | **PASS** | 양판 명시 ("No position is held in GIL securities" / "GIL에 대한 보유·공매도 포지션이 없다") |
| 4. 교육·정보 목적 면책 | **PASS** | 양판 명시 (not investment advice) |
| 5. 방법론·코드 공개 재현성 | **PASS** | blind_memo_run/extract/verify.py + runs/gil_memo_v1/ 원본 JSON + 컷오프 가드 로그. 재현 경로 memo 헤더 기재 |
| §5-5 범위 한정 문구 | **PASS** | 양판 명시 ("limited to a single Claude-based pipeline") |
| "채점: Claude 보조 + 인간 최종 확정" | **PASS** | 양판 명시 — 단 **서명 자체가 아직 없다** (Q-O01). 서명 전 게시 금지 |

**게시 전 소유자 체크리스트 (2026-07-16 갱신)**
- [x] Q-O01 서명: `citation_adjudication.md` 5건 + $201.6M 파생값 확인 + memo 승인 (D93)
- [x] 본 Issue 텍스트(Q-O03) 승인 — 제목 proposal 1 확정 (D93)
- [x] §6 자가 감사 재실행 (2026-07-16): 금지 어휘 grep 양판 0 히트 유지 ·
      선정 배경·포지션 없음·면책·§5-5 문구 전부 존치 — 7/7 PASS
- [x] access_log 해시 핀 반영: 양판 선정 배경 절에 스냅샷 sha256 `856d50f3984d`
      기재 (hash-only 규약, 원본 로그 미커밋)
- [ ] **게시 (소유자)**: `gh issue create --repo lastwhisper906-gif/aaer-evals
      --title "EQ Memo #1 — Gildan Activewear (GIL): what pre-report filings alone reconstruct"
      --body-file <본 파일의 'Proposed issue body' 절>` → 게시 후 README
      'Publication' 절 링크 + 본 파일 헤더 PUBLISHED 갱신 + URL D-엔트리
- [ ] **독자 발송 5–10명 (소유자)**: `docs/reader_validation/` — OUTREACH의
      {ISSUE_URL}을 게시 URL로 치환 후 발송. **미발송 시 Tier 3 가치 검증은
      0점이다**
