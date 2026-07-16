# RP-18 — D53 wave-1 B3 비대칭 메모 발행 여부 (diff-only, 소유자 결정)

> Authored by Claude Code, 2026-07-13. 발행 결정은 소유자 몫 (PROJECT.md §7 —
> 발행 결정은 사용자 확정 사항). 이 패킷은 "yes"의 비용을 0으로 만드는 준비물:
> 아래 텍스트는 게시 가능 완성본이며, 이 세션은 아무것도 게시하지 않았다.
> 원본: `analysis/EXPLORATORY_wave1_b3_asymmetry.md` (D53,
> NOT-FOR-PUBLICATION 표식은 소유자 서명 시 이 패킷 §2 텍스트로만 대체 발행).

## 1. 배치 제안 (둘 중 소유자 선택)

- **(A) Issue 1 부록 코멘트** (권장 쪽 — 1문장 근거: 비대칭의 판정 tier가
  Issue 1의 wave-2이고, 독립 Issue로 띄우기엔 N=8/9 산술 메모라 과대 포장
  위험): `gh issue comment 2 --body-file <아래 §2>`.
- **(B) 신규 짧은 Issue**: 제목 "Exploratory: decomposing the wave-1/wave-2
  B3 asymmetry" — 시리즈 번호 3 (GitHub #4). 본문 동일.

## 2. 게시 텍스트 (영문, 완성본 — 수정 없이 사용 가능)

```markdown
### Exploratory appendix — decomposing the wave-1/wave-2 B3 asymmetry

**Status: exploratory arithmetic, not a finding.** This decomposes numbers
already published (B3 report); it adds no new runs, no new claims, and every
causal-sounding sentence below is deliberately phrased as a question.

The B3 filing-chronology baseline separates wave-1 strongly (AUC 0.7898,
attribution ratio 0.89 vs the LLM's 0.8239) but is near-uninformative on
wave-2 (AUC 0.5483, ratio 0.147 — the pre-registered decision tier). The
indicator-level arithmetic behind that asymmetry:

| indicator (W8) | w1 fraud (n=8) | w1 control (n=22) | w2 fraud (n=9) | w2 control (n=23) |
|---|---|---|---|---|
| NT 10-K/Q | 1/8 | 1/22 | 2/9 | 1/23 |
| **10-K/A** | **4/8** | **2/22** | **1/9** | **6/23** |
| 10-Q/A | 2/8 | 2/22 | 1/9 | 1/23 |
| 8-K item 4.01 (auditor change) | 0/8 | 1/22 | 1/9 | 0/23 |
| 8-K item 4.02 (non-reliance) | 1/8 | 0/22 | 0/9 | 0/23 |
| 8-K frequency spike | 2/8 | 1/22 | 0/9 | 1/23 |

The single largest wave-1 contributor is the 10-K/A indicator (50% of fraud
cases vs 9.1% of controls) — and the *same indicator inverts* on wave-2
(11.1% vs 26.1%).

**The label-circularity hypothesis (flagged as hypothesis, not conclusion):**
famous frauds may be famous partly *because* they restated — so a 10-K/A
indicator may be **selection showing through, not detection**. Wave-2's
inversion is consistent with the base rate that most amendments are benign
little-r corrections, which would make 10-K/A prevalence in any given sample
a property of how the sample was drawn rather than of misconduct.

Open questions we register but do not answer here: era effects on amendment
practice (wave-1 cutoffs are late-2000s–2010s vs wave-2's 2010s); control-pool
survivorship (registered separately as an audit item); and whether the LLM's
wave-1 rank order rode the same chronology signal or reached similar ranks by
different routes (undecidable without the earliness data).

*Limitations: N=8/9 fraud cases per tier; no single prevalence difference
here is a statistical claim on its own; results are scoped to a single
Claude-based pipeline (methodology limitations L-1…L-7 apply).*
```

## 3. 게시 명령 (소유자 실행 — 이 세션 미실행)

```bash
# (A) 부록 코멘트:
gh issue comment 2 --repo lastwhisper906-gif/aaer-evals --body-file /tmp/rp18_body.md
# (B) 신규 Issue:
gh issue create --repo lastwhisper906-gif/aaer-evals \
  --title "Exploratory: decomposing the wave-1/wave-2 B3 asymmetry" \
  --body-file /tmp/rp18_body.md
# 게시 후: 신규 D-엔트리 (게시 URL 기록) + EXPLORATORY 메모 헤더의
# NOT-FOR-PUBLICATION → PUBLISHED(RP-18) 주석 + lint DOCS 편입 여부 확인.
```

## 4. 검토 노트

- 텍스트는 원 메모의 산술 표를 그대로 옮기고 가설은 전부 질문/가설 표지 유지
  — 인과 주장 0. lint 규칙과의 충돌 없음 (사전 스캔: 0% 오탐류·확률 언어·
  대조군 주어 위반 없음; "fraud cases"는 판결 확정 AAER 케이스 지칭으로 G2
  현재 기업 금지와 무관).
- 이 판단에서 알아야 할 것: EXPLORATORY를 발행 표면으로 옮기는 비용의
  대부분은 글쓰기가 아니라 "가설이 결론으로 굳는 문장"을 걸러내는 일이다 —
  게시본이 원 메모보다 단정적이면 그 diff가 바로 위반이다.

---

## 서명 블록

**결정: 발행 승인 — 배치 (A) Issue #2 부록 코멘트** (owner, 2026-07-16,
this session's structured decision responses). 게시 텍스트는 §2 그대로
`review_packets/RP-18_body.md`로 추출 (D92). 게시 명령(소유자 실행):
`gh issue comment 2 --repo lastwhisper906-gif/aaer-evals --body-file review_packets/RP-18_body.md`
게시 후: URL을 D-엔트리로 기록. 추가 근거 (결정 시점): 배치 B는 GitHub #4를
점유해 GIL 메모 Issue와 번호 충돌.
