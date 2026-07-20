# V1 Partial De-identification Audit — accession-level provenance retained in the perturbed frame

> 2026-07-20. Session audit under the owner plan of 2026-07-20 (§1), ledger D99.
> v1 artifacts are untouched: no frozen output is recomputed, no historical text
> is rewritten. This document narrows *interpretation*, not results.
> 한 줄 요약: v1 교란(perturbed) 프레임은 회사명·티커·CIK를 제거하고 금액을
> 재척도했지만, **원본 accession 번호와 실제 제출 연대기를 그대로 유지**했다.
> 따라서 "부분 탈익명화(partially de-identified)"로만 서술해야 한다.

## 1. Original v1 perturbation behavior

`pipeline/build_payload.py::build_payload(case, perturb=True)`:

- The case header is rebuilt with only 4 fields (`case_id`, `ticker="XXnn"`,
  `company_name="Company CASE_NN"`, `cutoff_date`); CIK is omitted
  (`build_payload.py:148-154`, comment "cik 제공하지 않음").
- Monetary XBRL values are multiplied by a deterministic per-case log-uniform
  constant k ∈ [0.4, 2.5] (`perturb_factor`, `build_payload.py:71-76,147`).
- Each financial fact dict is preserved via spread (`{**v, "value": ...}`,
  `build_payload.py:155-157`) — so `accession`, `filed`, `start`, `end`,
  `form` pass through **unchanged** (accession set at `build_payload.py:108`).
- `filing_chronology` (`build_payload.py:115-137`) is not perturbed at all:
  real form types and real filing dates, full history (case_01: 732 entries
  back to 2002). This was the deliberate D8 decision (dates held constant).
- `pipeline/runner.py:110-147` sends the whole payload to the evaluatee; the
  output schema requires `source_accession_no` on every evidence quote, i.e.
  the model is explicitly prompted to read and cite the accession numbers.
  The same payload path feeds the identity 3-arm run
  (`tools/run_identity_arms.py:37` — arms (a) and (b)) and the recognition
  probes (`pipeline/probe_runner.py:55-62`).

Deterministic re-confirmation (2026-07-20, frozen builder + committed case
headers + local corpus): wave-1 case_01 perturbed payload carries **18 original
accession numbers** (e.g. `0000950123-11-075023`, `0001158172-12-000049`) and
the full real chronology; wave-2 case_44 likewise (e.g.
`0001273685-15-000007`). Committed frozen outputs echo the same strings
(`runs/perturbed/case_01.json`, `runs/wave2/perturbed/case_39.json`).
Pinned by `pipeline/test_deid_disclosure.py` (characterization test).

## 2. Identity fields removed in the v1 perturbed frame

- `company_name` (→ `"Company CASE_NN"`)
- `ticker` (→ `"XXnn"`)
- `cik` (omitted from header and prompt; `runner.py:112` adds CIK to the task
  prompt only in the non-perturbed arm)
- Monetary values (rescaled by k — not an identity field, but the memorized-
  number channel)

## 3. Identity fields retained

- **SEC accession numbers**, verbatim, on every financial fact.
- **Real filing dates** (`filed` per fact; `filing_date` per chronology entry)
  and real period `start`/`end` dates.
- **Real form types and the complete filing chronology** (structure, gaps,
  NT filings, amendment sequence).
- Standard `us-gaap`/`dei` tags only (no custom company-prefixed XBRL tags
  were present); no file paths, no legal/successor names in the input.

## 4. Why retained accession numbers matter

An accession number `PPPPPPPPPP-YY-NNNNNN` is a globally unique EDGAR document
ID. Its prefix is the **submitting filer's CIK** and its middle segment encodes
the **filing year**. Two qualifications, both verified in repo data:

- The prefix CIK is the *submitter's*, which for agent-filed documents is a
  third-party filing agent, not the company (e.g. `data/candidates/
  edgar_verification.json`: RINO company CIK `0001394220`, accession prefix
  `0001144204` = filing agent). So the prefix does not always identify the
  company directly.
- Regardless, each accession is a unique public document ID: any system with
  EDGAR access (or memorized EDGAR content) can resolve it to the exact filing
  and therefore the exact company. The year segment additionally leaks true
  chronology even where dates were (in other designs) shifted.

Conclusion: with accessions present, the perturbed frame is trivially
re-identifiable *in principle*; the measured name-ID rates (wave-1 50%,
wave-2 21.9%) therefore cannot be read as "recognition despite full masking."

## 5. Other direct identifiers found

None beyond §3. The header scrub itself works as designed (verified by
`pipeline/test_build_payload.py` and re-verified here): no company name, no
ticker, no CIK field in the perturbed header. The v1 leak surface is
accession + chronology provenance, not header fields.

## 6. Which v1 claims must be narrowed

- Any description of the perturbed arm as "identity-masked," "anonymized," or
  "de-identified" **without qualification** must become "partially
  de-identified" / "direct identifiers removed; accession-level filing
  provenance retained."
- The v1 recognition-rate readings (wave-1 name-ID 50%, wave-2 21.9%, 3-arm
  b−a contrast) must not be attributed solely to reconstruction from financial
  patterns: recognition may have operated through accession metadata, filing
  chronology, financial structure, or memorized financial patterns — these
  channels are not separable in the v1 design.
- The already-published caveat that the perturbed frame is "not a clean lower
  bound" (README, L-5) remains correct and is *strengthened* by this audit;
  L-5's stated channels ("ratio/trend patterns + retained original dates")
  were incomplete — the accession channel is added by the dated addendum.

## 7. Which v1 numerical results remain unchanged

All of them. This audit changes no computation:

- Separation statistics (wave-1 perturbed p=0.0021, AUC 0.864; identity-exposed
  p=0.00114; wave-2 standalone p=0.00116) are unaffected — they measure score
  separation under the frame as it actually was.
- Name-ID rates (50% / 21.9%), outcome-recognition probe results, 3-arm
  medians, holdout results: unchanged as numbers; only their *causal
  interpretation* is narrowed per §6.
- The v2 date-shift design (`specs/perturb_v2.md` §3, `pipeline/date_shift.py`)
  already replaces accessions with neutral sequential IDs (`acc-001`…) and is
  the standard any future "identity-masked"-grade description must meet
  (`pipeline/test_deid_disclosure.py::assert_fully_deidentified`).

## Recommended standing description

> The v1 perturbed frame removed company names, tickers, and explicit CIK
> fields and rescaled monetary values, but retained accession-level filing
> provenance and exact structural reporting patterns. It should therefore be
> described as partially de-identified, not fully identity-masked.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
